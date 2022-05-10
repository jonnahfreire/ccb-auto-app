import sqlite3
from sqlite3 import Connection, Cursor

from app.config.paths import logpath

class Log:

    def __init__(self) -> None:
        self.logdb: str = logpath
        self.cursor: Cursor = None
        self.conn: Connection = None

        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.logdb)
        self.cursor = self.conn.cursor()
        self.create_table_execlogs()

    def create_table_execlogs(self) -> bool:
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS execlogs (
                        date VARCHAR(10),
                        logmessage VARCHAR(500),
                        time VARCHAR(20)
                )
            """)
        except Exception:
            return False

    def insert_execlog(self, logmessage: str) -> bool:
        try:
            date = None
            time = None
            self.cursor.execute("INSERT INTO execlogs VALUES(?,?,?)", (date, logmessage, time))
            
            return True
        except Exception:
            return False
    
    def get_execlogs(self) -> list:
        try:
            self.cursor.execute("SELECT * FROM execlogs")
            execlogs = self.cursor.fetchall()
            return execlogs
        except Exception:
            return []

    def clear_logs(self) -> bool:
        try:
            self.cursor.execute("DELETE FROM execlogs")
            return True
        except Exception:
            return False
    
    def commit(self) -> None:
        self.conn.commit()
        self.conn.close()


def insert_execlog(logmessage: str) -> bool:
    log = Log()
    success = log.insert_execlog(logmessage)
    log.commit()
    return success

def clear_logs() -> bool:
    log = Log()
    success = log.clear_logs()
    log.commit()
    return success

def get_execlogs() -> list:
    log = Log()
    logs = log.get_execlogs()
    log.commit()
    return logs


if __name__ == "__main__":
    pass