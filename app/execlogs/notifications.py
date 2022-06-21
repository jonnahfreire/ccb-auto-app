import sqlite3
from sqlite3 import Connection, Cursor

from app.config.paths import notification_path

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


def insert_based_template_notification(template: dict, item: dict) -> None:
    if item["insert-_type"] == "MOVINT":
        template["title"] = f'{item["file-name"]} - R$ {item["value"]}'
        insert_notification(template)

    if item["insert-_type"] == "DEBT":
        template["title"] = f'{item["file-name"]} - R$ {item["value"]} - DP {item["expenditure"]}'
        insert_notification(template)


def login_error_notification() -> None:
    insert_notification({
        "icon": "danger",
        "header": "Não foi possível logar no sistema.",
        "title": "ccb-auto: não conseguiu autenticar usuário.",
        "message": "Verifique seu acesso, ou redefina os dados de acesso."
    })



def access_error_notification() -> None:
    insert_notification({
        "icon": "danger",
        "header": "Não foi possível acessar o sistema.",
        "title": "ccb-auto: não conseguiu acessar o siga.",
        "message": "Não foi possível carregar página."
    })


def document_pattern_not_match(item: dict) -> None:
    template: dict = {
        "icon": "danger",
        "header": "Não foi possível adicionar documento.",
        "title": None,
        "message": "O padrão de nomeação não foi reconhecido"
    }

    insert_based_template_notification(template, item)


def document_already_inserted(item: dict) -> None:
    template: dict = {
        "icon": "danger",
        "header": "Não foi possível adicionar documento.",
        "title": None,
        "message": "Documento já consta nos lançamentos realizados."
    }

    insert_based_template_notification(template, item)


def document_already_exists_notification(item: dict) -> None:
    template: dict = {
        "icon": "danger",
        "header": Notification().header_error,
        "title": None,
        "message": Notification().document_exists_msg
    }

    insert_based_template_notification(template, item)


def insertion_success_notification(item: dict) -> None:
    template: dict = {
        "icon": "success",
        "header": Notification().header_success,
        "title": None,
        "message": Notification().document_sent_success
    }

    insert_based_template_notification(template, item)


def name_pattern_error_notification(item: dict) -> None:
    template: dict = {
        "icon": "danger",
        "header": "Não foi possível iniciar lançamento.",
        "title": None,
        "message": "O padrão de nomeação não foi reconhecido."
    }

    insert_based_template_notification(template, item)


def filepath_error_notification(item: dict) -> None:
    template: dict = {
        "icon": "danger",
        "header": Notification().header_error,
        "title": None,
        "message": "Caminho do arquivo não foi encontrado!"
    }

    insert_based_template_notification(template, item)


def insertion_error_notification(item: dict) -> None:
    template: dict = {
        "icon": "danger",
        "header": Notification().header_error,
        "title": None,
        "message": "Erro ao inserir dados. Contate o desenvolvedor!"
    }

    insert_based_template_notification(template, item)


def start_insertion_error_notification() -> None:
    insert_notification({
        "icon": "danger",
        "header": "Não foi possível iniciar lançamento.",
        "title": "ccb-auto: não foi possível abrir rotina de despesas.",
        "message": "Erro de rotina. Contate o desenvolvedor!"
    })

