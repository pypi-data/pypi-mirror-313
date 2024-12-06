import django_tables2 as tables
from netbox.tables import NetBoxTable, columns, ChoiceFieldColumn
from django.db.models import F

from netbox_cesnet_services_plugin.models import BGPConnection


class BGPConnectionTable(NetBoxTable):
    device = tables.RelatedLinkColumn(verbose_name="Device")
    raw_next_hop = tables.Column(verbose_name="Raw Next Hop")
    next_hop = tables.RelatedLinkColumn(verbose_name="Next Hop")
    next_hop_interface = tables.Column(
        orderable=True, linkify=True, verbose_name="Next Hop Interface"
    )
    raw_bgp_prefix = tables.Column(verbose_name="Raw BGP Prefix")
    bgp_prefix = tables.RelatedLinkColumn(verbose_name="BGP Prefix")
    bgp_prefix_tenant = tables.Column(
        orderable=True, linkify=True, verbose_name="BGP Prefix Tenant"
    )
    raw_vrf = tables.Column(verbose_name="Raw VRF")
    vrf = tables.RelatedLinkColumn(verbose_name="VRF")
    role = ChoiceFieldColumn(orderable=True, linkify=True, verbose_name="Role")
    import_data = tables.JSONColumn()
    tags = columns.TagColumn()

    def order_next_hop_interface(self, queryset, is_descending):
        queryset = queryset.annotate(
            next_hop__interface__name=F("next_hop__interface__name")
        ).order_by(("-" if is_descending else "") + "next_hop__interface__name")
        return (queryset, True)

    def order_bgp_prefix_tenant(self, queryset, is_descending):
        queryset = queryset.annotate(
            bgp_prefix__tenant__name=F("bgp_prefix__tenant__name")
        ).order_by(("-" if is_descending else "") + "bgp_prefix__tenant__name")
        return (queryset, True)

    class Meta(NetBoxTable.Meta):
        model = BGPConnection
        fields = (
            "pk",
            "id",
            "device",
            "raw_next_hop",
            "next_hop",
            "next_hop_interface",
            "raw_bgp_prefix",
            "bgp_prefix",
            "bgp_prefix_tenant",
            "raw_vrf",
            "vrf",
            "role",
            "actions",
        )
        default_columns = (
            "id",
            "device",
            "next_hop_interface",
            "next_hop",
            "bgp_prefix",
            "bgp_prefix_tenant",
            "vrf",
            "role",
        )
