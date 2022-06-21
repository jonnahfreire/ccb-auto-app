from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFrame, QVBoxLayout, QWidget

from view.ui.styles import context_item_style, set_element_shadow, context_menu_style


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
