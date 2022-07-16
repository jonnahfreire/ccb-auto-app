from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame, QVBoxLayout

from view.ui.listView.main import ListView
from view.ui.styles import set_element_shadow, context_menu_style


class NotificationContainerList(QFrame):

    def __init__(self, parent, width=120, height=80, left=0, top=0):
        super().__init__()
        self.parent = parent

        self.is_shown = False
        self.items = []
        self.current_item = None
        self.width = width
        self.height = height
        self.left = left
        self.top = top

        self.notification_container = QFrame(self.parent)
        self.notification_container.setFrameShape(QFrame.StyledPanel)
        self.notification_container.setFrameStyle(QFrame.Raised)
        self.notification_container.setStyleSheet(context_menu_style)
        self.notification_container.setMinimumSize(self.width, self.height)
        self.notification_container.setMaximumSize(self.width, self.height)
        self.notification_container.setVisible(False)
        set_element_shadow(self.notification_container)

        self.notification_container_layout = QVBoxLayout(self.notification_container)
        self.notification_container_layout.setContentsMargins(0, 0, 0, 0)
        self.notification_container_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.set_position(left, top)

        self.no_notifications_message = QLabel("Nenhuma notificação para exibir")
        self.notification_container_layout.addWidget(self.no_notifications_message)

        self.content_container = QFrame()

        self.content_container.setMinimumSize(self.width, 170)
        self.content_container.setMaximumSize(self.width, 180)

        self.list_container = ListView(self.content_container, self.width,  120)
        self.list_container.hide_vertical_scrollbar()

        self.footer = QFrame()
        self.footer.setStyleSheet(
            """
                background: rgb(240, 240, 240);
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
                border-top: 1px solid rgb(210, 210, 210);
            """)
        self.footer.setCursor(Qt.PointingHandCursor)
        self.footer.setMinimumSize(self.width, 23)
        self.footer.setMaximumSize(self.width, 23)

        self.footer_layout = QHBoxLayout(self.footer)
        self.footer_layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_clear = QLabel("Limpar", self.footer)
        self.btn_clear.setStyleSheet(
            """
                QLabel {
                    font-size: 9pt;
                    font-family: 'SegoeUI Semibold';
                    border: none;
                    border-radius: 0px;
                }
                QLabel:hover {
                    border-bottom: 1px solid rgb(0, 0, 0);
                }
            """
        )
        self.btn_clear.mousePressEvent = self.clear_all_notifications

        trash_icon = QLabel()
        trash_icon.setStyleSheet("border: none; border-radius: 0px;")
        trash_icon.setPixmap(QPixmap("view/assets/trash.png").scaled(15, 15))
        self.footer_layout.addWidget(self.btn_clear)
        self.footer_layout.addWidget(trash_icon)

        self.notification_container_layout.addWidget(self.content_container)
        self.notification_container_layout.addWidget(self.footer)

    def set_position(self, left_pos, top):
        self.notification_container.move(left_pos, top)

    def add_item(self, item):
        if item is not None:
            self.no_notifications_message.hide()
        self.list_container.add_item(item)

        self.list_container.item_clicked(self.handle_item_clicked)

    def show(self, left=0, top=0):
        self.is_shown = True
        self.set_position(left, top)
        self.notification_container.show()
        self.content_container.show()
        self.footer.show()

    def hide(self):
        self.is_shown = False
        self.notification_container.hide()

    def clear_all_notifications(self, e):
        self.list_container.clear()
        self.content_container.hide()
        self.footer.hide()
        self.no_notifications_message.show()

    def handle_item_clicked(self):
        print("Clicou")


