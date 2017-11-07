from django.core.exceptions import ImproperlyConfigured

from django_lindau.models import Settings

class Config(object):

    def __init__(self):
        self._registry = {}

    def __getattr__(self, key):
        if key in self._registry:
            default = self._registry[key]['default']
            setting, created = Settings.objects.get_or_create(key=key, defaults=dict(value=default))
        else:
            setting = Settings.objects.get(key=key)
        return setting.value

    def register(self, key, default=None):
        '''
        Register a setting
        '''
        if key in dir(self):
            raise ImproperlyConfigured(
                "Setting with key '%s' not allowed, since it's a method or attribute of '%s'."
                % (key, self.__class__.__name__)
            )
        self._registry[key] = dict(default=default)