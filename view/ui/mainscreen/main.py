import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from app.main import get_month_directories
from app.main import get_username
from app.main import remove_current_user
from app.main import remove_month_directory
from app.main import open_directory

from app.utils.main import get_month_list, get_current_month
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
        self.create_content_view()

    def set_username(self):
        username = get_username()
        self.userName.setText(username)

    def set_folders_list(self):
        months = get_month_directories()

        if len(self.folders) > 0:
            self.folders = []

        for index, month in enumerate(months):
            folder = FolderItem(self.folder_view, month.replace("-", "/"))
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

    def create_content_view(self):
        list_view_widget = ListView(self.itemsContainer,
                                    self.itemsContainer.width(), self.itemsContainer.height(), 0, 0)
        list_view_widget.hide_horizontal_scrollbar()
        list_view_widget.hide_vertical_scrollbar()
        list_view_widget.set_vertical()

        items_1000 = [
            {"name": "NF 922", "date": "12/06/2022", "value": "120,00", "expenditure": "3026"},
            {"name": "CF 22", "date": "01/06/2022", "value": "150,00", "expenditure": "3026"}
        ]

        items_1010 = [
            {"name": "NF 122", "checknum": "900534", "date": "19/06/2022", "value": "1220,00", "expenditure": "1120"},
            {"name": "NF 202", "checknum": "900534", "date": "24/06/2022", "value": "900,00", "expenditure": "1120"}
        ]

        items_extrato = [
            {"name": "RESGATE", "date": "29/06/2022", "value": "2000,00", "expenditure": "1033"},
            {"name": "APLICAÇÃO", "date": "09/06/2022", "value": "5000,00", "expenditure": "1010"},
        ]

        list_item_1000 = ContentItem(list_view_widget, "Caixa Geral - 1000", items_1000)
        list_item_1010 = ContentItem(list_view_widget, "Banco - 1010", items_1010)
        list_item_extrato = ContentItem(list_view_widget, "Extrato - 1010", items_extrato)
        list_view_widget.add_item(list_item_1000)
        list_view_widget.add_item(list_item_1010)
        list_view_widget.add_item(list_item_extrato)

    def handle_mouse_press(self, event):
        self.hide_open_contexts()

    def handle_folder_callback(self, event, folder):
        self.folder_context.set_clicked_item(folder)
        self.hide_open_contexts()
        self.folder_view.setCurrentRow(folder.get_id())

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


class ListView(QListWidget):

    def __init__(self, parent, width=100, height=100, x=0, y=0) -> None:
        super().__init__()
        self.parent = parent
        self.items = []
        self.current_id = 0

        self.list_view_widget = QListWidget(self.parent)
        self.list_view_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.list_view_widget.setGeometry(x, y, width, height)
        self.list_view_widget.setFocusPolicy(Qt.NoFocus)
        self.list_view_widget.sortItems(Qt.AscendingOrder)
        self.list_view_widget.setStyleSheet(list_view_style)

    def set_style(self, style):
        self.list_view_widget.setStyleSheet(style)

    def hide_horizontal_scrollbar(self):
        scrollbar = QScrollBar(self.parent)
        scrollbar.setStyleSheet("width: 0px; height: 0px;")
        self.list_view_widget.setHorizontalScrollBar(scrollbar)

    def hide_vertical_scrollbar(self):
        scrollbar = QScrollBar(self.parent)
        scrollbar.setStyleSheet("width: 0px; height: 0px;")
        self.list_view_widget.setVerticalScrollBar(scrollbar)

    def set_content_padding(self, pd):
        self.list_view_widget.setSpacing(pd)

    def set_horizontal(self):
        self.list_view_widget.setFlow(QListView.LeftToRight)
        self.list_view_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

    def set_vertical(self):
        self.list_view_widget.setFlow(QListView.TopToBottom)
        self.list_view_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def set_fixed_size(self, width, height):
        self.list_view_widget.setMinimumSize(width, height)
        self.list_view_widget.setMaximumSize(width, height)

    def add_item(self, item):
        list_item = QListWidgetItem(self.list_view_widget)
        list_item.setSizeHint(item.sizeHint())
        self.current_id += 1
        self.items.append({"id": self.current_id, "widget": list_item, "item": item})
        self.list_view_widget.addItem(list_item)
        self.list_view_widget.setItemWidget(list_item, item)

        return self.current_id

    def item_clicked(self, callback=None):
        if callback is not None:
            self.list_view_widget.itemClicked.connect(callback)

    def get_item(self, widget):
        for it in self.items:
            if it["widget"] == widget:
                return it["item"]

    def get_item_widget(self, item):
        for it in self.items:
            if it["item"] == item:
                return it["widget"]

    def get_item_id(self, item):
        for it in self.items:
            if it["item"] == item:
                return it["id"]

    def remove_item(self, widget):
        item = self.get_item(widget)
        self.list_view_widget.removeItemWidget(widget)
        return item

    def get_self(self):
        return self.list_view_widget

    def clear(self):
        self.items = []


