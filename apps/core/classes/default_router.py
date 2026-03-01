from django.urls import path

from rest_framework.routers import SimpleRouter, APIRootView
from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.views import SchemaView
from rest_framework.settings import api_settings
from rest_framework.urlpatterns import format_suffix_patterns


class DefaultRouter(SimpleRouter):
    """
    The default router extends the SimpleRouter, but also adds in a default
    API root view, and adds format suffix patterns to the URLs.
    """

    include_root_view = True
    include_format_suffixes = True
    root_view_name = "api-root"
    default_schema_renderers = None
    APIRootView = APIRootView
    APISchemaView = SchemaView
    SchemaGenerator = SchemaGenerator

    def __init__(self, *args, **kwargs):
        if "root_renderers" in kwargs:
            self.root_renderers = kwargs.pop("root_renderers")
        else:
            self.root_renderers = list(api_settings.DEFAULT_RENDERER_CLASSES)
        super().__init__(*args, **kwargs)

    def get_api_root_view(self, api_urls=None):
        """
        Return a basic root view.
        """
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        return self.APIRootView.as_view(api_root_dict=api_root_dict)

    def get_urls(self):
        """
        Generate the list of URL patterns, including a default root view
        for the API, and appending `.json` style format suffixes.
        """
        urls = super().get_urls()

        if self.include_root_view:
            view = self.get_api_root_view(api_urls=urls)
            root_url = path("", view, name=self.root_view_name)
            urls.append(root_url)

        if self.include_format_suffixes:
            urls = format_suffix_patterns(urls, suffix_required=False, allowed=["api", "json"])

        return urls
