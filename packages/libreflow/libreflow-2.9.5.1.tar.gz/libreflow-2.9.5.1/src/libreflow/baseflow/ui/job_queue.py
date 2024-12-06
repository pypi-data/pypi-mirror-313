import re
import os
import subprocess
import pprint
import six
import time
import timeago
from datetime import datetime, timedelta
from minio import Minio
from traceback import print_exc
# from ..scripts.minio_progress import Progress

from kabaret import flow
from kabaret.app.ui.gui.widgets.flow.flow_view import QtWidgets, QtCore, QtGui, CustomPageWidget
from kabaret.app.ui.gui.widgets.flow.flow_field import ObjectActionMenuManager
from kabaret.app import resources
from kabaret.app.ui.gui.icons import flow as _

from .controller import Controller
from .mytasks.components import LabelIcon


class RunnerSignals(QtCore.QObject):
    
    # Signals for QRunnable must be outside the class.

    progress = QtCore.Signal(dict)
    progress_refresh = QtCore.Signal(dict, object)
    finished = QtCore.Signal()


class RefreshRunner(QtCore.QRunnable):

    # Main worker for update Job list widget

    def __init__(self, page_widget, oid, item=None):
        super(RefreshRunner, self).__init__()
        self.page_widget = page_widget
        self.signals = RunnerSignals()
        self.oid = oid
        self.item = item

    def run(self):
        emitter_oid = self.page_widget.session.cmds.Flow.call(
            self.oid, 'get_property', ['emitter_oid'], {}
        )
        split = emitter_oid.split('/')
        indices = list(range(len(split) - 4, 2, -2))
        indices[:0] = [len(split)-1]
        source_display = ' – '.join([split[i] for i in reversed(indices)])

        job_type   = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['type'], {}) 
        status = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['status'], {})
        size = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['file_size'], {})
        user   = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['requested_by_user'], {})
        site   = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['requested_by_studio'], {})

        date = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['date'], {})
        progress_value = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['progress_value'], {})

        data = {
            "oid": self.oid,
            "emitter_oid": emitter_oid,
            "source_display": source_display,
            "job_type": job_type,
            "size": size,
            "status": status,
            "user": user,
            "site": site,
            "date": date,
            "progress_value": progress_value
        }

        if self.item:
            self.signals.progress_refresh.emit(data, self.item)
        else:
            self.signals.progress.emit(data)

        self.signals.finished.emit()


class RefreshProgressRunner(QtCore.QObject):

    progress_time = QtCore.Signal()
    progress = QtCore.Signal(object)
    finished = QtCore.Signal()

    def __init__(self, item):
        super(RefreshProgressRunner, self).__init__()
        self.page_widget = item.page_widget
        self.item = item
        self.initial_time = time.time()
    
    def run(self):
        self.progress_time.emit()
        while (self.item.job_data['status'] == 'PROCESSING'):
            try:
                progress_value = self.page_widget.session.cmds.Flow.call( self.item.job_data['oid'], 'get_property', ['progress_value'], {})
                self.item.job_data['progress_value'] = progress_value

                if self.item.paint_time_left is True and self.item.job_data['size']:
                    self.update_time_left(progress_value)

                self.progress.emit(self.item)
            except Exception as e:
                print_exc()
                self.page_widget.session.log_error(f'[JobQueue] An error has occurred')
        
        self.finished.emit()

    def update_time_left(self, progress_value):
        elapsed_time = time.time() - self.initial_time
        total_length = self.item.job_data['size']
        if not isinstance(progress_value,int):
            progress_value = 1
        current_size = progress_value / 100 * total_length
        self.item.time_left = self.seconds_to_time(elapsed_time / current_size * (total_length - current_size))
        self.item.paint_time_left = False

    def seconds_to_time(self, seconds):
        """
        Consistent time format to be displayed on the elapsed time in screen.
        :param seconds: seconds
        """
        minutes, seconds = divmod(int(seconds), 60)
        hours, m = divmod(minutes, 60)
        if hours:
            return '%dh%02dm%02d' % (hours, m, seconds)
        elif minutes:
            return '%02dmin%02d' % (m, seconds)
        else:
            return '%02dsec' % (seconds)


