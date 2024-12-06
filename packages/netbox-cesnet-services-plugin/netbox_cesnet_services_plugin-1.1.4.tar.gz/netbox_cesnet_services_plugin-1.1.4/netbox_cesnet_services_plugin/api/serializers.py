from ipam.api.serializers import IPAddressSerializer, PrefixSerializer, VRFSerializer
from dcim.api.serializers import DeviceSerializer, InterfaceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from netbox_cesnet_services_plugin.models import BGPConnection, LLDPNeighbor, LLDPNeighborLeaf




class LLDPNeighborLeafSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_cesnet_services_plugin-api:lldpneighborleaf-detail"
    )
    device_nb = DeviceSerializer(nested=True)
    interface_nb = InterfaceSerializer(nested=True)
    
    class Meta:
        model = LLDPNeighborLeaf
        fields = (
            "id",
            "url",
            "device_nb",
            "interface_nb",
            "device_ext",
            "interface_ext",
            "status",
            "comments",
            "tags",
            "imported_data",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "device_nb",
            "interface_nb",
            "device_ext",
            "interface_ext",
            "status",
        )



class LLDPNeighborSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_cesnet_services_plugin-api:lldpneighbor-detail"
    )
    device_a = DeviceSerializer(nested=True)
    interface_a = InterfaceSerializer(nested=True)
    device_b = DeviceSerializer(nested=True)
    interface_b = InterfaceSerializer(nested=True)

    class Meta:
        model = LLDPNeighbor
        fields = (
            "id",
            "url",
            "device_a",
            "interface_a",
            "device_b",
            "interface_b",
            "status",
            "comments",
            "tags",
            "imported_data",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "device_a",
            "interface_a",
            "device_b",
            "interface_b",
            "status",
        )


class BGPConnectionSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_cesnet_services_plugin-api:bgpconnection-detail"
    )
    device = DeviceSerializer(nested=True)
    next_hop = IPAddressSerializer(nested=True, allow_null=True)
    bgp_prefix = PrefixSerializer(nested=True, allow_null=True)
    vrf = VRFSerializer(nested=True, allow_null=True)

    class Meta:
        model = BGPConnection
        fields = (
            "id",
            "display",
            "url",
            "device",
            "raw_next_hop",
            "next_hop",
            "raw_bgp_prefix",
            "bgp_prefix",
            "raw_vrf",
            "vrf",
            "role",
            "tags",
            "import_data",
            "custom_fields",
            "created",
            "last_updated",
            "tags",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "device",
            "raw_next_hop",
            "next_hop",
            "raw_bgp_prefix",
            "bgp_prefix",
            "raw_vrf",
            "vrf",
            "role",
            "tags",
        )
