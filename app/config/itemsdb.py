import json
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Union, Dict, List, Any, Tuple

from app.config.paths import items_path


class Item:

    def __init__(self) -> None:
        self.items_db: str = items_path
        self.cursor: Cursor = None
        self.conn: Connection = None

        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.items_db)
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

    def set_item(self, _type: int, *item: tuple) -> bool:
        try:
            if _type == 1000:
                if self.cursor.execute(f"""INSERT INTO item1000 (item, month, inserted) VALUES (?, ?, ?)""", item):
                    return True

            if _type == 1010:
                if self.cursor.execute(f"""INSERT INTO item1010 (item, month, inserted) VALUES (?, ?, ?)""", item):
                    return True

            if _type == 10:
                if self.cursor.execute(f"""INSERT INTO extract (item, month, inserted) VALUES (?, ?, ?)""", item):
                    return True

        except Exception:
            return False

    def get_items1000(self, month: str = None, inserted: int = 0, all: bool = False) -> tuple:
        try:
            if all:
                self.cursor.execute(f"SELECT item FROM extract")
            elif month is None:
                self.cursor.execute(f"SELECT item FROM item1000 WHERE inserted = {inserted}")
            else:
                self.cursor.execute(f"SELECT item FROM item1000 WHERE month='{month}' AND inserted = {inserted}")
            items = self.cursor.fetchall()
            return items

        except Exception:
            return None

    def get_items1010(self, month: str = None, inserted: int = 0, all_items: bool = False) -> tuple:
        try:
            if all_items:
                self.cursor.execute(f"SELECT item FROM extract")
            elif month is None:
                self.cursor.execute(f"SELECT item FROM item1010 WHERE inserted = {inserted}")
            else:
                self.cursor.execute(f"SELECT item FROM item1010 WHERE month='{month}' AND inserted = {inserted}")
            items = self.cursor.fetchall()

            return items
        except Exception:
            return None

    def get_extract_items(self, month: str = None, inserted: int = 0, all: bool = False) -> tuple:
        try:
            if all:
                self.cursor.execute(f"SELECT item FROM extract")
            elif month is None:
                self.cursor.execute(f"SELECT item FROM extract WHERE inserted = {inserted}")
            else:
                self.cursor.execute(f"SELECT item FROM extract WHERE month='{month}' AND inserted = {inserted}")
            items = self.cursor.fetchall()

            return items
        except Exception:
            return None

    def get_item_id(self, table: str, _item: dict, month: str = None) -> int:
        if month is None and table is not None:
            self.cursor.execute(f"SELECT oid, item FROM {table}")

        elif month is not None and table is not None:
            self.cursor.execute(f"SELECT oid, item FROM {table} WHERE month='{month}'")

        items = self.cursor.fetchall()
        _id: list = [item[0] for item in items if json.loads(item[1]).get("file-name") == _item["file-name"]]
        if len(_id) > 0:
            return _id[0]
        else:
            return 0

    def set_inserted_item(self, _type: int, month: str, item: dict, inserted: int) -> tuple:
        try:

            if _type == 1000:
                _id = self.get_item_id("item1000", item, month)
                if _id > 0:
                    if self.cursor.execute(f"UPDATE item1000 SET inserted = {inserted} WHERE oid={_id}"):
                        return True

            if _type == 1010:
                _id = self.get_item_id("item1010", item, month)
                if _id > 0:
                    if self.cursor.execute(f"UPDATE item1010 SET inserted = {inserted} WHERE oid={_id}"):
                        return True

            if _type == 10:
                _id = self.get_item_id("extract", item, month)
                if _id > 0:
                    if self.cursor.execute(f"UPDATE extract SET inserted = {inserted} WHERE oid={_id}"):
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
            if table is not None:
                self.cursor.execute(f"DELETE FROM {table} WHERE oid = {id}")
                return True
            return False
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

        if item.get("insert-type") == "DEBT" and item.get("cost-account") == "1010" \
                and not item.get("file-name") == "DB CEST PJ" and not item.get("file-name") == "MANUT CAD":
            success = item_obj.set_item(
                1010,
                json.dumps(item),
                get_item_month(item),
                0
            )

        if item.get("insert-type") == "MOVINT" or item.get("file-name") == "DB CEST PJ" \
                or item.get("file-name") == "MANUT CAD":
            success = item_obj.set_item(
                10,
                json.dumps(item),
                get_item_month(item),
                0
            )

    item_obj.commit()
    return success


def get_item_table(item: dict) -> str:
    if item.get("insert-type") == "DEBT" and item.get("cost-account") == "1000":
        return "item1000"

    if item.get("insert-type") == "DEBT" and item.get("cost-account") == "1010" \
            and not item.get("file-name") == "DB CEST PJ" and not item.get("file-name") == "MANUT CAD":
        return "item1010"

    if item.get("insert-type") == "MOVINT" or item.get("file-name") == "DB CEST PJ" \
            or item.get("file-name") == "MANUT CAD":
        return "extract"


