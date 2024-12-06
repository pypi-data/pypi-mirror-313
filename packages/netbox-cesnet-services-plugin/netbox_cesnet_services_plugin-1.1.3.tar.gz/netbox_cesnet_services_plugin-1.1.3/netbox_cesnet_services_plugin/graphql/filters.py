import strawberry_django
from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

from netbox_cesnet_services_plugin.models import LLDPNeighbor, LLDPNeighborLeaf, BGPConnection
from netbox_cesnet_services_plugin.filtersets import (
    LLDPNeighborFilterSet,
    LLDPNeighborLeafFilterSet,
    BGPConnectionFilterSet,
)


@strawberry_django.filter(LLDPNeighbor, lookups=True)
@autotype_decorator(LLDPNeighborFilterSet)
class LLDPNeigborFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(LLDPNeighborLeaf, lookups=True)
@autotype_decorator(LLDPNeighborLeafFilterSet)
class LLDPNeigborLeafFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(BGPConnection, lookups=True)
@autotype_decorator(BGPConnectionFilterSet)
class BGPConnectionFilter(BaseFilterMixin):
    pass
