import json
from pathlib import Path

from core.database import Database
from core.logger import info, error
from core.normalizer import normalize

from config import (
    CACHE_DB,
    CALL_DB,
    STATE_FILE
)


class SyncEngine:

    def __init__(self):

        self.cache = Database(CACHE_DB)
        self.call = Database(CALL_DB)

        self.phone_index = {}
        self.label_index = {}
        self.identification_index = {}

        self.extension_id = 0

        self.next_phone_id = 1
        self.next_label_id = 1
        self.next_identification_id = 1

        self.stats = {
            "added": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0
        }

    # -------------------------------------------------

    def open(self):

        self.cache.connect()
        self.call.connect()

    # -------------------------------------------------

    def close(self):

        self.cache.close()
        self.call.close()

    # -------------------------------------------------

    def load_state(self):

        if not Path(STATE_FILE).exists():
            return 0

        try:

            with open(
                STATE_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                state = json.load(f)

            return state.get(
                "last_cached_at",
                0
            )

        except Exception:

            return 0

    # -------------------------------------------------

    def save_state(self, timestamp):

        with open(
            STATE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "last_cached_at": timestamp
                },
                f,
                indent=4
            )

    # -------------------------------------------------

    def load_extension(self):

        row = self.call.query_one(
            "SELECT id FROM Extension LIMIT 1"
        )

        self.extension_id = row["id"]

    # -------------------------------------------------

    def load_next_ids(self):

        self.next_phone_id = self.call.scalar(
            "SELECT IFNULL(MAX(id),0)+1 FROM PhoneNumber"
        )

        self.next_label_id = self.call.scalar(
            "SELECT IFNULL(MAX(id),0)+1 FROM Label"
        )

        self.next_identification_id = self.call.scalar(
            """
            SELECT IFNULL(MAX(id),0)+1
            FROM PhoneNumberIdentificationEntry
            """
        )
