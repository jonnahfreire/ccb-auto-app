from time import sleep
from config.localdb import LocalDB



class Credential:

    def __init__(self) -> None:
        self.username: str = None
        self.userpass: str = None

    def get_user_credentials(self) -> list:    
        db = LocalDB()
        db.connect()

        db.cursor.execute("SELECT username, userpass FROM user")
        user_data = db.cursor.fetchone()
        
        db.commit()
        return user_data or []
    
    def reset_all(self):
        db = LocalDB()
        db.connect()

        db.cursor.execute("DELETE FROM user")
        db.commit()

    def set_user_credential(self, username: str, userpass: str):
        self.username = username
        self.userpass = userpass

        db = LocalDB()
        db.connect()

        user = self.get_user_credentials()
        if self.username and self.userpass\
            and not user or not username in user and not userpass in user:
            if db.cursor.execute("INSERT INTO user (username, userpass) VALUES (?,?) ",(self.username, self.userpass)): 
                print('Usuário inserido com sucesso!')
                sleep(4)
            else:
                print('Não foi possível inserir usuário!')
                sleep(4)
        else:
            db.cursor.execute("UPDATE user SET username=?, userpass=?", (self.username, self.userpass))
        db.commit()

