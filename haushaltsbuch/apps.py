from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "haushaltsbuch"
    verbose_name = "Haushaltsbuch"
