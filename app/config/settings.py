import sqlite3
from sqlite3 import Connection, Cursor
from app.config.paths import settings_path


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
                    driver_path TEXT NULL
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
        try:
            self.cursor.execute(f"INSERT INTO driver_settings (driver_path) VALUES(?)", (driver_path))
            
            return True
        except Exception:
            return False    
    
    def get_chromedriver_path(self) -> str:
        try:
            self.cursor.execute("SELECT driver_path FROM driver_settings")
            chrome_driver_path = self.cursor.fetchone()
            return chrome_driver_path[0]
        except Exception:
            return None
    
    def clear_driver_path(self) -> bool:
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

    if get_chromedriver_path():
        clear_chromedriver_path()

    success = settings.set_chromedriver_path(driver_path)
    settings.commit()
    return success


def get_chromedriver_path() -> str:
    settings = Settings()
    driver_path = settings.get_chromedriver_path()
    settings.commit()
    return driver_path


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


def clear_chromedriver_path() -> str:
    settings = Settings()
    success = settings.clear_driver_path()
    settings.commit()
    return success


def clear_browser_settings() -> str:
    settings = Settings()
    success = settings.clear_browser_settings()
    settings.commit()
    return success
