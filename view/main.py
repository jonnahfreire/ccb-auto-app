import sys, os

from PyQt5.uic import loadUi
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .styles import *

WIN = sys.platform == "win32"

def open_dir(dirpath: str) -> None:
    path = os.path.realpath(dirpath)
    if not WIN: os.system(f"xdg-open {path}")
    else: os.startfile(path)


class HSeparator(QWidget):
    def __init__(self, parent, parent_width, parent_height, sep_height=1) -> None:
        super().__init__()
        self.width = parent_width
        self.height = parent_height
        self.sep_height = sep_height

        self.separator = QLabel(parent)
        self.set_position(0, 0)
        self.separator.setMinimumSize(self.width-20, self.sep_height)
        self.separator.setMaximumSize(self.width-20, self.sep_height)
        self.separator.setStyleSheet(u"background-color: rgb(206, 206, 206);")
    
    def set_position(self, left=0, top=0):
        self.separator.move(self.width-left, self.height-top)
    
    def set_size(self, width, height):
        self.separator.setMinimumSize(width, height)
        self.separator.setMaximumSize(width, height)



class AlertModal(QWidget):

    def __init__(self, parent, width=400, height=300, title=None, body=None) -> None:
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
        self.backdrop.setMinimumSize(800, 600)
        self.backdrop.setMaximumSize(800, 600)
        self.backdrop.setVisible(True)

        self.container = QFrame(self.backdrop)
        self.container.setFrameShape(QFrame.StyledPanel)
        self.container.setFrameStyle(QFrame.Raised)
        self.container.setStyleSheet(context_menu_style)
        self.container.setMinimumSize(self.width, self.height)
        self.container.setMaximumSize(self.width, self.height)

        self.modal_title = QLabel(self.title, self.container)
        self.modal_title.move(10, 20)
        self.modal_title.setStyleSheet("font: 11pt 'Segoe UI'; font-weight: 500;")

        self.modal_close = QLabel(self.container)
        self.modal_close.setCursor(Qt.PointingHandCursor)
        self.modal_close.move(self.width-40, 10)
        self.modal_close.setScaledContents(True)
        self.modal_close.setMinimumSize(35, 35)
        self.modal_close.setMaximumSize(35, 35)
        self.modal_close.setMargin(10)
        self.modal_close.setPixmap(QPixmap("view/assets/close.png"))
        self.modal_close.setStyleSheet(modal_btn_close_style)

        self.modal_body = QLabel(self.body, self.container)
        self.modal_body.move(10, 60)
        self.modal_body.setStyleSheet("font: 11pt 'Segoe UI'; font-weight: 400;")
        self.modal_body.setWordWrap(True)

        # modal line separator
        separator = HSeparator(self.container, self.width, self.height)
        separator.set_position(292, 150)

        separator = HSeparator(self.container, self.width, self.height)
        separator.set_position(292, 50)

        self.modal_btn_ok = QLabel("OK", self.container)
        self.modal_btn_ok.setCursor(Qt.PointingHandCursor)
        self.modal_btn_ok.setStyleSheet(modal_btn_ok_style)
        self.modal_btn_ok.move(self.width - 150, self.height-40)

        self.modal_btn_cancel = QLabel("Cancelar", self.container)
        self.modal_btn_cancel.setCursor(Qt.PointingHandCursor)
        self.modal_btn_cancel.move(self.width - 90, self.height-40)
        self.modal_btn_cancel.setStyleSheet(modal_btn_cancel_style)
        
        self.modal_btn_cancel.mousePressEvent = self.handle_btn_cancel
        self.modal_close.mousePressEvent = self.handle_btn_close

        self.set_position(250, 120)
    
    def set_body_text(self, text):
        self.modal_body.setText(text)

    def on_ok_press(self, callback):
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

    def set_position(self, left, top):
        self.container.move(left, top)
    
    def show(self):
        self.backdrop.setVisible(True)
    
    def hide(self):
        self.backdrop.setVisible(False)


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
        self.alert_container.setStyleSheet(context_menu_style if self.style is None else self.style)
        self.set_position(int(p_w/2)-int(container_w/2), int(p_h/2)-80-int(container_h/2))

        self.movie = QMovie("view/assets/loading-line.gif")
        
        self.message_text = QLabel(self.message, self.alert_container)
        self.message_text.move(20, int(container_h/3))
        self.message_text.setStyleSheet(alert_loading_text_style)

        self.label_animation = QLabel(self.alert_container)
        self.label_animation.setMovie(self.movie)
        self.label_animation.setStyleSheet("background: transparent;")
        self.label_animation.setScaledContents(True)
        self.label_animation.setMinimumSize(icon_w, icon_h)
        self.label_animation.setMaximumSize(icon_w, icon_h)
        self.label_animation.move(int(container_w-icon_w-20), int(container_h/4))
                
    def set_position(self, left=0, top=0):
        self.alert_container.move(left, top)

    def start_animation(self):
        self.alert_container.setVisible(True)
        self.is_running = True
        self.movie.start()

        if not self.infinity:
            timer = QTimer()
            timer.singleShot(self.duration, self.stop_animation)
    
    def stop_animation(self):
        self.movie.stop()
        self.is_running = False

        if self.on_animation_end is not None:
            if not self.is_running:
                return self.on_animation_end()
    
    def hide(self):
        self.alert_container.setVisible(False)
    
    def set_style(self, style):
        self.alert_container.setStyleSheet(style)


