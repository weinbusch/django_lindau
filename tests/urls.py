from django.conf.urls import url, include
from django.views.generic import FormView, ListView

from django_lindau.models import Settings
from django_lindau.forms import SettingsForm

urlpatterns = [
    url(r'^$', FormView.as_view(form_class=SettingsForm, template_name='tests/settings_form.html'), name='index'),
    url(r'^list$', ListView.as_view(model=Settings), name='list'),
]