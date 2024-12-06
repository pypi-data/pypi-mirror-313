"""Top-level package for NetBox cesnet_services Plugin."""

__author__ = """Jan Krupa"""
__email__ = "jan.krupa@cesnet.cz"
__version__ = "0.1.0"


from netbox.plugins import PluginConfig


class CesnetServicesConfig(PluginConfig):
    name = "netbox_cesnet_services_plugin"
    verbose_name = "NetBox cesnet_services Plugin"
    description = "NetBox plugin for cesnet_services."
    version = __version__
    base_url = "netbox-cesnet-services-plugin"


config = CesnetServicesConfig
