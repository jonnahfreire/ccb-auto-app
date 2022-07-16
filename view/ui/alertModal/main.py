from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QFrame

from view.ui.hSeparator.main import HSeparator
from view.ui.styles import modal_btn_cancel_style, set_element_shadow, modal_btn_ok_style, modal_btn_close_style, \
    context_menu_style, modal_backdrop_style


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

    def show(self, allow_resize=True):
        self.backdrop.setMinimumSize(self.parent.width(), self.parent.height())

        self.set_position(int(self.backdrop.width() / 2) - int(self.container.width() / 2),
                          int(self.backdrop.height() / 2) - 50 - int(self.container.height() / 2))
        self.backdrop.setVisible(True)
        self.backdrop.show()

    def hide(self):
        self.backdrop.setVisible(False)
