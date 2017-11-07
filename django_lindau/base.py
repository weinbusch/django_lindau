from django.core.exceptions import ImproperlyConfigured

from django_lindau.models import Settings

class Config(object):

    def __init__(self):
        self._registry = {}

    def __getattr__(self, key):
        setting = self.get_setting(key)
        return setting.value

    def save_setting(self, key, value):
        Settings.objects.filter(key=key).update(value=value)

    def register(self, key, default=None, verbose_name=None, field_class=None):
        '''
        Register a setting
        '''
        if key in dir(self):
            raise ImproperlyConfigured(
                "Setting with key '%s' not allowed, since it's a method or attribute of '%s'."
                % (key, self.__class__.__name__)
            )
        defaults = dict(value=default)
        self._registry[key] = dict(defaults=defaults, verbose_name=verbose_name, field_class=field_class)

    def get_setting(self, key):
        if key in self._registry:
            defaults = self._registry[key]['defaults']
            setting, created = Settings.objects.get_or_create(key=key, defaults=defaults)
            return setting
        raise ImproperlyConfigured(
            "Setting '%s' has not been registered." % (key,)
        )