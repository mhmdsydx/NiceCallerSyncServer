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
