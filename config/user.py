
class User:

    def __init__(self, username: str, userpass: str) -> None:
        self.username: str = username
        self.userpass: str = userpass
    
    def get_user(self):
        return self.username

    def get_pass(self):
        return self.userpass
