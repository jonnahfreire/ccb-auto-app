import sqlite3
from sqlite3 import Connection, Cursor

from config.globals import notification_path

class Notification:

    def __init__(self) -> None:
        self.notificationsdb: str = notification_path
        self.cursor: Cursor = None
        self.conn: Connection = None

        self.header_success: str        = "Lançamento salvo com sucesso."
        self.header_error: str          = "Não foi possível salvar lançamento."
        self.document_exists_msg: str   = "Documento com o mesmo número já existe."
        self.document_sent_success: str = "Documento enviado."

        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.notificationsdb)
        self.cursor = self.conn.cursor()
        self.create_table_notifications()

    def create_table_notifications(self) -> bool:
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                        date VARCHAR(10) NULL,
                        icon VARCHAR(30) NOT NULL,
                        header VARCHAR(200) NOT NULL,
                        title VARCHAR(100) NOT NULl,
                        message VARCHAR(500) NOT NULL,
                        time VARCHAR(20) NULL
                )
            """)
        except Exception:
            return False

    def insert_notification(self, notification: dict) -> bool:
        try:
            date = None
            time = None
            icon = notification["icon"]
            header = notification["header"]
            title = notification["title"]
            message = notification["message"]
            self.cursor.execute("INSERT INTO notifications VALUES(?,?,?,?,?,?)",
                (date, icon, header, title, message, time))
            
            return True
        except Exception:
            return False
    
    def get_notifications(self) -> list:
        try:
            self.cursor.execute("SELECT oid, * FROM notifications")
            notifications = self.cursor.fetchall()
            return notifications
        except Exception:
            return []
    
    def delete_notification(self, id: int) -> bool:
        try:
            self.cursor.execute(f"SELECT oid FROM notifications WHERE oid = '{id}'")
            _id = self.cursor.fetchone()

            if _id:
                if self.cursor.execute(f"DELETE FROM notifications WHERE oid = '{_id[0]}'"):
                    return True

            return False

        except Exception:
            return False

    def clear_notifications(self) -> bool:
        try:
            self.cursor.execute("DELETE FROM notifications")
            return True
        except Exception:
            return False
    
    def commit(self) -> None:
        self.conn.commit()
        self.conn.close()



# -----------------------------------------------------------------
def insert_notification(notification_item: dict) -> bool:
    notification = Notification()
    success = notification.insert_notification(notification_item)
    notification.commit()
    return success


def clear_notifications() -> bool:
    notification = Notification()
    success = notification.clear_notifications()
    notification.commit()
    return success


def delete_notification(id: int) -> bool:
    notification = Notification()
    success = notification.delete_notification(id)
    notification.commit()
    return success


def get_notifications() -> list:
    notification_obj = Notification()
    notification_list: list[dict] = []

    for notification in notification_obj\
        .get_notifications():
        notification_list.append({
            "id": notification[0],
            "icon": notification[2],
            "header": notification[3],
            "title": notification[4],
            "message": notification[5],
        })

    notification_obj.commit()
    return notification_list
