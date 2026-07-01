from database import Database
from normalizer import normalize
from logger import info, error

from config import CACHE_DB
from config import CALL_DB

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

            "added":0,

            "updated":0,

            "skipped":0

        }
