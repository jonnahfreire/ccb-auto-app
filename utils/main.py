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


class InsertionStatus:

    def __init__(self) -> None:
        self.current: dict = {}
        self.starting: bool = False
        self.started: bool = False
        self.finished: bool = False
        self.finished_all: bool = False
        self.failed: bool = False
        self.failed_all: bool = False
        self.fail_cause: str = None
        self.errors: dict = {
            "start_insertion_error": "",
            "access_error": ""
        }
    
    def set_current(self, current: dict):
        self.current = current
    
    def set_starting(self):
        self.starting = True

    def set_started(self):
        self.started = True

    def set_finished(self, finished: bool):
        self.finished = finished
        
    def set_finished_all(self):
        self.finished_all = True
    
    def set_failed(self, failed: bool):
        self.failed = failed

    def set_failed_all(self):
        self.failed_all = True
    
    def set_fail_cause(self, cause: str):
        self.fail_cause = cause
    
    def set_insertion_error(self, error_msg):
        self.errors["start_insertion_error"] = error_msg
    
    def set_access_error(self, error_msg):
        self.errors["access_error"] = error_msg
    
    def get_status(self):
        return {
            "status": {
                "current": self.current,
                "starting": self.starting,
                "started": self.started,
                "finished": self.finished,
                "finished_all": self.finished_all,
                "failed": self.failed,
                "failed_all": self.failed_all,
                "fail_cause": self.fail_cause,
            },
            "errors": self.errors
        }



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
        

def get_items_models_list(module) -> list[dict]:
    return [
        _class.__name__[5:]
        for _class in get_class_list_by_module(module)    
    ][1:]


