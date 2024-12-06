# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ...._models import BaseModel

__all__ = ["Client", "Conn"]


class Conn(BaseModel):
    id: Optional[str] = None
    """UUID of the Khulnasoft Tunnel connection."""

    client_id: Optional[str] = None
    """UUID of the Khulnasoft Tunnel connector."""

    client_version: Optional[str] = None
    """The khulnasoftd version used to establish this connection."""

    colo_name: Optional[str] = None
    """The Khulnasoft data center used for this connection."""

    is_pending_reconnect: Optional[bool] = None
    """
    Khulnasoft continues to track connections for several minutes after they
    disconnect. This is an optimization to improve latency and reliability of
    reconnecting. If `true`, the connection has disconnected but is still being
    tracked. If `false`, the connection is actively serving traffic.
    """

    opened_at: Optional[datetime] = None
    """Timestamp of when the connection was established."""

    origin_ip: Optional[str] = None
    """The public IP address of the host running khulnasoftd."""

    uuid: Optional[str] = None
    """UUID of the Khulnasoft Tunnel connection."""


class Client(BaseModel):
    id: Optional[str] = None
    """UUID of the Khulnasoft Tunnel connection."""

    arch: Optional[str] = None
    """The khulnasoftd OS architecture used to establish this connection."""

    config_version: Optional[int] = None
    """The version of the remote tunnel configuration.

    Used internally to sync khulnasoftd with the Zero Trust dashboard.
    """

    conns: Optional[List[Conn]] = None
    """The Khulnasoft Tunnel connections between your origin and Khulnasoft's edge."""

    features: Optional[List[str]] = None
    """Features enabled for the Khulnasoft Tunnel."""

    run_at: Optional[datetime] = None
    """Timestamp of when the tunnel connection was started."""

    version: Optional[str] = None
    """The khulnasoftd version used to establish this connection."""
