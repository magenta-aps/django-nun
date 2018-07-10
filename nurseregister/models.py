from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords


def timezoned_date():
    return timezone.now().date()


class NurseRegistration(models.Model):

    class Meta:
        verbose_name = _(u"sygeplejerskeautorisation")
        verbose_name_plural = _(u"sygeplejerskeautorisationer")

    name = models.CharField(
        verbose_name=_(u"Navn"),
        max_length=2048,
        blank=True,
    )

    number = models.CharField(
        verbose_name=_(u"Aut. Nr."),
        max_length=256,
        blank=True,
    )

    birthday = models.DateField(
        verbose_name=_(u"Fødselsdato"),
        blank=True,
        null=True
    )

    STATE_VALID = 1
    STATE_INVALID = 0

    state_choices = (
        (STATE_VALID, _(u"Gyldig")),
        (STATE_INVALID, _("Ugyldig")),
    )

    state = models.IntegerField(
        verbose_name=_(u"Aut. Status"),
        choices=state_choices,
        default=STATE_VALID,
    )

    date = models.DateField(
        verbose_name=_(u"Aut. Dato"),
        default=timezoned_date
    )

    history = HistoricalRecords()

    def __str__(self):
        return "%s (%s), %s siden %s" % (
            self.name,
            self.birthday,
            self.get_state_display().lower(),
            self.date
        )
