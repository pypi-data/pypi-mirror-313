from django.db.models import Q
import django_filters
from extras.filters import TagFilter
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Device, Interface
from netbox_cesnet_services_plugin.models import LLDPNeighbor


class LLDPNeighborFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(method="search", label="Search")
    device_a = django_filters.ModelMultipleChoiceFilter(queryset=Device.objects.all())
    interface_a = django_filters.ModelMultipleChoiceFilter(queryset=Interface.objects.all())
    device_b = django_filters.ModelMultipleChoiceFilter(queryset=Device.objects.all())
    interface_b = django_filters.ModelMultipleChoiceFilter(queryset=Interface.objects.all())

    device_a_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device_a__id",
        queryset=Device.objects.all(),
        to_field_name="id",
        label="Device (ID)",
    )
    device_b_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device_b__id",
        queryset=Device.objects.all(),
        to_field_name="id",
        label="Device (ID)",
    )
    interface_a_id = django_filters.ModelMultipleChoiceFilter(
        field_name="interface_a__id",
        queryset=Interface.objects.all(),
        to_field_name="id",
        label="Interface (ID)",
    )
    interface_b_id = django_filters.ModelMultipleChoiceFilter(
        field_name="interface_b__id",
        queryset=Interface.objects.all(),
        to_field_name="id",
        label="Interface (ID)",
    )

    tag = TagFilter()

    class Meta:
        model = LLDPNeighbor
        fields = {
            "id",
            "device_a",
            "interface_a",
            "device_b",
            "interface_b",
            "status",
            "device_a_id",
            "device_b_id",
            "interface_a_id",
            "interface_b_id",
        }

    def search(self, queryset, name, value):
        filters = (
            Q(device_a__name__icontains=value)
            | Q(device_b__name__icontains=value)
            | Q(interface_a__name__icontains=value)
            | Q(interface_a__name__icontains=value)
        )

        return queryset.filter(filters)
