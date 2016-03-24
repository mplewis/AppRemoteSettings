from django.contrib import admin

from .models import App, Identifier, Key


admin.site.register(App)
admin.site.register(Identifier)
admin.site.register(Key)
