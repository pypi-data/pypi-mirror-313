
# Uncomplicated Port Forwarder (UPF)

Uncomplicated Port Forwarder (UPF) is a simple command-line tool to manage port forwarding rules using `iptables`. It supports both TCP and UDP protocols, making it easy to set up port forwarding for specific ports or ranges of ports.


## Installation

```bash
sudo pipx install upf
```
Run the script with `sudo` for administrative privileges (required to modify `iptables`).

## Usage

### Add a Single Port Forwarding Rule

Add a port forwarding rule from a host to a remote IP and port.

#### TCP (default)
```bash
sudo upf add <host-port> <remote-ip>:<remote-port>
```

Example:
```bash
sudo upf add 2200 192.168.0.2:22 # tcp by default
```

#### UDP
```bash
sudo upf add <host-port> <remote-ip>:<remote-port> --udp
sudo upf add <host-port>/<protocol> <remote-ip>:<remote-port>

```

Example:
```bash
sudo upf add 2200 192.168.0.2:22 --udp
sudo upf add 2200/udp 192.168.0.2:22
sudo upf add 2200/tcp 192.168.0.2:22
```

### Add a Range of Port Forwarding Rules

Add a range of port forwarding rules for a subnet starting from a specified port.

#### TCP (default)
```bash
sudo upf add-range <starting-port>/<protocol> <gateway>/<subnet>:<start port> [--max <count>] [--start-at <number>]
```

Example:
```bash
sudo upf add-range 2200 192.180.12.1/24:80 [--max 10] [--start-at 20]
sudo upf add-range 2200 192.180.12.20/24:80
```

#### UDP
```bash
sudo  upf add-range 2200/udp 192.180.12.1/24:80 --max 10 --start-at 20
```

### List All Managed Port Forwarding Rules

List all the port forwarding rules that have been added using UPF.

```bash
sudo upf list
```

### Delete a Specific Port Forwarding Rule

Delete a specific port forwarding rule by host port.

#### TCP (default)
```bash
sudo upf delete <host-port>/<protocol>
```

Example:
```bash
sudo upf delete 2200 # tcp by default
sudo upf delete 2200/tcp
```

#### UDP
```bash
sudo upf delete <host-port> --udp
```

Example:
```bash
sudo upf delete 2200 --udp
sudo upf delete 2200/udp
```

### Prune portforwarding

Clear all portforwarding added by upf

```bash
sudo upf prune
```

### Sync

In case there is rules which are not part of upf, you can sync them.

```bash
sudo upf sync
```

## Notes

- **Persistence:** By default, changes made using `iptables` are not persistent after reboot. To make them persistent, you can save the rules using `iptables-save` and restore them with `iptables-restore`.