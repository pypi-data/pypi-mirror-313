from netbox.api.routers import NetBoxRouter

from . import views

app_name = 'netbox_cesnet_services_plugin'
router = NetBoxRouter()
router.register('bgp-connections', views.BGPConnectionViewSet)
router.register('lldp-neighbors', views.LLDPNeighborViewSet)
router.register('lldp-neighbor-leafs', views.LLDPNeighborLeafViewSet)

urlpatterns = router.urls