from django.db import models

from picklefield import PickledObjectField

class Settings(models.Model):

    key = models.CharField(max_length=255, unique=True)
    value = PickledObjectField(null=True)
