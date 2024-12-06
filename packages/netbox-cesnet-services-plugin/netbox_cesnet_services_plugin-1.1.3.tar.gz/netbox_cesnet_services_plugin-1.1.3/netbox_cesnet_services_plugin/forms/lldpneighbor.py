from dcim.models import Device, Interface
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from django.forms import ChoiceField
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from netbox_cesnet_services_plugin.models import LLDPNeighbor
from utilities.forms.rendering import FieldSet
from netbox.plugins import get_plugin_config

from netbox_cesnet_services_plugin.choices import LLDPNeigborStatusChoices


class LLDPNeighborForm(NetBoxModelForm):
    device_a = DynamicModelChoiceField(
        queryset=Device.objects.filter(status="active"),
        required=True,
        query_params={
            "has_primary_ip": True,
            "platform": get_plugin_config("netbox_cesnet_services_plugin", "platforms"),
        },
        label="Device A",
        help_text="Device A",
        selector=True,
    )
    interface_a = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=True,
        query_params={"device_id": "$device_a"},
        label="Interface A",
        help_text="Interface A",
        selector=True,
    )
    device_b = DynamicModelChoiceField(
        queryset=Device.objects.filter(status="active"),
        required=True,
        query_params={
            "has_primary_ip": True,
            "platform": get_plugin_config("netbox_cesnet_services_plugin", "platforms"),
        },
        label="Device B",
        help_text="Device B",
        selector=True,
    )
    interface_b = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=True,
        query_params={"device_id": "$device_b"},
        label="Interface B",
        help_text="Interface B",
        selector=True,
    )

    status = ChoiceField(
        label=('Status'),
        choices=LLDPNeigborStatusChoices,
        required=False
    )

    comments = CommentField(required=False, label="Comments", help_text="Comments")

    fieldsets = (
        FieldSet(
            "device_a",
            "interface_a",
            "device_b",
            "interface_b",
            "status",
            name="NetBox Related Objects",
        ),
        FieldSet("imported_data", name="Imported Data"),
        FieldSet("tags", name="Misc"),
    )

    class Meta:
        model = LLDPNeighbor
        fields = (
            "device_a",
            "interface_a",
            "device_b",
            "interface_b",
            "status",
            "imported_data",
            "comments",
            "tags",
        )


class LLDPNeighborFilterForm(NetBoxModelFilterSetForm):
    model = LLDPNeighbor

    device_a = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device A",
    )
    interface_a = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        label="Interface A",
    )
    device_b = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device B",
    )
    interface_b = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        label="Interface B",
    )

    status = ChoiceField(
        label=('Status'),
        choices=LLDPNeigborStatusChoices,
        required=False
    )

    fieldsets = (
        FieldSet("filter_id", "q"),
        FieldSet(
            "device_a",
            "interface_a",
            "device_b",
            "interface_b",
            "status",
            name="NetBox Related Objects",
        ),
    )
