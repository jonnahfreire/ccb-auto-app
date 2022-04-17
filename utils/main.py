import os, sys
from time import sleep
import pyautogui

# from PyPDF2 import PdfFileMerger
from config.credentials import Credential

from execlogs.logs import *
from cli.colors import *

WIN = sys.platform == "win32" 


# def merge_pdf(merge_list: list, filename: str):
#     merger = PdfFileMerger()

#     for pdf in merge_list:
#         merger.append(pdf)

#     merger.write(filename)
#     merger.close()


def reset_db() -> bool:
    return Credential().reset_all()


def clear() -> None:
    os.system("cls") if WIN else os.system("clear")


def enter(times: int = 1, delay: int = 0.5):
    for _ in range(times):
        pyautogui.press("enter")
        sleep(delay)


def get_class_list_by_module(module):
    md = module.__dict__
    return [
        md[c] for c in md if (
            isinstance(md[c], type) 
            and md[c].__module__ == module.__name__
        )
    ]


def model_name_exists(module, model_name: str) -> bool:
    models_name = [
        model.__name__ 
        for model in get_class_list_by_module(module)
    ]
    if model_name not in models_name:
        insert_execlog(f"{red}Model: {yellow}'{model_name}' Não encontrado{bg}")

    return model_name in models_name
        

def get_debt_models_list(module) -> list[dict]:
    return [
        _class.__name__[5:]
        for _class in get_class_list_by_module(module)    
    ][1:]
