from .database import Database

class UPF:
    @staticmethod
    def is_enabled():
        with Database.connect(readonly=True) as conn:
            result = conn.execute(
                "SELECT enabled FROM system_status WHERE id = 1"
            ).fetchone()
            return bool(result[0]) if result else False

    @staticmethod
    def enable():
        with Database.connect() as conn:
            conn.execute("UPDATE system_status SET enabled = 1 WHERE id = 1")

    @staticmethod
    def disable():
        with Database.connect() as conn:
            conn.execute("UPDATE system_status SET enabled = 0 WHERE id = 1")