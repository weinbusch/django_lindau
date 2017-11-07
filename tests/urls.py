from django.conf.urls import url

from django_lindau.views import SettingsView

urlpatterns = [
    url(r'^$', SettingsView.as_view(template_name='tests/settings_form.html', success_url='/'), name='settings'),
]