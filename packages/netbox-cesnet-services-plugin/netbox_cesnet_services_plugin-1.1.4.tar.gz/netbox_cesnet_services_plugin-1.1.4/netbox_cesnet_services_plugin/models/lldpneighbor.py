"""
device_a - @property a nebo before_save validace - domluvili jsem se na before_save
interface_a - foreing key na interface

remote_system_name_a - (@property a nebo validace na before_save) - domluvili jsme se na before save
pojmenovat se to asi může jako device_b (lepší analogie)
remote_interface_a - foreing key na interface - jméno interface_b (lepší analogie)

+  to samé pro b, přičemž z definice se interface_a == remote_interface_b a interface_b == remote_interface_a
   - Tady nám asi stačí vždy jen jedna strana - na směru v podstatě nezáleží.
    směr (a <-> b) == (b <-> a) - takže before_save validace na unikátnost záznamu
   - To by měl asi kontrolovat script pro import aby tam nebyla duplicita
   - Případně before_save validace, co zkontroluje, jestli ty data uz neexistuji

- imported_data - json, kde se budou ukládat data, která byla importována

ERRORS: netbox_cesnet_services_plugin.LLDPNeighbor.device_a: (fields.E304) Reverse
accessor 'Device.lldpneighbor_set' for 'netbox_cesnet_services_plugin.LLDPNeighbor.device_a'
clashes with reverse accessor for 'netbox_cesnet_services_plugin.LLDPNeighbor.device_b'. HINT: Add
or change a related_name argument to the definition
for 'netbox_cesnet_services_plugin.LLDPNeighbor.device_a'
or 'netbox_cesnet_services_plugin.LLDPNeighbor.device_b'.
netbox_cesnet_services_plugin.LLDPNeighbor.device_b:(fields.E304) Reverse
accessor 'Device.lldpneighbor_set' for 'netbox_cesnet_services_plugin.LLDPNeighbor.device_b'
clashes with reverse accessor for 'netbox_cesnet_services_plugin.LLDPNeighbor.device_a'. HINT: Add
or change a related_name argument to the definition
for 'netbox_cesnet_services_plugin.LLDPNeighbor.device_b'
or 'netbox_cesnet_services_plugin.LLDPNeighbor.device_a'.
netbox_cesnet_services_plugin.LLDPNeighbor.interface_a:(fields.E304) Reverse
accessor 'Interface.lldpneighbor_set' for 'netbox_cesnet_services_plugin.LLDPNeighbor.interface_a'
clashes with reverse accessor for 'netbox_cesnet_services_plugin.LLDPNeighbor.interface_b'. HINT:
Add or change a related_name argument to the definition
for 'netbox_cesnet_services_plugin.LLDPNeighbor.interface_a'
or 'netbox_cesnet_services_plugin.LLDPNeighbor.interface_b'.
netbox_cesnet_services_plugin.LLDPNeighbor.interface_b:(fields.E304) Reverse
accessor 'Interface.lldpneighbor_set' for 'netbox_cesnet_services_plugin.LLDPNeighbor.interface_b'
clashes with reverse accessor for 'netbox_cesnet_services_plugin.LLDPNeighbor.interface_a'. HINT:
Add or change a related_name argument to the definition
for 'netbox_cesnet_services_plugin.LLDPNeighbor.interface_b'
or 'netbox_cesnet_services_plugin.LLDPNeighbor.interface_a'.
"""

from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from netbox.models import NetBoxModel
from dcim.models import Interface, Device

from netbox_cesnet_services_plugin.choices import LLDPNeigborStatusChoices


class LLDPNeighbor(NetBoxModel):

    device_a = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        verbose_name=_("Device A"),
        help_text=_("Device A"),
        related_name="lldp_neighbors_device_a",
        null=False,
        blank=False,
    )
    interface_a = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        verbose_name=_("Interface A"),
        help_text=_("Interface A"),
        related_name="lldp_neighbors_interface_a",
        null=False,
        blank=False,
    )
    device_b = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        verbose_name=_("Device B"),
        help_text=_("Device B"),
        related_name="lldp_neighbors_device_b",
        null=False,
        blank=False,
    )
    interface_b = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        verbose_name=_("Interface B"),
        help_text=_("Interface B"),
        related_name="lldp_neighbors_interface_b",
        null=False,
        blank=False,
    )

    imported_data = JSONField(
        verbose_name=_("Imported Data"),
        help_text=_("Imported Data"),
        null=True,
        blank=True,
    )

    status = models.CharField(
        verbose_name=_('status'),
        max_length=50,
        choices=LLDPNeigborStatusChoices,
        default=LLDPNeigborStatusChoices.STATUS_ACTIVE,
    )

    comments = models.TextField(verbose_name=_("Comments"), blank=True)

    def get_absolute_url(self):
        return reverse(
            "plugins:netbox_cesnet_services_plugin:lldpneighbor", kwargs={"pk": self.pk}
        )

    class Meta:
        verbose_name = _("LLDP Neighbor")
        verbose_name_plural = _("LLDP Neighbors")
        ordering = ["device_a", "interface_a", "device_b", "interface_b"]
        unique_together = ["device_a", "interface_a", "device_b", "interface_b"]

    def __str__(self):
        return f"{self.device_a} - {self.interface_a} <-> {self.device_b} - {self.interface_b}"

    def clean(self):
        super().clean()

        validation_errors = {}
        if self.interface_a.device.id != self.device_a.id:
            validation_errors["device_a"] = _(
                "Interface A is not connected to Device A"
            )
        if self.interface_b.device.id != self.device_b.id:
            validation_errors["device_b"] = _(
                "Interface B is not connected to Device B"
            )

        if validation_errors:
            raise ValidationError(validation_errors)

    def get_status_color(self):
        return LLDPNeigborStatusChoices.colors.get(self.status)
