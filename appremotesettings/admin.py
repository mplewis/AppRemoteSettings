from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin

from appremotesettings import settings
from .models import App, Identifier, Key


class IdentifierInline(TabularInline):
    model = Identifier
    extra = 1
    fields = ('value', 'desc')


class KeyInline(TabularInline):
    model = Key
    extra = 1
    fields = ('datatype', 'key', 'value', 'desc')


class AppAdmin(ModelAdmin):
    inlines = [IdentifierInline, KeyInline]


admin.site.register(App, AppAdmin)
admin.site.site_header = settings.ADMIN_SITE_HEADER
