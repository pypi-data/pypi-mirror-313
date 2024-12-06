import django_tables2 as tables
from netbox.tables import NetBoxTable, columns


from netbox_cesnet_services_plugin.models import LLDPNeighbor


class LLDPNeighborTable(NetBoxTable):
    device_a = tables.RelatedLinkColumn(verbose_name="Device A")
    interface_a = tables.RelatedLinkColumn(verbose_name="Interface A")
    device_b = tables.RelatedLinkColumn(verbose_name="Device B")
    interface_b = tables.RelatedLinkColumn(verbose_name="Interface B")
    status = columns.ChoiceFieldColumn()
    imported_data = tables.JSONColumn()
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = LLDPNeighbor
        fields = (
            "pk",
            "id",
            "device_a",
            "interface_a",
            "device_b",
            "interface_b",
            "status",
            "imported_data",
            "tags",
            "actions",
        )
        default_columns = (
            "id",
            "device_a",
            "interface_a",
            "device_b",
            "interface_b",
            "status",
        )
