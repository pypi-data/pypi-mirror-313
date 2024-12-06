import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Device, Interface
from netbox_cesnet_services_plugin.models import LLDPNeighborLeaf


class LLDPNeighborLeafFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(method="search", label="Search")
    device_nb = django_filters.ModelMultipleChoiceFilter(queryset=Device.objects.all())
    interface_nb = django_filters.ModelMultipleChoiceFilter(queryset=Interface.objects.all())

    class Meta:
        model = LLDPNeighborLeaf
        fields = {"id", "device_nb", "interface_nb", "device_ext", "interface_ext", "status"}

    def search(self, queryset, name, value):
        filters = (
            Q(device_nb__name__icontains=value)
            | Q(interface_nb__name__icontains=value)
            | Q(device_ext__icontains=value)
            | Q(interface_ext__icontains=value)
        )

        return queryset.filter(filters)
