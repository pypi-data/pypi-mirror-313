from netbox.views import generic
from netbox_cesnet_services_plugin.models import LLDPNeighbor
from netbox_cesnet_services_plugin.tables import LLDPNeighborTable
from netbox_cesnet_services_plugin.forms.lldpneighbor import (
    LLDPNeighborForm,
    LLDPNeighborFilterForm,
)
from netbox_cesnet_services_plugin.filtersets.lldpneighbor import LLDPNeighborFilterSet


class LLDPNeigborView(generic.ObjectView):
    queryset = LLDPNeighbor.objects.all()
    template_name = "netbox_cesnet_services_plugin/lldpneighbor/lldpneighbor.html"


class LLDPNeighborListView(generic.ObjectListView):
    queryset = LLDPNeighbor.objects.all()
    table = LLDPNeighborTable
    filterset = LLDPNeighborFilterSet
    filterset_form = LLDPNeighborFilterForm


class LLDPNeighborEditView(generic.ObjectEditView):
    queryset = LLDPNeighbor.objects.all()
    form = LLDPNeighborForm


class LLDPNeighborDeleteView(generic.ObjectDeleteView):
    queryset = LLDPNeighbor.objects.all()


class LLDPNeighborBulkDeleteView(generic.BulkDeleteView):
    queryset = LLDPNeighbor.objects.all()
    table = LLDPNeighborTable
    filterset = LLDPNeighborFilterSet
