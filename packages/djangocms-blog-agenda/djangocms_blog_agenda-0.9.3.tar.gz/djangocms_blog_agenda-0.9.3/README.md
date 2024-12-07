Add an Agenda to your blog that displays upcoming events!

*Easy! ~~Cheap~~Free! Not seen on TV!*

----

## Install

* Install the package
    ```bash
    python3 -m pip install djangocms-blog-agenda
    ```

* Add it in your `INSTALLED_APPS`:
    ```python
    "djangocms_blog_agenda",
    "recurrence",
    ```

* Run the migration:
    ```sh
    python3 manage.py migrate djangocms_blog_agenda
    ```

* Update the `djangocms-blog` urls by the ones in this module, by using this lovely [setting](https://djangocms-blog.readthedocs.io/en/latest/features/urlconf.html):
    ```py
    BLOG_URLCONF = "djangocms_blog_agenda.patched_urls"
    ```

* Create a new blog configuration.
  * Instance namespace: *put what you want*.
  * Application title: *put what you want*.
  * Object name: *put what you want*.
  * [...]
  * <b>Click on <kbd>Layout (Show)</kbd></b>:
    * [...]
    * **Template prefix**: `djangocms_blog_agenda`.
    > That's ***very*** important since this application will check this value multiple times (to update the queryset, to check the templates, to add the post extension "event date" only to the Agenda app...).
  * Save this config.

* ![that's all folks!](https://gitlab.com/kapt/open-source/djangocms-blog-agenda/uploads/2a4d7f27d4eaf5e3b07ed4779dde76d2/image.png)

----

## Explanations/Views/Misc

* A new `Event date` DateTime field has been added to blog posts that have the template prefix set to `djangocms_blog_agenda`.
* A new post list view was created for the Agenda view, it includes all the posts where the `event_date` is set to a date in the future.
* Another view is available at `_("/past/")`, that will display each post where the `event_date` is in the past.
* The templates are *not* in `djangocms_blog/templates` anymore, but in `djangocms_blog_agenda/templates`. Something's not appearing on your templates? Try to edit the file in `djangocms_blog_agenda/templates/`!
* We removed the mention of comments & liveblog in the admin form, because we're not using this.
* We use some very special bits of code that are using some internal features of djangocms-blog (see `misc.py`, and `apps.py`). Try the module before pushing an update.

----

## Config

### Settings

#### `DJANGOCMS_BLOG_AGENDA_HIDE_UPCOMING_EVENTS_AFTER_CHOICES`
a tuple of choices describing when `AgendaUpcomingEntriesPlugin` will hide events.

Default choices are:
```py
(
    ("start", _("just after event start date")),
    ("start+1h", _("1 hour after event start date")),
    ("start+4h", _("4 hours after event start date")),
    ("start+1d", _("1 day after event start date")),
    ("start+2d", _("2 days after event start date")),
    ("start+3d", _("3 days after event start date")),
    ("start+7d", _("7 days after event start date")),
    ("end", _("just after event end date")),
)
```

#### `DJANGOCMS_BLOG_AGENDA_RECURRENCE_MAX_DAYS_SEARCH`
a number of days (int) to limit the search of recurring events. Defaults to `365`.

### Multisite

This modules handles multisite just fine; just add `BLOG_MULTISITE = True` in your settings, and our module will inject the `get_site` function directly inside the class returned by `get_user_model()`! (it is done in AppConfig `ready()` method)

You will then need to create a new "Global Page Permission" entry with your user/group, and to select the site where the user/group will have the right to post new articles/agenda posts.

*If you're curious about this function, [here it is](djangocms_blog_agenda/apps.py).*

### Recurrences

Recurring events are handled with the help of django-recurrence package. Only the first event is saved into database, and following recurring events are added into querysets just before they are displayed. Only events that occurs `n` days after the first event are displayed. You can change this `n` with the setting `DJANGOCMS_BLOG_AGENDA_RECURRENCE_MAX_DAYS_SEARCH`.
