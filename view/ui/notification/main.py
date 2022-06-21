from PyQt5.QtGui import Qt, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame, QVBoxLayout

from view.ui.styles import insertion_item_style, set_element_shadow


class NotificationContainerList(QWidget):

    def __init__(self, text):
        super().__init__()
        self.item = QLabel(text)
        self.item.setStyleSheet(insertion_item_style)
        set_element_shadow(self.item)

        self.item.setAlignment(Qt.AlignCenter)
        self.item.setLayoutDirection(Qt.RightToLeft)
        self.item.setCursor(Qt.PointingHandCursor)

        self.item.setMinimumSize(100, 32)
        self.item.setMaximumSize(100, 32)

    def item(self):
        return self.item()


class NotificationItem(QWidget):

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

