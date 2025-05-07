from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField  # if using PostgreSQL
from django.conf import settings

class Country(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    cca2 = models.CharField(max_length=2, unique=True)
    capital = models.CharField(max_length=128, blank=True)
    population = models.BigIntegerField()
    region = models.CharField(max_length=64)
    timezones = models.JSONField()                 # list of strings
    flag = models.URLField()
    languages = models.JSONField(blank=True, null=True)  # {"eng":"English","spa":"Spanish"}

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
