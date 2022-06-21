from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFrame, QWidget

from app.utils.main import get_current_month
from view.ui.styles import folder_style, folder_style_active, folder_text_style, set_element_shadow, folder_icon_style


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

    def get_month_text(self):
        return self.month_text.text().replace("/", "-")

    def click(self, folders, callback):
        self.container.mousePressEvent = lambda e: self.check_btn_clicked(folders, e, callback)
