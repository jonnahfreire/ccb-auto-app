from PyQt5.QtCore import QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from app.main import set_user_credential
from ..alertLoading.main import AlertLoading
from ..mainScreen.main import MainScreen
from ..styles import set_element_shadow


class UserCredentialScreen(QMainWindow):

    def __init__(self, parent, ui_path) -> None:
        super().__init__()
        self.parent = parent
        loadUi(ui_path, self)

        set_element_shadow(self.formContainer, offset=2)

        self.username = self.userInput
        self.password = self.passwordInput
        self.confirm_pass = self.confirmPasswordInput

        self.username.mousePressEvent = self.clear_messages
        self.password.mousePressEvent = self.clear_messages
        self.confirm_pass.mousePressEvent = self.clear_messages

        self.top_error_message_container = self.TopErrorMessageContainer
        set_element_shadow(self.top_error_message_container)
        self.top_error_message_container.hide()

        self.top_success_message_container = self.TopSuccessMessageContainer
        set_element_shadow(self.top_success_message_container)
        self.top_success_message_container.hide()

        self.error_message_container = self.CredentialErrorMessageContainer
        self.error_message_container.hide()

        set_element_shadow(self.error_message_container)
        self.error_message = self.credentialErrorMessage

        self.eye = self.passEye1
        self.eye.setIcon(QIcon("view/assets/hidden.png"))
        self.eye2 = self.passEye2
        self.eye2.setIcon(QIcon("view/assets/hidden.png"))

        self.saveCredentialBtn.clicked.connect(self.btn_save_clicked)
        set_element_shadow(self.saveCredentialBtn, offset=2)
        self.eye.clicked.connect(self.pass_eye_clicked)
        self.eye2.clicked.connect(self.pass_eye2_clicked)

        self.load_screen = AlertLoading(
            self,
            p_w=self.parent.width,
            p_h=self.parent.height,
            infinity=False,
            duration=2000,
            container_w=380,
            message="Lendo diretórios de trabalho, aguarde..",
            on_animation_end=self.show_main_screen)

    def clear_messages(self, ev):
        self.error_message_container.hide()
        self.error_message.setText("")

    def btn_save_clicked(self):
        self.error_message_container.hide()

        if not self.username.text() or not self.password.text() or not self.confirm_pass.text():
            self.error_message.setText("Por favor, informe todos os campos!")
            self.error_message_container.show()

        elif self.password.text() != self.confirm_pass.text():
            self.error_message.setText("Senhas não conferem!")
            self.error_message_container.show()

        elif set_user_credential(self.username.text(), self.password.text()):
            self.topSuccessMessage.setText("Usuário salvo com sucesso!")
            self.top_success_message_container.show()

            timer = QTimer()
            timer.singleShot(1500, lambda: self.userScreenContainer.hide())
            timer.singleShot(1500, self.load_main_screen)

        else:
            self.topErrorMessage.setText("Desculpe, não foi possível salvar usuário! Tente novamente.")
            self.top_error_message_container.show()

    def pass_eye_clicked(self):
        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.eye.setIcon(QIcon("view/assets/eye.png"))
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.eye.setIcon(QIcon("view/assets/hidden.png"))

    def pass_eye2_clicked(self):
        if self.confirm_pass.echoMode() == QLineEdit.Password:
            self.confirm_pass.setEchoMode(QLineEdit.Normal)
            self.eye2.setIcon(QIcon("view/assets/eye.png"))
        else:
            self.confirm_pass.setEchoMode(QLineEdit.Password)
            self.eye2.setIcon(QIcon("view/assets/hidden.png"))

    def load_main_screen(self):
        main = MainScreen(self.parent, "view/ui/mainScreen/main-screen.ui")
        self.parent.addWidget(main)

        self.load_screen.start_animation()

    def show_main_screen(self):
        self.parent.setCurrentIndex(self.parent.currentIndex() + 1)