class FolderItem(QWidget):

    def __init__(self, parent, month=None) -> None:
        super().__init__()
        self.parent = parent
        self.__id = 0
        self.item_parent = None

        self.container = QFrame()
        self.container.setStyleSheet(folder_style)
        self.container.setMinimumSize(115, 55)
        self.container.setMaximumSize(115, 55)
        self.container.setCursor(Qt.PointingHandCursor)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 5, 0)
        self.layout.addWidget(self.container)
        self.setLayout(self.layout)

        self.folder_icon = QLabel(self.container)
        self.folder_icon.setStyleSheet(folder_icon_style)
        self.folder_icon.move(11, 9)
        self.folder_icon.setMinimumSize(38, 38)
        self.folder_icon.setMaximumSize(38, 38)
        self.folder_icon.setScaledContents(True)
        self.folder_icon.setPixmap(QPixmap("view/assets/folder.png"))
        set_element_shadow(self.container,
                           offset=1, shadow_color=QColor.fromRgbF(0.0, 0.0, 0.0, 0.9))

        self.month_text = QLabel(month, self.container)
        self.month_text.setStyleSheet(folder_text_style)
        self.month_text.move(55, 14)
        self.month_text.setMinimumSize(55, 30)
        self.month_text.setMaximumSize(55, 30)
        if self.month_text.text() == get_current_month():
            self.set_active()

    def set_active(self):
        self.set_folder_open()

    def set_id(self, folder_id):
        self.__id = folder_id

    def get_id(self):
        return self.__id

    def set_folder_open(self):
        if self.container is not None:
            self.container.setStyleSheet(folder_style_active)
            self.folder_icon.setPixmap(QPixmap("view/assets/folder-open.png"))

    def set_folder_closed(self):
        if self.container is not None:
            self.container.setStyleSheet(folder_style)
            self.folder_icon.setPixmap(QPixmap("view/assets/folder.png"))

    def set_month_text(self, text):
        self.month_text.setText(text)

    def check_btn_clicked(self, folders, event, callback):
        if event.buttons() == Qt.RightButton:
            callback(event, self)
        else:
            for folder in folders:
                try:
                    folder.set_folder_closed()
                except RuntimeError:
                    folders.remove(folder)

            self.set_folder_open()
            callback(event, self)

    def click(self, folders, callback):
        self.container.mousePressEvent = lambda e: self.check_btn_clicked(folders, e, callback)


