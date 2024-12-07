def get_inline_instances(self, request, obj=None):
    from json import loads

    from djangocms_blog.admin import PostAdmin
    from djangocms_blog.cms_appconfig import BlogConfig

    from .admin import PostExtensionInline

    inline_instances = super(PostAdmin, self).get_inline_instances(request, obj)

    if "app_config" in request.GET:
        # get blog config instance from request
        blog_config = BlogConfig.objects.filter(pk=request.GET["app_config"])
        # get config from saved json
        config = loads(blog_config.values()[0]["app_data"])
        # get template_prefix from config

        if config:
            template_prefix = config["config"]["template_prefix"]
            if template_prefix == "djangocms_blog_agenda":
                return inline_instances

    return list(
        filter(
            lambda instance: not isinstance(instance, PostExtensionInline),
            inline_instances,
        )
    )
