from django.core.exceptions import ImproperlyConfigured

from django_lindau.models import Settings

class Config(object):

    def __init__(self):
        self._registry = {}

    def __getattr__(self, key):
        if key in self._registry:
            defaults = self._registry[key]['defaults']
            setting, created = Settings.objects.get_or_create(key=key, defaults=defaults)
        else:
            setting = Settings.objects.get(key=key)
        return setting.value

    def register(self, key, default=None, verbose_name=None):
        '''
        Register a setting
        '''
        if key in dir(self):
            raise ImproperlyConfigured(
                "Setting with key '%s' not allowed, since it's a method or attribute of '%s'."
                % (key, self.__class__.__name__)
            )
        defaults = dict(value=default, verbose_name=verbose_name)
        self._registry[key] = dict(defaults=defaults)