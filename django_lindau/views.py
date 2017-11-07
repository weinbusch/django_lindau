from django.views.generic import FormView

from django_lindau.forms import SettingsForm

class SettingsView(FormView):
    form_class = SettingsForm
    template_name = 'django_lindau/settings_form.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)