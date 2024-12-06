from typing import Annotated
from strawberry import auto, lazy
from strawberry_django import type as strawberry_django_type
from dcim.graphql.types import DeviceType, InterfaceType
from ipam.graphql.types import IPAddressType, PrefixType, VRFType
from netbox.graphql.types import NetBoxObjectType


from netbox_cesnet_services_plugin.models import LLDPNeighbor, LLDPNeighborLeaf, BGPConnection

from .filters import LLDPNeigborFilter, LLDPNeigborLeafFilter, BGPConnectionFilter

__all__ = (
    "LLDPNeighborType",
    "LLDPNeighborLeafType",
    "BGPConnectionType",
)


@strawberry_django_type(LLDPNeighbor, filters=LLDPNeigborFilter)
class LLDPNeighborType(NetBoxObjectType):
    id: auto
    device_a: Annotated["DeviceType", lazy("dcim.graphql.types")] | None
    interface_a: Annotated["InterfaceType", lazy("dcim.graphql.types")] | None
    device_b: Annotated["DeviceType", lazy("dcim.graphql.types")] | None
    interface_b: Annotated["InterfaceType", lazy("dcim.graphql.types")] | None
    imported_data: auto
    status: auto
    comments: auto


@strawberry_django_type(LLDPNeighborLeaf, filters=LLDPNeigborLeafFilter)
class LLDPNeighborLeafType(NetBoxObjectType):
    id: auto
    device_nb: Annotated["DeviceType", lazy("dcim.graphql.types")]
    interface_nb: Annotated["InterfaceType", lazy("dcim.graphql.types")]
    device_ext: auto
    interface_ext: auto
    status: auto
    imported_data: auto


@strawberry_django_type(BGPConnection, filters=BGPConnectionFilter)
class BGPConnectionType(NetBoxObjectType):
    id: auto
    device: Annotated["DeviceType", lazy("dcim.graphql.types")]
    next_hop: Annotated["IPAddressType", lazy("ipam.graphql.types")]
    bgp_prefix: Annotated["PrefixType", lazy("ipam.graphql.types")]
    vrf: Annotated["VRFType", lazy("ipam.graphql.types")]
    role: auto
    import_data: auto
    comments: auto
    raw_next_hop: str
    raw_bgp_prefix: str
    raw_vrf: str
