from django.contrib import admin
from .models import Country

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'cca2', 'region', 'population')
    search_fields = ('name', 'cca2', 'region')