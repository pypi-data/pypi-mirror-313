import pytest
from unittest.mock import Mock, MagicMock
from click.testing import CliRunner
import sys
from .mock import MockTable, MockRule, MockState

mock_iptc = MagicMock()
mock_iptc.Table = MockTable
mock_iptc.Rule = MockRule
mock_iptc.Target = lambda rule, target: Mock(to_destination=None)
sys.modules["iptc"] = mock_iptc

from uncomplicated_port_forwarder.app import (  # noqa: E402
    cli,
)


@pytest.fixture
def runner():
    """Fixture for CLI runner"""
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_state():
    """Fixture to reset mock state before each test"""
    state = MockState()
    mock_iptc.Chain = lambda table, chain: state.get_chain(table, chain)
    return state


def test_add_single_rule(runner):
    """Test adding a single port forwarding rule"""
    result = runner.invoke(cli, ["add", "192.168.1.100", "8080:80"])
    assert result.exit_code == 0
    assert "Added TCP forwarding: 8080 -> 192.168.1.100:80" in result.output


def test_add_range_rules(runner):
    """Test adding multiple port forwarding rules for a subnet"""
    result = runner.invoke(cli, ["add-range", "192.168.1.0/30", "8080"])
    assert result.exit_code == 0
    assert "Forwarded" in result.output


@pytest.mark.parametrize(
    "protocol_flag,expected_protocol",
    [
        ([], "TCP"),  # Default case
        (["--udp"], "UDP"),
    ],
)
def test_add_protocol_rules(runner, protocol_flag, expected_protocol):
    """Test adding rules with different protocols"""
    result = runner.invoke(cli, ["add", "192.168.1.100", "8080:80"] + protocol_flag)
    assert result.exit_code == 0
    assert (
        f"Added {expected_protocol} forwarding: 8080 -> 192.168.1.100:80"
        in result.output
    )


def test_list_rules(runner):
    """Test listing managed rules"""
    # Add a rule first
    runner.invoke(cli, ["add", "192.168.1.100", "8080:80"])

    # List rules
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Managed NAT Rules:" in result.output


def test_delete_existing_rule(runner):
    """Test deleting an existing rule"""
    # Add then delete
    runner.invoke(cli, ["add", "192.168.1.100", "8080:80"])
    result = runner.invoke(cli, ["delete", "8080"])
    assert result.exit_code == 0
    assert "Deleted TCP rule" in result.output


def test_delete_nonexistent_rule(runner):
    """Test deleting a rule that doesn't exist"""
    result = runner.invoke(cli, ["delete", "8080"])
    assert result.exit_code == 0
    assert "No managed TCP rule found for port 8080" in result.output


@pytest.mark.parametrize(
    "input_data,expected_code,expected_error",
    [
        (
            ["add", "192.168.1.100", "not-a-port"],
            1,  # Click returns 1 for ValueError
            "invalid literal for int()",  # Part of the error message
        ),
        (
            ["add-range", "not-a-subnet", "8080"],
            1,  # Click returns 1 for ValueError
            "does not appear to be an IPv4 or IPv6 network",  # Part of the error message
        ),
    ],
)
def test_invalid_inputs(runner, input_data, expected_code, expected_error):
    """Test handling of invalid inputs"""
    result = runner.invoke(cli, input_data)
    assert result.exit_code == expected_code
    assert expected_error in str(result.exception)


def test_duplicate_rule(runner):
    """Test adding duplicate rule"""
    # Add first rule
    runner.invoke(cli, ["add", "192.168.1.100", "8080:80"])

    # Try to add same rule again
    result = runner.invoke(cli, ["add", "192.168.1.100", "8080:80"])
    assert result.exit_code == 0
    assert "TCP rule already exists: 8080 -> 192.168.1.100:80" in result.output


def test_add_multiple_with_custom_dest_port(runner):
    """Test adding multiple rules with custom destination port"""
    result = runner.invoke(
        cli, ["add-range", "192.168.1.0/30", "8080", "--dest-port", "443"]
    )
    assert result.exit_code == 0
    assert "Forwarded" in result.output
