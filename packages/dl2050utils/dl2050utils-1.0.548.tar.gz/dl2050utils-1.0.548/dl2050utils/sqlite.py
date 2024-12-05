import datetime
import sqlite3
from dl2050utils.core import date_to_srt, str_to_date

class Sqlite():
    def __init__(self, dbname):
        dbname = dbname or ':memory:'
        # Register the adapters and converters
        sqlite3.register_adapter(datetime.datetime, date_to_srt)
        sqlite3.register_converter("DATETIME", str_to_date)
        # Create connection and ensure rows are returned as dictionaries
        self.conn = sqlite3.connect(dbname)
        self.conn.row_factory = sqlite3.Row 
    def close(self):
        self.conn.close()
    def execute(self, q, params=None):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(q, params)
            else:
                cursor.execute(q)
            self.conn.commit()
        except sqlite3.DatabaseError as exc:
            print(f"Sqlite.execute error: {exc}")
            self.conn.rollback()
        return cursor
    def delete_all(self, tbl):
        self.execute(f'''DELETE FROM {tbl}''')
    def insert(self, tbl, d):
        cols,placeholders = ", ".join(d.keys()),", ".join(["?" for _ in d])
        q = f'''INSERT INTO {tbl} ({cols}) VALUES ({placeholders})'''
        values = list(d.values())
        cursor = self.execute(q, values)
        return cursor.lastrowid
    def update(self, tbl, key_col, d):
        set_clause = ", ".join([f"{col} = ?" for col in d.keys()])
        q = f"UPDATE {tbl} SET {set_clause} WHERE {key_col} = ?"
        values = list(d.values()) + [d[key_col]]
        cursor = self.execute(q, values)
        return cursor.rowcount > 0
    def delete(self, tbl, key_col, key_val):
        q = f"DELETE FROM {tbl} WHERE {key_col} = ?"
        self.execute(q, (key_val,))
    def select(self, tbl):
        cursor = self.execute(f"SELECT * FROM {tbl}")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]  # Return rows as a list of dictionaries
    def select_one(self, tbl, key_col, key_val):
        q = f"SELECT * FROM {tbl} WHERE {key_col} = ? LIMIT 1"
        cursor = self.execute(q, (key_val,))
        row = cursor.fetchone()
        return dict(row) if row else None
    def select_and_update(self, tbl, key_col, d):
        cursor = self.conn.cursor()
        try:
            cursor.execute("BEGIN IMMEDIATE")
            d1 = self.select_one(tbl, key_col, d[key_col])
            if d1 is None:
                self.conn.rollback()
                return False
            d = {**d1, **d}
            ret = self.update(tbl, key_col, d)
            self.conn.commit()
            return ret
        except sqlite3.DatabaseError as exc:
            print(f"Sqlite.select_and_update EXCEPTION: {exc}")
            self.conn.rollback()
            return False
