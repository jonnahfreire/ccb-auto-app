from sys import exit
import getpass

from time import sleep

from utils.main import clear
from utils.filemanager import create_config_path

from config.credentials import Credential
from config.user import User

from cli.colors import *


def banner():
    clear()
    print(f"{green}#########################################################")
    print(f"{yellow}   #####  #####  ####*    ###### ##  ## ######## ######")
    print("   ##     ##     ##   #   ##  ## ##  ## ######## ##  ##")
    print("   ##     ##     #####    ###### ##  ##    ##    ##  ##")
    print("   ##     ##     ##   #   ##  ## ##  ##    ##    ##  ##")
    print("   #####  #####  ####*  # ##  ## ######    ##    ######")
    print(f"{green}#########################################################{bg}")


def set_work_month() -> str:
    clear()
    banner()
    try:
        work_month = input(f"{cyan}Selecione o mês de trabalho Ex: 01/2022: {bg}").strip()

        if len(work_month) == 7 \
            and "/" in work_month \
            or "-" in work_month \
            and work_month.replace("/", "").isdigit() \
            or work_month.replace("-", "").isdigit():
            
            if work_month is None: set_work_month()
            return work_month

        print(f"{red}Houve um erro. {yellow}Digite novamente o mês de trabalho.{bg}")
        print(f"{cyan}Ex: 01/2022{bg}")
        sleep(5)
        set_work_month()
    except KeyboardInterrupt:
        exit(0)

def set_initial_user_config() -> None:
    try:
        banner()
        create_config_path()
        user_credential = Credential()
        user_data = user_credential.get_user_credentials()

        if len(user_data) == 0:
            new_user = input(f"{cyan}Informe seu usuário do siga: ").strip()
            new_pass = getpass.getpass(f"{cyan}Infrome sua senha do siga: {bg}").strip()
            user = User(new_user, new_pass)
            user_credential.set_user_credential(user.get_user(), user.get_pass())
    
    except KeyboardInterrupt:
        exit(0)


def select_initial_routine(debts_1000: list[dict], debts_1010: list[dict]) -> str:
    try:
        clear()
        banner()
        msg = "{}\tEncontrados {} despesas para lançar.\n{}"
        print(f"\n{cyan}*** Selecione os lançamentos que deseja efetuar ***\n")
        print("1000 - Caixa 1000")
        print(msg.format(yellow, len(debts_1000), cyan))
        print("1010 - Banco")
        print(msg.format(yellow, len(debts_1010), cyan))
        print("1 - Todos\n")
        print("***************************************")

        option = input(f"{cyan}Digite o código dos lançamentos: {bg}")
        return option
    except KeyboardInterrupt:
        exit(0)