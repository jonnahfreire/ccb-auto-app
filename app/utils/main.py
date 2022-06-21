import os, sys
import subprocess
import datetime
from time import sleep


# from PyPDF2 import PdfFileMerger
from app.config.credentials import Credential

from app.execlogs.logs import *
from app.cli.colors import *

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
        self.finished_all_with_exceptions: bool = False
        self.failed: bool = False
        self.failed_all: bool = False
        self.fail_cause: str = None
        self.errors: dict = {
            "start_insertion_error": None,
            "access_error": None
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
    
    def set_finished_all_with_exceptions(self):
        self.finished_all_with_exceptions = True
    
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
                "finished_all_with_exceptions": self.finished_all_with_exceptions,
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
        

def get_items_models_list(module) -> list:
    return [
        _class.__name__[5:]
        for _class in get_class_list_by_module(module)    
    ][1:]


def get_version_from_file(cmd: str, config_path: str) -> str:
    with open(os.path.join(config_path, "driver-version.txt"), "w") as f:
        subprocess.run(cmd, stdout=f)

    with open(os.path.join(config_path, "driver-version.txt"), "r") as f:
        line_content: str = f.readline()
        if line_content is not None:
            return line_content.split()[1]


def get_stdout(command: str) -> str:
    encoding = "ISO-8859-1"

    command = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
    
    output_byte = command.stdout.read() + command.stderr.read()
    output_str = str(output_byte.decode(encoding))
    return output_str


def get_month_list() -> list:
    today = datetime.datetime.now()
    months = []
    for m in range(12):
        if m < 9: 
            months.append("0"+str(m+1) + f"/{today.year}")
        else: months.append(str(m+1) + f"/{today.year}")
    
    return months


def get_current_month() -> str:
    today = datetime.datetime.now()
    if today.month < 9: 
        return "0"+str(today.month) + f"/{today.year}"

    return str(today.month) + f"/{today.year}"
