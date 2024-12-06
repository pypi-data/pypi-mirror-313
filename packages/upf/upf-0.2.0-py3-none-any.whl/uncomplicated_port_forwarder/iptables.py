import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models.port_forward import PortForward
    
def add_rule(port_forward: "PortForward") -> None:
    commands = [
        [
            "iptables", "-t", "nat", "-A", "PREROUTING",
            "-p", port_forward.protocol,
            "--dport", str(port_forward.host_port),
            "-j", "DNAT",
            "--to-destination", f"{port_forward.dest_ip}:{port_forward.dest_port}",
            "-m", "comment",
            "--comment", port_forward.prerouting_rule_id,
        ],
        [
            "iptables", "-t", "nat", "-A", "POSTROUTING",
            "-p", port_forward.protocol,
            "-d", port_forward.dest_ip,
            "--dport", str(port_forward.dest_port),
            "-j", "MASQUERADE",
            "-m", "comment",
            "--comment", port_forward.postrouting_rule_id,
        ],
    ]
    for cmd in commands:
        subprocess.run(cmd, check=True)

def delete_rule(port_forward: "PortForward") -> None:
    commands = [
        [
            "iptables", "-t", "nat", "-D", "PREROUTING",
            "-p", port_forward.protocol,
            "--dport", str(port_forward.host_port),
            "-j", "DNAT",
            "--to-destination", f"{port_forward.dest_ip}:{port_forward.dest_port}",
            "-m", "comment",
            "--comment", port_forward.prerouting_rule_id,
        ],
        [
            "iptables", "-t", "nat", "-D", "POSTROUTING",
            "-p", port_forward.protocol,
            "-d", port_forward.dest_ip,
            "--dport", str(port_forward.dest_port),
            "-j", "MASQUERADE",
            "-m", "comment",
            "--comment", port_forward.postrouting_rule_id,
        ],
    ]
    for cmd in commands:
        subprocess.run(cmd, check=True)