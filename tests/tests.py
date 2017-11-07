from decimal import Decimal

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django import forms

from django_lindau import config
from django_lindau.models import Settings
from django_lindau.base import Config
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

    def setUp(self):
        self.config = Config()
    
    def test_accessing_unregistered_settings(self):
        with self.assertRaises(ImproperlyConfigured):
            self.assertEqual(self.config.doesnt_exist, '')

    def test_register_setting(self):
        self.config.register(key='foo', default='bar', verbose_name='Test')
        self.assertEqual(self.config.foo, 'bar')
        self.assertEqual(self.config._registry['foo']['verbose_name'], 'Test')
        Settings.objects.filter(key='foo').update(value='test')
        self.assertEqual(self.config.foo, 'test')

    def test_invalid_key(self):
        # Cannot register methods or attributes of Config as settings
        with self.assertRaises(ImproperlyConfigured):
            self.config.register(key='register')

        with self.assertRaises(ImproperlyConfigured):
            self.config.register(key='_registry')

class Form(TestCase):

    def test_autodiscovered_settings(self):
        '''
        Settings can be registered in a lindau.py file in each app directory (here in the tests package)
        '''
        self.assertEqual(config.name, 'Tim')
        self.assertEqual(config.number, 10)
        self.assertEqual(config.float, 6.66)
        self.assertEqual(config.decimal, Decimal('7.50'))   
        self.assertEqual(config.email, 'test@test.com')
        
    def test_default_fields(self):
        form = SettingsForm()
        fields = form.fields

        self.assertIsInstance(fields['name'], forms.CharField)
        self.assertIsInstance(fields['number'], forms.IntegerField)
        self.assertIsInstance(fields['float'], forms.FloatField)
        self.assertIsInstance(fields['decimal'], forms.DecimalField)
        self.assertIsInstance(fields['email'], forms.EmailField)

        self.assertEqual(fields['email'].label, 'E-Mail')
        
    def test_save_fields(self):
        data = {'number': 10, 'float': 6.66, 'name': 'Max Mustermann', 'decimal': Decimal('7.50'), 'email': 'test@test.com'}
        form = SettingsForm(data=data)
        form.is_valid()
        form.save()
        self.assertEqual(Settings.objects.get(key='name').value, 'Max Mustermann')

    def test_wrong_input(self):
        data = {'number': 'wrong input!', 'float': 6.66, 'name': 'Max Mustermann', 'decimal': Decimal('7.50'), 'email': 'test@test.com'}
        form = SettingsForm(data=data)
        form.is_valid()
        self.assertIn('number', form.errors)

    def test_set_setting_to_None_and_reinit_form(self):
        data = {'number': '', 'float': 6.66, 'name': 'Max Mustermann', 'decimal': Decimal('7.50'), 'email': 'test@test.com'}
        form = SettingsForm(data=data)
        form.is_valid()
        form.save()

        form = SettingsForm()
        self.assertIsInstance(form.fields['number'], forms.IntegerField)

class View(TestCase):

    def test_settings_view(self):
        response = self.client.get(reverse('settings'))
        form = response.context['form']
        self.assertIsInstance(form, SettingsForm)

        data = {'number': 10, 'float': 6.66, 'name': 'Max Mustermann', 'decimal': Decimal('7.50'), 'email': 'test@test.com'}
        response = self.client.post(reverse('settings'), data=data)
        self.assertEqual(Settings.objects.get(key='name').value, 'Max Mustermann')

        response = self.client.post(reverse('settings'), data={'number': 'wrong input!'})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIsNotNone(form.errors['number'])