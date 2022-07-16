from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QFrame, QWidget, QBoxLayout

from view.ui.styles import set_element_shadow, insertion_item_style, content_item_style, frame_bg_danger, \
    frame_bg_success


class OptionContainer(QFrame):

    def __init__(self, parent=None, item=None) -> None:
        super().__init__()
        self.parent = parent
        self.item = item

        self.is_shown = False

        self.setMinimumSize(500, 30)
        self.setMaximumSize(500, 30)
        self.setStyleSheet("background: transparent;")
        self.setContentsMargins(0, 0, 0, 0)
        self.hide()

        self.item_layout = QHBoxLayout(self)
        self.item_layout.setContentsMargins(0, 0, 0, 0)
        self.item_layout.setSpacing(10)
        self.item_layout.setAlignment(Qt.AlignLeft)

    def add(self, text, icon_path, bg_style):
        self.item_layout.addWidget(self.option_item(text, icon_path, bg_style))

    def toggle(self):
        if self.is_shown:
            self.hide()
            self.is_shown = False
        else:
            self.show()
            self.is_shown = True

        return self.is_shown

    @staticmethod
    def option_item(text, icon_path, bg_style):
        item_frame = QFrame()
        if bg_style == "danger":
            bg_style = frame_bg_danger

        if bg_style == "success":
            bg_style = frame_bg_success

        item_frame.setMaximumHeight(20)
        set_element_shadow(item_frame)
        item_frame.setStyleSheet(bg_style)
        item_frame.setCursor(Qt.PointingHandCursor)

        item_container = QHBoxLayout(item_frame)
        item_container.setContentsMargins(0, 0, 0, 0)
        item_container.setSpacing(2)
        item_container.setAlignment(Qt.AlignLeft)

        btn = QLabel(text)
        btn.setStyleSheet("background: transparent;")

        icon = QLabel()
        icon.setStyleSheet("background: transparent;")

        icon.setPixmap(QPixmap(icon_path).scaled(20, 20))
        icon.setMaximumSize(20, 20)
        icon.setScaledContents(True)
        icon.setMargin(1)

        item_container.addWidget(btn)
        item_container.addWidget(icon)

        return item_frame


class ContentItem(QWidget):

    def __init__(self, parent, header_text: str, items: list, width=100, height=30) -> None:
        super().__init__()
        self.parent = parent
        self.items = items
        self.header_text = header_text
        self.width = width
        self.height = height

        self.container = QFrame(self.parent)
        self.layout_container = QVBoxLayout(self.container)
        self.layout_container.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.layout_container.setSpacing(5)
        self.layout_container.setContentsMargins(0, 5, 0, 10)
        self.setLayout(self.layout_container)

        self.fill_items(self.items)

    def fill_items(self, items):
        header = QLabel()
        header.setMinimumSize(self.width-2, 32)
        header.setStyleSheet(content_item_style)
        header.setText(self.header_text)
        set_element_shadow(header, blur=3.5)
        self.layout_container.addWidget(header)

        if len(items) == 0:
            item_container = QHBoxLayout()
            item_container.setContentsMargins(0, 0, 0, 0)
            item_container.setSpacing(10)
            item_container.setAlignment(Qt.AlignLeft)
            items_not_found = QLabel("Nenhuma despesa / receita encontrada")
            items_not_found.setStyleSheet(insertion_item_style + "background-color: #fff;")
            item_container.addWidget(items_not_found)
            self.layout_container.addLayout(item_container)

        for index, item in enumerate(items, 1):
            item_widget = self.__set_item(item)
            self.layout_container.addWidget(item_widget)

            options_container = OptionContainer(item)
            options_container.add("Excluir", "view/assets/trash-white.png", "danger")
            options_container.add("Abrir local", "view/assets/folder-symlink-white.png", "success")
            options_container.add("Marcar como lançado", "view/assets/check-square.png", "success")

            item_widget.mousePressEvent = lambda e: self.handle_show_options(options_container)
            self.layout_container.addWidget(options_container)

        self.layout_container.addWidget(self.set_bottom_line())

    def handle_show_options(self, options_container):
        if options_container.toggle():
            self.container.setContentsMargins(0, 5, 0, 5)
        else:
            self.parent.resize(self.parent.width(), self.parent.height()+100)
            self.container.setContentsMargins(0, 5, 0, 5)

    @staticmethod
    def set_bottom_line():
        line_container = QFrame()
        line_container.setStyleSheet("background: transparent; color: rgb(210, 210, 210);")
        line_container.setFrameShape(QFrame.HLine)
        return line_container

    def __set_item(self, item):
        item_frame_container = QFrame()
        item_frame_container.setStyleSheet("background: transparent;")
        item_frame_container.setMinimumSize(self.parent.width(), 35)
        item_frame_container.setMaximumSize(self.parent.width(), 35)
        item_frame_container.setContentsMargins(0, 5, 0, 5)
        item_frame_container.setCursor(Qt.PointingHandCursor)

        h_layout_container = QHBoxLayout(item_frame_container)
        h_layout_container.setContentsMargins(0, 0, 0, 5)
        h_layout_container.setSpacing(10)
        h_layout_container.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        item_icon = self.set_icon()
        filename = item.get("file-name")
        if "DB AT" in filename:
            filename = f"{item.get('file-name')[:5]} {item.get('num')}"

        expenditure = item.get("expenditure")
        if item.get("insert-type") == "MOVINT":
            expenditure = item.get("orig-account")
        expenditure = f"DP {expenditure}"

        item_name = self.create_item(filename)
        item_date = self.create_item("/".join(item.get("date")))
        item_value = self.create_item("R$ {}".format(item.get('value'), "2f"))
        item_expenditure = self.create_item(expenditure)

        h_layout_container.addWidget(item_icon)
        h_layout_container.addWidget(item_name)
        h_layout_container.addWidget(item_date)
        h_layout_container.addWidget(item_value)
        h_layout_container.addWidget(item_expenditure)

        return item_frame_container

    @staticmethod
    def create_item(text: str, minwh: int = 100, maxwh: int = 100, minht: int = 32, maxht: int = 32) -> QLabel:
        item = QLabel(text)
        item.setStyleSheet(insertion_item_style)
        set_element_shadow(item)

        item.setAlignment(Qt.AlignCenter)
        item.setLayoutDirection(Qt.RightToLeft)
        item.setCursor(Qt.PointingHandCursor)

        item.setMinimumSize(minwh, minht)
        item.setMaximumSize(maxwh, maxht)
        return item

    @staticmethod
    def set_icon():
        item_icon = QLabel()
        icon_path = "view/assets/file-earmark-pdf.png"
        item_icon.setPixmap(QPixmap(icon_path).scaled(30, 30))
        item_icon.setMaximumSize(28, 32)
        item_icon.setMinimumHeight(32)
        item_icon.setMaximumHeight(32)
        item_icon.setFixedHeight(32)

        item_icon.setStyleSheet(insertion_item_style)
        set_element_shadow(item_icon)
        item_icon.setScaledContents(True)
        item_icon.setMargin(5)
        return item_icon
