from django.contrib import admin

from .models import (
    ActiveSecretSantaFilter, Application, SantaPair, SecretSantaConfiguration,
    Webhook, Year,
)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['year', 'user']


@admin.register(SantaPair)
class SantaPairAdmin(admin.ModelAdmin):
    list_display = ['year', 'santa', 'santee', 'delivered']


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']


@admin.register(SecretSantaConfiguration)
class SecretSantaConfigurationAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ['year', 'open']


@admin.register(ActiveSecretSantaFilter)
class ActiveSecretSantaFilterAdmin(admin.ModelAdmin):
    list_display = ['year', 'reversed_logic']
