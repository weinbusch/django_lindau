from decimal import Decimal

from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django import forms

from django_lindau.models import Settings
from django_lindau import config
from django_lindau.forms import SettingsForm

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
    
    def test_accessing_unregistered_settings(self):
        with self.assertRaises(ImproperlyConfigured):
            self.assertEqual(config.doesnt_exist, '')

    def test_register_setting(self):
        config.register(key='foo', default='bar', verbose_name='Test')
        self.assertEqual(config.foo, 'bar')
        self.assertEqual(Settings.objects.get(key='foo').verbose_name, 'Test')
        Settings.objects.filter(key='foo').update(value='test')
        self.assertEqual(config.foo, 'test')

        # Cannot register methods or attributes of Config as settings
        with self.assertRaises(ImproperlyConfigured):
            config.register(key='register')

        with self.assertRaises(ImproperlyConfigured):
            config.register(key='_registry')

    def test_registered_settings(self):
        '''
        Settings can be registered in a lindau.py file in each app directory (here in the tests package)
        '''
        self.assertEqual(config.name, 'Tim')
        self.assertEqual(config.number, 10)
        self.assertEqual(config.float, 6.66)
        self.assertEqual(config.decimal, Decimal('7.50'))   

class Form(TestCase):

    def test_default_fields(self):
        form = SettingsForm()
        fields = form.fields

        self.assertIsInstance(fields['name'], forms.CharField)
        self.assertIsInstance(fields['number'], forms.IntegerField)
        self.assertIsInstance(fields['float'], forms.FloatField)
        self.assertIsInstance(fields['decimal'], forms.DecimalField)
        
    def test_custom_field(self):
        config.register(key='email', default='test@test.com', field_class=forms.EmailField)

        form = SettingsForm()
        fields = form.fields

        self.assertIsInstance(fields['email'], forms.EmailField)