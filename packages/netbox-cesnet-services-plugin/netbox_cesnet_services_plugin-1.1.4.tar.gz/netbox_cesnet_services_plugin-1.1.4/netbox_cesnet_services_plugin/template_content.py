from dcim.models import Device, Interface
from django.conf import settings
from django.db.models import F
from ipam.models import VRF, IPAddress, Prefix
from netbox.plugins import PluginTemplateExtension
from netbox.views import generic
from tenancy.models import Tenant
from utilities.views import ViewTab, register_model_view

from netbox_cesnet_services_plugin.filtersets import (
    BGPConnectionFilterSet,
    LLDPNeighborFilterSet,
    LLDPNeighborLeafFilterSet,
)
from netbox_cesnet_services_plugin.models import (
    BGPConnection,
    LLDPNeighbor,
    LLDPNeighborLeaf,
)
from netbox_cesnet_services_plugin.tables import (
    BGPConnectionTable,
    LLDPNeighborLeafTable,
    LLDPNeighborTable,
)

plugin_settings = settings.PLUGINS_CONFIG.get("netbox_cesnet_services_plugin", {})


class LLDPNeighborPluginTemplateExtension(PluginTemplateExtension):
    model = ""
    related_property = ""

    def get_page_position(self):
        return plugin_settings.get("lldp_ext_page", "")

    def left_page(self):
        return self.get_page() if self.get_page_position() == "left" else ""

    def right_page(self):
        return self.get_page() if self.get_page_position() == "right" else ""

    def full_width_page(self):
        return self.get_page() if self.get_page_position() == "full_width" else ""

    def get_page(self):
        related_object = self.context["object"]
        lldp_neighbors = LLDPNeighbor.objects.annotate(related_property=F(self.related_property)).filter(
            **{self.related_property: related_object.id}
        )
        lldp_neighbor_table = LLDPNeighborTable(lldp_neighbors)

        return self.render(
            "netbox_cesnet_services_plugin/lldpneighbor/lldpneighbor_include.html",
            extra_context={
                "lldpneighbors": lldp_neighbors,
                "related_session_table": lldp_neighbor_table,
            },
        )


class InterfaceLLDPNeighborList(LLDPNeighborPluginTemplateExtension):
    model = "dcim.interface"
    related_property = "interface_a"


class DeviceLLDPNeighborList(LLDPNeighborPluginTemplateExtension):
    model = "dcim.device"
    related_property = "device_a"


class BGPConnectionPluginTemplateExtension(PluginTemplateExtension):
    model = ""
    related_property = ""

    def get_page_position(self):
        return plugin_settings.get("bgp_ext_page", "")

    def left_page(self):
        return self.get_page() if self.get_page_position() == "left" else ""

    def right_page(self):
        return self.get_page() if self.get_page_position() == "right" else ""

    def full_width_page(self):
        return self.get_page() if self.get_page_position() == "full_width" else ""

    def get_page(self):
        related_object = self.context["object"]
        bgp_connections = BGPConnection.objects.annotate(related_property=F(self.related_property)).filter(
            **{self.related_property: related_object.id}
        )
        bgp_connection_table = BGPConnectionTable(bgp_connections)

        return self.render(
            "netbox_cesnet_services_plugin/bgpconnection/bgpconnection_include.html",
            extra_context={
                "bgpconnections": bgp_connections,
                "related_session_table": bgp_connection_table,
            },
        )


class TenantBGPConnectionList(BGPConnectionPluginTemplateExtension):
    model = "tenancy.tenant"
    related_property = "bgp_prefix__tenant"


class InterfaceBGPConnectionList(BGPConnectionPluginTemplateExtension):
    model = "dcim.interface"
    related_property = "next_hop__interface"


class IPAddressBGPConnectionList(BGPConnectionPluginTemplateExtension):
    model = "ipam.ipaddress"
    related_property = "next_hop"


class PrefixBGPConnectionList(BGPConnectionPluginTemplateExtension):
    model = "ipam.prefix"
    related_property = "bgp_prefix"


class DeviceBGPConnectionList(BGPConnectionPluginTemplateExtension):
    model = "dcim.device"
    related_property = "device"


class VRFBGPConnectionList(BGPConnectionPluginTemplateExtension):
    model = "ipam.vrf"
    related_property = "vrf"


template_extensions = [
    TenantBGPConnectionList,
    InterfaceBGPConnectionList,
    IPAddressBGPConnectionList,
    DeviceBGPConnectionList,
    PrefixBGPConnectionList,
    DeviceLLDPNeighborList,
    InterfaceLLDPNeighborList,
]


