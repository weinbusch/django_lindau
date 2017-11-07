from django.utils.functional import LazyObject
from django.utils.module_loading import autodiscover_modules

class LazyConfig(LazyObject):
    def _setup(self):
        from django_lindau.base import Config
        self._wrapped = Config()

config = LazyConfig()

def autodiscover():
    autodiscover_modules('lindau', register_to=config)

default_app_config = 'django_lindau.apps.LindauAppConfig'