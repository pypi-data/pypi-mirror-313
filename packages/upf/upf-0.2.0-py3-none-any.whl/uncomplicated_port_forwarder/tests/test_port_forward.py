import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from uncomplicated_port_forwarder.models.port_forward import PortForward

@pytest.fixture
def mock_db(tmp_path):
    with patch('uncomplicated_port_forwarder.models.database.DB_PATH', tmp_path / 'test.db'):
        from uncomplicated_port_forwarder.models.database import Database
        Database.migrate()
        yield

@pytest.fixture
def mock_requires():
    with patch('uncomplicated_port_forwarder.models.port_forward.validate_ip') as ip_mock, \
        patch('uncomplicated_port_forwarder.models.port_forward.add_rule') as add_mock, \
        patch('uncomplicated_port_forwarder.models.port_forward.delete_rule') as del_mock, \
        patch('uncomplicated_port_forwarder.models.port_forward.UPF') as upf_mock, \
        patch('subprocess.run') as subprocess_run_mock:
        upf_mock.is_enabled.return_value = True
        yield ip_mock, add_mock, del_mock, upf_mock, subprocess_run_mock

@pytest.fixture
def sample_port_forward():
    return PortForward(
        host_port=80,
        protocol='tcp',
        dest_ip='192.168.1.2',
        dest_port=8080
    )

class TestPortForward:
    def test_post_init_generates_ids(self):
        pf = PortForward(host_port=80, protocol='tcp')
        assert len(pf.id) == 32
        assert pf.prerouting_rule_id.startswith('upf-pre-')
        assert pf.postrouting_rule_id.startswith('upf-post-')
        assert isinstance(pf.created_at, datetime)

    def test_find_existing_rule(self, mock_db, sample_port_forward, mock_requires):
        sample_port_forward.insert()
        found = PortForward.find(sample_port_forward.host_port, sample_port_forward.protocol)
        assert found.id == sample_port_forward.id
        assert found.dest_ip == sample_port_forward.dest_ip

    def test_find_nonexistent_rule(self, mock_db):
        assert PortForward.find(9999, 'tcp') is None

    def test_all_returns_rules_ordered(self, mock_db, mock_requires):
        pf1 = PortForward(host_port=80, protocol='tcp', dest_ip='192.168.1.2', dest_port=8080)
        pf2 = PortForward(host_port=443, protocol='tcp', dest_ip='192.168.1.2', dest_port=8443)
        pf1.insert()
        pf2.insert()
        
        rules = PortForward.all()
        assert len(rules) == 2
        assert rules[0].host_port == 443  # Most recent first
        assert rules[1].host_port == 80

    def test_insert_adds_rule_and_updates_iptables(self, mock_db, mock_requires, sample_port_forward):
        ip_mock, add_mock, _, upf_mock, subprocess_run_mock = mock_requires
        
        sample_port_forward.insert()

        ip_mock.assert_called_once_with(sample_port_forward.dest_ip)
        add_mock.assert_called_once_with(sample_port_forward)

    def test_insert_duplicate_raises_error(self, mock_db, mock_requires, sample_port_forward):
        sample_port_forward.insert()
        
        duplicate = PortForward(
            host_port=sample_port_forward.host_port,
            protocol=sample_port_forward.protocol
        )
        
        with pytest.raises(ValueError, match="already in use"):
            duplicate.insert()

    def test_delete_removes_rule_and_updates_iptables(self, mock_db, mock_requires, sample_port_forward):
        ip_mock, _, del_mock, _, _ = mock_requires
        sample_port_forward.insert()
        
        sample_port_forward.delete()
        
        ip_mock.assert_called_with(sample_port_forward.dest_ip)
        del_mock.assert_called_once_with(sample_port_forward)
        
        assert PortForward.find(sample_port_forward.host_port, sample_port_forward.protocol) is None

    def test_iptables_not_updated_when_upf_disabled(self, mock_db, mock_requires, sample_port_forward):
        _, _, add_mock, _, upf_mock = mock_requires
        upf_mock.is_enabled.return_value = False
        
        sample_port_forward.insert()
        add_mock.assert_not_called()