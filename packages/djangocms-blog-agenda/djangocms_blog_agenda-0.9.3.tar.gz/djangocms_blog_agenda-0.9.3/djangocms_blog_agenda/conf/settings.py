from django.conf import settings
from django.utils.translation import gettext_lazy as _


DEFAULT_HIDE_UPCOMING_EVENTS_AFTER_CHOICES = (
    ("start", _("just after event start date")),
    ("start+1h", _("1 hour after event start date")),
    ("start+4h", _("4 hours after event start date")),
    ("start+1d", _("1 day after event start date")),
    ("start+2d", _("2 days after event start date")),
    ("start+3d", _("3 days after event start date")),
    ("start+7d", _("7 days after event start date")),
    ("end", _("just after event end date")),
)

HIDE_UPCOMING_EVENTS_AFTER_CHOICES = getattr(
    settings,
    "DJANGOCMS_BLOG_AGENDA_HIDE_UPCOMING_EVENTS_AFTER_CHOICES",
    DEFAULT_HIDE_UPCOMING_EVENTS_AFTER_CHOICES,
)

RECURRENCE_MAX_DAYS_SEARCH = getattr(
    settings, "DJANGOCMS_BLOG_AGENDA_RECURRENCE_MAX_DAYS_SEARCH", 365
)
