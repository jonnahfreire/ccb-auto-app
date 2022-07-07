import sys
from PyQt5.QtWidgets import QApplication

from app.main import create_work_directory
from app.utils.filemanager import create_config_path
from app.utils.main import get_current_month
from view.main import Window


def init_conf() -> bool:
    if create_config_path():
        month: str = get_current_month().replace("/", "-")
        return create_work_directory(month)
    return False


if __name__ == "__main__":
    init_conf()

    app = QApplication(sys.argv)
    window = Window()
    window.load_window()

    sys.exit(app.exec_())
