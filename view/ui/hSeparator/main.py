from PyQt5.QtWidgets import QWidget, QLabel


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
