from collections import Counter
from datetime import timedelta

from cms.plugin_pool import plugin_pool
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from djangocms_blog.cms_plugins import (
    BlogArchivePlugin,
    BlogCategoryPlugin,
    BlogPlugin,
    BlogTagsPlugin,
)
from djangocms_blog.forms import LatestEntriesForm
from djangocms_blog.models import Post
from djangocms_blog.settings import get_setting

from .models import AgendaBlogCategory, PastEventsPlugin, UpcomingEventsPlugin
from .utils import past_events_query, upcoming_events_query


class BaseLatestEntriesPlugin(BlogPlugin):
    form = LatestEntriesForm
    filter_horizontal = ("categories",)
    cache = False
    base_render_template = "latest_entries.html"

    def get_fields(self, request, obj=None):
        """
        Return the fields available when editing the plugin.

        'template_folder' field is added if ``BLOG_PLUGIN_TEMPLATE_FOLDERS`` contains multiple folders.

        """
        fields = ["app_config", "latest_posts", "tags", "categories"]
        if len(get_setting("PLUGIN_TEMPLATE_FOLDERS")) > 1:
            fields.append("template_folder")
        return fields

    def render(self, context, instance, placeholder):
        """Render the plugin."""
        context = super().render(context, instance, placeholder)
        context["posts_list"] = self.get_posts(
            instance, context["request"], published_only=False
        )
        context["TRUNCWORDS_COUNT"] = get_setting("POSTS_LIST_TRUNCWORDS_COUNT")
        return context


@plugin_pool.register_plugin
class AgendaUpcomingEntriesPlugin(BaseLatestEntriesPlugin):
    """
    Return upcoming events
    """

    name = _("Upcoming events")
    model = UpcomingEventsPlugin

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        fields.insert(2, "hide_events_after")
        return fields

    def get_posts(self, instance, request, published_only=True):
        posts = instance.post_queryset(request, published_only)

        filters = upcoming_events_query

        duration = instance.hide_events_duration
        if duration is not None:
            deadline = timezone.now() - timedelta(
                weeks=duration.get("w", 0),
                days=duration.get("d", 0),
                hours=duration.get("h", 0),
                minutes=duration.get("m", 0),
                seconds=duration.get("s", 0),
            )
            filters |= Q(extension__event_start_date__gte=deadline)
        elif instance.hide_events_after == "end":
            filters |= Q(extension__event_end_date__isnull=False) & Q(
                extension__event_end_date__gte=timezone.now()
            )

        posts = posts.order_by("extension__event_start_date").filter(filters)

        if instance.tags.exists():
            posts = posts.filter(tags__in=list(instance.tags.all()))
        if instance.categories.exists():
            posts = posts.filter(categories__in=list(instance.categories.all()))
        posts = instance.optimize(posts.distinct())
        return instance.add_recurrent_posts(posts, after=timezone.now())[
            : instance.latest_posts
        ]


@plugin_pool.register_plugin
class AgendaPastEntriesPlugin(BaseLatestEntriesPlugin):
    """
    Return a list of past events
    """

    name = _("Past events")
    model = PastEventsPlugin

    def get_posts(self, instance, request, published_only=True):
        posts = instance.post_queryset(request, published_only)

        # Keep only posts with an event date in the past
        posts = posts.order_by("-extension__event_start_date").filter(past_events_query)

        if instance.tags.exists():
            posts = posts.filter(tags__in=list(instance.tags.all()))
        if instance.categories.exists():
            posts = posts.filter(categories__in=list(instance.categories.all()))
        return instance.optimize(posts.distinct())[: instance.latest_posts]


class DateCountMixin:
    start_date_field = "extension__event_start_date"
    end_date_field = "extension__event_end_date"

    def get_months(self, queryset):
        """
        Get months with aggregate count (how much posts is in the month).
        Results are ordered by date.
        """

        def months_between(d1, d2):
            dates = []
            if d1 and not d2:
                dates.append([d1.year, d1.month])
                return dates
            if d2 and not d1:
                dates.append([d2.year, d2.month])
                return dates
            # continue only if there's 2 dates
            d1 = [d1.year, d1.month]
            d2 = [d2.year, d2.month]
            while d1[0] < d2[0] or (d1[0] == d2[0] and d1[1] <= d2[1]):
                dates.append(d1.copy())
                d1[1] += 1
                if d1[1] > 12:
                    d1[1] = 1
                    d1[0] += 1
            return dates

        dates_qs = queryset.values_list(
            "extension__event_start_date", "extension__event_end_date"
        )
        dates = []
        for start_date, end_date in dates_qs:
            for month in months_between(start_date, end_date):
                dates.append(tuple(month))

        date_counter = Counter(dates)
        dates = set(dates)
        dates = sorted(dates, reverse=True)
        return [
            {
                "date": timezone.now().replace(year=year, month=month, day=1),
                "count": date_counter[year, month],
            }
            for year, month in dates
        ]


@plugin_pool.register_plugin
class AgendaArchivePlugin(BlogArchivePlugin, DateCountMixin):
    name = _("All events archive")

    def render(self, context, instance, placeholder):
        """Render the plugin."""
        context = super().render(context, instance, placeholder)
        request = context["request"]
        self.posts = instance.post_queryset(request)

        if (
            not getattr(request, "toolbar", None)
            or not request.toolbar.edit_mode_active
        ):
            self.posts = self.posts.published()

        context["dates"] = self.get_months(queryset=self.posts)
        context["only_past_events"] = False
        return context


@plugin_pool.register_plugin
class AgendaArchivePastEventsPlugin(AgendaArchivePlugin):
    name = _("Past events archive")

    def render(self, context, instance, placeholder):
        """Render the plugin."""
        context = super().render(context, instance, placeholder)

        # Keep only posts with an event date in the past
        context["dates"] = self.get_months(
            queryset=self.posts.filter(past_events_query)
        )
        context["only_past_events"] = True
        return context


@plugin_pool.register_plugin
class AgendaCategoryUpcomingEventsPlugin(BlogCategoryPlugin):
    name = _("Upcoming events categories")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        qs = AgendaBlogCategory.objects.active_translations()

        if instance.app_config:
            qs = qs.namespace(instance.app_config.namespace)
        if instance.current_site:
            site = get_current_site(context["request"])
            qs = qs.filter(
                Q(blog_posts__sites__isnull=True) | Q(blog_posts__sites=site.pk)
            )

        categories = qs.distinct()
        if instance.app_config and not instance.app_config.menu_empty_categories:
            categories = qs.filter(blog_posts__isnull=False).distinct()
        context["categories"] = categories
        context["only_upcoming_events"] = True
        return context


@plugin_pool.register_plugin
class AgendaTagsUpcomingEventsPlugin(BlogTagsPlugin):
    name = _("Upcoming events tags")

    def render(self, context, instance, placeholder):
        """Render the plugin."""
        context = super().render(context, instance, placeholder)
        qs = instance.post_queryset(context["request"])
        context["tags"] = Post.objects.tag_cloud(
            queryset=qs.filter(upcoming_events_query).published()
        )
        return context
