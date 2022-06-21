import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from app.main import get_month_directories
from app.main import get_username
from app.main import get_data
from app.main import remove_current_user
from app.main import remove_month_directory
from app.main import open_directory
from app.config.paths import syspath

from app.utils.main import get_month_list, get_current_month
from ..alertModal.main import AlertModal
from ..contentItem.main import ContentItem
from ..contextMenu.main import ContextMenu
from ..folderItem.main import FolderItem
from ..listView.main import ListView
from ..settings.main import SettingsScreen
from ..styles import *


class MainScreen(QDialog):

    def __init__(self, parent, ui_path) -> None:
        super().__init__()
        self.itemsContainer = None
        self.remove_month_modal = None
        self.remove_user_modal = None
        self.parent = parent
        self.folders = []
        self.open_contexts = []
        self.month = get_current_month().replace("/", "-")

        loadUi(ui_path, self)

        self.appHeader.setStyleSheet(app_header_bg)
        self.parent.mousePressEvent = self.handle_mouse_press
        QListView.mousePressEvent = self.handle_mouse_press

        self.status_container = self.leftStatusFrame

        self.folder_view = self.folderListView
        self.folder_view.setSpacing(5)
        self.folder_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.folder_view.setFocusPolicy(Qt.NoFocus)
        self.content_view = self.contentListView

        self.list_view_widget = ListView(self.itemsContainer,
                                         self.itemsContainer.width(), self.itemsContainer.height(), 0, 0)
        self.list_view_widget.hide_horizontal_scrollbar()
        self.list_view_widget.hide_vertical_scrollbar()
        self.list_view_widget.set_vertical()

        self.folder_context = ContextMenu(self, 120)
        self.folder_context.add_item("Abrir Local", self.handle_open_folder_location, "view/assets/folder-symlink.png")
        self.folder_context.add_separator()
        self.folder_context.add_item("Remover", self.handle_remove_folder, "view/assets/trash.png")

        self.user_context_menu = ContextMenu(self, 142)
        self.user_context_menu.set_position(650, 50)
        self.user_context_menu.add_item("Resetar Usuário", self.handle_remove_user, "view/assets/person.png")
        self.user_context_menu.add_separator()
        self.user_context_menu.add_item("Configurações", self.handle_settings_view, "view/assets/gear.png")

        self.add_extract_option = ContextMenu(self, 125, 40)
        self.add_extract_option.add_item("Adicionar Extrato", self.handle_add_extract)
        self.add_extract_option.set_position(520, 470)

        self.start_insertion_option = ContextMenu(self, 120, 120)
        self.start_insertion_option.add_item("Caixa 1000")
        self.start_insertion_option.add_separator()
        self.start_insertion_option.add_item("Banco 1010")
        self.start_insertion_option.add_separator()
        self.start_insertion_option.add_item("Extrato")
        self.start_insertion_option.set_position(650, 390)

        self.status_started = self.statusStarted
        self.status_not_started = self.statusNotStarted
        self.status_finished = self.statusFinished
        self.status_finished_exception = self.statusFinishedException

        self.createDirBtn.clicked.connect(self.create_dir_clicked)
        self.createDirBtn.setStyleSheet(btn_primary)
        set_element_shadow(self.createDirBtn)

        self.addItemsBtn.clicked.connect(self.add_items_clicked)
        self.addItemsBtn.mousePressEvent = self.add_items_clicked
        self.addItemsBtn.setStyleSheet(btn_primary)
        set_element_shadow(self.addItemsBtn)

        self.startInsertionBtn.clicked.connect(self.start_insertion_clicked)
        self.startInsertionBtn.mousePressEvent = self.start_insertion_clicked
        self.startInsertionBtn.setStyleSheet(btn_success)
        set_element_shadow(self.startInsertionBtn)

        self.userName.mousePressEvent = self.handle_user_click
        self.userIcon.mousePressEvent = self.handle_user_click

        self.workingMonthHeader.setStyleSheet(main_view_headings_style)
        self.debtReceivingHeader.setStyleSheet(main_view_headings_style)
        set_element_shadow(self.workingMonthHeader)
        set_element_shadow(self.debtReceivingHeader)

        self.set_username()
        self.handle_status(-1)
        self.months = get_month_list()
        self.set_folders_list()
        self.create_modals()
        self.create_content_view(self.month)

    def set_username(self):
        username = get_username()
        self.userName.setText(username)

    def set_folders_list(self):
        months = get_month_directories()

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

    def create_modals(self):
        self.remove_user_modal = AlertModal(self, 300, 200, "Remover usuário?",
                                            "Esta ação irá remover o usuário atual.\
                                            Tem certeza que deseja continuar?")
        self.remove_user_modal.ok(self.remove_user)
        self.remove_user_modal.hide()

        self.remove_month_modal = AlertModal(self, 300, 200, "Remover mês selecionado?",
                                             "Esta ação irá remover o mês selecionado.\
                                             Tem certeza que deseja continuar?")
        self.remove_month_modal.ok(self.remove_folder)
        self.remove_month_modal.hide()

    def handle_remove_user(self, event):
        self.remove_user_modal.show()
        self.hide_open_contexts()

    def handle_settings_view(self, event):
        settings_view = SettingsScreen(self.parent, "view/ui/settings/settings.ui")
        self.parent.addWidget(settings_view)
        self.hide_open_contexts()
        self.parent.setCurrentIndex(self.parent.currentIndex() + 1)

    def handle_user_click(self, event):
        if event.buttons() == Qt.LeftButton:
            self.hide_open_contexts()
            self.open_contexts.append(self.user_context_menu)
            self.user_context_menu.show()

    def create_content_view(self, month):
        self.list_view_widget.clear()

        data = get_data(month)
        items_1000 = data['1000']
        items_1010 = data['1010']
        items_extrato = data['extract']

        list_item_1000 = ContentItem(self.list_view_widget, "Caixa Geral - 1000", items_1000)
        list_item_1010 = ContentItem(self.list_view_widget, "Banco - 1010", items_1010)
        list_item_extrato = ContentItem(self.list_view_widget, "Extrato - 1010", items_extrato)
        self.list_view_widget.add_item(list_item_1000)
        self.list_view_widget.add_item(list_item_1010)
        self.list_view_widget.add_item(list_item_extrato)

    def handle_mouse_press(self, event):
        self.hide_open_contexts()

    def handle_folder_callback(self, event, folder):
        self.folder_context.set_clicked_item(folder)
        self.hide_open_contexts()
        self.folder_view.setCurrentRow(folder.get_id())

        if event.buttons() == Qt.LeftButton:
            self.create_content_view(folder.get_month_text())

        if event.buttons() == Qt.RightButton:
            self.open_contexts.append(self.folder_context)
            self.folder_context.show()

            context_left = folder.x() + 15
            context_top = folder.height() + folder.y() + self.folder_view.height() + 110 / folder.height() * 13

            self.folder_context.set_position(context_left, context_top)

    def create_dir_clicked(self):
        pass

    def remove_user(self):
        if remove_current_user():
            self.parent.setCurrentIndex(self.parent.currentIndex() - 1)

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
                self, 'Selecione o Extrato', 'c:\\', "Pdf files (*.pdf)")[0]
            print(filename)

    def add_items_clicked(self, event):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)

        if event.buttons() == Qt.RightButton:
            self.hide_open_contexts()
            self.open_contexts.append(self.add_extract_option)
            return self.add_extract_option.show()

        if dlg.exec_():
            folder_path = dlg.selectedFiles()
            print(folder_path)

    def start_insertion_clicked(self, event):
        if event.buttons() == Qt.RightButton:
            self.hide_open_contexts()
            self.open_contexts.append(self.start_insertion_option)
            self.start_insertion_option.show()

    def hide_open_contexts(self):
        for context in self.open_contexts:
            context.hide()

    def handle_status(self, status):
        if status == -1:
            self.status_container.hide()

        if status == 0:
            self.status_started.hide()
            self.status_finished.hide()
            self.status_finished_exception.hide()
        if status == 1:
            self.status_not_started.hide()
            self.status_finished.hide()
            self.status_finished_exception.hide()
        if status == 2:
            self.status_started.hide()
            self.status_not_started.hide()
            self.status_finished_exception.hide()
        if status == 3:
            self.status_started.hide()
            self.status_not_started.hide()
            self.status_finished.hide()


class ListItem(QListWidgetItem):

    def __init__(self, parent, content) -> None:
        super().__init__(parent)
        self.setSizeHint(content.sizeHint())

