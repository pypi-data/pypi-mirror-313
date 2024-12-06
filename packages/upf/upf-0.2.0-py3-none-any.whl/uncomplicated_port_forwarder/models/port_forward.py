from dataclasses import dataclass
from typing import List, Optional
import uuid
import sqlite3
from datetime import datetime

from uncomplicated_port_forwarder.models.upf import UPF
from ..utils import validate_ip
from .database import Database
from ..iptables import add_rule, delete_rule

@dataclass
class PortForward:
    host_port: int = None
    protocol: str = None
    dest_ip: str = None
    dest_port: int = None
    id: str = None
    created_at: datetime = None
    prerouting_rule_id: str = None
    postrouting_rule_id: str = None

    def __post_init__(self):
        self.id = self.id or uuid.uuid4().hex
        self.created_at = self.created_at or datetime.now()
        self.prerouting_rule_id = self.prerouting_rule_id or f"upf-pre-{self.id[:8]}"
        self.postrouting_rule_id = self.postrouting_rule_id or f"upf-post-{self.id[:8]}"

    @staticmethod
    def find(host_port, protocol) -> Optional["PortForward"]:
        with Database.connect() as conn:
            rule = conn.execute(
                """
                SELECT host_port, protocol, dest_ip, dest_port, id, 
                       created_at, prerouting_rule_id, postrouting_rule_id
                FROM port_forwards
                WHERE host_port = ? AND protocol = ?
            """,
                (host_port, protocol),
            ).fetchone()

            if rule is None:
                return None

        return PortForward(*rule)

    @staticmethod
    def all() -> List["PortForward"]:
        with Database.connect(readonly=True) as conn:
            rows = conn.execute("""
                SELECT host_port, protocol, dest_ip, dest_port, id, 
                       created_at, prerouting_rule_id, postrouting_rule_id
                FROM port_forwards
                ORDER BY created_at DESC
            """).fetchall()
            return [PortForward(*row) for row in rows]

    def delete(self):
        validate_ip(self.dest_ip)
        with Database.connect() as conn:
            try:
                conn.execute(
                    """
                    DELETE FROM port_forwards
                    WHERE id = ?
                """,
                    (self.id,),
                )
                delete_rule(self)
            except sqlite3.IntegrityError:
                raise ValueError(
                    f"Port {self.host_port}/{self.protocol} already in use"
                )

    def insert(self):
        validate_ip(self.dest_ip)
        with Database.connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO port_forwards 
                    (id, host_port, dest_ip, dest_port, protocol, created_at,
                     prerouting_rule_id, postrouting_rule_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        self.id,
                        self.host_port,
                        self.dest_ip,
                        self.dest_port,
                        self.protocol,
                        self.created_at,
                        self.prerouting_rule_id,
                        self.postrouting_rule_id,
                    ),
                )
                if UPF.is_enabled():
                    add_rule(self)
            except sqlite3.IntegrityError:
                raise ValueError(
                    f"Port {self.host_port}/{self.protocol} already in use"
                )