def update(item: dict, inserted: int = 1) -> bool:
    item_obj = Item()
    success: bool = False
    if item.get("insert-type") == "DEBT" and item.get("cost-account") == "1000":
        success = item_obj.set_inserted_item(
            1000,
            get_item_month(item),
            item,
            inserted
        )

    if item.get("insert-type") == "DEBT" and item.get("cost-account") == "1010" \
            and not item.get("file-name") == "DB CEST PJ" and not item.get("file-name") == "MANUT CAD":
        success = item_obj.set_inserted_item(
            1010,
            get_item_month(item),
            item,
            inserted
        )

    if item.get("insert-type") == "MOVINT" or item.get("file-name") == "DB CEST PJ":
        success = item_obj.set_inserted_item(
            10,
            get_item_month(item),
            item,
            inserted
        )

    item_obj.commit()
    return success


def set_item(item_list) -> bool:
    if len(item_list) > 0 and isinstance(item_list, list):
        return verify_insertion(item_list)

    elif len(item_list) > 0 and isinstance(item_list, dict):
        return verify_insertion([item_list])
    return False


def objectify(items1000: tuple = (),
              items1010: tuple = (),
              extract_items: tuple = ()
              ) -> Tuple[List[Any], List[Any], List[Any]]:
    if len(items1000) > 0 and items1000 is not None:
        items1000 = [json.loads(item[0]) for item in items1000]
    else:
        items1000 = []

    if len(items1010) > 0 and items1010 is not None:
        items1010 = [json.loads(item[0]) for item in items1010]
    else:
        items1010 = []

    if len(extract_items) > 0 and extract_items is not None:
        extract_items = [json.loads(item[0]) for item in extract_items]
    else:
        extract_items = []

    return items1000, items1010, extract_items


def get_item_id(item: dict, table: str) -> int:
    item_obj = Item()

    month: str = get_item_month(item)
    _id: int = item_obj.get_item_id(table, item, month=month)

    item_obj.commit()
    return _id


def get_items1000(month: str = None, inserted: int = 0) -> dict:
    item_obj = Item()
    items: tuple = item_obj.get_items1000(month, inserted)
    items, _, _ = objectify(items1000=items)

    item_obj.commit()
    return {"1000": items, "1010": [], "extract": []}


def get_items1010(month: str = None, inserted: int = 0) -> dict:
    item_obj = Item()
    items: tuple = item_obj.get_items1010(month, inserted)
    _, items, _ = objectify(items1010=items)

    item_obj.commit()
    return {"1000": [], "1010": items, "extract": []}


def get_extract_items(month: str = None, inserted: int = 0,
                      return_type: str = None,
                      all_items: bool = False
                      ) -> Union[tuple, Dict[str, Union[List[Any], tuple]]]:
    item_obj = Item()
    extract_items: tuple = item_obj.get_extract_items(month, inserted, all_items)
    _, _, extract_items = objectify(extract_items=extract_items)

    if return_type == "list":
        return extract_items

    item_obj.commit()
    return {"1000": [], "1010": [], "extract": extract_items}


def get_all_items(month: str = None, inserted: int = 0, return_type: str = None) -> Dict[str, tuple]:
    item_obj = Item()

    items1000: tuple = item_obj.get_items1000(month, inserted)
    items1010: tuple = item_obj.get_items1010(month, inserted)
    extract_items: tuple = item_obj.get_extract_items(month, inserted)

    items1000, items1010, extract_items = objectify(items1000, items1010, extract_items)

    item_obj.commit()
    if return_type == "list":
        return items1000 + items1010 + extract_items

    return {"1000": items1000, "1010": items1010, "extract": extract_items}


def get_all_inserted_items(month: str = None) -> Dict[str, tuple]:
    item_obj = Item()

    items1000: tuple = item_obj.get_items1000(month, 1)
    items1010: tuple = item_obj.get_items1010(month, 1)
    extract_items: tuple = item_obj.get_extract_items(month, 1)

    items1000, items1010, extract_items = objectify(items1000, items1010, extract_items)

    item_obj.commit()
    return {"1000": items1000, "1010": items1010, "extract": extract_items}


def set_inserted_item(item: dict, inserted: int = 1) -> bool:
    return update(item, inserted)


def remove_item(item: dict) -> bool:
    table: str = get_item_table(item)
    _id: int = get_item_id(item, table)

    if _id > 0:
        item_obj = Item()
        success = item_obj.remove_item(_id, table)
        item_obj.commit()
        return success

    return False


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
