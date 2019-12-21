from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Malware(models.Model):
    name = models.CharField(max_length=100)
    data = JSONField()

    def __str__(self):
        return self.name