class ContentItem(QWidget):

    def __init__(self, parent, header, items) -> None:
        super().__init__()
        self.parent = parent
        self.items = items

        self.container = QFrame(self.parent)
        self.container.setMinimumSize(self.parent.width(), 50)

        self.layout_container = QVBoxLayout(self.container)
        self.layout_container.setSpacing(5)
        self.layout_container.setContentsMargins(0, 10, 0, 10)
        self.setLayout(self.layout_container)

        self.header = QLabel()
        self.header.setMinimumSize(self.parent.width()+128, 32)
        self.header.setMaximumSize(self.parent.width(), 32)
        self.header.setStyleSheet(
            """
            background-color: rgb(250,250,250);
            padding-left: 5px;
            border-radius: 5px;
            
            margin-top: 5px;
            margin-bottom: 5px;
            padding: 5px;
            
            font-size: 10pt;
            """
        )
        self.header.setText(header)
        set_element_shadow(self.header, blur=3.5)

        self.layout_container.addWidget(self.header)

        for index, item in enumerate(self.items, 1):
            self.item_container = QHBoxLayout()
            self.item_container.setContentsMargins(0, 0, 0, 0)
            self.item_container.setSpacing(10)
            self.item_container.setAlignment(Qt.AlignLeft)

            item_icon = self.set_icon()
            item_name = self.create_item(item.get("name"))
            item_date = self.create_item(item.get("date"))
            item_value = self.create_item(item.get("value"))
            item_expenditure = self.create_item(item.get("expenditure"))

            self.item_container.addWidget(item_icon, index)
            self.item_container.addWidget(item_name, index)
            self.item_container.addWidget(item_date, index)
            self.item_container.addWidget(item_value, index)
            self.item_container.addWidget(item_expenditure, index)

            self.layout_container.addLayout(self.item_container)
            # self.items.append(item)

        self.end_line = QLabel()
        self.end_line.setMinimumSize(self.parent.width() + 128, 1)
        self.end_line.setMaximumSize(self.parent.width(), 1)
        self.end_line.setStyleSheet(
            "border-bottom: 0.5px solid rgb(210, 210, 210);"
        )

        self.layout_container.addWidget(self.end_line)

    @staticmethod
    def create_item(text: str) -> QLabel:
        item = QLabel(text)
        item.setStyleSheet(insertion_item_style)
        set_element_shadow(item)

        item.setAlignment(Qt.AlignCenter)
        item.setLayoutDirection(Qt.RightToLeft)
        item.setCursor(Qt.PointingHandCursor)

        item.setMinimumSize(100, 32)
        item.setMaximumSize(100, 32)
        return item

    @staticmethod
    def set_icon():
        item_icon = QLabel()
        icon_path = "view/assets/file-earmark-pdf.png"
        item_icon.setPixmap(QPixmap(icon_path).scaled(30, 30))
        item_icon.setMaximumSize(28, 30)

        item_icon.setStyleSheet(insertion_item_style)
        set_element_shadow(item_icon)
        item_icon.setScaledContents(True)
        item_icon.setMargin(5)
        return item_icon


class InsertionItem(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.id = 0

        self.container = QVBoxLayout()
        self.container.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.container)

        self.account1000_container = QFrame()
        self.account1000_container.setStyleSheet("background-color: green;")
        self.account1010_container = QFrame()
        self.extract_container = QFrame()

        self.account1000_header = QLabel("Caixa Geral - 1000", self.account1000_container)
        self.account1010_header = QLabel("Banco - 1010", self.account1010_container)
        self.extract_header = QLabel("Extrato", self.extract_container)

        self.container.addWidget(self.account1000_header)
        self.container.addWidget(self.account1010_header)
        self.container.addWidget(self.extract_header)

        self.item_container1000 = QHBoxLayout()
        self.item_container1000.setSpacing(10)
        self.item_container1000.setAlignment(Qt.AlignLeft)

        self.item_icon = QLabel()
        self.icon("view/assets/file-earmark-pdf.png")
        self.item_icon.setMaximumSize(30, 30)

        self.items = []

        self.item_container1000.addWidget(self.item_icon, 0)
        for index, item in enumerate(["NF 922", "12/06/2022", "R$ 120,00", "DP 3026", "Não lançado"], 1):
            item = QLabel(item)

            item.setStyleSheet(insertion_item_style)
            set_element_shadow(item)

            item.setAlignment(Qt.AlignCenter)
            item.setLayoutDirection(Qt.RightToLeft)
            item.setCursor(Qt.PointingHandCursor)

            item.setMinimumSize(100, 30)
            item.setMaximumSize(100, 30)

            self.item_container1000.addWidget(item, index)
            self.items.append(item)

        self.container.addLayout(self.item_container1000)

    def icon(self, icon):
        self.item_icon.setStyleSheet(insertion_item_style)
        self.item_icon.setScaledContents(True)
        self.item_icon.setMargin(4)
        self.item_icon.setPixmap(QPixmap(icon).scaled(30, 30))


