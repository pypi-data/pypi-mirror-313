# Copyright (C) 2024-2025 Bruno Bernard
# SPDX-License-Identifier: Apache-2.0

import subprocess
import uuid
import click
import re
from .models.port_forward import PortForward
from .models.upf import UPF
from .models.database import Database
from .utils import (
    calculate_ip_range,
    parse_port_spec,
    require_root,
    validate_ip,
    validate_port,
    validate_port_range,
    validate_start_at,
    validate_subnet,
)


@click.group()
@require_root
def cli():
    """UPF - Uncomplicated Port Forwarder"""
    Database.migrate()


@cli.command()
@click.argument("port_spec")
@click.argument("destination")
@click.option("--udp", is_flag=True, help="Use UDP instead of TCP")
@require_root
def add(port_spec, destination, udp):
    """Add a port forward: upf add PORT[/PROTOCOL] DEST_IP:DEST_PORT"""
    try:
        port, protocol = parse_port_spec(port_spec, udp)
        dest_ip, dest_port = destination.split(":")

        PortForward(port, protocol, dest_ip, int(dest_port)).insert()

        click.echo(f"Added: {port} ({protocol}) → {dest_ip}:{dest_port}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}")


@cli.command()
@click.argument("port_spec")
@click.option("--udp", is_flag=True, help="Use UDP instead of TCP")
@require_root
def remove(port_spec, udp):
    """Remove a port forward"""
    try:
        port, protocol = parse_port_spec(port_spec, udp)
        forward = PortForward.find(port, protocol)
        if forward:
            forward.delete()
            click.echo(f"Removed: {port}")
        else:
            click.echo("Not found")
    except ValueError as e:
        click.echo(f"Error: {str(e)}")


@cli.command()
def list():
    """List all port forwards"""
    rules = PortForward.all()
    status = "active" if UPF.is_enabled() else "disabled"

    click.echo(f"Status: {status}")
    click.echo("Port                      Forward To")
    click.echo("----                      ----------")

    if not rules:
        return

    for rule in rules:
        click.echo(
            f"{rule.host_port}/{rule.protocol:<19} {rule.dest_ip}:{rule.dest_port}"
        )


@cli.command()
@require_root
def prune():
    """Remove all port forwarding rules"""
    rules = PortForward.all()
    count = 0

    for rule in rules:
        rule.delete()
        count += 1
        click.echo(f"Rule {rule.host_port}/{rule.protocol} removed")

    click.echo(f"Removed {count} rules")


@cli.command()
@require_root
def sync():
    """Sync database with actual iptables rules"""
    rules = subprocess.run(
        ["iptables-save", "-t", "nat"], capture_output=True, text=True
    ).stdout

    pre_rules = {}
    post_rules = {}

    for line in rules.splitlines():
        if "-A PREROUTING" in line:
            match = re.search(
                r"-A PREROUTING -p tcp -m tcp --dport (\d+).* -m comment --comment (upf-pre-\w+) -j DNAT --to-destination ([0-9\.]+):(\d+).*",
                line,
            )
            if match:
                port, pre_id, dest_ip, dest_port = match.groups()
                pre_rules[pre_id.replace("upf-pre-", "")] = (
                    int(port),
                    dest_ip,
                    int(dest_port),
                )

    # Parse POSTROUTING rules to validate pairs
    for line in rules.splitlines():
        if "-A POSTROUTING" in line:
            match = re.search(
                r"-A POSTROUTING -d ([0-9\.]+)/32 -p tcp -m tcp --dport (\d+).* -m comment --comment (upf-post-\w+) -j MASQUERADE",
                line,
            )
            if match:
                dest_ip, dest_port, post_id = match.groups()
                post_rules[post_id.replace("upf-post-", "")] = (dest_ip, int(dest_port))

    with Database.connect() as conn:
        conn.execute("DELETE FROM port_forwards")
        for id, (port, dest_ip, dest_port) in pre_rules.items():
            if id in post_rules.keys():
                conn.execute(
                    """INSERT INTO port_forwards 
                (host_port, protocol, dest_ip, dest_port, prerouting_rule_id, postrouting_rule_id, created_at, id)
                VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)""",
                    (
                        port,
                        "tcp",
                        dest_ip,
                        dest_port,
                        f"upf-pre-{id}",
                        f"upf-post-{id}",
                        uuid.uuid4().hex,
                    ),
                )

    click.echo(f"Synced {len(pre_rules)} rules")


@cli.command()
@click.argument("port_spec")
@click.argument("target")
@click.option("--start-at", type=int, default=2, help="Start at IP")
@click.option("--max", type=int, default=24, help="Maximum forwards")
@require_root
def add_range(port_spec, target, start_at, max):
    """Add port forwards: PORT[/PROTOCOL] GATEWAY/SUBNET:TARGET_PORT"""
    try:
        # Parse and validate source port/protocol
        port, protocol = parse_port_spec(port_spec, False)
        validate_port(port)
        validate_start_at(start_at)

        # Parse target specification
        gateway_subnet, target_port = target.split(":")
        gateway, subnet = gateway_subnet.split("/")
        subnet = int(subnet)
        validate_subnet(subnet)
        validate_port(int(target_port))

        # Parse and validate gateway IP
        ip_parts = validate_ip(gateway)
        available_ips = calculate_ip_range(subnet)
        num_hosts = min(available_ips, max)
        validate_port_range(port, num_hosts)

        # Create port forwards
        count = 0
        for i in range(start_at, start_at + num_hosts):
            if i > 254:  # Skip broadcast
                break

            current_ip_parts = ip_parts.copy()
            current_ip_parts[3] = i
            current_ip = ".".join(map(str, current_ip_parts))

            try:
                rule = PortForward(port + count, protocol, current_ip, int(target_port))
                rule.insert()
                click.echo(
                    f"Added: {port + count} ({protocol}) → {current_ip}:{target_port}"
                )
                count += 1
            except ValueError as e:
                click.echo(f"Warning: {str(e)}")
                continue

        click.echo(f"Added {count} port forwards")

    except ValueError as e:
        click.echo(f"Error: {str(e)}")


@cli.command()
@require_root
def enable():
    """Enable port forwarding"""
    UPF.enable()
    click.echo("Port forwarding enabled")


@cli.command()
@require_root
def disable():
    """Disable port forwarding"""
    UPF.disable()
    click.echo("Port forwarding disabled")