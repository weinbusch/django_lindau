from decimal import Decimal

from django import forms

from django_lindau import config

config.register(
    key='name',
    default='Tim'
)

config.register(
    key='number',
    default=10
)

config.register(
    key='float',
    default=6.66
)

config.register(
    key='decimal',
    default=Decimal('7.50'),
    verbose_name='Dezimalzahl'
)

config.register(
    key='email',
    default='test@test.com',
    field_class=forms.EmailField,
    verbose_name='E-Mail',
)