class ContextMenu(QWidget):

    def __init__(self, parent, width=120, height=80):
        super().__init__()
        self.parent = parent

        self.is_shown = False
        self.items = []
        self.current_item = None
        self.width = width
        self.height = height

        self.context_menu_container = QFrame(self.parent)
        self.context_menu_container.setFrameShape(QFrame.StyledPanel)
        self.context_menu_container.setFrameStyle(QFrame.Raised)

        self.context_menu_container.setStyleSheet(context_menu_style)
        self.context_menu_container.setMinimumSize(self.width, self.height)
        self.context_menu_container.setMaximumSize(self.width, self.height)
        self.context_menu_container.setVisible(False)
        set_element_shadow(self.context_menu_container)

        self.context_menu_layout = QVBoxLayout(self.context_menu_container)
        self.set_position(150, 100)

    def set_position(self, left_pos, top):
        self.context_menu_container.move(left_pos, top)

    def set_clicked_item(self, item):
        self.current_item = item

    def add_item(self, item_title, callback=None, icon=None):
        if icon is not None:
            item_frame = QFrame()
            item_layout = QHBoxLayout(item_frame)
            item_layout.setContentsMargins(0, 0, 0, 0)

            item = QLabel(item_title)
            item.setStyleSheet(context_item_style + "padding-left: 2px;")
            item.setMinimumSize(50, 20)
            item.setMaximumSize(self.width - 20, 20)
            item.setAlignment(Qt.AlignLeft)
            item.setCursor(Qt.PointingHandCursor)
            item_frame.mousePressEvent = callback
            item_layout.addWidget(item)

            self.items.append(item)

            icon_container = QLabel()
            icon_container.setPixmap(QPixmap(icon))
            icon_container.setScaledContents(True)
            icon_container.setMinimumSize(18, 18)
            icon_container.setMaximumSize(18, 18)
            icon_container.setAlignment(Qt.AlignHCenter)
            icon_container.setCursor(Qt.PointingHandCursor)
            item_layout.addWidget(icon_container)

            self.context_menu_layout.addWidget(item_frame)
        else:
            item = QLabel(item_title)
            item.setStyleSheet(context_item_style)
            item.setMinimumSize(self.context_menu_container.width() - 20, 20)
            item.setMaximumSize(self.context_menu_container.width(), 20)
            item.setAlignment(Qt.AlignHCenter)
            item.setCursor(Qt.PointingHandCursor)
            item.mousePressEvent = callback
            self.context_menu_layout.addWidget(item)

    def add_separator(self):
        separator = QLabel()
        separator.setMinimumSize(self.width - 20, 1)
        separator.setMaximumSize(self.width - 20, 1)
        separator.setStyleSheet(u"background-color: rgb(206, 206, 206);")
        self.context_menu_layout.addWidget(separator)

    def show(self):
        self.is_shown = True
        self.context_menu_container.show()

    def hide(self):
        self.is_shown = False
        self.context_menu_container.hide()


