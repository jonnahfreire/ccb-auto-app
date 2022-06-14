import sys
from PyQt5.QtWidgets import QApplication

from view.main import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.load_window()

    sys.exit(app.exec_())