class NotificationItem(QWidget):

    def __init__(self, parent, item: dict, width=100, height=30) -> None:
        super().__init__()
        self.close_btn = None
        self.parent = parent
        self.item = item
        self.width = width
        self.height = height

        self.setStyleSheet("""
            QWidget {
                background-color: rgb(240, 240, 240); 
                border-bottom: 1px solid rgb(230, 230, 230);
                font-family: 'SegoeUi Semibold';
                border: none;
                border-radius: 0px;
            }
            """)
        set_element_shadow(self, blur=2)
        self.setContentsMargins(0, 2, 0, 3)

        self.container = QFrame(self.parent)
        self.container.setContentsMargins(0, 0, 0, 0)

        self.layout_container = QHBoxLayout(self.container)
        self.layout_container.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout_container.setSpacing(0)
        self.layout_container.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_container)

        self.fill_items(self.item)

    def fill_items(self, item):
        icon = self.set_icon(item.get("icon"))

        # notification main content
        main_content_container = QFrame()
        main_content_layout = QVBoxLayout(main_content_container)
        main_content_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        main_content_layout.setContentsMargins(0, 0, 0, 0)

        # notification header
        notification_header = QLabel()
        notification_header.setMinimumSize(self.parent.width - 105, 30)
        notification_header.setMaximumSize(self.parent.width - 105, 30)
        notification_header.setText(item.get("header"))
        notification_header.setStyleSheet(
            """
                background: transparent; 
                border-bottom: 1px solid rgb(210, 210, 210);
                font-size: 10pt;
                font-family: 'SegoeUi Semibold';
                border-radius: 0px;
            """)

        # notification title
        notification_title = QLabel()
        notification_title.setMinimumSize(self.parent.width - 105, 20)
        notification_title.setMaximumSize(self.parent.width - 105, 20)
        notification_title.setText(item.get("title"))

        # notification message
        notification_message = QLabel()
        notification_message.setMinimumSize(self.parent.width - 105, 15)
        notification_message.setMaximumSize(self.parent.width - 105, 15)
        notification_message.setWordWrap(True)
        notification_message.setText(item.get("message"))
        self.close_btn = self.remove_notification_btn()

        main_content_layout.addWidget(notification_header)
        main_content_layout.addWidget(notification_title)
        main_content_layout.addWidget(notification_message)

        # place contents
        self.layout_container.addWidget(icon)
        self.layout_container.addWidget(main_content_container)
        self.layout_container.addWidget(self.close_btn)

    def handle_remove_item(self, e):
        self.parent.list_container.remove_current_item()
        # self.parent.list_container.takeItem(self.parent.list_container.currentRow())
        print("current row: ", self.parent.list_container.currentRow())
        print("Clicked to remove!!")


    @staticmethod
    def set_icon(icon_type=None):
        icon_container = QFrame()
        icon_container.setMinimumSize(50, 80)
        icon_container.setLayoutDirection(Qt.RightToLeft)
        icon_layout_container = QVBoxLayout(icon_container)

        item_icon = QLabel(icon_container)
        if icon_type == "danger":
            icon_path = "view/assets/exclamation-triangle-fill.png"
        else:
            icon_path = "view/assets/check-circle-fill.png"

        item_icon.setPixmap(QPixmap(icon_path).scaled(45, 45))
        item_icon.setMaximumSize(45, 45)
        item_icon.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        item_icon.setScaledContents(True)
        item_icon.setMargin(4)

        icon_layout_container.addWidget(item_icon)
        return icon_container

    @staticmethod
    def remove_notification_btn():
        icon_container = QFrame()
        icon_container.setMinimumSize(40, 80)
        icon_layout_container = QVBoxLayout(icon_container)
        icon_layout_container.setContentsMargins(0, 0, 0, 0)

        item_icon = QLabel(icon_container)
        item_icon.setCursor(Qt.PointingHandCursor)

        icon_path = "view/assets/close.png"
        item_icon.setPixmap(QPixmap(icon_path).scaled(45, 45))
        item_icon.setMaximumSize(35, 35)
        item_icon.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        item_icon.setScaledContents(True)
        item_icon.setMargin(8)

        icon_layout_container.addWidget(item_icon)
        return icon_container