def create_lldpneighbor_tabview(model):
    """Creates attachment tab. Append it to the passed model

    Args:
        model (Object): Model representation
    """
    name = f"{model._meta.model_name}-lldpneighbors"
    path = f"{model._meta.model_name}-lldpneighbors"

    class View(generic.ObjectChildrenView):
        child_model = LLDPNeighbor
        filterset = LLDPNeighborFilterSet
        template_name = "netbox_cesnet_services_plugin/details/multiple_children.html"
        table = LLDPNeighborTable
        queryset = model.objects.all()
        if model == Device:
            tab = ViewTab(
                label="LLDP Neighbors",
                badge=lambda obj: LLDPNeighbor.objects.filter(device_a=obj.id).count(),
                permission="netbox_cesnet_services_plugin.view_lldpneighbor",
            )

            def get_children(self, request, parent):
                childrens = self.child_model.objects.filter(device_a=parent.id).restrict(request.user, "view")
                return childrens

            def get_extra_context(self, request, instance):
                data = LLDPNeighborLeaf.objects.filter(device_nb=instance.id)
                demo_table = LLDPNeighborLeafTable(data)
                return {
                    "demo_table": demo_table,
                }

        elif model == Interface:
            tab = ViewTab(
                label="LLDP Neighbors",
                badge=lambda obj: LLDPNeighbor.objects.filter(interface_a=obj.id).count(),
                permission="netbox_cesnet_services_plugin.view_lldpneighbor",
            )

            def get_children(self, request, parent):
                childrens = self.child_model.objects.filter(interface_a=parent.id).restrict(request.user, "view")
                return childrens

            def get_extra_context(self, request, instance):
                data = LLDPNeighborLeaf.objects.filter(interface_nb=instance.id)
                demo_table = LLDPNeighborLeafTable(data)
                return {
                    "demo_table": demo_table,
                }

    register_model_view(model, name=name, path=path)(View)


def create_bgpconnection_tabview(model):
    """Creates attachment tab. Append it to the passed model

    Args:
        model (Object): Model representation
    """
    name = f"{model._meta.model_name}-bgpconnections"
    path = f"{model._meta.model_name}-bgpconnections"

    class View(generic.ObjectChildrenView):
        child_model = BGPConnection
        filterset = BGPConnectionFilterSet
        template_name = "generic/object_children.html"
        table = BGPConnectionTable
        queryset = model.objects.all()
        if model == Tenant:
            tab = ViewTab(
                label="BGP Connections",
                badge=lambda obj: BGPConnection.objects.annotate(related_property=F("bgp_prefix__tenant"))
                .filter(bgp_prefix__tenant=obj.id)
                .count(),
                permission="netbox_cesnet_services_plugin.view_bgpconnection",
            )

            def get_children(self, request, parent):
                childrens = (
                    self.child_model.objects.annotate(related_property=F("bgp_prefix__tenant"))
                    .filter(bgp_prefix__tenant=parent.id)
                    .restrict(request.user, "view")
                )
                return childrens

        elif model == Device:
            tab = ViewTab(
                label="BGP Connections",
                badge=lambda obj: BGPConnection.objects.filter(device=obj.id).count(),
                permission="netbox_cesnet_services_plugin.view_bgpconnection",
            )

            def get_children(self, request, parent):
                childrens = self.child_model.objects.filter(device=parent.id).restrict(request.user, "view")
                return childrens

        elif model == IPAddress:
            tab = ViewTab(
                label="BGP Connections",
                badge=lambda obj: BGPConnection.objects.filter(next_hop=obj.id).count(),
                permission="netbox_cesnet_services_plugin.view_bgpconnection",
            )

            def get_children(self, request, parent):
                childrens = self.child_model.objects.filter(next_hop=parent.id).restrict(request.user, "view")
                return childrens

        elif model == Interface:
            tab = ViewTab(
                label="BGP Connections",
                badge=lambda obj: BGPConnection.objects.annotate(related_property=F("next_hop__interface"))
                .filter(next_hop__interface=obj.id)
                .count(),
                permission="netbox_cesnet_services_plugin.view_bgpconnection",
            )

            def get_children(self, request, parent):
                childrens = (
                    self.child_model.objects.annotate(related_property=F("next_hop__interface"))
                    .filter(next_hop__interface=parent.id)
                    .restrict(request.user, "view")
                )
                return childrens

        elif model == Prefix:
            tab = ViewTab(
                label="BGP Connections",
                badge=lambda obj: BGPConnection.objects.filter(bgp_prefix=obj.id).count(),
                permission="netbox_cesnet_services_plugin.view_bgpconnection",
            )

            def get_children(self, request, parent):
                childrens = self.child_model.objects.filter(bgp_prefix=parent.id).restrict(request.user, "view")
                return childrens

        elif model == VRF:
            tab = ViewTab(
                label="BGP Connections",
                badge=lambda obj: BGPConnection.objects.filter(vrf=obj.id).count(),
                permission="netbox_cesnet_services_plugin.view_bgpconnection",
            )

            def get_children(self, request, parent):
                childrens = self.child_model.objects.filter(vrf=parent.id).restrict(request.user, "view")
                return childrens

    register_model_view(model, name=name, path=path)(View)


# TODO: Change the tabview to a plugin setting
# Register the tabview for each model
if plugin_settings.get("bgp_ext_page", "tabview") == "tabview":
    for model in [Tenant, Device, IPAddress, Interface, Prefix, VRF]:
        create_bgpconnection_tabview(model)

if plugin_settings.get("lldp_ext_page", "tabview") == "tabview":
    for model in [Device, Interface]:
        create_lldpneighbor_tabview(model)
