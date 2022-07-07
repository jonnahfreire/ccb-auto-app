import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QStackedWidget, QApplication

from view.ui.mainScreen.main import MainScreen
from view.ui.settings.main import SettingsScreen
from view.ui.userScreen.main import UserCredentialScreen
from view.ui.alertLoading.main import AlertLoading

from app.main import is_user_set


class Window(QStackedWidget):

    def __init__(self) -> None:
        super().__init__()
        self.settings_view = None
        self.main_view = None
        self.user_credential_view = None
        self.top = 100
        self.left = 300
        self.width = 800
        self.height = 600
        self.title = "CCB AUTO"
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

        self.alert_loading = AlertLoading(
            self, p_w=self.width, p_h=self.height, infinity=False, duration=2000,
            container_w=280, message="Iniciando, aguarde..",
            on_animation_end=self.load_views)
        self.alert_loading.start_animation()

    def load_views(self):
        self.user_credential_view = UserCredentialScreen(self, "view/ui/userScreen/user-screen.ui")
        self.addWidget(self.user_credential_view)
        self.main_view = MainScreen(self, "view/ui/mainScreen/main-screen.ui")
        self.addWidget(self.main_view)
        self.settings_view = SettingsScreen(self, "view/ui/settings/settings.ui")
        self.addWidget(self.settings_view)

        if not is_user_set():
            self.setCurrentIndex(self.currentIndex()-1)
        else:
            self.setCurrentIndex(self.currentIndex()+1)

    def load_window(self) -> None:
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon("view/assets/favicon.png"))
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.load_window()

    sys.exit(app.exec_())