def get_icon_ref(icon_name, resource_folder='icons.flow'):
    if isinstance(icon_name, six.string_types):
        icon_ref = (resource_folder, icon_name)
    else:
        icon_ref = icon_name

    return icon_ref


class JobQueueFooter(QtWidgets.QWidget):
    def __init__(self, page_widget):
        super(JobQueueFooter,self).__init__(page_widget)
        self.page_widget = page_widget
        self.build()

    def build(self):
        self.stats_label = QtWidgets.QLabel()
        self.loading_label = QtWidgets.QLabel()
        self.last_auto_sync_label = QtWidgets.QLabel()
        self.last_manual_sync_label = QtWidgets.QLabel()

        self.stats_label.hide()
        self.last_auto_sync_label.hide()
        self.last_manual_sync_label.hide()

        self.loading_label.setText('Loading queue...')


        flo = QtWidgets.QGridLayout()
        flo.addWidget(self.stats_label,0,0)
        flo.addWidget(self.loading_label,1,0)
        flo.addWidget(self.last_auto_sync_label,0,1, alignment=QtCore.Qt.AlignRight)
        flo.addWidget(self.last_manual_sync_label,1,1, alignment=QtCore.Qt.AlignRight)

        self.setLayout(flo)

    def refresh(self):

        site_oid = os.path.split(self.page_widget.oid)[0]

        all_count = self.page_widget.session.cmds.Flow.call( site_oid, 'count_jobs', [], {})
        all_count = f'{all_count} Jobs in queue'
        processed_count = self.page_widget.session.cmds.Flow.call( site_oid, 'count_jobs', [None, "PROCESSED"], {})
        processed_count = f'<font color="#61f791">{processed_count} PROCESSED</font>'
        error_count = self.page_widget.session.cmds.Flow.call( site_oid, 'count_jobs', [None, "ERROR"], {})
        error_count = f'<font color="#ff5842">{error_count} ERROR</font>'
        waiting_count = self.page_widget.session.cmds.Flow.call( site_oid, 'count_jobs', [None, "WAITING"], {})
        waiting_count = f'<font color="#EFDD5B">{waiting_count} WAITING</font>'

        last_auto_sync = self.page_widget.session.cmds.Flow.get_value(self.page_widget.oid + '/last_auto_sync')
        if last_auto_sync is not None :
            date = datetime.fromtimestamp(last_auto_sync)
            full_date = date.strftime('%Y-%m-%d %H:%M:%S')
            nice_date = timeago.format(full_date, datetime.now())
            self.last_auto_sync_label.setText(f'Last auto sync: {full_date} ({nice_date})')


        last_manual_sync = self.page_widget.session.cmds.Flow.get_value(self.page_widget.oid + '/last_manual_sync')
        if last_manual_sync is not None :
            date = datetime.fromtimestamp(last_manual_sync)
            full_date = date.strftime('%Y-%m-%d %H:%M:%S')
            nice_date = timeago.format(full_date, datetime.now())
            self.last_manual_sync_label.setText(f'Last manual sync: {full_date} ({nice_date})')

        if all_count == "0 Jobs in queue" :
            self.stats_label.setText("No jobs in queue")
        else : self.stats_label.setText(f'{all_count} / {processed_count} - {waiting_count} - {error_count}')
    
    # def get_summary(self):
    #     text = self.page_widget.session.cmds.Flow.call(
    #                 self.page_widget.oid, 'summary', [], {})
    #     return text


