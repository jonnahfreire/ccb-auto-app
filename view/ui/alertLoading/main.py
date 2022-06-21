from PyQt5.QtCore import QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QFrame, QLabel
from ..styles import *


class AlertLoading(QWidget):

    def __init__(self, parent, p_w=0, p_h=0, container_w=200, container_h=50,
                 icon_w=30, icon_h=30, message=None, infinity=True, style=None, duration=3000,
                 on_animation_end=None) -> None:
        super().__init__()
        self.parent = parent
        self.duration = duration
        self.infinity = infinity
        self.message = message
        self.style = style

        self.is_running = False
        self.on_animation_end = on_animation_end

        self.alert_container = QFrame(self.parent)
        self.alert_container.setVisible(False)

        self.alert_container.setMinimumSize(container_w, container_h)
        self.alert_container.setMaximumSize(container_w, container_h)
        self.alert_container.setStyleSheet(alert_loading_container_style if self.style is None else self.style)
        set_element_shadow(self.alert_container)

        self.set_position(int(p_w / 2) - int(container_w / 2), int(p_h / 2) - 80 - int(container_h / 2))

        self.movie = QMovie("view/assets/loading-line.gif")

        self.message_text = QLabel(self.message, self.alert_container)
        self.message_text.move(20, int(container_h / 3))
        self.message_text.setStyleSheet(alert_loading_text_style)

        self.label_animation = QLabel(self.alert_container)
        self.label_animation.setMovie(self.movie)
        self.label_animation.setStyleSheet("background: transparent;")
        self.label_animation.setScaledContents(True)
        self.label_animation.setMinimumSize(icon_w, icon_h)
        self.label_animation.setMaximumSize(icon_w, icon_h)
        self.label_animation.move(int(container_w - icon_w - 20), int(container_h / 4))

    def set_position(self, pos_left=0, top=0):
        """

        @param top:
        @_type pos_left: int
        """
        self.alert_container.move(pos_left, top)

    def start_animation(self):
        self.movie.start()
        self.alert_container.setVisible(True)
        self.is_running = True

        if not self.infinity:
            timer = QTimer()
            timer.singleShot(self.duration, self.stop_animation)

    def stop_animation(self):
        self.movie.stop()
        self.is_running = False
        self.hide()

        if self.on_animation_end is not None:
            if not self.is_running:
                return self.on_animation_end()

    def hide(self):
        self.alert_container.setVisible(False)

    def set_style(self, style):
        self.alert_container.setStyleSheet(style)
