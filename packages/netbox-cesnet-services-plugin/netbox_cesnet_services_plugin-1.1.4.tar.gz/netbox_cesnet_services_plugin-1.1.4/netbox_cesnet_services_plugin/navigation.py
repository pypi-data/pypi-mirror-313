from netbox.plugins import PluginMenu, PluginMenuItem


menu = PluginMenu(
    label='Cesnet Services',
    icon_class="mdi mdi-shovel-off",
    groups=(
        ("Connections", (
            PluginMenuItem(
                link="plugins:netbox_cesnet_services_plugin:bgpconnection_list",
                link_text="BGP Connections",
                permissions=['netbox_cesnet_services_plugin.view_bgpconnection']
            ),
            PluginMenuItem(
                link="plugins:netbox_cesnet_services_plugin:lldpneighbor_list",
                link_text="LLDP Neighbors",
                permissions=['netbox_cesnet_services_plugin.view_lldpneighbor']
            ),
            PluginMenuItem(
                link="plugins:netbox_cesnet_services_plugin:lldpneighborleaf_list",
                link_text="LLDP Neighbor Leafs",
                permissions=['netbox_cesnet_services_plugin.view_lldpneighborleaf']
            ),
        )),
    ),
)
