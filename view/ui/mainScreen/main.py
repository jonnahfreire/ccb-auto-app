import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from app.config.paths import syspath
from app.execlogs.notifications import get_notifications
from app.main import get_data, set_extract_data
from app.main import get_files_from_folder
from app.main import get_month_directories, create_work_directory
from app.main import get_username
from app.main import open_directory
from app.main import remove_current_user
from app.main import remove_month_directory
from app.utils.main import get_month_list, get_current_month
from ..alertLoading.main import AlertLoading
from ..alertModal.main import AlertModal
from ..contentItem.main import ContentItem
from ..contextMenu.main import ContextMenu
from ..folderItem.main import FolderItem
from ..listView.main import ListView
from ..notification.main import NotificationContainerList, NotificationItem
from ..settings.main import SettingsScreen
from ..styles import *


class MainScreen(QMainWindow):

    def __init__(self, parent, ui_path) -> None:
        super().__init__()
        self.notification_container = None
        self.start_insertion_option = None
        self.add_extract_option = None
        self.user_context_menu = None
        self.folder_context = None
        self.add_extract_alert_loading = None
        self.month = None
        self.debtReceivingHeader = None
        self.userIcon = None
        self.userName = None
        self.startInsertionBtn = None
        self.addItemsBtn = None
        self.createDirBtn = None
        self.appHeader = None
        self.workingMonthHeader = None
        self.statusFinishedException = None
        self.statusFinished = None
        self.statusNotStarted = None
        self.statusStarted = None
        self.contentListView = None
        self.leftStatusFrame = None
        self.folderListView = None
        self.add_items_alert_loading = None
        self.itemsContainer = None
        self.remove_month_modal = None
        self.remove_user_modal = None
        self.parent = parent
        self.folders = []
        self.open_contexts = []

        loadUi(ui_path, self)

        self.appHeader.setStyleSheet(app_header_bg)
        self.parent.mousePressEvent = self.handle_mouse_press
        QListView.mousePressEvent = self.handle_mouse_press

        self.status_container = self.leftStatusFrame

        self.folder_view = self.folderListView
        self.folder_view.setSpacing(5)
        self.folder_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.folder_view.setFocusPolicy(Qt.NoFocus)

        self.list_view_widget = ListView(self.itemsContainer,
                                         self.itemsContainer.width(),
                                         self.itemsContainer.height(), 0, 0)

        self.list_view_widget.hide_horizontal_scrollbar()
        self.list_view_widget.hide_vertical_scrollbar()
        self.list_view_widget.set_vertical()

        self.status_started = self.statusStarted
        self.status_not_started = self.statusNotStarted
        self.status_finished = self.statusFinished
        self.status_finished_exception = self.statusFinishedException

        self.createDirBtn.mousePressEvent = self.create_month_clicked
        self.createDirBtn.setStyleSheet(btn_primary)
        set_element_shadow(self.createDirBtn)

        self.addItemsBtn.mousePressEvent = self.add_items_clicked
        self.addItemsBtn.setStyleSheet(btn_primary)
        set_element_shadow(self.addItemsBtn)

        self.startInsertionBtn.mousePressEvent = self.start_insertion_clicked
        self.startInsertionBtn.setStyleSheet(btn_success)
        set_element_shadow(self.startInsertionBtn)

        self.notificationContainer.mousePressEvent = self.handle_notifications_click
        self.userContainer.mousePressEvent = self.handle_user_click

        set_element_shadow(self.workingMonthHeader)
        set_element_shadow(self.debtReceivingHeader)

        self.filterItemsNotSent.mousePressEvent = self.set_items_not_sent_show
        self.filterItemsSent.mousePressEvent = self.set_items_sent_show
        set_element_shadow(self.filterItemsNotSent)
        set_element_shadow(self.filterItemsSent)

        self.month.setText(get_current_month())

        self.set_username()
        self.months = get_month_list()
        self.set_folders_list()
        self.set_content_data()
        self.create_modals()
        self.create_contexts()
        self.create_alerts()

        self.notification_container = NotificationContainerList(self, 370, 200)
        self.point.hide()

        self.handle_notifications_click(True)

    def set_items_sent_show(self, ev):
        self.filterItemsSent.setStyleSheet(btn_filters_style_active)
        self.filterItemsNotSent.setStyleSheet(btn_filters_style)
        month = [folder for folder in self.folders if folder.is_active]

        if month:
            month = month[0].month_text.text().replace("/", "-")
            self.set_content_data(month, 1)

    def set_items_not_sent_show(self, ev):
        self.filterItemsNotSent.setStyleSheet(btn_filters_style_active)
        self.filterItemsSent.setStyleSheet(btn_filters_style)
        month = [folder for folder in self.folders if folder.is_active]

        if month:
            month = month[0].month_text.text().replace("/", "-")
            self.set_content_data(month, 0)

    def set_username(self):
        username = get_username()
        self.userName.setText(username)

    def set_folders_list(self):
        months = get_month_directories()
        self.folder_view.clear()

        if len(self.folders) > 0:
            self.folders = []

        for index, month in enumerate(months):
            month = month.replace("-", "/")
            folder = FolderItem(self.folder_view, month)
            folder.set_id(index)

            list_item = ListItem(self.folder_view, folder)
            self.folder_view.addItem(list_item)
            self.folder_view.setItemWidget(list_item, folder)

            folder.click(self.folders, self.handle_folder_callback)
            self.folders.append(folder)

            if month == get_current_month():
                self.folder_view.setCurrentRow(folder.get_id())
                folder.set_active()

    def create_contexts(self):
        self.folder_context = ContextMenu(self, 120)
        self.folder_context.add_item("Abrir Local",
                                     self.handle_open_folder_location,
                                     "view/assets/folder-symlink.png")
        self.folder_context.add_separator()
        self.folder_context.add_item("Remover",
                                     self.handle_remove_folder,
                                     "view/assets/trash.png")

        self.user_context_menu = ContextMenu(self, 142)
        self.user_context_menu.add_item("Resetar Usuário",
                                        self.handle_remove_user,
                                        "view/assets/person.png")

        self.user_context_menu.add_separator()
        self.user_context_menu.add_item("Configurações",
                                        self.handle_settings_view,
                                        "view/assets/gear.png")

        self.add_extract_option = ContextMenu(self, 125, 40)
        self.add_extract_option.add_item("Adicionar Extrato",
                                         self.handle_add_extract)

        self.start_insertion_option = ContextMenu(self, 120, 120)
        self.start_insertion_option.add_item("Caixa 1000")
        self.start_insertion_option.add_separator()
        self.start_insertion_option.add_item("Banco 1010")
        self.start_insertion_option.add_separator()
        self.start_insertion_option.add_item("Extrato")

    def create_modals(self):
        self.remove_user_modal = \
            AlertModal(self, 300, 200, "Remover usuário?",
                       "Esta ação irá remover o usuário atual.\
                        Tem certeza que deseja continuar?")
        self.remove_user_modal.ok(self.remove_user)
        self.remove_user_modal.hide()

        self.remove_month_modal = \
            AlertModal(self, 300, 200, "Remover mês selecionado?",
                       "Esta ação irá remover o mês selecionado.\
                        Tem certeza que deseja continuar?")
        self.remove_month_modal.ok(self.remove_folder)
        self.remove_month_modal.hide()

    def create_alerts(self):
        self.add_items_alert_loading = \
            AlertLoading(self, p_w=self.width(), p_h=self.height(),
                         infinity=False,
                         duration=5000,
                         container_w=300,
                         message="Lendo arquivos, aguarde..")

        self.add_extract_alert_loading = \
            AlertLoading(self, p_w=self.width(), p_h=self.height(),
                         infinity=False,
                         duration=5000,
                         container_w=350,
                         message="Lendo dados do arquivo, aguarde..")

    def handle_remove_user(self, event):
        self.remove_user_modal.show()
        self.hide_open_contexts()

    def handle_settings_view(self, event):
        settings_view = SettingsScreen(self.parent, "view/ui/settings/settings.ui")
        self.parent.addWidget(settings_view)
        self.hide_open_contexts()
        self.parent.setCurrentIndex(self.parent.currentIndex() + 1)

    def handle_notifications_click(self, e):
        if not self.notification_container.is_shown:
            notifications = get_notifications()

            if len(notifications) > 0:
                self.point.show()

            for notification in notifications:
                notification_item = NotificationItem(self.notification_container, notification)
                self.notification_container.add_item(notification_item)
                notification_item.close_btn.mousePressEvent = \
                    lambda ev: self.handle_remove_notification_item(notification_item)

            self.hide_open_contexts()
            self.notification_container.show(
                self.width() - self.notification_container.width - 50, 60)
            self.open_contexts.append(self.notification_container)

    def handle_remove_notification_item(self, item):
        # self.notification_container.list_container.remove_item(item)
        pass
    
    def handle_user_click(self, event):
        if event.buttons() == Qt.LeftButton:
            self.hide_open_contexts()

        if event.buttons() == Qt.RightButton:
            self.hide_open_contexts()
            self.open_contexts.append(self.user_context_menu)
            self.user_context_menu.show(self.width() - self.user_context_menu.width - 20, 60)

    def set_content_data(self, month=None, inserted: bool = 0):
        self.list_view_widget.clear()

        if month is None:
            month = get_current_month().replace("/", "-")

        data = get_data(month, inserted=inserted)
        items_1000 = data['1000']
        items_1010 = data['1010']
        items_extrato = data['extract']

        items = items_1000 + items_1010 + items_extrato

        if len(items) > 0:
            self.handle_status(0)
        else:
            self.handle_status(-1)

        list_item_1000 = ContentItem(self.list_view_widget,
                                     "Caixa Geral - 1000", items_1000,
                                     self.itemsContainer.width(),
                                     self.itemsContainer.height())
        list_item_1010 = ContentItem(self.list_view_widget,
                                     "Banco - 1010", items_1010,
                                     self.itemsContainer.width(),
                                     self.itemsContainer.height())
        list_item_extrato = ContentItem(self.list_view_widget,
                                        "Extrato - 1010", items_extrato,
                                        self.itemsContainer.width(),
                                        self.itemsContainer.height())
        self.list_view_widget.set_fixed_size(self.itemsContainer.width(),
                                             self.itemsContainer.height())
        self.list_view_widget.add_item(list_item_1000)
        self.list_view_widget.add_item(list_item_1010)
        self.list_view_widget.add_item(list_item_extrato)

    def handle_mouse_press(self, event):
        # self.hide_open_contexts()
        pass

    def handle_folder_callback(self, event, folder):
        self.folder_context.set_clicked_item(folder)
        self.hide_open_contexts()
        self.folder_view.setCurrentRow(folder.get_id())

        if event.buttons() == Qt.LeftButton:
            self.set_content_data(folder.get_month_text())

        if event.buttons() == Qt.RightButton:
            self.open_contexts.append(self.folder_context)

            context_left = folder.x() + 15
            context_top = folder.height() + folder.y()
            context_top += self.folder_view.height() + 115 / folder.height() * 13
            self.folder_context.show(context_left, context_top + 10)

    def remove_user(self):
        if remove_current_user():
            timer = QTimer()
            timer.singleShot(500, lambda: self.parent.setCurrentIndex(self.parent.currentIndex() - 1))

    def remove_folder(self):
        month = self.folders[self.folder_view.currentRow()].month_text.text().replace("/", "-")
        self.folder_view.takeItem(self.folder_view.currentRow())

        if remove_month_directory(month):
            # updating folders
            self.folders = [folder for folder in self.folders
                            if folder.get_id() != self.folder_view.currentRow()]

            # updating folder ids
            for index, folder in enumerate(self.folders):
                folder.set_id(index)

            self.set_content_data()

    def handle_remove_folder(self, event):
        self.remove_month_modal.show()
        self.hide_open_contexts()

    def handle_open_folder_location(self, event):
        month = self.folders[self.folder_view.currentRow()].month_text.text()
        path = os.path.join(syspath, month.replace("/", "-"))
        self.hide_open_contexts()
        return open_directory(path)

    def handle_add_extract(self, event):
        if event.buttons() == Qt.LeftButton:
            self.hide_open_contexts()
            filename = QFileDialog.getOpenFileName(
                self, 'Selecione o Extrato', 'c:\\', "Pdf files (*.pdf)")
            if len(filename) > 0:
                if self.add_extract_alert_loading.start_animation():
                    if set_extract_data(filename[0]):
                        self.set_folders_list()

    @staticmethod
    def create_month_clicked(ev):
        # Abrir a lista de meses para selecionar
        create_work_directory(get_current_month())
        pass

    def add_items_clicked(self, event):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        self.hide_open_contexts()

        if event.buttons() == Qt.RightButton:
            self.open_contexts.append(self.add_extract_option)
            return self.add_extract_option.show(
                self.width() - self.add_extract_option.width - 160,
                self.height() - self.add_extract_option.height - 90)

        if dlg.exec_():
            folder_path = dlg.selectedFiles()
            if len(folder_path) > 0:
                if self.add_items_alert_loading.start_animation():
                    if get_files_from_folder(folder_path[0]):
                        self.set_folders_list()

    def start_insertion_clicked(self, event):
        self.hide_open_contexts()
        if event.buttons() == Qt.RightButton:
            self.open_contexts.append(self.start_insertion_option)
            self.start_insertion_option.show(
                self.width() - self.start_insertion_option.width - 30,
                self.height() - self.start_insertion_option.height - 90
            )

    def hide_open_contexts(self):
        for context in self.open_contexts:
            context.hide()
        self.open_contexts = []

    def handle_status(self, status):
        if status == -1:
            self.status_container.hide()

        if status == 0:
            self.status_container.show()
            self.statusStarted.hide()
            self.statusFinished.hide()
            self.statusFinishedException.hide()
        if status == 1:
            self.status_container.show()
            self.status_not_started.hide()
            self.status_finished.hide()
            self.status_finished_exception.hide()
        if status == 2:
            self.status_container.show()
            self.status_started.hide()
            self.status_not_started.hide()
            self.status_finished_exception.hide()
        if status == 3:
            self.status_container.show()
            self.status_started.hide()
            self.status_not_started.hide()
            self.status_finished.hide()


class ListItem(QListWidgetItem):

    def __init__(self, parent, content) -> None:
        super().__init__(parent)
        self.setSizeHint(content.sizeHint())
