from netbox.views import generic
from netbox_cesnet_services_plugin.models import LLDPNeighborLeaf
from netbox_cesnet_services_plugin.tables import LLDPNeighborLeafTable
from netbox_cesnet_services_plugin.forms import (
    LLDPNeighborLeafForm,
    LLDPNeighborLeafFilterForm,
)
from netbox_cesnet_services_plugin.filtersets import (
    LLDPNeighborLeafFilterSet,
)


class LLDPNeigborLeafView(generic.ObjectView):
    queryset = LLDPNeighborLeaf.objects.all()
    template_name = "netbox_cesnet_services_plugin/lldpneighborleaf/lldpneighborleaf.html"


class LLDPNeighborLeafListView(generic.ObjectListView):
    queryset = LLDPNeighborLeaf.objects.all()
    table = LLDPNeighborLeafTable
    filterset = LLDPNeighborLeafFilterSet
    filterset_form = LLDPNeighborLeafFilterForm


class LLDPNeighborLeafEditView(generic.ObjectEditView):
    queryset = LLDPNeighborLeaf.objects.all()
    form = LLDPNeighborLeafForm


class LLDPNeighborLeafDeleteView(generic.ObjectDeleteView):
    queryset = LLDPNeighborLeaf.objects.all()


class LLDPNeighborLeafBulkDeleteView(generic.BulkDeleteView):
    queryset = LLDPNeighborLeaf.objects.all()
    table = LLDPNeighborLeafTable
    filterset = LLDPNeighborLeafFilterSet
