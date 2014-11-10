from django.views.generic import View, TemplateView
from fh.discourse import discourse_client, parse_timestamps
from fh.templatetags.mxit import discourse_url


class HomepageView(TemplateView):
    template_name = 'mxit/home.html'

    def get_context_data(self, *args, **kwargs):
        page_context = {}
        page_context['categories'] = self.get_categories()

        return page_context

    def get_categories(self):
        cats = discourse_client.categories()
        parse_timestamps(cats)
        return cats


class TopicView(TemplateView):
    template_name = 'mxit/topic.html'

    def get_context_data(self, topic_id):
        page_context = {}

        topic = self.get_topic(topic_id)
        post_stream = topic['post_stream']

        posts_by_id = dict((p['id'], p) for p in post_stream['posts'])

        posts = [posts_by_id[p] for p in post_stream['stream']]
        posts = [p for p in posts if not p['hidden']]

        page_context['topic'] = topic
        page_context['posts'] = posts
        page_context['d_topic_url'] = discourse_url('/t/%s/%s' % (topic['slug'], topic['id']))

        return page_context

    def get_topic(self, topic_id):
        cats = discourse_client.topic('', topic_id)
        parse_timestamps(cats)
        return cats
