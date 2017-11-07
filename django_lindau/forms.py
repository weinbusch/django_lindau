from decimal import Decimal

from django import forms
from django.core.exceptions import ImproperlyConfigured

from django_lindau import config

class SettingsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in config._registry:
            setting = config.get_setting(key)
            options = config._registry[key]
            field_class = options['field_class']
            self.fields[key] = field_class(initial=setting.value, label=options['verbose_name'])

    def save(self):
        for key in self.cleaned_data:
            config.save_setting(key, self.cleaned_data[key])