class ContextMenu(QWidget):

    def __init__(self, parent, width = 100, height = 80):
        super().__init__()
        self.parent = parent

        self.is_shown = False
        self.items = []
        self.current_item = None
        self.width = width
        self.height = height

        self.context_menu_container = QFrame(self.parent)
        self.context_menu_container.setFrameShape(QFrame.StyledPanel)
        self.context_menu_container.setFrameStyle(QFrame.Raised)

        self.context_menu_container.setStyleSheet(context_menu_style)
        self.context_menu_container.setMinimumSize(self.width, self.height)
        self.context_menu_container.setMaximumSize(self.width, self.height)
        self.context_menu_container.setVisible(False)

        self.context_menu_layout = QVBoxLayout(self.context_menu_container)
        self.set_position(150, 100)

    def set_position(self, left, top):
        self.context_menu_container.move(left, top)

    def set_clicked_item(self, item):
        self.current_item = item

    def add_item(self, item_title, callback=None):
        item = QLabel(item_title)
        item.setStyleSheet(context_item_style)
        item.setAlignment(Qt.AlignHCenter)
        item.setCursor(Qt.PointingHandCursor)
        item.mousePressEvent = callback
        self.context_menu_layout.addWidget(item)
        self.items.append(item)
    
    def add_separator(self):
        separator = QLabel()
        separator.setMinimumSize(self.width-20, 1)
        separator.setMaximumSize(self.width-20, 1)
        separator.setStyleSheet(u"background-color: rgb(206, 206, 206);")
        self.context_menu_layout.addWidget(separator)

    def show(self):
        self.is_shown = True
        self.context_menu_container.show()
    
    def hide(self):
        self.is_shown = False
        self.context_menu_container.hide()


class UserCredentialScreen(QDialog):

    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        loadUi("view/ui/user-screen.ui", self)

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


