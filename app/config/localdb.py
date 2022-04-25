import sqlite3
from sqlite3 import Cursor, Connection

from app.config.globals import db_path


class LocalDB:

    def __init__(self) -> None:
        self.dbname: str = db_path
        self.cursor: Cursor = None
        self.conn: Connection = None
    
    def connect(self) -> None:
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
        self.create_table_user()
    
    def create_table_user(self):
        query = """CREATE TABLE IF NOT EXISTS user (
            username VARCHAR(50) NOT NULL, userpass VARCHAR(200) NOT NULL)
            """
        self.cursor.execute(query)

    def commit(self):
        self.conn.commit()
        self.conn.close()
    