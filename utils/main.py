import os, sys
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