class MainScreen(QDialog):

    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent

        loadUi("view/ui/main-screen.ui", self)

        self.mousePressEvent = self.handle_mouse_press
        self.status_container = self.leftStatusFrame

        self.folder = self.folder
        self.folder.mousePressEvent = self.folder_clicked
        self.folder.setStyleSheet(folder_style)

        self.folder_context = ContextMenu(self)
        self.folder_context.add_item("Abrir Local", self.handle_open_folder_location)
        self.folder_context.add_separator()
        self.folder_context.add_item("Remover", self.handle_remove_folder)

        self.perfil_context = ContextMenu(self, 120)
        self.perfil_context.set_position(650, 50)
        self.perfil_context.add_item("Resetar Usuário")
        self.perfil_context.add_separator()
        self.perfil_context.add_item("Configurações")

        self.add_extract_option = ContextMenu(self, 120, 40)
        self.add_extract_option.add_item("Adicionar Extrato", self.handle_add_extract)
        self.add_extract_option.set_position(520, 460)
        
        self.start_insertion_option = ContextMenu(self, 120, 120)
        self.start_insertion_option.add_item("Caixa 1000")
        self.start_insertion_option.add_separator()
        self.start_insertion_option.add_item("Banco 1010")
        self.start_insertion_option.add_separator()
        self.start_insertion_option.add_item("Extrato")
        self.start_insertion_option.set_position(650, 380)

        self.status_started = self.statusStarted
        self.status_not_started = self.statusNotStarted
        self.status_finished = self.statusFinished
        self.status_finished_exception = self.statusFinishedException

        self.createDirBtn.clicked.connect(self.create_dir_clicked)
        self.createDirBtn.setStyleSheet(btn_primary)

        self.addItemsBtn.clicked.connect(self.add_items_clicked)
        self.addItemsBtn.mousePressEvent = self.add_items_clicked
        self.addItemsBtn.setStyleSheet(btn_primary)

        self.startInsertionBtn.clicked.connect(self.start_insertion_clicked)
        self.startInsertionBtn.mousePressEvent = self.start_insertion_clicked
        self.startInsertionBtn.setStyleSheet(btn_success)

        self.userName.mousePressEvent = self.handle_perfil_clicked
        self.userIcon.mousePressEvent = self.handle_perfil_clicked

        self.handle_status(-1)
        self.modal = AlertModal(
            self, 300, 200, "Remover usuário?",
            "Esta ação irá remover o usuário atual.\
            Tem certeza que deseja continuar?")
        self.modal.set_position(250, 120)
        self.modal.hide()

        p = lambda: print("Response modal: True")
        self.modal.on_ok_press(p)
    
    def handle_perfil_clicked(self, event):
        if event.buttons() == Qt.LeftButton:
            self.perfil_context.show()

    def handle_mouse_press(self, event):
        self.add_extract_option.hide()
        self.start_insertion_option.hide()
        self.folder_context.hide()
        self.perfil_context.hide()
    
    def folder_clicked(self, event):
        if event.buttons() == Qt.RightButton:
            self.folder_context.show()
            
        self.folder.setStyleSheet(folder_style_active)
        self.folderIcon.setPixmap(QPixmap(u"view/assets/folderOpen.png"))
        print(self.folderMonthTitle.text())            

    def create_dir_clicked(self):
        pass
    
    def handle_remove_folder(self, event):
        pass

    def handle_open_folder_location(self, event):
        path = r"C:\Users\adm\Downloads"
        return open_dir(path)

    def handle_add_extract(self, event):
        if event.buttons() == Qt.LeftButton:
            filename = QFileDialog.getOpenFileName(self, 'Selecione o Extrato', 'c:\\',"Pdf files (*.pdf)")[0]
            print(filename)
            return self.add_extract_option.hide()

    def add_items_clicked(self, event):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        
        if event.buttons() == Qt.RightButton:
            return self.add_extract_option.show()

        if dlg.exec_():
            folder_path = dlg.selectedFiles()
            print(folder_path)

    def start_insertion_clicked(self, event):
        if event.buttons() == Qt.RightButton:
            self.start_insertion_option.show()
    
    def handle_status(self, status):
        if status == -1:
            self.status_container.hide()

        if status == 0:
            self.status_started.hide()
            self.status_finished.hide()
            self.status_finished_exception.hide()
        if status == 1:
            self.status_not_started.hide()
            self.status_finished.hide()
            self.status_finished_exception.hide()
        if status == 2:
            self.status_started.hide()
            self.status_not_started.hide()
            self.status_finished_exception.hide()
        if status == 3:
            self.status_started.hide()
            self.status_not_started.hide()
            self.status_finished.hide()

        
class Window(QStackedWidget):

    def __init__(self) -> None:
        super().__init__()
        self.top = 100
        self.left = 300
        self.width = 800
        self.height = 600
        self.title = "CCB AUTO"
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        self.alert_loading = AlertLoading(
            self, p_w=800, p_h=600, infinity=False, duration=4000,
            container_w=240, message="Iniciando, aguarde..", 
            on_animation_end=self.load_default_screen)
        
        self.alert_loading.set_style("""
            QFrame {background-color: rgba(221, 221, 221, 0.801);border-radius: 5px;}""")
        
        self.alert_loading.start_animation()

    def load_default_screen(self):
        is_user_setted = False
        if not is_user_setted:
            self.user_credential_screen = UserCredentialScreen(self)
            self.addWidget(self.user_credential_screen)
        else:
            self.main_screen = MainScreen(self)
            self.addWidget(self.main_screen)   

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