from os import environ, path
from utils.main import WIN

sist_name = "ccb-autom"

chrome_driver_path = "/usr/local/bin/chromedriver" if not WIN else ""
chrome_window_size = "1920,1080"

unix_user_path = path.join("/home", environ["USER"], "Documentos" or "Documents")
unix_sist_path = path.join(unix_user_path, sist_name)

struct_dirs_1000 = ["1000", "3026", "3006",
                    "3007",  "3008", "3014"]

struct_dirs_1010 = ["1010", "3010", "3011", "3012",
                    "3016", "3020", "3021", "3023", 
                    "3027", "3030", "3051", "3052", 
                    "3300", "3301", "3302", "3006",
                    "3007", "3008", "3014", "1120", 
                    "11101", "11102"]

struct_dirs = [struct_dirs_1000, struct_dirs_1010]

