import os


def get_data_from_filename(model, file: str) -> dict:
    model.file_name = file.split("-")[0].strip()
    file_data = [os.path.splitext(f.strip())[0] for f in file.split("-")]

    for data in file_data:

        if len(data) > 0 and "CF" in data:
            model.type = "NOTA FISCAL"
            model.num = data.replace("CF", "").strip()
        
        if len(data) > 0 and "NF" in data or "NF RC" in data:
            model.type = "NOTA FISCAL"
            model.num = data.replace("CF", "")\
                                        .replace("NF", "")\
                                        .replace("RC", "")\
                                        .replace("NF RC", "").strip()

        if len(data) > 0 and "CH" in data:
            model.check_num = data.replace("CH", "").strip()
            model.hist2 = "011"
        
        if len(data) > 0 and "DB AT" in data:
            model.hist2 = "DÉBITO AUTOMÁTICO"

        if len(data) > 0 and ":" in data:
            model.date = data.split(":")

        if len(data) > 0 and "R$" in data:
            model.value = data.replace("R$", "").strip()
        
        if len(data) > 0 and not "R$" in data \
            or not "CF" in data or not ":" in data\
                or not "NF" in data or not "RC" in data\
                    or not "CH" in data:
            model.emitter = data.strip()

    return model.get_mapped_data()


def get_files_from(path):
    return os.listdir(path)

def get_data_by_model(model: dict, file: list) -> list:
    return [get_data_from_filename(model, f) for f in file]
        

if __name__ == "__main__":
    pass