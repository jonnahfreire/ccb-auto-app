from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QFrame, QWidget

from view.ui.styles import set_element_shadow, insertion_item_style, content_item_style


class ContentItem(QWidget):

    def __init__(self, parent, header, items: list) -> None:
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
        self.header.setMinimumSize(self.parent.width() + 128, 32)
        self.header.setMaximumSize(self.parent.width(), 32)
        self.header.setStyleSheet(content_item_style)
        self.header.setText(header)
        set_element_shadow(self.header, blur=3.5)
        self.layout_container.addWidget(self.header)

        if len(self.items) == 0:
            item_container = QHBoxLayout()
            item_container.setContentsMargins(0, 0, 0, 0)
            item_container.setSpacing(10)
            item_container.setAlignment(Qt.AlignLeft)
            items_not_found = QLabel("Nenhuma despesa / receita encontrada")
            items_not_found.setStyleSheet(insertion_item_style + "background-color: #fff;")
            item_container.addWidget(items_not_found)
            self.layout_container.addLayout(item_container)

        for index, item in enumerate(self.items, 1):
            self.item_container = QHBoxLayout()
            self.item_container.setContentsMargins(0, 0, 0, 0)
            self.item_container.setSpacing(10)
            self.item_container.setAlignment(Qt.AlignLeft)

            item_icon = self.set_icon()
            item_name = self.create_item("NF " + item.get("num"))
            item_date = self.create_item("/".join(item.get("date")))
            item_value = self.create_item("R$ " + item.get("value"))
            item_expenditure = self.create_item("DP " + item.get("expenditure"))

            self.item_container.addWidget(item_icon, index)
            self.item_container.addWidget(item_name, index)
            self.item_container.addWidget(item_date, index)
            self.item_container.addWidget(item_value, index)
            self.item_container.addWidget(item_expenditure, index)

            self.layout_container.addLayout(self.item_container)

        self.end_line = QLabel()
        self.end_line.setMinimumSize(self.parent.width() + 128, 1)
        self.end_line.setMaximumSize(self.parent.width(), 1)
        self.end_line.setStyleSheet("border-bottom: 0.5px solid rgb(210, 210, 210);")

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
