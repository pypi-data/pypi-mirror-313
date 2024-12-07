from datetime import timedelta
import re

from django.db import models
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from djangocms_blog.models import BasePostPlugin, BlogCategory, LatestPostsPlugin, Post
from djangocms_blog.settings import get_setting
from recurrence.fields import RecurrenceField
from taggit_autosuggest.managers import TaggableManager

from .conf import settings as local_settings
from .utils import add_recurrent_posts, upcoming_events_query


class PostExtension(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="extension")
    event_start_date = models.DateTimeField(verbose_name=_("Event start"))
    event_end_date = models.DateTimeField(
        verbose_name=_("Event end"),
        null=True,
        blank=True,
        help_text=_("If the event is held over several days"),
    )
    # This field only contains occurrences following the initial event.
    # We have to handle this every time we need to retrieve all occurrences.
    recurrences = RecurrenceField(include_dtstart=False, null=True, blank=True)

    # This field is filled on post save signal with the date of the last occurrence
    # or left blank if the recurrence is infinite
    recurrences_end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _("Event infos")
        verbose_name_plural = _("Events infos")

    def __str__(self):
        return _("Event infos") + " (#" + str(self.id) + ")"

    def get_next_occurrence(self):
        """Returns only futur occurrences of the event, including the initial event."""
        initial_event_date = self.event_start_date

        # The next occurrence from now.
        next_occurrence_date = self.recurrences.after(
            now(), inc=True, dtstart=self.event_start_date
        )

        # If the initial event is in the futur, it is the next occurrence.
        if initial_event_date >= now():
            return initial_event_date
        return next_occurrence_date

    @cached_property
    def occurrences(self) -> list:
        """Returns all occurrences of the event (past and futur), including the initial event."""
        if self.recurrences:
            dtstart = self.event_start_date
            dtend = now() + timedelta(days=local_settings.RECURRENCE_MAX_DAYS_SEARCH)
            following_occurrences = self.recurrences.between(
                dtstart, dtend, dtstart=dtstart
            )
            return [self.event_start_date] + following_occurrences
        return []

    def get_post_occurrences(self, after=None):
        original_instance = self.post
        post_occurrences = []

        for occurrence_date in self.occurrences:
            if after and occurrence_date >= after:
                new_instance = Post(
                    **{
                        field: value
                        for field, value in original_instance.__dict__.items()
                        if not field.startswith("_")
                    }
                )
                new_instance.occurrence = occurrence_date
                post_occurrences.append(new_instance)
        return post_occurrences


class RecurrentPostsMixin:
    def get_max_post_count(self):
        return self.latest_posts

    def add_recurrent_posts(self, qs, after=None):
        return add_recurrent_posts(qs, after=after)

    def get_posts(self, request, published_only=True):
        posts = super().get_posts(request, published_only)
        return self.add_recurrent_posts(posts)[: self.latest_posts]


class UpcomingEventsPlugin(RecurrentPostsMixin, BasePostPlugin):
    """Django-CMS forbids the inheritance of other classes than:
    - CMSPlugin
    - abstract classes inheriting from CMSPlugin
    So we must redefine here all fields form class djangocms_blog.LatestPostsPlugin.
    """

    latest_posts = models.IntegerField(
        _("articles"),
        default=get_setting("LATEST_POSTS"),
        help_text=_("The number of latests " "articles to be displayed."),
    )
    hide_events_after = models.CharField(
        choices=local_settings.HIDE_UPCOMING_EVENTS_AFTER_CHOICES,
        default=local_settings.HIDE_UPCOMING_EVENTS_AFTER_CHOICES[0][0],
        max_length=100,
        verbose_name=_("Hide events"),
    )
    tags = TaggableManager(
        _("filter by tag"),
        blank=True,
        help_text=_("Show only the blog articles tagged with chosen tags."),
        related_name="djangocms_blog_agenda_upcoming_events",
    )
    categories = models.ManyToManyField(
        "djangocms_blog.BlogCategory",
        blank=True,
        verbose_name=_("filter by category"),
        help_text=_("Show only the blog articles tagged " "with chosen categories."),
    )

    def copy_relations(self, oldinstance):
        for tag in oldinstance.tags.all():
            self.tags.add(tag)
        for category in oldinstance.categories.all():
            self.categories.add(category)

    def get_posts(self, request, published_only=True):
        posts = self.post_queryset(request, published_only)
        if self.tags.exists():
            posts = posts.filter(tags__in=list(self.tags.all()))
        if self.categories.exists():
            posts = posts.filter(categories__in=list(self.categories.all()))
        return self.optimize(posts.distinct())

    def __str__(self):
        return _("{} upcoming events").format(self.latest_posts)

    @property
    def hide_events_duration(self):
        DELTA_RE = r"^start\+(\d+)([wdhm])$"
        if re.match(DELTA_RE, self.hide_events_after):
            result = re.search(DELTA_RE, self.hide_events_after)
            try:
                return {result.group(2): int(result.group(1))}
            except ValueError:
                return None

    class Meta:
        verbose_name = _("Upcoming events plugin")
        verbose_name_plural = _("Upcoming events plugins")


class PastEventsPlugin(RecurrentPostsMixin, LatestPostsPlugin):
    def __str__(self):
        return _("{} past events").format(self.latest_posts)

    class Meta:
        proxy = True
        verbose_name = _("Past events plugin")
        verbose_name_plural = _("Past events plugins")


class AgendaBlogCategory(BlogCategory):
    class Meta:
        proxy = True

    @cached_property
    def count(self):
        posts = self.linked_posts.filter(upcoming_events_query).published()
        count = posts.count()
        for post in posts:
            post_event = post.extension.first()
            if post_event.occurrences:
                count += len(list(post_event.occurrences))
        return count
