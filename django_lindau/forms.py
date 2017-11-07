from decimal import Decimal

from django import forms
from django.core.exceptions import ImproperlyConfigured

from django_lindau import config

DEFAULT_FIELDS = {
    str: forms.CharField,
    int: forms.IntegerField,
    float: forms.FloatField,
    Decimal: forms.DecimalField,
}

class SettingsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in config._registry:
            setting = config.get_setting(key)
            options = config._registry[key]
            field_class = options['field_class']
            if not field_class:
                # Guess field class from settings value:
                try:
                    value = setting.value
                    _type = type(value)
                    field_class = DEFAULT_FIELDS[_type]
                except KeyError:
                    raise ImproperlyConfigured(
                        "%s does not provide a default field for settings of type '%s'."
                        % (self.__class__.__name__, _type)
                    )
            self.fields[key] = field_class(required=False, initial=setting.value, label=options['verbose_name'])

    def save(self):
        for key in self.cleaned_data:
            config.save_setting(key, self.cleaned_data[key])