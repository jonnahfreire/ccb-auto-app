from config.localdb import LocalDB



class Credential:

    def __init__(self) -> None:
        self.username: str = None
        self.userpass: str = None
        self.db: LocalDB = LocalDB()

    def get_user_credentials(self) -> list:    
        self.db.connect()

        self.db.cursor.execute("SELECT username, userpass FROM user")
        user_data = self.db.cursor.fetchone()
        
        self.db.commit()
        return user_data or []
    
    def reset_all(self):
        self.db.connect()

        self.db.cursor.execute("DELETE * FROM user")
        self.db.commit()

    def set_user_credential(self, username: str, userpass: str):
        self.username = username
        self.userpass = userpass

        self.db.connect()

        user = self.get_user_credentials()
        if self.username and self.userpass\
            and not user or not username in user and not userpass in user:
            if self.db.cursor.execute("INSERT INTO user (username, userpass) VALUES (?,?) ",(self.username, self.userpass)): 
                print('Usuário inserido com sucesso!')
            else:
                print('Não foi possível inserir usuário!')
        else:
            self.db.cursor.execute("UPDATE user SET username=?, userpass=?", (self.username, self.userpass))
        self.db.commit()