from core.database import Database
from core.normalizer import normalize
from core.logger import info, error

from config import CACHE_DB, CALL_DB, STATE_FILE

import json
from pathlib import Path


class SyncEngine:

    def __init__(self):
        self.cache = Database(CACHE_DB)
        self.call = Database(CALL_DB)

        self.phone_index = {}
        self.label_index = {}
        self.entry_index = {}

        self.extension_id = None

        self.next_phone_id = 1
        self.next_label_id = 1
        self.next_entry_id = 1

        self.stats = {
            "added": 0,
            "updated": 0,
            "skipped": 0,
        }

    def open(self):
        self.cache.connect()
        self.call.connect()

    def close(self):
        self.cache.close()
        self.call.close()

    def load_extension(self):
        row = self.call.query_one(
            "SELECT id FROM Extension LIMIT 1"
        )
        self.extension_id = row["id"]

    def load_next_ids(self):
        self.next_phone_id = self.call.scalar(
            "SELECT IFNULL(MAX(id),0)+1 FROM PhoneNumber"
        )

        self.next_label_id = self.call.scalar(
            "SELECT IFNULL(MAX(id),0)+1 FROM Label"
        )

        self.next_entry_id = self.call.scalar(
            """
            SELECT IFNULL(MAX(id),0)+1
            FROM PhoneNumberIdentificationEntry
            """
        )

    def load_phone_index(self):
        rows = self.call.query(
            """
            SELECT id, number
            FROM PhoneNumber
            """
        )

        self.phone_index = {
            str(r["number"]): r["id"]
            for r in rows
        }

        info(f"Loaded {len(self.phone_index)} phone numbers.")

    def load_label_index(self):
        rows = self.call.query(
            """
            SELECT id, localized_label
            FROM Label
            """
        )

        self.label_index = {
            r["localized_label"]: r["id"]
            for r in rows
        }

        info(f"Loaded {len(self.label_index)} labels.")

    def insert_phone(self, number):

        phone_id = self.next_phone_id

        self.call.execute(

            """
            INSERT INTO PhoneNumber
            (
                id,
                number
            )
            VALUES
            (
                ?,
                ?
            )
            """,

            (
                phone_id,
                int(number)
            )

        )

        self.phone_index[number] = phone_id

        self.next_phone_id += 1

        return phone_id

    def insert_label(self, label):

        if label in self.label_index:

            return self.label_index[label]

        label_id = self.next_label_id

        self.call.execute(

            """
            INSERT INTO Label
            (
                id,
                localized_label
            )
            VALUES
            (
                ?,
                ?
            )
            """,

            (
                label_id,
                label
            )

        )

        self.label_index[label] = label_id

        self.next_label_id += 1

        return label_id

    def insert_identification(self, phone_id, label_id):

        self.call.execute(

            """
            INSERT INTO PhoneNumberIdentificationEntry
            (
                id,
                extension_id,
                phone_number_id,
                label_id
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?
            )
            """,

            (
                self.next_entry_id,
                self.extension_id,
                phone_id,
                label_id
            )

        )

        self.next_entry_id += 1

    def sync(self):

        self.open()

        self.load_extension()

        self.load_next_ids()

        self.load_phone_index()

        self.load_label_index()

        rows = self.load_cache()

        self.call.begin()

        try:

            last_time = 0

            for row in rows:

                number = normalize(

                    row["phone"],
                    row["country"]
                )

                if not number:

                    continue

                label = row["name"]

                cached = row["cached_at"]

                if cached > last_time:

                    last_time = cached

                if number in self.phone_index:

                    self.stats["skipped"] += 1

                    continue

                phone_id = self.insert_phone(number)

                label_id = self.insert_label(label)

                self.insert_identification(
                    phone_id,
                    label_id
                )

                self.stats["added"] += 1

            self.call.commit()

            self.save_state(last_time)

        except Exception:

            self.call.rollback()

            raise

        finally:

            self.close()


