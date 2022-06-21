from PyQt5.uic import loadUi
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ..mainScreen.main import MainScreen
from ..styles import *



class UserCredentialScreen(QDialog):

    def __init__(self, parent, ui_path) -> None:
        super().__init__()
        self.parent = parent
        loadUi(ui_path, self)

        self.username = self.userInput.text()
        self.password = self.passwordInput
        self.confirm_pass = self.confirmPasswordInput
        
        self.eye = self.passEye1
        self.eye2 = self.passEye2
        
        self.saveCredentialBtn.clicked.connect(self.btn_save_clicked)
        self.eye.clicked.connect(self.pass_eye_clicked)
        self.eye2.clicked.connect(self.pass_eye2_clicked)
    
    def btn_save_clicked(self):
        print(self.username, self.password.text(), self.confirm_pass.text())
        self.load_main_screen()
    
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
        main = MainScreen(self.parent)
        self.parent.addWidget(main)
        self.parent.setCurrentIndex(self.parent.currentIndex() + 1)
