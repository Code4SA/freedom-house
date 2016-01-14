from cms.models.pluginmodel import CMSPlugin
from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool

from django.db import models
from filer.fields.image import FilerImageField


class DiscourseTopicModel(CMSPlugin):
    topic = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.topic or '(none)'


class CallToActionModel(CMSPlugin):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    button_text = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


class SpeakupPageExtension(PageExtension):
    header_image = FilerImageField(null=True, blank=True)


extension_pool.register(SpeakupPageExtension)
