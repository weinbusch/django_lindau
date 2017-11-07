from decimal import Decimal

from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured

from django_lindau.models import Settings
from django_lindau import config

class SettingsModel(TestCase):

    def test_create_some_settings(self):
        Settings.objects.create(key='foo', value=10.53)
        Settings.objects.create(key='bar', value='abracadabra')

        self.assertEqual(Settings.objects.get(key='foo').value, 10.53)
        self.assertEqual(Settings.objects.get(key='bar').value, 'abracadabra')

    def test_unique_key(self):
        Settings.objects.create(key='foo', value=10.53)
        with self.assertRaises(IntegrityError):
            Settings.objects.create(key='foo', value='abracadabra')

    def test_verbose_name(self):
        obj = Settings.objects.create(key='foo', value='bar')
        self.assertEqual(obj.verbose_name, 'Foo')

        obj = Settings.objects.create(key='bar', value='foo', verbose_name='Test')
        self.assertEqual(obj.verbose_name, 'Test')

class ConfigTest(TestCase):
    
    def test_accessing_config_variables(self):
        Settings.objects.create(key='foo', value=10.53)
        Settings.objects.create(key='bar', value='abracadabra')

        self.assertEqual(config.foo, 10.53)
        self.assertEqual(config.bar, 'abracadabra')

        with self.assertRaises(ObjectDoesNotExist):
            self.assertEqual(config.doesnt_exist, '')

    def test_register_setting(self):
        config.register(key='foo', default='bar', verbose_name='Test')
        self.assertEqual(config.foo, 'bar')
        self.assertEqual(Settings.objects.get(key='foo').verbose_name, 'Test')
        Settings.objects.filter(key='foo').update(value='test')
        self.assertEqual(config.foo, 'test')

        # Cannot register setting 'register' (since it's a method of config)
        with self.assertRaises(ImproperlyConfigured):
            config.register(key='register')

    def test_registered_settings(self):
        '''
        Settings can be registered in a lindau.py file in each app directory (here in the tests package)
        '''
        self.assertEqual(config.name, 'Tim')
        self.assertEqual(config.number, 10)
        self.assertEqual(config.float, 6.66)
        self.assertEqual(config.decimal, Decimal('7.50'))        