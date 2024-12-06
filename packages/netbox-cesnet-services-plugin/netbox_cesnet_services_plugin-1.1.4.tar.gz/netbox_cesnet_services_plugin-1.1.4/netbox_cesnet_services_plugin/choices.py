from utilities.choices import ChoiceSet
from django.utils.translation import gettext_lazy as _

class LLDPNeigborStatusChoices(ChoiceSet):

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    
    CHOICES = (
        (STATUS_ACTIVE, _('Active'), 'green'),
        (STATUS_INACTIVE, _('Inactive'), 'yellow'),
    )
