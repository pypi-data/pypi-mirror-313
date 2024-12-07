from django.db.models import Q
from django.utils import timezone
from djangocms_blog.views import (
    BaseBlogListView,
    CategoryEntriesView,
    PostArchiveView,
    PostDetailView,
    PostListView,
    TaggedListView,
)

from .utils import add_recurrent_posts, past_events_query, upcoming_events_query


class AgendaDetailView(PostDetailView):
    def post(self, *args, **kwargs):
        return self.get(args, kwargs)


class AgendaUpcomingEventsMixin:
    def get_queryset(self):
        qs = super().get_queryset()

        if "agenda" in self.config.template_prefix:
            if self.kwargs.get("only_upcoming_events", False):
                qs = qs.filter(upcoming_events_query)
            qs = qs.order_by("extension__event_start_date")
            qs = add_recurrent_posts(qs, after=timezone.now())
        return qs


class AgendaListView(AgendaUpcomingEventsMixin, PostListView):
    ...


class AgendaCategoryEntriesView(AgendaUpcomingEventsMixin, CategoryEntriesView):
    ...


class AgendaTaggedListView(AgendaUpcomingEventsMixin, TaggedListView):
    ...


class AgendaArchiveView(PostArchiveView):
    start_date_field = "extension__event_start_date"
    end_date_field = "extension__event_end_date"

    def get_queryset(self):
        if "agenda" in self.config.template_prefix:
            # Bypass PostArchiveView.get_queryset() because it does not handle `end_date_field`
            qs = super(BaseBlogListView, self).get_queryset()

            if self.kwargs.get("only_past_events", False):
                qs = qs.filter(past_events_query)

            if "month" in self.kwargs:
                qs = qs.filter(
                    Q(
                        **{
                            "%s__month__lte"
                            % self.start_date_field: self.kwargs["month"]
                        }
                    )
                    & Q(
                        **{"%s__month__gte" % self.end_date_field: self.kwargs["month"]}
                    )
                    | Q(
                        **{
                            "%s__month__exact"
                            % self.start_date_field: self.kwargs["month"]
                        }
                    )
                )
            if "year" in self.kwargs:
                qs = qs.filter(
                    Q(**{"%s__year" % self.start_date_field: self.kwargs["year"]})
                    | Q(**{"%s__year" % self.end_date_field: self.kwargs["year"]})
                )

            qs = qs.order_by("-extension__event_start_date")
            return add_recurrent_posts(qs, reverse=True)
        return super().get_queryset()
