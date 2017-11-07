# Django-Lindau

A Django app for storing dynamic settings in the database.

Inspired by [django-constance](https://github.com/jazzband/django-constance). It's just across the lake.

## Register a setting

You can register a setting by putting the following in a `lindau.py` file in your app directory:

    # lindau.py

    from django_lindau import config

    config.register(key='foo', default='bar', verbose_name='Foo Setting')

## Access settings

You can access settings in your code like this:

    from django_lindau import config

    # Just print the setting's value
    print(config.foo)

    # or get the Setting instance
    setting = config.get_setting('foo')
    print(setting.value)

## Change settings

Settings can be changed like this:

    from django_lindau import config

    config.save_setting('foo', 'New bar')

## Edit settings through a form

A special form class is provided to edit settings:

    from django_lindau.forms import SettingsForm

    form = SettingsForm(data={'foo': 'Brand new bar'})
    form.is_valid()
    form.save()

### Custom form fields

Default form fields are included based on the type of the setting's value. Alternativly, 
custom form fields can be specified when registering a setting like this:

    from django import forms
    from django_lindau import config

    config.register(key='bar', default='test@test.com', form_field=forms.EmailField)