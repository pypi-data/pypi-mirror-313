from django.db import models
from django.urls import reverse
from django.db.models import JSONField, GenericIPAddressField
from django.utils.translation import gettext_lazy as _

from netbox.models import NetBoxModel
from ipam.models import IPAddress, Prefix, VRF
from dcim.models import Device
from ipam.fields import IPNetworkField
from utilities.choices import ChoiceSet


class BGPConnectionChoices(ChoiceSet):
    key = "BGPConnection.role"

    CHOICES = [
        ("none", "None", "blue"),
        ("vrf", "VRF", "orange"),
    ]


class BGPConnection(NetBoxModel):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        verbose_name=_("Device"),
        help_text=_("Device"),
        null=False,
        blank=False,
    )
    raw_next_hop = GenericIPAddressField(
        help_text=_("IPv4 or IPv6 address (with mask)"),
        null=False,
        blank=False,
        verbose_name=_("Raw Next Hop"),
    )
    next_hop = models.ForeignKey(
        IPAddress,
        on_delete=models.CASCADE,
        verbose_name=_("Next Hop"),
        help_text=_("Next Hop"),
        null=True,
        blank=True,
    )
    raw_bgp_prefix = IPNetworkField(
        null=False,
        blank=False,
        verbose_name=_("Raw BGP Prefix"),
    )
    bgp_prefix = models.ForeignKey(
        Prefix,
        on_delete=models.CASCADE,
        related_name="bgp_prefix",
        verbose_name=_("BGP Prefix"),
        help_text=_("BGP Prefix"),
        null=True,
        blank=True,
    )
    raw_vrf = models.CharField(
        max_length=255,
        null=False,
        blank=True,
        verbose_name=_("Raw VRF"),
        default="",
    )
    vrf = models.ForeignKey(
        VRF,
        on_delete=models.CASCADE,
        verbose_name=_("VRF"),
        help_text=_("VRF"),
        null=True,
        blank=True,
    )
    role = models.CharField(
        max_length=255,
        choices=BGPConnectionChoices,
        default="none",  # BGPConnectionChoices.default,
        verbose_name=_("Role"),
        help_text=_("Role"),
        null=False,
        blank=False,
    )
    import_data = JSONField(
        blank=True,
        null=True,
        verbose_name=_("Imported Data"),
    )
    comments = models.TextField(verbose_name=_("Comments"), blank=True)

    @property
    def next_hop_interface(self):
        if (
            self.next_hop
            and f"{self.next_hop.assigned_object_type.app_label}.{self.next_hop.assigned_object_type.model}"
            == "dcim.interface"
        ):
            return self.next_hop.assigned_object
        return None

    @property
    def bgp_prefix_tenant(self):
        if self.bgp_prefix.tenant:
            return self.bgp_prefix.tenant
        return None

    class Meta:
        ordering = ("device", "bgp_prefix", "raw_next_hop", "role", "vrf")
        unique_together = ["device", "raw_next_hop",
                           "raw_bgp_prefix", "raw_vrf"]

    def __str__(self):
        if self.vrf:
            return f"{self.device.name} - {self.raw_next_hop} - {self.raw_bgp_prefix} - {self.vrf.name}"
        else:
            return f"{self.device.name} - {self.raw_next_hop} - {self.raw_bgp_prefix}"

    def get_absolute_url(self):
        return reverse(
            "plugins:netbox_cesnet_services_plugin:bgpconnection", args=[self.pk]
        )

    def get_role_color(self):
        return BGPConnectionChoices.colors.get(self.role)
