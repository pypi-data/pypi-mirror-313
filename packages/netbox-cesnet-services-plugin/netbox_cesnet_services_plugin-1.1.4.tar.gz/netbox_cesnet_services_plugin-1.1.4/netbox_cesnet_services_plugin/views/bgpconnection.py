from netbox.views import generic
from ..models.bgpconnection import BGPConnection
from ..tables.bgpconnection import BGPConnectionTable
from ..forms.bgpconnection import BGPConnectionForm, BGPConnectionFilterForm
from ..filtersets.bgpconnection import BGPConnectionFilterSet
from ipam.choices import PrefixStatusChoices
from ipam.tables import PrefixTable
from ipam.models import Prefix
from django.db.models import Q


class BGPConnectionView(generic.ObjectView):
    # controls = []
    queryset = BGPConnection.objects.all()
    template_name = "netbox_cesnet_services_plugin/bgpconnection/bgpconnection.html"

    def get_extra_context(self, request, instance):
        if instance.bgp_prefix:
            parent_bgp_prefixes = (
                Prefix.objects.restrict(request.user, "view")
                .filter(Q(vrf=instance.bgp_prefix.vrf) | Q(vrf__isnull=True, status=PrefixStatusChoices.STATUS_CONTAINER))
                .filter(prefix__net_contains=str(instance.bgp_prefix))
                .prefetch_related(
                    "site",
                    "role",
                    "tenant",
                    "vlan",
                )
            )
            parent_bgp_prefix_table = PrefixTable(
                list(parent_bgp_prefixes), exclude=("vrf", "utilization"), orderable=False
            )
        else:
            parent_bgp_prefix_table = None

        return {
            "parent_prefix_table": parent_bgp_prefix_table,
        }


class BGPConnectionListView(generic.ObjectListView):
    queryset = BGPConnection.objects.all()
    table = BGPConnectionTable
    filterset = BGPConnectionFilterSet
    filterset_form = BGPConnectionFilterForm


class BGPConnectionEditView(generic.ObjectEditView):
    queryset = BGPConnection.objects.all()
    form = BGPConnectionForm


class BGPConnectionDeleteView(generic.ObjectDeleteView):
    queryset = BGPConnection.objects.all()
