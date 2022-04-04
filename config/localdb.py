from os import path, getcwd
import sqlite3
from sqlite3 import Cursor, Connection



class LocalDB:

    def __init__(self) -> None:
        self.dbname: str = path.join(getcwd(), "config/user.db")
        self.cursor: Cursor = None
        self.conn: Connection = None
    
    def connect(self) -> None:
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS user (
            username VARCHAR(50) NOT NULL, userpass VARCHAR(200) NOT NULL)
            """
        self.cursor.execute(query)

    def commit(self):
        self.conn.commit()
        self.conn.close()
    