import os

from document_models.models import *

def get_data_from_filename(document_model, file):

    file_data = [os.path.splitext(f.strip())[0] for f in file.split("-")]

    for data in file_data:

        if len(data) > 0 and "CF" in data:
            document_model["type"] = "NOTA FISCAL"
            document_model["num"] = data.replace("CF", "").strip()
        
        if len(data) > 0 and "NF" in data or "NF RC" in data:
            document_model["type"] = "NOTA FISCAL"
            document_model["num"] = data.replace("CF", "")\
                                        .replace("NF", "")\
                                        .replace("RC", "")\
                                        .replace("NF RC", "").strip()

        if len(data) > 0 and "CH" in data:
            document_model["check-num"] = data.replace("CH", "").strip()

        if len(data) > 0 and ":" in data:
            document_model["date"] = data.split(":")

        if len(data) > 0 and "R$" in data:
            document_model["value"] = data.replace("R$", "").strip()
        
        if len(data) > 0 and not "R$" in data \
            or not "CF" in data or not ":" in data\
                or not "NF" in data or not "RC" in data\
                    or not "CH" in data:
            document_model["emitter"] = data.strip()

    return document_model


if __name__ == "__main__":
    files = []
    for file in os.listdir("files/1000/3026"):
        files.append(get_data_from_filename(model3026, file))
        
    for f in files:
        print(f)