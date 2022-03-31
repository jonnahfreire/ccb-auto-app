from PyPDF2 import PdfFileMerger



def merge_pdf(merge_list: list, filename: str):
    merger = PdfFileMerger()

    for pdf in merge_list:
        merger.append(pdf)

    merger.write(filename)
    merger.close()