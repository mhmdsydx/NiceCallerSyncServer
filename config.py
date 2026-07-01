from pathlib import Path

# =====================================================
# Databases
# =====================================================

CACHE_DB = Path(
    "/var/jb/var/mobile/Library/Preferences/PhoneHubDB/getcontact_cache.sqlite"
)

CALL_DB = Path(
    "/var/jb/var/mobile/Library/Caches/NC-CallDirectory.db"
)

# =====================================================
# Project
# =====================================================

ROOT = Path(__file__).parent

DATA_DIR = ROOT / "data"

STATE_FILE = ROOT / "state.json"

LOG_FILE = DATA_DIR / "sync.log"

BACKUP_DIR = DATA_DIR / "backups"

# =====================================================
# HTTP
# =====================================================

HOST = "127.0.0.1"

PORT = 8080

# =====================================================
# Country
# =====================================================

DEFAULT_COUNTRY = "EG"

DEFAULT_COUNTRY_CODE = "20"

# =====================================================
# Create directories
# =====================================================

DATA_DIR.mkdir(exist_ok=True)

BACKUP_DIR.mkdir(exist_ok=True)
