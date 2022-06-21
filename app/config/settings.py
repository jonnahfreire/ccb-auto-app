import sqlite3
from sqlite3 import Connection, Cursor
from app.config.paths import settings_path, config_path
from app.utils.main import get_version_from_file


class Settings:

    def __init__(self) -> None:
        self.settingsdb: str = settings_path
        self.cursor: Cursor = None
        self.conn: Connection = None

        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.settingsdb)
        self.cursor = self.conn.cursor()
        self.create_table_settings()

    def create_table_settings(self) -> bool:
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS driver_settings (
                    driver_path TEXT NULL,
                    driver_version TEXT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS browser_settings (
                    browser_window_show INTEGER NULL
                )
            """)
        except Exception:
            return False

    def set_browserwindow_show(self, show: int) -> bool:
        try:
            self.cursor.execute(f"INSERT INTO browser_settings (browser_window_show) VALUES({show})")

            return True
        except Exception:
            return False

    def get_browserwindow_show(self) -> bool:
        try:
            self.cursor.execute("SELECT * FROM browser_settings")
            show = self.cursor.fetchone()

            if show is None or show[0] == 0: return False
            return True
        except Exception:
            return False

    def set_chromedriver_path(self, *driver_path: tuple) -> bool:
        driver_version: str = get_version_from_file(driver_path[0] + " --version", config_path)
        try:
            self.cursor.execute(
                f"INSERT INTO driver_settings (driver_path, driver_version) VALUES(?,?)",
                (driver_path[0], driver_version))

            return True
        except Exception:
            return False

    def get_chromedriver_settings(self) -> tuple:
        try:
            self.cursor.execute("SELECT driver_path, driver_version FROM driver_settings")
            chrome_driver_settings = self.cursor.fetchone()
            return chrome_driver_settings
        except Exception:
            return None

    def clear_driver_settings(self) -> bool:
        try:
            self.cursor.execute("DELETE FROM driver_settings")
            return True
        except Exception:
            return False

    def clear_browser_settings(self) -> bool:
        try:
            self.cursor.execute("DELETE FROM browser_settings")
            return True
        except Exception:
            return False

    def commit(self) -> None:
        self.conn.commit()
        self.conn.close()


# -----------------------------------------------------------------
def set_chromedriver_path(driver_path: str) -> bool:
    settings = Settings()

    if get_chromedriver_settings():
        clear_chromedriver_settings()

    success = settings.set_chromedriver_path(driver_path)
    settings.commit()
    return success


def get_chromedriver_path() -> str:
    return get_chromedriver_settings()["path"]


def get_chromedriver_settings() -> dict:
    settings = Settings()
    driver_settings = settings.get_chromedriver_settings()
    settings.commit()

    if driver_settings:
        return {"path": driver_settings[0], "version": driver_settings[1]}
    return {"path": "Caminho não definido", "version": "Versão: Não definido"}


def get_chromedriver_version() -> str:
    return get_chromedriver_settings()["version"]


def set_browserwindow_show(show: bool) -> bool:
    settings = Settings()
    clear_browser_settings()

    if show:
        show = 1
    else:
        show = 0

    success = settings.set_browserwindow_show(show)
    settings.commit()
    return success


def get_browserwindow_show() -> bool:
    settings = Settings()
    show = settings.get_browserwindow_show()
    settings.commit()
    return show


def clear_chromedriver_settings() -> str:
    settings = Settings()
    success = settings.clear_driver_settings()
    settings.commit()
    return success


def clear_browser_settings() -> str:
    settings = Settings()
    success = settings.clear_browser_settings()
    settings.commit()
    return success
