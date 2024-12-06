from netbox.api.metadata import ContentTypeMetadata
from netbox.api.viewsets import NetBoxModelViewSet

from netbox_cesnet_services_plugin import filtersets, models
from .serializers import BGPConnectionSerializer, LLDPNeighborSerializer, LLDPNeighborLeafSerializer


class BGPConnectionViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = models.BGPConnection.objects.all()
    serializer_class = BGPConnectionSerializer
    filterset_class = filtersets.BGPConnectionFilterSet


class LLDPNeighborViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = models.LLDPNeighbor.objects.all()
    serializer_class = LLDPNeighborSerializer
    filterset_class = filtersets.LLDPNeighborFilterSet


class LLDPNeighborLeafViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = models.LLDPNeighborLeaf.objects.all()
    serializer_class = LLDPNeighborLeafSerializer
    filterset_class = filtersets.LLDPNeighborLeafFilterSet
