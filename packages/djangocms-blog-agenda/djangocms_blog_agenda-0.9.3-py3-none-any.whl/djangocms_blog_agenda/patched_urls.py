from django.urls import path
from djangocms_blog.urls import urlpatterns as original_patterns

from .views import (
    AgendaArchiveView,
    AgendaCategoryEntriesView,
    AgendaDetailView,
    AgendaListView,
    AgendaTaggedListView,
)


# Here are the patched urls that still includes the original urlpattern of djangocms_blog.
# But it also adds an AgendaAndPostListView (that replace the original PostListView).

for pattern in original_patterns:
    if pattern.name == "post-detail":
        pattern.callback = AgendaDetailView.as_view()


urlpatterns = [
    path(
        "<int:year>/",
        AgendaArchiveView.as_view(),
        {"only_past_events": False},
        name="agenda-archive",
    ),
    path(
        "<int:year>/<int:month>/",
        AgendaArchiveView.as_view(),
        {"only_past_events": False},
        name="agenda-archive",
    ),
    path(
        "<int:year>/past/",
        AgendaArchiveView.as_view(),
        {"only_past_events": True},
        name="agenda-archive",
    ),
    path(
        "<int:year>/<int:month>/past/",
        AgendaArchiveView.as_view(),
        {"only_past_events": True},
        name="agenda-archive",
    ),
    path(
        "",
        AgendaListView.as_view(),
        {"only_upcoming_events": True},
        name="agenda-upcoming-events",
    ),
    path(
        "category/<str:category>/",
        AgendaCategoryEntriesView.as_view(),
        {"only_upcoming_events": False},
        name="agenda-events-category",
    ),
    path(
        "category/<str:category>/upcoming/",
        AgendaCategoryEntriesView.as_view(),
        {"only_upcoming_events": True},
        name="agenda-events-category",
    ),
    path(
        "tag/<slug:tag>/",
        AgendaTaggedListView.as_view(),
        {"only_upcoming_events": False},
        name="agenda-events-tagged",
    ),
    path(
        "tag/<slug:tag>/upcoming/",
        AgendaTaggedListView.as_view(),
        {"only_upcoming_events": True},
        name="agenda-events-tagged",
    ),
    *original_patterns,
]