class JobQueueSearch(QtWidgets.QLineEdit):

    def __init__(self, header):
        super(JobQueueSearch, self).__init__()
        self.header = header
        self.page_widget = header.page_widget

        self.setStyleSheet('''
        QLineEdit {
            background-color: #232d33;
            border: 2px solid #4c4c4c;
            border-radius: 7px;
            padding-left: 30px;
        }''')

        self.setMaximumWidth(36)
        self.setMaximumHeight(32)

        self.build()

    def build(self):
        self.search_icon = LabelIcon(('icons.search', 'magn-glass'), 18)

        lo = QtWidgets.QHBoxLayout(self)
        lo.setContentsMargins(9,0,0,0)
        lo.addWidget(self.search_icon, 0, QtCore.Qt.AlignLeft)

        self.setClearButtonEnabled(True)

        self.anim = QtCore.QPropertyAnimation(self, b'maximumWidth')
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutQuint)
        self.anim.setDuration(400)
    
    def focusInEvent(self, event):
        if self.text() == '':
            self.anim.setStartValue(36)
            self.anim.setEndValue(225)
            self.anim.start()
        
        super(JobQueueSearch, self).focusInEvent(event)

    def focusOutEvent(self, event):
        if self.text() == '':
            self.setText('')
            self.anim.setStartValue(225)
            self.anim.setEndValue(36)
            self.anim.start()

        super(JobQueueSearch, self).focusOutEvent(event)

    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Escape) or (event.key() == QtCore.Qt.Key_Return):
            self.clearFocus()
        else:
            super(JobQueueSearch, self).keyPressEvent(event)


class JobQueueHeader(QtWidgets.QWidget):

    def __init__(self, content_widget):
        super(JobQueueHeader,self).__init__(content_widget)
        self.content_widget = content_widget
        self.page_widget = self.content_widget.page_widget
        self.build()

    def build(self):

        combobox_stylesheet = '''
        QComboBox {
            background-color: #232d33;
            border: 2px solid #4c4c4c;
            border-radius: 7px;
        }
        QComboBox::drop-down {
            background-color: #616160;
            border-radius: 4px;
        }
        QComboBox QAbstractItemView::item {
            min-height: 20px;
        }'''

        self.filter_label = QtWidgets.QLabel('Filter by:')

        self.filter_status_label = QtWidgets.QLabel('Status:')

        self.filter_status_combobox = QtWidgets.QComboBox()
        self.filter_status_combobox.addItems(['ALL', 'PROCESSING','PROCESSED', 'WAITING', 'ERROR', 'PAUSE', 'WFA'])
        self.filter_status_combobox.setCurrentIndex(0)
        self.filter_status_combobox.currentTextChanged.connect(self._on_filter_changed)
        self.filter_status_combobox.setView(QtWidgets.QListView())
        self.filter_status_combobox.setStyleSheet(combobox_stylesheet)

        self.filter_user_label = QtWidgets.QLabel('User:')

        self.filter_user_combobox = QtWidgets.QComboBox()
        self.filter_user_combobox.setCurrentIndex(0)
        self.filter_user_combobox.currentTextChanged.connect(self._on_filter_changed)
        self.filter_user_combobox.setView(QtWidgets.QListView())
        self.filter_user_combobox.setStyleSheet(combobox_stylesheet)

        self.search = JobQueueSearch(self)

        self.auto_refresh_box = QtWidgets.QCheckBox('Enable Auto-refresh')
        self.auto_refresh_box.setChecked(True)
        self.auto_refresh_box.stateChanged.connect(self._on_auto_refresh_toggle)

        self.clear_button = QtWidgets.QPushButton(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'clean'))), '')
        self.clear_button.clicked.connect(self._on_clear_button_clicked)
        self.clear_button.setIconSize(QtCore.QSize(20,20))
        self.clear_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.clear_button.setToolTip("Clear queue")

        self.removejobs_button = QtWidgets.QPushButton(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'waiting'))), '')
        self.removejobs_button.clicked.connect(self._on_removejobs_button_clicked)
        self.removejobs_button.setIconSize(QtCore.QSize(20,20))
        self.removejobs_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.removejobs_button.setToolTip("Remove outdated jobs")

        self.resetjobs_button = QtWidgets.QPushButton(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'refresh'))), '')
        self.resetjobs_button.clicked.connect(self._on_resetjobs_button_clicked)
        self.resetjobs_button.setIconSize(QtCore.QSize(20,20))
        self.resetjobs_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.resetjobs_button.setToolTip("Reset erroneous jobs")

        hlo = QtWidgets.QHBoxLayout()
        hlo.addWidget(self.filter_label)
        hlo.addWidget(self.filter_status_label)
        hlo.addWidget(self.filter_status_combobox)
        hlo.addWidget(self.filter_user_label)
        hlo.addWidget(self.filter_user_combobox)
        hlo.addWidget(self.search)
        hlo.addStretch()
        hlo.addWidget(self.auto_refresh_box)
        hlo.addWidget(self.clear_button)
        hlo.addWidget(self.resetjobs_button)
        hlo.addWidget(self.removejobs_button)

        self.setLayout(hlo)
    
    def _on_clear_button_clicked(self):
        self.page_widget.page.show_action_dialog(
                f"{self.page_widget.oid}/job_list/clear_queue"
            )

    def _on_removejobs_button_clicked(self):
        self.page_widget.page.show_action_dialog(
                f"{self.page_widget.oid}/job_list/remove_outdated_jobs"
            )
        self.page_widget.refresh_timer.stop()
        self.page_widget.refresh_list()

    def _on_resetjobs_button_clicked(self):
        self.page_widget.page.show_action_dialog(
                f"{self.page_widget.oid}/job_list/reset_jobs"
            )
        self.page_widget.refresh_timer.stop()
        self.page_widget.refresh_list()
    
    def _on_auto_refresh_toggle(self,value):
        if self.auto_refresh_box.isChecked() is True :
            self.page_widget.refresh_timer.start()
        else : self.page_widget.refresh_timer.stop()
    
    def _on_filter_changed(self, value):
        self.content_widget.listbox.list.refresh_filter()


class ProgressDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        # progress = index.data(QtCore.Qt.UserRole+1000)

        self.tree = (index.model().parent())

        self.item = self.tree.itemFromIndex(index)

        if not self.item.job_data['progress_value']:
            progress = 0
        
        else : progress = round(float(self.item.job_data['progress_value']), 2)
        #Set Default values
        if self.item.job_data['status'] == 'PROCESSED':
            progress = 100
        elif self.item.job_data['status'] == 'WAITING':
            progress = 0
        
        self.item.setData(1, QtCore.Qt.DisplayRole, progress)
        # Base rectangle
        painter.save()
        painter.setBrush(QtGui.QColor(75,75,75)) # Background base color
        painter.setPen(QtGui.QColor("transparent"))
        rect2 = QtCore.QRect(option.rect.x()+3, option.rect.y()+12, option.rect.width()-10,
                    option.rect.height()-20)
        painter.drawRoundedRect(rect2, 5, 5)

        # Progress rectangle
        progBarWidth = float((option.rect.width() * progress) / 100)
        if (progBarWidth > 5):

            if self.item.job_data['status'] == 'PROCESSED':
                painter.setBrush(QtGui.QColor(108,211,150)) # Progress color
            elif  self.item.job_data['status'] == 'PROCESSING' :
                painter.setBrush(QtGui.QColor(65,123,216)) # Progress color

            rect5 = QtCore.QRect(option.rect.x()+3, option.rect.y()+12, progBarWidth-10,
                        option.rect.height()-20)
            painter.drawRoundedRect(rect5, 5, 5)
        
        # Text value
        painter.setPen(QtGui.QColor(QtCore.Qt.white))
        if  self.item.job_data['status'] == 'ERROR' :
            painter.setPen(QtGui.QColor(255,88,66))
        elif  self.item.job_data['status'] == 'WAITING' :
            painter.setPen(QtGui.QColor(239,221,91))
        painter.drawText(rect2, QtCore.Qt.AlignCenter, str(progress)+"%")
        painter.restore()


