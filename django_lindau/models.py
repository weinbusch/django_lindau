from django.db import models

from picklefield import PickledObjectField

class Settings(models.Model):

    key = models.CharField(max_length=255, unique=True)
    value = PickledObjectField(null=True)
    verbose_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.verbose_name:
            self.verbose_name = self.key.title()
        return super().save(*args, **kwargs)