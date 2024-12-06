from dcim.models import Device, Interface
from django import forms
from ipam.models import VRF, IPAddress, Prefix
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from tenancy.models import Tenant
from utilities.forms.constants import BOOLEAN_WITH_BLANK_CHOICES
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)
from utilities.forms.rendering import FieldSet

from netbox_cesnet_services_plugin.models import BGPConnection, BGPConnectionChoices


class BGPConnectionForm(NetBoxModelForm):
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        label="Device",
        help_text="Device",
        selector=True,
    )
    raw_next_hop = forms.GenericIPAddressField(
        required=True,
        label="Next Hop IP Address",
        help_text="IPv4 or IPv6 address (without mask)",
    )
    next_hop = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=True,
        label="Next Hop Interface IP Address",
        help_text="Next Hop Interface IP Address",
        selector=True,
    )
    bgp_prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=True,
        label="BGP Prefix",
        help_text="BGP Prefix",
        selector=True,
    )
    comments = CommentField(required=False, label="Comments", help_text="Comments")

    fieldsets = (
        FieldSet("raw_next_hop", "raw_bgp_prefix", "raw_vrf", name="Raw Data"),
        FieldSet(
            "device", "next_hop", "bgp_prefix", "vrf", name="NetBox Related Objects"
        ),
        FieldSet("import_data", name="Imported Data"),
        FieldSet("role", "tags", name="Misc"),
    )

    class Meta:
        model = BGPConnection
        fields = (
            "device",
            "raw_next_hop",
            "next_hop",
            "raw_bgp_prefix",
            "bgp_prefix",
            "raw_vrf",
            "vrf",
            "role",
            "import_data",
            "comments",
            "tags",
        )


class BGPConnectionFilterForm(NetBoxModelFilterSetForm):
    model = BGPConnection

    # RAW
    raw_next_hop__ic = forms.CharField(
        required=False,
        label="Next Hop IP Address",
        help_text="IP Address | Treated as Char => contains",
    )
    raw_bgp_prefix__ic = forms.CharField(
        required=False,
        label="BGP Prefix",
        help_text="Prefix | Treated as CharField => contains",
    )
    raw_vrf = forms.CharField(
        required=False,
        label="VRF",
        help_text="VRF | Treated as CharField => contains",
    )

    # NetBox Related
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=("NetBox Device"),
        help_text="Device assigned to BGP Connection",
    )
    next_hop_interface_id = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        query_params={"device_id": "$device_id"},
        label="NetBox Interface",
        help_text="Interface assigned to Next Hop",
    )
    next_hop_id = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        query_params={"interface_id": "$next_hop_interface_id"},
        label="NetBox IP Address",
        help_text="IP Address assigned to Interface",
        # selector=True, # Selector does not work in FilterForm
    )
    bgp_prefix_id = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        label="NetBox Prefix",
        help_text="BGP Prefix ",
        # selector=True, # Selector does not work in FilterForm
    )
    bgp_prefix_tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label="NetBox Tenant",
        help_text="Tenant assigned to BGP Prefix",
    )
    vrf_id = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        label=("NetBox VRF"),
        help_text="VRF assigned to BGP Connection",
    )
    vrf_none = forms.NullBooleanField(
        required=False,
        label="Empty VRF",
        help_text="VRF is not assigned | VRF is None",
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    # Other
    tag = TagFilterField(model)
    role = forms.MultipleChoiceField(
        choices=BGPConnectionChoices, required=False, label="Role", help_text="Role"
    )

    fieldsets = (
        FieldSet("filter_id", "q"),
        FieldSet("raw_next_hop__ic", "raw_bgp_prefix__ic", "raw_vrf", name="Raw Data"),
        FieldSet(
            "device_id",
            "next_hop_interface_id",
            "next_hop_id",
            "bgp_prefix_id",
            "bgp_prefix_tenant_id",
            "vrf_id",
            "vrf_none",
            name="NetBox Related Objects",
        ),
        FieldSet("role", "tag", name="Misc"),
    )
