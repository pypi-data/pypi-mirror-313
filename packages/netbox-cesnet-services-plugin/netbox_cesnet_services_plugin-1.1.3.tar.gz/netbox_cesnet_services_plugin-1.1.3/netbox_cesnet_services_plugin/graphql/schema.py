import strawberry
import strawberry_django
from strawberry_django.optimizer import DjangoOptimizerExtension

from .types import LLDPNeighborType, LLDPNeighborLeafType, BGPConnectionType


@strawberry.type(name="Query")
class CESNETServicesQuery:
    lldp_neighbor: LLDPNeighborType = strawberry_django.field()
    lldp_neighbor_list: list[LLDPNeighborType] = strawberry_django.field()

    lldp_neighbor_leaf: LLDPNeighborLeafType = strawberry_django.field()
    lldp_neighbor_leaf_list: list[LLDPNeighborLeafType] = strawberry_django.field()

    bgp_connection: BGPConnectionType = strawberry_django.field()
    bgp_connection_list: list[BGPConnectionType] = strawberry_django.field()


schema = strawberry.Schema(
    query=CESNETServicesQuery,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
