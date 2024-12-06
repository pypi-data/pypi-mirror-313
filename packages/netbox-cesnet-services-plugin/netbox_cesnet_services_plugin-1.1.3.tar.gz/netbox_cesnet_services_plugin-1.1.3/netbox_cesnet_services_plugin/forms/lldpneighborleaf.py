from dcim.models import Device, Interface
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from django.forms import CharField, ChoiceField
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from netbox_cesnet_services_plugin.models import LLDPNeighborLeaf
from utilities.forms.rendering import FieldSet
from netbox.plugins import get_plugin_config

from netbox_cesnet_services_plugin.choices import LLDPNeigborStatusChoices


class LLDPNeighborLeafForm(NetBoxModelForm):
    device_nb = DynamicModelChoiceField(
        queryset=Device.objects.filter(status="active"),
        required=True,
        query_params={
            "has_primary_ip": True,
            "platform": get_plugin_config("netbox_cesnet_services_plugin", "platforms"),
        },
        label="Device Netbox",
        help_text="Device in NetBox",
        selector=True,
    )
    interface_nb = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=True,
        query_params={"device_id": "$device_nb"},
        label="Interface Netbox",
        help_text="Interface in NetBox",
        selector=True,
    )
    device_ext = CharField(
        required=True,
        label="Device outside Netbox",
        help_text="Device outside Netbox",
        max_length=255,
    )
    interface_b = CharField(
        required=True,
        label="Interface outside Netbox",
        help_text="Interface outside Netbox",
        max_length=255,
    )

    status = ChoiceField(
        label=('Status'),
        choices=LLDPNeigborStatusChoices,
        required=False
    )

    comments = CommentField(required=False, label="Comments", help_text="Comments")

    fieldsets = (
        FieldSet("device_nb", "interface_nb", name="NetBox Related Objects"),
        FieldSet("device_ext", "interface_ext", name="External Objects"),
        FieldSet("status", name="Status"),
        FieldSet("imported_data", name="Imported Data"),
        FieldSet("tags", name="Misc"),
    )

    class Meta:
        model = LLDPNeighborLeaf
        fields = (
            "device_nb",
            "interface_nb",
            "device_ext",
            "interface_ext",
            "imported_data",
            "comments",
            "tags",
        )


class LLDPNeighborLeafFilterForm(NetBoxModelFilterSetForm):
    model = LLDPNeighborLeaf

    device_nb = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device Netbox",
    )
    interface_nb = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        label="Interface Netbox",
    )
    device_ext = CharField(
        required=False,
        label="Device External",
    )
    interface_ext = CharField(
        required=False,
        label="Interface External",
    )

    status = ChoiceField(
        label=('Status'),
        choices=LLDPNeigborStatusChoices,
        required=False
    )

    fieldsets = (
        FieldSet("device_nb", "interface_nb", name="NetBox Related Objects"),
        FieldSet("device_ext", "interface_ext", name="External Objects"),
        FieldSet("status", name="Status"),
    )
