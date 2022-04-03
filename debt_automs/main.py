import os


def get_data_from_filename(model, file: str) -> dict:
    model.file_name = file.split("-")[0].strip()
    file_data = [os.path.splitext(f.strip())[0] for f in file.split("-")]

    for data in file_data:

        if len(data) > 0 and "NF" in data or "NF RC" in data \
            or "CF" in data or "CF RC" in data or "CP" in data\
            or "CP RC" in data:
            model.type = "NOTA FISCAL"
            model.hist1 = "021"
            model.hist2 = "023"
            model.num = data.replace("CF", "")\
                            .replace("CF RC", "")\
                            .replace("NF", "")\
                            .replace("NF RC", "")\
                            .replace("RC", "")\
                            .replace("CP", "")\
                            .replace("CP RC", "").strip()

        elif len(data) > 0 and "05_" in data:
            model.cost_center = data.replace("_", "-").strip()

        elif len(data) > 0 and "CH" in data:
            model.check_num = data.replace("CH", "").strip()
            model.payment_form = "CHEQUE"
            model.hist2 = "011" # CH Nº
            model.cost_account = "1010"

        elif len(data) > 0 and "DB AT" in data:
            model.type = "NOTA FISCAL"
            model.num = data.replace("DB AT", "")\
                            .replace("LUZ", "")\
                            .replace("FONE", "").strip()
            model.hist1 = "021"
            model.hist2 = "007" #"AVISO DE DÉBITO"
            model.cost_account = "1010"
            model.payment_form = "DEBITO AUTOMATICO"
            if "LUZ" in data:
                model.doc_num = "200118"
            if "FONE" in data:
                model.doc_num = "300200"


        elif len(data) > 0 and ":" in data:
            model.date = data.split(":")

        elif len(data) > 0 and "R$" in data:
            model.value = data.replace("R$", "").strip()
        
        else:
            model.emitter = data.strip()

    return model.get_mapped_data()


def get_files_from(path):
    return os.listdir(path)

def get_data_by_model(model: dict, file: list) -> list:
    return [get_data_from_filename(model, f) for f in file]
        

if __name__ == "__main__":
    pass