class JobData(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree, data):
        super(JobData,self).__init__(tree)
        self.tree = self.treeWidget()
        self.page_widget = tree.page_widget
        self.job_data = data
        self.time_left = None

        self.progress_thread = QtCore.QThread()
        self.progress_runner = RefreshProgressRunner(self)
        self.progress_runner.moveToThread(self.progress_thread)

        self.progress_thread.started.connect(self.progress_runner.run)
        self.progress_runner.finished.connect(self.progress_thread.quit)
        self.progress_runner.progress.connect(self.refresh_progress)
        self.progress_runner.progress_time.connect(self.update_time_left)

        self.paint_time_left = False
        self.time_left_timer = QtCore.QTimer()
        self.time_left_timer.setInterval(500)
        self.time_left_timer.timeout.connect(self.update_time_left)

        self.refresh()
    
    def refresh(self):
        if self.job_data['job_type'] == "Download" :
            self.setIcon(0,self.tree.dl_icon)
        else : self.setIcon(0,self.tree.up_icon)

        self.setText(0, self.job_data['source_display'])

        if self.job_data['status'] == "PROCESSING":
            self.progress_thread.start()

        if self.job_data['status'] == "PROCESSED":
            for i in range(self.tree.columnCount()):
                self.setForeground(i,QtGui.QBrush(QtGui.QColor(150, 150, 150)))
        if self.job_data['status'] == "WAITING":
            self.setForeground(3,QtGui.QBrush(QtGui.QColor(239,221,91)))
        if self.job_data['status'] == "ERROR":
            self.setForeground(3,QtGui.QBrush(QtGui.QColor(255,88,66)))

        locale = QtCore.QLocale()
        if self.job_data["size"] != '' :
            display_size = locale.formattedDataSize(self.job_data["size"],format = locale.DataSizeTraditionalFormat)
        else : display_size = ''
        self.setText(2, display_size)

        self.setText(3, self.job_data['status'])
    
        self.setData(4, QtCore.Qt.DisplayRole, QtCore.QDateTime.fromSecsSinceEpoch(int(self.job_data['date'])))
        self.setText(5, self.job_data['user'])
        self.setText(6, self.job_data['site'])

        self.setToolTip(0,self.job_data['source_display'])

        self.tree.refresh_completed()

    def refresh_progress(self):
        self.tree.viewport().update()
        if self.time_left:
            self.setText(3, self.time_left)
            if self.time_left == '00sec':
                self.setText(3, self.job_data['status'])
    
    def update_time_left(self):
        self.paint_time_left = True
        self.time_left_timer.start()


