import json
import sqlite3
from sqlite3 import Connection, Cursor
from app.config.paths import items_path



class Item:

    def __init__(self) -> None:
        self.itemsdb: str = items_path
        self.cursor: Cursor = None
        self.conn: Connection = None

        self.connect()
    
    def connect(self):
        self.conn = sqlite3.connect(self.itemsdb)
        self.cursor = self.conn.cursor()
        self.create_table_items()
    
    def create_table_items(self) -> bool:
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS item1000 (
                    item TEXT NULL,
                    month TEXT NOT NULL,
                    inserted INT NULL,
                    inserted_at DATE NULL
                )""")
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS item1010 (
                    item TEXT NULL,
                    month TEXT NOT NULL,
                    inserted INT NULL,
                    inserted_at DATE NULL
                )""")
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS extract (
                    item TEXT NULL,
                    month TEXT NOT NULL,
                    inserted INT NULL,
                    inserted_at DATE NULL
                )""")
            
        except Exception:
            return False
    

    def set_item(self, type: int, *item: tuple) -> bool:
        try:
            if type == 1000:
                if self.cursor.execute(f"""INSERT INTO item1000 (item, month, inserted) VALUES (?, ?, ?)""", item): 
                    return True

            if type == 1010:
                if self.cursor.execute(f"""INSERT INTO item1010 (item, month, inserted) VALUES (?, ?, ?)""", item): 
                    return True
            
            if type == 10:
                if self.cursor.execute(f"""INSERT INTO extract (item, month, inserted) VALUES (?, ?, ?)""", item): 
                    return True

        except Exception:
            return False

    def get_items1000(self, month: str = None, inserted: int = 0) -> tuple:
        try:
            if month is None:
                self.cursor.execute(f"SELECT item FROM item1000 WHERE inserted = {inserted}")
            else: self.cursor.execute(f"SELECT item FROM item1000 WHERE month='{month}' AND inserted = {inserted}")
            items = self.cursor.fetchall()
            return items

        except Exception:
            return None
    
    def get_items1010(self, month: str = None, inserted: int = 0) -> tuple:
        try:
            if month is None:
                self.cursor.execute(f"SELECT item FROM item1010 WHERE inserted = {inserted}")
            else: self.cursor.execute(f"SELECT item FROM item1010 WHERE month='{month}' AND inserted = {inserted}")
            items = self.cursor.fetchall()
            
            return items
        except Exception:
            return None
    
    def get_extractItems(self, month: str = None, inserted: int = 0) -> tuple:
        try:
            if month is None:
                self.cursor.execute(f"SELECT item FROM extract WHERE inserted = {inserted}")
            else: self.cursor.execute(f"SELECT item FROM extract WHERE month='{month}' AND inserted = {inserted}")
            items = self.cursor.fetchall()

            return items
        except Exception:
            return None
    
    def get_item_id(self, table: str, _item: dict, month: str = None) -> int:
        if month is None:
            self.cursor.execute(f"SELECT oid, item FROM {table}")
        else: self.cursor.execute(f"SELECT oid, item FROM {table} WHERE month='{month}'")
        items = self.cursor.fetchall()
        
        return [item[0] for item in items if json.loads(item[1]).get("file-name") == _item["file-name"]][0]

    def set_inserted_item(self, type: int, month: str,  item: dict) -> tuple:
        try:

            if type == 1000:
                id = self.get_item_id("item1000", item, month)
                if self.cursor.execute(f"UPDATE item1000 SET inserted = 1 WHERE oid={id}"):
                    return True

            if type == 1010:
                id = self.get_item_id("item1010", item, month)
                if self.cursor.execute(f"UPDATE item1010 SET inserted = {True} WHERE oid={id}"): 
                    return True
            
            if type == 10:
                id = self.get_item_id("extract", item, month)
                if self.cursor.execute(f"UPDATE extract SET inserted = {True} WHERE oid={id}"): 
                    return True

        except Exception:
            return None

    def remove_extract_items(self, month: str = None, inserted: int = 0) -> bool:
        try:
            if month is None and inserted == 0:
                self.cursor.execute("DELETE FROM extract")
            else:
                self.cursor.execute(f"DELETE FROM extract WHERE month='{month}' AND inserted={inserted}")
            return True
        except Exception:
            return False
    
    def remove_items1000(self, month: str = None, inserted: int = 0) -> bool:
        try:
            if month is None and inserted == 0:
                self.cursor.execute("DELETE FROM item1000")
            else:
                self.cursor.execute(f"DELETE FROM item1000 WHERE month='{month}' AND inserted={inserted}")
            return True
        except Exception:
            return False
    
    def remove_items1010(self, month: str = None, inserted: int = 0) -> bool:
        try:
            if month is None and inserted == 0:
                self.cursor.execute("DELETE FROM item1010")
            else:
                self.cursor.execute(f"DELETE FROM item1010 WHERE month='{month}' AND inserted={inserted}")
            return True
        except Exception:
            return False

    def remove_all_items(self) -> bool:
        try:
            self.cursor.execute("DELETE FROM item1000")
            self.cursor.execute("DELETE FROM item1010")
            self.cursor.execute("DELETE FROM extract")
            
        except Exception:
            return False
    
    def remove_item(self, id: int, table: str = None) -> bool:
        try:
            if table == "1000":
                self.cursor.execute(f"DELETE FROM item1000 WHERE oid = {id}")

            if table == "1010":
                self.cursor.execute(f"DELETE FROM item1010 WHERE oid = {id}")

            if table == "extract":
                self.cursor.execute(f"DELETE FROM extract WHERE oid = {id}")

            return True
        except Exception:
            return False
    
    def commit(self) -> None:
        self.conn.commit()
        self.conn.close()


# -----------------------------------------------------------------
def get_item_month(item: dict) -> str:
    if isinstance(item, dict):
        month = item.get("date")
        month = f"{month[1]}-{month[2]}"

        return month
    return None


def verify_insertion(items: list) -> bool:
    item_obj = Item()
    success: bool = False
    for item in items:
        if item.get("insert-type") == "DEBT" and item.get("cost-account") == "1000":
            success = item_obj.set_item(
                1000,
                json.dumps(item),
                get_item_month(item),
                0
            )

        if item.get("insert-type") == "DEBT" and item.get("cost-account") == "1010"\
            and not item.get("file-name") == "DB CEST PJ":
            success = item_obj.set_item(
                1010,
                json.dumps(item),
                get_item_month(item),
                0
            )

        if item.get("insert-type") == "MOVINT" or item.get("file-name") == "DB CEST PJ":
            success = item_obj.set_item(
                10,
                json.dumps(item),
                get_item_month(item),
                0
            )

    item_obj.commit()
    return success


def verify_update(item: dict) -> bool:
    item_obj = Item()
    success: bool = False
    if item.get("insert-type") == "DEBT" and item.get("cost-account") == "1000":
        success = item_obj.set_inserted_item(
            1000,
            get_item_month(item),
            item
        )

    if item.get("insert-type") == "DEBT" and item.get("cost-account") == "1010"\
        and not item.get("file-name") == "DB CEST PJ":
        success = item_obj.set_inserted_item(
            1010,
            get_item_month(item),
            item
        )

    if item.get("insert-type") == "MOVINT" or item.get("file-name") == "DB CEST PJ":
        success = item_obj.set_inserted_item(
            10,
            get_item_month(item),
            item
        )

    item_obj.commit()
    return success


def set_item(itemList) -> bool:
    if len(itemList) > 0 and isinstance(itemList, list):
        return verify_insertion(itemList)

    elif len(itemList) > 0 and isinstance(itemList, dict):
        return verify_insertion([itemList])
    return False


def objectfy(items1000: list = [], items1010: list = [], extractItems: list = []) -> list:
    if len(items1000) > 0 and items1000 is not None:
        items1000 = [json.loads(_item[0]) for _item in items1000]
    else: items1000 = []

    if len(items1010) > 0 and items1010 is not None:
        items1010 = [json.loads(_item[0]) for _item in items1010]
    else: items1010 = []

    if len(extractItems) > 0 and extractItems is not None:
        extractItems = [json.loads(_item[0]) for _item in extractItems]
    else: extractItems = []
    
    return (items1000, items1010, extractItems)


def get_item_id(table: str, item: dict) -> int:
    item_obj = Item()
    id: int = item_obj.get_item_id(table, item, get_item_month(item))
    item_obj.commit()
    return id


def get_items1000(month: str = None, inserted: int = 0) -> list:
    item_obj = Item()
    items: list = item_obj.get_extractItems(month, inserted)
    items,_,_ = objectfy(items1000=items)

    item_obj.commit()
    return items


def get_items1010(month: str = None, inserted: int = 0) -> list:
    item_obj = Item()
    items: list = item_obj.get_items1010(month, inserted)
    _,items,_ = objectfy(items1010=items)

    item_obj.commit()
    return items


def get_extract_items(month: str = None, inserted: int = 0) -> list:
    item_obj = Item()
    extractItems: list = item_obj.get_extractItems(month, inserted)
    _,_,extractItems = objectfy(extractItems=extractItems)

    item_obj.commit()
    return extractItems


def get_all_items(month: str = None, inserted: int = 0, return_type: str = None) -> dict:
    item_obj = Item()

    items1000: list = item_obj.get_items1000(month, inserted)
    items1010: list = item_obj.get_items1010(month, inserted)
    extractItems: list = item_obj.get_extractItems(month, inserted)
   
    items1000, items1010, extractItems = objectfy(items1000, items1010, extractItems)

    item_obj.commit()
    if return_type == "list":
        return items1000+items1010+extractItems

    return {"1000": items1000, "1010": items1010, "extract": extractItems}


def get_all_inserted_items(month: str = None) -> bool:
    item_obj = Item()

    items1000: list = item_obj.get_items1000(month, 1)
    items1010: list = item_obj.get_items1010(month, 1)
    extractItems: list = item_obj.get_extractItems(month, 1)
    
    items1000, items1010, extractItems = objectfy(items1000, items1010, extractItems)

    item_obj.commit()
    return {"1000": items1000, "1010": items1010, "extract": extractItems}


def set_inserted_item(item: dict) -> bool:
    verify_update(item)


def remove_all_items() -> bool:
    item_obj = Item()
    success = item_obj.remove_all_items()
    item_obj.commit()
    return success


def remove_items1000(month: str = None, inserted: int = 0) -> bool:
    item_obj = Item()
    success = item_obj.remove_items1000(month, inserted)
    item_obj.commit()
    return success


def remove_items1010(month: str = None, inserted: int = 0) -> bool:
    item_obj = Item()
    success = item_obj.remove_items1010(month, inserted)
    item_obj.commit()
    return success


def remove_extract_items(month: str = None, inserted: int = 0) -> bool:
    item_obj = Item()
    success = item_obj.remove_extract_items(month, inserted)
    item_obj.commit()
    return success
