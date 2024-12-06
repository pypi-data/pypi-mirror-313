import pytest
from unittest.mock import patch, Mock
import sqlite3
from uncomplicated_port_forwarder.models.database import Database, DB_PATH

@pytest.fixture
def mock_db_path(tmp_path):
    with patch('uncomplicated_port_forwarder.models.database.DB_PATH', tmp_path / 'test.db'):
        yield tmp_path / 'test.db'

class TestDatabase:
    def test_migrate_creates_db_and_tables(self, mock_db_path):
        Database.migrate()
        
        assert mock_db_path.exists()
        
        with sqlite3.connect(mock_db_path) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            table_names = {table[0] for table in tables}
            assert 'port_forwards' in table_names
            assert 'system_status' in table_names
            
            status = conn.execute(
                "SELECT enabled FROM system_status WHERE id = 1"
            ).fetchone()
            assert status[0] == 1

    def test_migrate_sets_permissions(self, mock_db_path):
        Database.migrate()
        
        assert oct(mock_db_path.parent.stat().st_mode)[-3:] == '755'
        assert oct(mock_db_path.stat().st_mode)[-3:] == '644'

    def test_connect_readonly_raises_if_db_missing(self, mock_db_path):
        with pytest.raises(FileNotFoundError):
            Database.connect(readonly=True)

    def test_connect_readonly(self, mock_db_path):
        Database.migrate()
        
        with Database.connect(readonly=True) as conn:
            assert isinstance(conn, sqlite3.Connection)
            with pytest.raises(sqlite3.OperationalError):
                conn.execute("INSERT INTO system_status (id, enabled) VALUES (2, 1)")

    def test_connect_writable(self, mock_db_path):
        Database.migrate()
        
        with Database.connect(readonly=False) as conn:
            assert isinstance(conn, sqlite3.Connection)
            conn.execute("UPDATE system_status SET enabled = 0 WHERE id = 1")
            conn.commit()
            
            result = conn.execute(
                "SELECT enabled FROM system_status WHERE id = 1"
            ).fetchone()
            assert result[0] == 0

    def test_migrate_idempotent(self, mock_db_path):
        Database.migrate()
        first_mtime = mock_db_path.stat().st_mtime
        
        Database.migrate()
        second_mtime = mock_db_path.stat().st_mtime
        
        assert first_mtime == second_mtime
