# Django-Lindau

A Django app for storing dynamic settings in the database.

Inspired by [django-constance](https://github.com/jazzband/django-constance). It's just across the lake.

## Register a setting

You can register a setting by putting the following in a `lindau.py` file in your app directory:

    # lindau.py

    from django_lindau import config

    config.register(key='foo', default='bar', verbose_name='Foo Setting')

## Accessing settings

You can access settings in your code like this:

    from django_lindau import config

    print(config.foo)