from cms.models.pluginmodel import CMSPlugin

from django.db import models


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
