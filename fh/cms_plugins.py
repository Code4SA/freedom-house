from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_pool import toolbar_pool
from django.utils.translation import ugettext_lazy as _

from .models import DiscourseTopicModel, CallToActionModel, SpeakupPageExtension


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


@toolbar_pool.register
class SpeakupPageExtensionToolbar(ExtensionToolbar):
    # defineds the model for the current toolbar
    model = SpeakupPageExtension

    def populate(self):
        # setup the extension toolbar with permissions and sanity checks
        current_page_menu = self._setup_extension_toolbar()
        # if it's all ok
        if current_page_menu:
            # retrieves the instance of the current extension (if any) and the toolbar item URL
            page_extension, url = self.get_page_extension_admin()
            if url:
                # adds a toolbar item
                current_page_menu.add_modal_item(_('Speak Up Page Settings'), url=url, disabled=not self.toolbar.edit_mode)
