import os, sys
from time import sleep
import pyautogui

from PyPDF2 import PdfFileMerger

WIN = sys.platform == "win32" 

def merge_pdf(merge_list: list, filename: str):
    merger = PdfFileMerger()

    for pdf in merge_list:
        merger.append(pdf)

    merger.write(filename)
    merger.close()

def clear() -> None:
    os.system("cls") if WIN else os.system("clear")


def enter(times: int = 1, delay: int = 0.5):
    for _ in range(times):
        pyautogui.press("enter")
        sleep(delay)