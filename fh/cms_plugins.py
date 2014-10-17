from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import DiscourseTopicModel

class DiscourseTopicPlugin(CMSPluginBase):
    model = DiscourseTopicModel
    name = _("Discourse Topic")
    render_template = "discourse_topic.html"

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(DiscourseTopicPlugin)
