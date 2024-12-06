import os
import sys
import socket
import psutil
from functools import wraps

def require_root(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if os.geteuid() != 0:
            sys.exit("This command requires root privileges")
        return func(*args, **kwargs)
    return wrapper


def check_port_usage(port: int, protocol: str) -> tuple[bool, str]:
    """
    Check if a port is in use outside of UPF
    Returns: (is_in_use, details)
    """
    # Check using psutil for more detailed process info
    for conn in psutil.net_connections(kind=protocol):
        if conn.laddr.port == port:
            try:
                process = psutil.Process(conn.pid)
                return (
                    True,
                    f"Port {port}/{protocol} in use by {process.name()} (PID: {conn.pid})",
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return True, f"Port {port}/{protocol} in use by unknown process"

    sock = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM if protocol == "udp" else socket.SOCK_STREAM
    )
    try:
        sock.bind(("", port))
        return False, ""
    except socket.error:
        return True, f"Port {port}/{protocol} in use"
    finally:
        sock.close()


def parse_port_spec(port_spec: str, udp_flag: bool = False) -> tuple[int, str]:
    """Parse port specification in format PORT[/PROTOCOL] with optional --udp flag"""
    if "/" in port_spec:
        port, protocol = port_spec.split("/")
        if protocol.lower() not in ["tcp", "udp"]:
            raise ValueError("Protocol must be tcp or udp")
        if udp_flag and protocol.lower() == "tcp":
            raise ValueError("Conflicting protocol specifications")
        return int(port), protocol.lower()
    return int(port_spec), "udp" if udp_flag else "tcp"


def validate_ip(ip: str) -> list[int]:
    """Validate IP address and return octets"""
    ip_parts = [int(x) for x in ip.split(".")]
    if len(ip_parts) != 4:
        raise ValueError("Invalid IP address format")
    return ip_parts


def validate_subnet(subnet: int) -> None:
    if subnet < 0 or subnet > 32:
        raise ValueError("Invalid subnet mask (0-32)")


def validate_port(port: int) -> None:
    if port < 1 or port > 65535:
        raise ValueError("Invalid port (1-65535)")


def validate_start_at(start: int) -> None:
    if start < 2 or start > 254:
        raise ValueError("Invalid start IP (2-254)")


def calculate_ip_range(mask: int) -> int:
    return 2 ** (32 - mask) - 2  # Subtract network and broadcast


def validate_port_range(start_port: int, count: int) -> None:
    if start_port + count > 65535:
        raise ValueError(
            f"Port range {start_port}-{start_port + count} exceeds maximum port 65535"
        )
