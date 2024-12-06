from pathlib import Path
import sqlite3
import os
from datetime import datetime

DB_PATH = Path("/var/lib/upf/upf.db")

def adapt_datetime(dt: datetime) -> str:
    return dt.isoformat()

def convert_datetime(s: bytes) -> datetime:
    return datetime.fromisoformat(s.decode('utf-8'))

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("DATETIME", convert_datetime)

class Database:
    @staticmethod
    def migrate():
        if not DB_PATH.exists():
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            os.chmod(DB_PATH.parent, 0o755)

            with sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS port_forwards (
                        id TEXT PRIMARY KEY,
                        host_port INTEGER,
                        dest_ip TEXT,
                        dest_port INTEGER,
                        protocol TEXT,
                        created_at TIMESTAMP,
                        prerouting_rule_id TEXT,
                        postrouting_rule_id TEXT,
                        UNIQUE(host_port, protocol)
                    )
                """)

                conn.execute("""
                    CREATE TABLE IF NOT EXISTS system_status (
                        id INTEGER PRIMARY KEY CHECK (id = 1),
                        enabled INTEGER DEFAULT 1
                    )
                """)

                conn.execute(
                    "INSERT OR IGNORE INTO system_status (id, enabled) VALUES (1, 1)"
                )
            os.chmod(DB_PATH, 0o644)

    @staticmethod
    def connect(readonly=False):
        if readonly and not DB_PATH.exists():
            raise FileNotFoundError("Database not initialized")
        uri = f"file:{DB_PATH}?mode=ro" if readonly else str(DB_PATH)
        return sqlite3.connect(uri, uri=True if readonly else False)