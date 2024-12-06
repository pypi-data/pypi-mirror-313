import django_filters
from dcim.models import Device, Interface
from django.db.models import Q
from django.utils.translation import gettext as _
from extras.filters import TagFilter
from ipam.models import VRF, IPAddress, Prefix
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.models import Tenant
from utilities.forms.fields import DynamicMultipleChoiceField

from netbox_cesnet_services_plugin.models import BGPConnection, BGPConnectionChoices


class BGPConnectionFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(method="search", label="Search")
    device = django_filters.ModelMultipleChoiceFilter(queryset=Device.objects.all())
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device__id",
        queryset=Device.objects.all(),
        to_field_name="id",
        label="Device (ID)",
    )
    next_hop = django_filters.ModelMultipleChoiceFilter(queryset=IPAddress.objects.all())
    next_hop_id = django_filters.ModelMultipleChoiceFilter(
        field_name="next_hop__id",
        queryset=IPAddress.objects.all(),
        to_field_name="id",
        label="Next Hop (ID)",
    )

    next_hop_interface_id = django_filters.ModelMultipleChoiceFilter(
        field_name="next_hop__interface__id",
        queryset=Interface.objects.all(),
        to_field_name="id",
        label="Next Hop Interface (ID)",
    )
    bgp_prefix = django_filters.ModelMultipleChoiceFilter(queryset=Prefix.objects.all())
    bgp_prefix_id = django_filters.ModelMultipleChoiceFilter(
        field_name="bgp_prefix__id",
        queryset=Prefix.objects.all(),
        to_field_name="id",
        label="BGP Prefix (ID)",
    )
    bgp_prefix_tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name="bgp_prefix__tenant__id",
        queryset=Tenant.objects.all(),
        to_field_name="id",
        label="BGP Prefix Tenant (ID)",
    )
    vrf = django_filters.ModelMultipleChoiceFilter(queryset=VRF.objects.all())
    vrf_id = django_filters.ModelMultipleChoiceFilter(
        field_name="vrf__id",
        queryset=VRF.objects.all(),
        to_field_name="id",
        label="VRF (ID)",
    )
    vrf_none = django_filters.BooleanFilter(method="_vrf_none", label="Empty VRF")

    # TODO: as CHAR filter or as IPAddress filter?
    raw_next_hop = django_filters.CharFilter(
        # method='filter_address',
        label=_("Address"),
    )
    raw_bgp_prefix = django_filters.CharFilter(
        # method='filter_prefix',
        label=_("Prefix"),
    )
    raw_vrf = django_filters.CharFilter(
        label=_("VRF"),
    )

    role = DynamicMultipleChoiceField(choices=BGPConnectionChoices, required=False)

    tag = TagFilter()

    class Meta:
        model = BGPConnection
        fields = [
            "raw_next_hop",
            "next_hop",
            "bgp_prefix",
            "raw_vrf",
            "vrf",
            "role",
            "tag",
        ]

    def search(self, queryset, name, value):
        filters = (
            Q(device__name=value)
            | Q(raw_next_hop__icontains=value)
            | Q(raw_bgp_prefix__icontains=value)
            | Q(bgp_prefix__tenant__name__icontains=value)
            | Q(raw_vrf__icontains=value)
            | Q(vrf__name__icontains=value)
            | Q(role__icontains=value)
        )

        return queryset.filter(filters)

    def _vrf_none(self, queryset, name, value):
        if value:
            return queryset.filter(vrf=None)
        else:
            return queryset.filter(vrf__isnull=False)

    # TODO: Filter `raw`` Address and Prefix with netaddr or treat it like a string?
    """
    def filter_address(self, queryset, name, value):
        # Let's first parse the addresses passed
        # as argument. If they are all invalid,
        # we return an empty queryset
        # TODO: Use Netaddr or ipaddress module
        value = self.parse_inet_addresses(value)
        if len(value) == 0:
            return queryset.none()
        try:
            return queryset.filter(address__net_in=value)
        except ValidationError:
            return queryset.none()

    def filter_prefix(self, queryset, name, value):
        query_values = []
        for v in value:
            try:
                query_values.append(netaddr.IPNetwork(v))
            except (AddrFormatError, ValueError):
                pass
        return queryset.filter(prefix__in=query_values)
    """
