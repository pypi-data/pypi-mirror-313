from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from netbox_cesnet_services_plugin.views.bgpconnection import (
    BGPConnectionDeleteView,
    BGPConnectionEditView,
    BGPConnectionListView,
    BGPConnectionView,
)
from netbox_cesnet_services_plugin.views.lldpneighbor import (
    LLDPNeighborDeleteView,
    LLDPNeighborEditView,
    LLDPNeighborListView,
    LLDPNeigborView,
    LLDPNeighborBulkDeleteView,
)
from netbox_cesnet_services_plugin.views.lldpneighborleaf import (
    LLDPNeighborLeafDeleteView,
    LLDPNeighborLeafEditView,
    LLDPNeighborLeafListView,
    LLDPNeigborLeafView,
    LLDPNeighborLeafBulkDeleteView,
)
from netbox_cesnet_services_plugin.models import BGPConnection, LLDPNeighbor


urlpatterns = (
    path(
        "bgp-connections/", BGPConnectionListView.as_view(), name="bgpconnection_list"
    ),
    path(
        "bgp-connections/add/",
        BGPConnectionEditView.as_view(),
        name="bgpconnection_add",
    ),
    path(
        "bgp-connections/<int:pk>/", BGPConnectionView.as_view(), name="bgpconnection"
    ),
    path(
        "bgp-connections/<int:pk>/edit/",
        BGPConnectionEditView.as_view(),
        name="bgpconnection_edit",
    ),
    path(
        "bgp-connections/<int:pk>/delete/",
        BGPConnectionDeleteView.as_view(),
        name="bgpconnection_delete",
    ),
    path(
        "bgp-connections/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(
            base_template="netbox_cesnet_services_plugin/bgpconnection/bgpconnection.html"
        ),
        name="bgpconnection_changelog",
        kwargs={"model": BGPConnection},
    ),
    path("lldp-neighbors/", LLDPNeighborListView.as_view(), name="lldpneighbor_list"),
    path(
        "lldp-neighbors/add/",
        LLDPNeighborEditView.as_view(),
        name="lldpneighbor_add",
    ),
    path("lldp-neighbors/<int:pk>/", LLDPNeigborView.as_view(), name="lldpneighbor"),
    path(
        "lldp-neighbors/<int:pk>/edit/",
        LLDPNeighborEditView.as_view(),
        name="lldpneighbor_edit",
    ),
    path(
        "lldp-neighbors/<int:pk>/delete/",
        LLDPNeighborDeleteView.as_view(),
        name="lldpneighbor_delete",
    ),
    path(
        "lldp-neighbors/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(
            base_template="netbox_cesnet_services_plugin/lldpneighbor/lldpneighbor.html"
        ),
        name="lldpneighbor_changelog",
        kwargs={"model": LLDPNeighbor},
    ),
    path("lldp-neighbors/delete/",
         LLDPNeighborBulkDeleteView.as_view(),
         name="lldpneighbor_bulk_delete",
    ),
    path("lldp-neighbor-leafs/", LLDPNeighborLeafListView.as_view(), name="lldpneighborleaf_list"),
    path(
        "lldp-neighbor-leafs/add/",
        LLDPNeighborLeafEditView.as_view(),
        name="lldpneighborleaf_add",
    ),
    path("lldp-neighbor-leafs/<int:pk>/", LLDPNeigborLeafView.as_view(), name="lldpneighborleaf"),
    path(
        "lldp-neighbor-leafs/<int:pk>/edit/",
        LLDPNeighborLeafEditView.as_view(),
        name="lldpneighborleaf_edit",
    ),
    path(
        "lldp-neighbor-leafs/<int:pk>/delete/",
        LLDPNeighborLeafDeleteView.as_view(),
        name="lldpneighborleaf_delete",
    ),
    path(
        "lldp-neighbor-leafs/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(
            base_template="netbox_cesnet_services_plugin/lldpneighborleaf/lldpneighborleaf.html"
        ),
        name="lldpneighborleaf_changelog",
        kwargs={"model": LLDPNeighbor},
    ),
    path("lldp-neighbor-leafs/delete/",
         LLDPNeighborLeafBulkDeleteView.as_view(),
         name="lldpneighborleaf_bulk_delete",)     
)
