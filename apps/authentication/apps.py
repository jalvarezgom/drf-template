from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authentication"

    def ready(self):
        # from actstream import registry
        # registry.register(self.get_model("User"))
        from django.contrib import admin

        admin.register(self.get_model("User"))
