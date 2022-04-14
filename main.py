import os
import eel

from utils.filemanager import list_files, get_files_by_account, create_config_path
from data.main import get_modelized_debts
from config.globals import sist_path, screen_size

from config.credentials import Credential
from config.user import User


@eel.expose
def is_user_set() -> bool:
    create_config_path()
    user_credential = Credential()
    user_data = user_credential.get_user_credentials()

    if len(user_data) == 0:
        return False
    return True


@eel.expose
def get_username() -> str:
    user_credential = Credential()
    user_data = user_credential.get_user_credentials()

    if len(user_data) > 0:
        return user_data[0]
    
    return ""


@eel.expose
def set_user_credential(username: str, passwd: str) -> bool:
    user = User(username, passwd)
    user_credential = Credential()

    if user_credential.set_user_credential(user.get_user(), user.get_pass()):
        return True
    
    return False


@eel.expose
def get_screen_size():
    return screen_size


@eel.expose
def get_data(work_month):

    if work_month is None: pass
    work_month_path: str = os.path.join(sist_path, work_month.replace("/", "-"))

    files: list = list_files(work_month_path)

    if len(files) > 0:
        debts_1000, debts_1010 = get_files_by_account(files)

        modelized_debts_1000: list[dict] = get_modelized_debts(debts_1000)
        modelized_debts_1010: list[dict] = get_modelized_debts(debts_1010)

        # all_debts: list[dict] = modelized_debts_1000 + modelized_debts_1010

        return {"1000": modelized_debts_1000, "1010": modelized_debts_1010}

    return {"data": []}


@eel.expose
def main(work_month: str) -> None:
    pass


if __name__ == "__main__":
    eel.init("UI/src")
    eel.start("index.html", port=8090, size=(int(screen_size[0]), int(screen_size[1])), position=(230, 50))

    