from decimal import Decimal

from django.test import TestCase
from django.core.urlresolvers import reverse
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

class ConfigTest(TestCase):
    
    def test_accessing_unregistered_settings(self):
        with self.assertRaises(ImproperlyConfigured):
            self.assertEqual(config.doesnt_exist, '')

    def test_register_setting(self):
        config.register(key='foo', default='bar', verbose_name='Test')
        self.assertEqual(config.foo, 'bar')
        self.assertEqual(config._registry['foo']['verbose_name'], 'Test')
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

    def test_save_fields(self):
        data = {'number': 10, 'float': 6.66, 'name': 'Max Mustermann', 'decimal': Decimal('7.50')}
        form = SettingsForm(data=data)
        form.is_valid()
        form.save()
        self.assertEqual(Settings.objects.get(key='name').value, 'Max Mustermann')

class View(TestCase):

    def test_settings_view(self):
        response = self.client.get(reverse('settings'))
        form = response.context['form']
        self.assertIsInstance(form, SettingsForm)

        response = self.client.post(reverse('settings'), data={'name': 'Max Mustermann'})
        self.assertEqual(Settings.objects.get(key='name').value, 'Max Mustermann')