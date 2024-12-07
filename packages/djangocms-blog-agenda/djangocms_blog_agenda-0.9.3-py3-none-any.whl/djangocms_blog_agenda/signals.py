from datetime import timedelta

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now

from djangocms_blog_agenda.models import PostExtension

from .conf import settings as local_settings
from .utils import is_infinite_recurrence


@receiver(pre_save, sender=PostExtension)
def fill_recurrences_end_date(sender, instance, **kwargs):
    dtstart = instance.event_start_date
    if is_infinite_recurrence(instance.recurrences):
        instance.recurrences_end_date = None
    elif instance.recurrences.count() > 0:
        dtend = now() + timedelta(days=local_settings.RECURRENCE_MAX_DAYS_SEARCH)
        instance.recurrences_end_date = list(
            instance.recurrences.between(dtstart, dtend, dtstart=dtstart)
        )[::-1][0]
