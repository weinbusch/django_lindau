from django.apps import AppConfig

class LindauAppConfig(AppConfig):
    name = 'django_lindau'

    def ready(self):
        self.module.autodiscover()