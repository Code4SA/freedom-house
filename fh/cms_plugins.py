from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import DiscourseTopicModel, CallToActionModel


class DiscourseTopicPlugin(CMSPluginBase):
    model = DiscourseTopicModel
    name = _("Discourse Topic")
    render_template = "discourse_topic.html"

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class CallToActionPlugin(CMSPluginBase):
    model = CallToActionModel
    name = _("Call to Action")
    render_template = "plugins/call_to_action.html"

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(DiscourseTopicPlugin)
plugin_pool.register_plugin(CallToActionPlugin)
