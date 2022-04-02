import os

sist_name = "ccb-autom"

unix_user_path = os.path.join("/home", os.environ["USER"], "Documentos" or "Documents")
unix_sist_path = os.path.join(unix_user_path, sist_name)

struct_dirs_1000 = ["1000", "3026", "3008", "3014"]
struct_dirs_1010 = ["1010", "3008", "3014"]

struct_dirs = [struct_dirs_1000, struct_dirs_1010]


def get_files_path(work_path: str) -> list:
    files_path = []

    for dir in struct_dirs:
        for sub_dir in os.listdir(os.path.join(work_path, dir[0])):
            for file_name in os.listdir(os.path.join(work_path, dir[0], sub_dir)):
                if file_name:
                    full_path = os.path.join(work_path, dir[0], 
                        os.path.join(work_path, dir[0], sub_dir), file_name)
                    files_path.append(full_path)
    return files_path