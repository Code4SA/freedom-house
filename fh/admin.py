from django.contrib import admin
from cms.extensions import PageExtensionAdmin

from .models import SpeakupPageExtension


class SpeakupPageExtensionAdmin(PageExtensionAdmin):
    pass

admin.site.register(SpeakupPageExtension, SpeakupPageExtensionAdmin)
