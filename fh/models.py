from cms.models.pluginmodel import CMSPlugin

from django.db import models

class DiscourseTopicModel(CMSPlugin):
    topic = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.topic or '(none)'