class JobQueueListWidget(QtWidgets.QTreeWidget):
    def __init__(self,box_widget):
        super(JobQueueListWidget, self).__init__(box_widget)
        self.box_widget = box_widget
        self.content_widget = self.box_widget.content_widget
        self.page_widget = self.content_widget.page_widget

        self.setStyleSheet('''QTreeWidget {
                                background-color: transparent;
                                border: none;
                            }
                            QTreeWidget::item {
                                padding: 4px;
                            } 
                            QHeaderView {
                                background-color: transparent;
                                border-top: none;
                                border-left: none;
                                border-right: none;
                                border-color: #535151
                            }
                            QHeaderView::section {
                                background-color: transparent; 
                                border-color: #535151
                            }'''
                            )

        self.setHeaderLabels(['Name', 'Progress', 'Size', 'Status', 'Emitted On', 'User', 'Site'])
        self.search_keys = ['source_display', 'job_type', 'status', 'user', 'site']

        self.dl_icon = QtGui.QIcon(resources.get_icon(('icons.libreflow', 'download')))
        self.up_icon = QtGui.QIcon(resources.get_icon(('icons.libreflow', 'upload')))

        self.setItemDelegateForColumn(1,ProgressDelegate())
        
        self.header().setDefaultAlignment(QtCore.Qt.AlignCenter)
        # self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.setTextElideMode(QtCore.Qt.ElideLeft)
        self.setSortingEnabled(True)
        self.sortByColumn(4, QtCore.Qt.DescendingOrder)
        self.setRootIsDecorated(False)

        self.action_manager = ObjectActionMenuManager(
            self.page_widget.session, self.page_widget.page.show_action_dialog, 'Flow.map'
        )

        self.itemDoubleClicked.connect(self.on_item_doubleClicked)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu_requested)

        self.refresh()

    def refresh(self):
        self.blockSignals(True)
        self.page_widget.refresh_timer.stop()
        self.page_widget.data_fetched = False
        
        self.page_widget.start = time.time()

        map_oid = self.page_widget.oid + "/job_list"
        self.oid_list = self.page_widget.session.cmds.Flow.get_mapped_oids(map_oid)

        self.page_widget.footer.refresh()
        
        self.blockSignals(False)

    def refresh_completed(self):
        if self.page_widget.getThreadCount() == 0 and self.page_widget.data_fetched is False:
            if self.content_widget.header.filter_user_combobox.count() != (len(self.get_users()) + 1):
                self.content_widget.header.filter_user_combobox.clear()
                self.content_widget.header.filter_user_combobox.addItems(['all'] + self.get_users())

            self.page_widget.refresh_timer.start()
            if self.content_widget.header.auto_refresh_box.isChecked() is True:
               self.page_widget.refresh_timer.start()
            self.page_widget.footer.loading_label.hide() 
            self.page_widget.footer.stats_label.show()
            self.page_widget.footer.last_auto_sync_label.show()
            self.page_widget.footer.last_manual_sync_label.show()
            self.page_widget.data_fetched = True
            return True

    def addJob(self, data):
        self.blockSignals(True)

        item = JobData(self, data)

        # prog_bar = QtWidgets.QProgressBar()
        # self.setItemWidget(item,1,prog_bar)

        self.setColumnWidth(0, 400)
        self.setColumnWidth(1,200)
        self.resizeColumnToContents(2)
        self.resizeColumnToContents(3)
        self.resizeColumnToContents(4)
        self.resizeColumnToContents(5)
        self.resizeColumnToContents(6)

        self.blockSignals(False)

    def jobExists(self, oid):
        job_items = [self.topLevelItem(i) for i in range(self.topLevelItemCount()) if self.topLevelItem(i).job_data['oid'] == oid]
        return job_items[0] if job_items else None

    def refresh_search(self, query_filter):
        count = 0
        keywords = query_filter.split()
        query_filter = '.*'+'.*'.join(keywords)
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if item is not None:
                matches = [i for key in self.search_keys if item.job_data.get(key) and re.match(query_filter, item.job_data[key])]
                
                # Use case for date
                if item.job_data.get('date'):
                    formatted_date = datetime.fromtimestamp(item.job_data['date']).strftime('%d/%m/%Y %H:%M')
                    if re.match(query_filter, formatted_date):
                        matches.append(i)
                
                if matches:
                    self.topLevelItem(i).setHidden(False)
                else:
                    self.topLevelItem(i).setHidden(True)
    
    def refresh_filter(self):
        self.reset_filter()

        status_value = self.content_widget.header.filter_status_combobox.currentText()
        user_value = self.content_widget.header.filter_user_combobox.currentText()
        
        if status_value == 'ALL' and user_value == 'all':
            return
        
        for i in range(self.topLevelItemCount()):
            if self.topLevelItem(i).job_data['status'] != status_value and status_value != 'ALL':
                self.topLevelItem(i).setHidden(True)
            if self.topLevelItem(i).job_data['user'] != user_value and user_value != 'all':
                self.topLevelItem(i).setHidden(True)
    
    def reset_filter(self):
        for i in range(self.topLevelItemCount()):
            self.topLevelItem(i).setHidden(False)
    
    def get_users(self):
        user_list = []
        for i in range(self.topLevelItemCount()):
            if self.topLevelItem(i).job_data['user'] not in user_list:
                user_list.append(self.topLevelItem(i).job_data['user'])
        return user_list
    
    def on_item_doubleClicked(self,item):
        self.page_widget.page.goto(item.job_data['oid'])
    
    def _on_context_menu_requested(self, pos):

        action_menu = QtWidgets.QMenu(self)

        index = self.indexAt(pos)

        if not index.isValid():
            return

        item = self.itemAt(pos)

        has_actions = self.action_manager.update_oid_menu(
            item.job_data['oid'], action_menu, with_submenus=True
        )

        if has_actions:
            action_menu.exec_(self.viewport().mapToGlobal(pos))


