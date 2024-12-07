from django.contrib import admin
from django.utils.dateformat import DateFormat
from django.utils.translation import gettext as _, gettext_lazy
import djangocms_blog.admin as blog_admin
from djangocms_blog.admin import PostAdmin
from djangocms_blog.models import Post

from .misc import get_inline_instances as patched_get_inline_instances
from .models import PostExtension


# replace PostAdmin get_inlines function in order to hide event_start_date on
# regular blog posts
PostAdmin.get_inline_instances = patched_get_inline_instances


class PostExtensionInline(admin.StackedInline):
    model = PostExtension
    fields = ("event_start_date", "event_end_date", "recurrences")
    classes = []
    extra = 1
    can_delete = False
    verbose_name = gettext_lazy("Event infos")
    verbose_name_plural = gettext_lazy("Event infos")
    min_num = 1
    max_num = 1


blog_admin.register_extension(PostExtensionInline)


admin.site.unregister(Post)


@admin.register(Post)
class AgendaPostAdmin(PostAdmin):
    """Better layout of Post admin form"""

    list_display = [
        "title",
        "get_event_dates",
        "publish",
        "date_published",
        "author",
        "all_languages_column",
        "app_config",
    ]

    date_hierarchy = "extension__event_start_date"
    ordering = ("-extension__event_start_date",)

    _fieldsets = [
        (None, {"fields": ["title", "subtitle", "slug", "publish", "categories"]}),
        (
            gettext_lazy("Info"),
            {
                "fields": [
                    ["tags"],
                    ["date_published", "date_published_end"],
                    "app_config",
                ],
                "classes": ("collapse",),
            },
        ),
        (
            gettext_lazy("Images"),
            {
                "fields": [["main_image", "main_image_thumbnail", "main_image_full"]],
                "classes": ("collapse",),
            },
        ),
        (
            gettext_lazy("SEO"),
            {
                "fields": [["meta_description", "meta_title", "meta_keywords"]],
                "classes": ("collapse",),
            },
        ),
    ]
    _fieldset_extra_fields_position = {
        "sites": [0, 1],
        "abstract": [0, 1],
        "post_text": [0, 1],
        "author": [0, 1],
        "enable_liveblog": None,
        "related": [1, 1, 0],
    }

    @admin.display(
        description=gettext_lazy("Event dates"), ordering="extension__event_start_date"
    )
    def get_event_dates(self, obj):
        extension = obj.extension.first()
        if extension is not None:
            start = extension.event_start_date
            end = extension.event_end_date
            df_start = DateFormat(start)
            df_end = DateFormat(end)
            DAY_FORMAT = _("jS")
            DAY_MONTH_FORMAT = _("jS F")
            DAY_MONTH_YEAR_FORMAT = _("jS F Y")

            if end is None:
                return _("on {date}").format(
                    date=df_start.format(DAY_MONTH_YEAR_FORMAT)
                )
            else:
                if start.year == end.year:
                    if start.month == end.month:
                        if start.day == end.day:
                            return _("on {date}").format(
                                date=df_start.format(DAY_MONTH_YEAR_FORMAT)
                            )
                        else:
                            start_part = df_start.format(DAY_FORMAT)
                            end_part = df_end.format(DAY_MONTH_YEAR_FORMAT)
                            return _("from {start_part} to {end_part}").format(
                                start_part=start_part, end_part=end_part
                            )
                    else:
                        start_part = df_start.format(DAY_MONTH_FORMAT)
                        end_part = df_end.format(DAY_MONTH_YEAR_FORMAT)
                        return _("from {start_part} to {end_part}").format(
                            start_part=start_part, end_part=end_part
                        )
                else:
                    start_part = df_start.format(DAY_MONTH_YEAR_FORMAT)
                    end_part = df_end.format(DAY_MONTH_YEAR_FORMAT)
                    return _("from {start_part} to {end_part}").format(
                        start_part=start_part, end_part=end_part
                    )

    def get_list_filter(self, request):
        filters = super().get_list_filter(request)
        filters.append("categories")
        return filters
