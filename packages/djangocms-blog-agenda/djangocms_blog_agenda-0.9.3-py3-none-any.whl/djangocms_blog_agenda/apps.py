from django.apps import AppConfig
from django.contrib.auth import get_user_model
from djangocms_blog.settings import get_setting


class DjangocmsBlogAgendaConfig(AppConfig):
    name = "djangocms_blog_agenda"

    def ready(self):
        def get_sites(user):
            # The apps should be initialized since we're in ready(), so we can use GlobalPagePermission objects,
            # or "Permissions globales des pages" in the French CMS
            from cms.models.permissionmodels import GlobalPagePermission
            from django.contrib.sites.models import Site

            from . import signals  # noqa: F401

            try:
                # we got a GlobalPagePermission for this user, take this and only this!
                user_perms = GlobalPagePermission.objects.get(user=user)
                return user_perms.sites.all()
            except GlobalPagePermission.DoesNotExist:
                # GlobalPagePermission may be assigned to a group instead of a user, so we need
                # to list all the Sites in all the Groups of the current user, and allow all those sites
                #
                # Take all the GlobalPagePermission for the groups of the user
                group_perms = GlobalPagePermission.objects.filter(
                    group__in=user.groups.all()
                )
                # Take all sites that are in those GlobalPagePermissions
                sites = Site.objects.filter(
                    globalpagepermission__in=group_perms
                ).distinct()
                return sites

        if get_setting("MULTISITE"):
            # set the get_site function to the current user model dynamically, so djangocms-blog can use it
            setattr(get_user_model(), "get_sites", get_sites)
