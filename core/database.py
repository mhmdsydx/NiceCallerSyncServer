import sqlite3
from pathlib import Path


class Database:

    def __init__(self, db_path):

        self.db_path = str(Path(db_path))

        self.conn = None

        self.cursor = None

    def connect(self):

        if self.conn:
            return

        self.conn = sqlite3.connect(self.db_path)

        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

        self.cursor.execute("PRAGMA foreign_keys=ON")

        self.cursor.execute("PRAGMA journal_mode=WAL")

        self.cursor.execute("PRAGMA synchronous=NORMAL")

    def close(self):

        if self.conn:

            self.conn.close()

            self.conn = None

            self.cursor = None

    def begin(self):

        self.cursor.execute("BEGIN IMMEDIATE")

    def commit(self):

        self.conn.commit()

    def rollback(self):

        self.conn.rollback()

    def execute(self, sql, params=()):

        return self.cursor.execute(sql, params)

    def executemany(self, sql, values):

        return self.cursor.executemany(sql, values)

    def query(self, sql, params=()):

        cur = self.cursor.execute(sql, params)

        return cur.fetchall()

    def query_one(self, sql, params=()):

        cur = self.cursor.execute(sql, params)

        return cur.fetchone()

    def scalar(self, sql, params=()):

        row = self.query_one(sql, params)

        if row is None:
            return None

        return row[0]

    def table_exists(self, table):

        row = self.query_one(

            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=?
            """,

            (table,)

        )

        return row is not None
