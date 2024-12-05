# Copyright (C) 2024-2025 Bruno Bernard
# SPDX-License-Identifier: Apache-2.0

import iptc
import click
import ipaddress

UPF_TAG = "managed_by_upf"


def rule_exists(chain, rule):
    """
    Check if a rule exists in a chain.
    """
    return any(r == rule for r in chain.rules)


def add_rule(ip, host_port, other_port, protocol):
    """
    Add a port forwarding rule with a UPF tag.
    """
    # Add PREROUTING rule
    prerouting_chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "PREROUTING")
    rule = iptc.Rule()
    rule.protocol = protocol
    match = rule.create_match(protocol)
    match.dport = str(host_port)
    rule.target = iptc.Target(rule, "DNAT")
    rule.target.to_destination = f"{ip}:{other_port}"
    rule.comment = UPF_TAG

    if not rule_exists(prerouting_chain, rule):
        prerouting_chain.insert_rule(rule)
        click.echo(
            f"Added {protocol.upper()} forwarding: {host_port} -> {ip}:{other_port}"
        )
    else:
        click.echo(
            f"{protocol.upper()} rule already exists: {host_port} -> {ip}:{other_port}"
        )

    # Add POSTROUTING rule
    postrouting_chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "POSTROUTING")
    rule = iptc.Rule()
    rule.protocol = protocol
    rule.target = iptc.Target(rule, "MASQUERADE")
    rule.comment = UPF_TAG

    if not rule_exists(postrouting_chain, rule):
        postrouting_chain.insert_rule(rule)


def add_multiple(gateway, start_port, protocol, dest_port=22):
    """
    Add a range of port forwarding rules for a subnet.
    """
    ip_network = ipaddress.ip_network(gateway, strict=False)
    current_port = start_port

    for ip in ip_network.hosts():
        # Skip the network and broadcast addresses
        if ip in [ip_network.network_address, ip_network.broadcast_address]:
            continue
        try:
            add_rule(str(ip), current_port, dest_port, protocol)
            click.echo(f"Forwarded {current_port} -> {ip}:{dest_port}")
            current_port += 1
        except ValueError as e:
            click.echo(f"Error: {e}")
            break


def list_rules():
    """
    List all NAT rules managed by UPF.
    """
    table = iptc.Table(iptc.Table.NAT)
    table.refresh()
    click.echo("Managed NAT Rules:")
    for chain_name in ["PREROUTING", "POSTROUTING"]:
        chain = iptc.Chain(table, chain_name)
        for rule in chain.rules:
            if UPF_TAG in rule.comment:
                click.echo(f"- {rule}")


def delete_rule(host_port, protocol):
    """
    Delete a specific forwarding rule managed by UPF.
    """
    chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "PREROUTING")
    for rule in chain.rules:
        if (
            UPF_TAG in rule.comment
            and rule.protocol == protocol
            and any(match.dport == str(host_port) for match in rule.matches)
        ):
            chain.delete_rule(rule)
            click.echo(f"Deleted {protocol.upper()} rule for port {host_port}")
            return
    click.echo(f"No managed {protocol.upper()} rule found for port {host_port}")


@click.group()
def cli():
    """Uncomplicated Port Forwarder (UPF)"""
    pass


@cli.command()
@click.argument("ip")
@click.argument("ports")
@click.option("--udp", is_flag=True, help="Use UDP instead of TCP")
def add(ip, ports, udp):
    """Add a port forwarding rule"""
    host_port, other_port = map(int, ports.split(":"))
    protocol = "udp" if udp else "tcp"
    add_rule(ip, host_port, other_port, protocol)


@cli.command()
@click.argument("gateway")
@click.argument("start_port", type=int)
@click.option("--udp", is_flag=True, help="Use UDP instead of TCP")
@click.option(
    "--dest-port", default=22, type=int, help="Destination port (default: 22)"
)
def add_range(gateway, start_port, udp, dest_port):
    """Add a range of forwarding rules"""
    protocol = "udp" if udp else "tcp"
    add_multiple(gateway, start_port, protocol, dest_port)


@cli.command()
def list():
    """List all port forwarding rules managed by UPF"""
    list_rules()


@cli.command()
@click.argument("host_port", type=int)
@click.option("--udp", is_flag=True, help="Use UDP instead of TCP")
def delete(host_port, udp):
    """Delete a specific port forwarding rule"""
    protocol = "udp" if udp else "tcp"
    delete_rule(host_port, protocol)
