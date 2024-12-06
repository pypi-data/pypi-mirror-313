from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from netbox.models import NetBoxModel
from dcim.models import Interface, Device

from netbox_cesnet_services_plugin.choices import LLDPNeigborStatusChoices


class LLDPNeighborLeaf(NetBoxModel):
    """
    Leaf model for LLDP Neighbor is used to store LLDP information from Napalm
    when the other part of the connection is not in NetBox. This other part
    is called leaf.
    """

    device_nb = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        verbose_name=_("Device Netbox"),
        help_text=_("Device in NetBox"),
        related_name="lldp_neighbors_device_nb",
        null=False,
        blank=False,
    )
    interface_nb = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        verbose_name=_("Interface Netbox"),
        help_text=_("Interface in NetBox"),
        related_name="lldp_neighbors_interface_nb",
        null=False,
        blank=False,
    )
    device_ext = models.CharField(
        max_length=255,
        verbose_name=_("Device Ext"),
        help_text=_("External Device Name"),
        null=False,
        blank=False,
    )
    interface_ext = models.CharField(
        max_length=255,
        verbose_name=_("Interface Ext"),
        help_text=_("External Interface Name"),
        null=False,
        blank=False,
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=50,
        choices=LLDPNeigborStatusChoices,
        default=LLDPNeigborStatusChoices.STATUS_ACTIVE,
    )

    imported_data = JSONField(
        verbose_name=_("Imported Data"),
        help_text=_("Imported Data"),
        null=True,
        blank=True,
    )

    comments = models.TextField(verbose_name=_("Comments"), blank=True)

    def get_absolute_url(self):
        return reverse(
            "plugins:netbox_cesnet_services_plugin:lldpneighborleaf",
            kwargs={"pk": self.pk},
        )

    class Meta:
        verbose_name = _("LLDP Neighbor Leaf")
        verbose_name_plural = _("LLDP Neighbor Leafs")
        ordering = ["device_nb", "interface_nb", "device_ext", "interface_ext"]
        unique_together = ["device_nb", "interface_nb", "device_ext", "interface_ext"]

    def __str__(self):
        return f"{self.device_nb} - {self.interface_nb} <-> {self.device_ext} - {self.interface_ext}"

    def clean(self):
        super().clean()

        validation_errors = {}
        if self.interface_nb.device.id != self.device_nb.id:
            validation_errors["device_nb"] = _(
                "Interface is not connected to Device in NetBox"
            )

        if validation_errors:
            raise ValidationError(validation_errors)

    def get_status_color(self):
        return LLDPNeigborStatusChoices.colors.get(self.status)
