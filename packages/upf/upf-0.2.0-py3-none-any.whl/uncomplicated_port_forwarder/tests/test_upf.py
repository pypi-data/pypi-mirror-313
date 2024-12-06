import pytest
from unittest.mock import patch
from uncomplicated_port_forwarder.models.upf import UPF
from uncomplicated_port_forwarder.models.database import Database

@pytest.fixture
def mock_db(tmp_path):
    with patch('uncomplicated_port_forwarder.models.database.DB_PATH', tmp_path / 'test.db'):
        from uncomplicated_port_forwarder.models.database import Database
        Database.migrate()
        yield

class TestUPF:
    def test_is_enabled_returns_true_by_default(self, mock_db):
        assert UPF.is_enabled() is True

    def test_disable_sets_enabled_false(self, mock_db):
        UPF.disable()
        assert UPF.is_enabled() is False

    def test_enable_sets_enabled_true(self, mock_db):
        UPF.disable()
        UPF.enable()
        assert UPF.is_enabled() is True

    def test_is_enabled_returns_false_when_no_record(self, mock_db):
        with Database.connect() as conn:
            conn.execute("DELETE FROM system_status")
        assert UPF.is_enabled() is False

    def test_status_operations_are_idempotent(self, mock_db):
        UPF.enable()
        assert UPF.is_enabled() is True
        UPF.enable()
        assert UPF.is_enabled() is True
        
        UPF.disable()
        assert UPF.is_enabled() is False
        UPF.disable()
        assert UPF.is_enabled() is False