from django.db.models import Q
from django.utils import timezone


upcoming_events_query = (
    (
        Q(extension__event_end_date__isnull=True)
        & Q(extension__event_start_date__gte=timezone.now())
    )
    | (
        Q(extension__event_end_date__isnull=False)
        & Q(extension__event_end_date__gte=timezone.now())
    )
    | (  # Include events that have upcoming occurrences
        Q(extension__recurrences__isnull=False)
        & Q(extension__recurrences_end_date__gte=timezone.now())
    )
)

past_events_query = (
    Q(extension__event_end_date__isnull=True)
    & Q(extension__event_start_date__lt=timezone.now())
) | (
    Q(extension__event_end_date__isnull=False)
    & Q(extension__event_end_date__lt=timezone.now())
)


def add_recurrent_posts(qs, reverse=False, after=None):
    """Return a list containing all posts from the given quersyet and a clone post
    for each post that have recurring occurrences.
    """
    posts_with_recurrences = []

    for object in qs:
        if object.extension.exists():
            post_event = object.extension.first()
            posts_with_recurrences.extend(post_event.get_post_occurrences(after))

    def get_key(item):
        return getattr(item, "occurrence", item.extension.first().event_start_date)

    posts_with_recurrences.sort(key=get_key, reverse=reverse)
    return posts_with_recurrences


def is_infinite_recurrence(recurrences) -> bool:
    return any([rule.count is rule.until is None for rule in recurrences.rrules])
