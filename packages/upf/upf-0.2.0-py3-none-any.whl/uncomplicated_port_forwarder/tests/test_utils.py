import pytest
import os
import socket
import psutil
from unittest.mock import patch, Mock
from uncomplicated_port_forwarder.utils import (
    require_root, check_port_usage, parse_port_spec, validate_ip,
    validate_subnet, validate_port, validate_start_at, calculate_ip_range,
    validate_port_range
)

def test_require_root():
    @require_root
    def dummy_func(): return True
    
    with patch('os.geteuid', return_value=0):
        assert dummy_func() is True
    
    with patch('os.geteuid', return_value=1000), \
         pytest.raises(SystemExit):
        dummy_func()

@pytest.fixture
def mock_psutil():
    conn = Mock(laddr=Mock(port=80), pid=1234)
    process = Mock(name=lambda: "nginx")
    
    with patch('psutil.net_connections', return_value=[conn]), \
         patch('psutil.Process', return_value=process):
        yield conn, process

def test_check_port_usage_socket_error():
    with patch('socket.socket') as mock_socket:
        mock_socket.return_value.bind.side_effect = socket.error
        is_used, details = check_port_usage(80, "tcp")
        assert is_used
        assert "in use" in details

def test_parse_port_spec_basic():
    assert parse_port_spec("80") == (80, "tcp")
    assert parse_port_spec("80", udp_flag=True) == (80, "udp")

def test_parse_port_spec_with_protocol():
    assert parse_port_spec("80/tcp") == (80, "tcp")
    assert parse_port_spec("80/udp") == (80, "udp")

def test_parse_port_spec_invalid():
    with pytest.raises(ValueError):
        parse_port_spec("80/http")
    with pytest.raises(ValueError):
        parse_port_spec("80/tcp", udp_flag=True)

def test_validate_ip():
    assert validate_ip("192.168.1.1") == [192, 168, 1, 1]
    
    with pytest.raises(ValueError):
        validate_ip("192.168.1")
        
    validate_ip("192.168.1.256")

def test_validate_subnet():
    validate_subnet(24)
    
    with pytest.raises(ValueError):
        validate_subnet(-1)
    with pytest.raises(ValueError):
        validate_subnet(33)

def test_validate_port():
    validate_port(80)
    
    with pytest.raises(ValueError):
        validate_port(0)
    with pytest.raises(ValueError):
        validate_port(65536)

def test_validate_start_at():
    validate_start_at(2)
    
    with pytest.raises(ValueError):
        validate_start_at(1)
    with pytest.raises(ValueError):
        validate_start_at(255)

def test_calculate_ip_range():
    assert calculate_ip_range(24) == 254
    assert calculate_ip_range(30) == 2

def test_validate_port_range():
    validate_port_range(1000, 100)
    
    with pytest.raises(ValueError):
        validate_port_range(65500, 100)