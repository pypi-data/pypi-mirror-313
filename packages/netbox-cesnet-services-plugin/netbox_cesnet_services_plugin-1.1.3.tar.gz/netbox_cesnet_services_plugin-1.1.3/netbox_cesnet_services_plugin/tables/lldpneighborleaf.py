import django_tables2 as tables
from netbox.tables import NetBoxTable, columns


from netbox_cesnet_services_plugin.models import LLDPNeighborLeaf


class LLDPNeighborLeafTable(NetBoxTable):
    device_nb = tables.RelatedLinkColumn(verbose_name="Device Netbox ")
    interface_nb = tables.RelatedLinkColumn(verbose_name="Interface Netbox")
    device_ext = tables.Column(verbose_name="Device outside Netbox")
    interface_ext = tables.Column(verbose_name="Interface outside Netbox")
    status = columns.ChoiceFieldColumn()
    imported_data = tables.JSONColumn()
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = LLDPNeighborLeaf
        fields = (
            "pk",
            "id",
            "device_nb",
            "interface_nb",
            "device_ext",
            "interface_ext",
            "status",
            "imported_data",
            "tags",
            "actions",
        )
        default_columns = (
            "id",
            "device_nb",
            "interface_nb",
            "device_ext",
            "interface_ext",
            "status",
        )