class AlertModal(QFrame):

    def __init__(self, parent, width=300, height=200, title=None, body=None) -> None:
        super().__init__()
        self.parent = parent
        self.result = False

        self.width = width
        self.height = height
        self.title = title
        self.body = body

        self.backdrop = QFrame(self.parent)
        self.backdrop.setFrameShape(QFrame.StyledPanel)
        self.backdrop.setFrameStyle(QFrame.Raised)
        self.backdrop.setStyleSheet(modal_backdrop_style)
        self.backdrop.setMinimumSize(self.parent.width(), self.parent.height())
        self.backdrop.setMaximumSize(self.parent.width(), self.parent.height())
        self.backdrop.setVisible(True)

        self.container = QFrame(self.backdrop)
        self.container.setFrameShape(QFrame.StyledPanel)
        self.container.setFrameStyle(QFrame.Raised)
        self.container.setStyleSheet(context_menu_style)
        self.container.setMinimumSize(self.width, self.height)
        self.container.setMaximumSize(self.width, self.height)
        set_element_shadow(self.container)

        self.modal_title = QLabel(self.title, self.container)
        self.modal_title.setMinimumSize(self.container.width() - 45, 50)
        self.modal_title.setMaximumSize(self.container.width() - 45, 50)
        self.modal_title.setStyleSheet("font: 12pt 'Segoe UI'; font-weight: 500; padding-left: 5px;")

        self.modal_close = QLabel(self.container)
        self.modal_close.setCursor(Qt.PointingHandCursor)
        self.modal_close.move(self.width - 40, 10)
        self.modal_close.setScaledContents(True)
        self.modal_close.setMinimumSize(35, 35)
        self.modal_close.setMaximumSize(35, 35)
        self.modal_close.setMargin(10)
        self.modal_close.setPixmap(QPixmap("view/assets/close.png"))
        self.modal_close.setStyleSheet(modal_btn_close_style)

        self.modal_body = QLabel(self.container)
        self.modal_body.setText(self.body)
        self.modal_body.move(0, self.modal_title.height() + 5)
        self.modal_body.setMinimumSize(self.container.width(), 50)
        self.modal_body.setMaximumSize(self.container.width(), 100)
        self.modal_body.setStyleSheet("font: 11pt 'Segoe UI'; font-weight: 400; padding-left: 5px;")
        self.modal_body.setWordWrap(True)

        # modal line separator
        separator = HSeparator(self.container, self.width, self.height)
        separator.set_position(292, 150)

        separator = HSeparator(self.container, self.width, self.height)
        separator.set_position(292, 50)

        self.modal_btn_ok = QLabel("OK", self.container)
        self.modal_btn_ok.setCursor(Qt.PointingHandCursor)
        self.modal_btn_ok.setStyleSheet(modal_btn_ok_style)
        set_element_shadow(self.modal_btn_ok)
        self.modal_btn_ok.move(self.width - 140, self.height - 40)

        self.modal_btn_cancel = QLabel("Cancelar", self.container)
        self.modal_btn_cancel.setCursor(Qt.PointingHandCursor)
        self.modal_btn_cancel.move(self.width - 90, self.height - 40)
        self.modal_btn_cancel.setStyleSheet(modal_btn_cancel_style)
        set_element_shadow(self.modal_btn_cancel)

        self.modal_btn_cancel.mousePressEvent = self.handle_btn_cancel
        self.modal_close.mousePressEvent = self.handle_btn_close

        self.set_position(int(self.backdrop.width() / 2) - int(self.container.width() / 2),
                          int(self.backdrop.height() / 2) - 50 - int(self.container.height() / 2))

    def set_body_text(self, text):
        self.modal_body.setText(text)

    def ok(self, callback):
        def handle_ok_press(event):
            if event.buttons() == Qt.LeftButton:
                self.hide()
                callback()

        self.modal_btn_ok.mousePressEvent = handle_ok_press

    def handle_btn_cancel(self, event):
        if event.buttons() == Qt.LeftButton:
            self.hide()

    def handle_btn_close(self, event):
        if event.buttons() == Qt.LeftButton:
            self.hide()

    def set_position(self, left_pos, top):
        self.container.move(left_pos, top)

    def show(self):
        self.backdrop.setVisible(True)
        self.backdrop.show()

    def hide(self):
        self.backdrop.setVisible(False)


class HSeparator(QWidget):
    def __init__(self, parent, parent_width, parent_height, sep_height=1) -> None:
        super().__init__()
        self.width = parent_width
        self.height = parent_height
        self.sep_height = sep_height

        self.separator = QLabel(parent)
        self.set_position(0, 0)
        self.separator.setMinimumSize(self.width - 20, self.sep_height)
        self.separator.setMaximumSize(self.width - 20, self.sep_height)
        self.separator.setStyleSheet(u"background-color: rgb(206, 206, 206);")

    def set_position(self, left_pos=0, top=0):
        self.separator.move(self.width - left_pos, self.height - top)

    def set_size(self, width, height):
        self.separator.setMinimumSize(width, height)
        self.separator.setMaximumSize(width, height)