class JobQueueListBox(QtWidgets.QWidget):
    def __init__(self, content_widget):
        super(JobQueueListBox, self).__init__(content_widget)
        self.setObjectName('JobQueueListBox')
        self.content_widget = content_widget
        self.page_widget = self.content_widget.page_widget

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('#JobQueueListBox { background-color: #626261; border-radius: 5px; }')

        self.build()

    def build(self):
        box = QtWidgets.QVBoxLayout(self)
        self.list = JobQueueListWidget(self)
        box.addWidget(self.list)


class JobQueueContent(QtWidgets.QWidget):
    def __init__(self, page_widget):
        super(JobQueueContent, self).__init__(page_widget)
        self.setObjectName('JobQueueContent')
        self.page_widget = page_widget

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('#JobQueueContent { background-color: #232d33; border-radius: 5px; }')

        self.build()

    def build(self):
        grid = QtWidgets.QGridLayout(self)

        self.listbox = JobQueueListBox(self)
        self.header = JobQueueHeader(self)
        self.header.search.textChanged.connect(self.listbox.list.refresh_search)
        grid.addWidget(self.header, 0, 0)
        grid.addWidget(self.listbox, 1, 0)


class JobQueueWidget(CustomPageWidget):

    def build(self):
        self.__pool = QtCore.QThreadPool()
        self.__pool.setMaxThreadCount(self.__pool.globalInstance().maxThreadCount())

        self.data_fetched = False

        self.start = time.time()

        self.thread = QtCore.QThread()
        self.thread.started.connect(self.init_list)
        self.thread.finished.connect(self.thread.quit)

        self.refresh_timer = QtCore.QTimer(self)
        self.refresh_timer.setInterval(5000)
        self.refresh_timer.timeout.connect(self.refresh_list)

        self.setStyleSheet('outline: 0;')

        self.footer = JobQueueFooter(self)
        self.content = JobQueueContent(self)

        vlo = QtWidgets.QVBoxLayout(self)
        vlo.setContentsMargins(0,0,0,0)
        vlo.setSpacing(1)
        vlo.addWidget(self.content)
        vlo.addWidget(self.footer)

        self.content.listbox.list.refresh()
        self.thread.start()
    
    def on_touch_event(self,oid):
        return None
    #     job_list_oid = self.oid + "/job_list"
    #     if oid == job_list_oid:
    #         print ("MAP TOUCHED")

    def init_list(self):
        self.jobs_count = len(self.content.listbox.list.oid_list)

        self.footer.stats_label.hide()
        self.footer.last_auto_sync_label.hide()
        self.footer.last_manual_sync_label.hide()

        if self.jobs_count > 0 :
            for oid in self.content.listbox.list.oid_list:
                refresh_runner = RefreshRunner(self, oid)
                refresh_runner.signals.progress.connect(self.addJobWidget)
                self.__pool.start(refresh_runner)

        else : self.content.listbox.list.refresh_completed()
        

        self.thread.finished.emit()
    
    def refresh_list(self):
        self.content.listbox.list.refresh()

        self.jobs_count = len(self.content.listbox.list.oid_list)
        # print (self.jobs_count)
        self.footer.loading_label.show() 
        if self.jobs_count > 0 :
            for oid in self.content.listbox.list.oid_list:
                # Check if already exists
                item = self.content.listbox.list.jobExists(oid)
                refresh_runner = RefreshRunner(self, oid, item)
                if item:
                    refresh_runner.signals.progress_refresh.connect(self.updateJobWidget)
                else:
                    refresh_runner.signals.progress.connect(self.addJobWidget)

                self.__pool.start(refresh_runner)

        else : self.content.listbox.list.refresh_completed()

        self.thread.finished.emit()

    def addJobWidget(self, data):
        self.content.listbox.list.addJob(data)
    
    def updateJobWidget(self, data, item):
        item.job_data = data
        item.refresh()
    
    def clearPool(self):
        self.__pool.clear()
    
    def getThreadCount(self):
        return self.__pool.activeThreadCount()
    
    def die(self):
        for oid in self.content.listbox.list.oid_list:
            item = self.content.listbox.list.jobExists(oid)
            if item is not None and item.progress_thread.isRunning():
                item.progress_runner.progress.disconnect(item.refresh_progress)
                item.progress_thread.quit()
                