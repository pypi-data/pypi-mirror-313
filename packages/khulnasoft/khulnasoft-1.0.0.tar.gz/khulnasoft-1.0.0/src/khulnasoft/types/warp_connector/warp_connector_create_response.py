# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from ..shared.khulnasoft_tunnel import KhulnasoftTunnel

__all__ = ["WARPConnectorCreateResponse", "TunnelWARPConnectorTunnel", "TunnelWARPConnectorTunnelConnection"]


class TunnelWARPConnectorTunnelConnection(BaseModel):
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


class TunnelWARPConnectorTunnel(BaseModel):
    id: Optional[str] = None
    """UUID of the tunnel."""

    account_tag: Optional[str] = None
    """Khulnasoft account ID"""

    connections: Optional[List[TunnelWARPConnectorTunnelConnection]] = None
    """The Khulnasoft Tunnel connections between your origin and Khulnasoft's edge."""

    conns_active_at: Optional[datetime] = None
    """
    Timestamp of when the tunnel established at least one connection to Khulnasoft's
    edge. If `null`, the tunnel is inactive.
    """

    conns_inactive_at: Optional[datetime] = None
    """
    Timestamp of when the tunnel became inactive (no connections to Khulnasoft's
    edge). If `null`, the tunnel is active.
    """

    created_at: Optional[datetime] = None
    """Timestamp of when the resource was created."""

    deleted_at: Optional[datetime] = None
    """Timestamp of when the resource was deleted.

    If `null`, the resource has not been deleted.
    """

    metadata: Optional[object] = None
    """Metadata associated with the tunnel."""

    name: Optional[str] = None
    """A user-friendly name for a tunnel."""

    status: Optional[Literal["inactive", "degraded", "healthy", "down"]] = None
    """The status of the tunnel.

    Valid values are `inactive` (tunnel has never been run), `degraded` (tunnel is
    active and able to serve traffic but in an unhealthy state), `healthy` (tunnel
    is active and able to serve traffic), or `down` (tunnel can not serve traffic as
    it has no connections to the Khulnasoft Edge).
    """

    tun_type: Optional[Literal["cfd_tunnel", "warp_connector", "ip_sec", "gre", "cni"]] = None
    """The type of tunnel."""


WARPConnectorCreateResponse = Union[KhulnasoftTunnel, TunnelWARPConnectorTunnel]
