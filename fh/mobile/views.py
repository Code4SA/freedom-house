import urllib
import logging

from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages

from pydiscourse.exceptions import DiscourseClientError

from fh.mobile.forms import LoginForm
from fh.discourse import discourse_client, parse_timestamps

log = logging.getLogger(__name__)

class BaseMobileView(TemplateView):
    def dispatch(self, *args, **kwargs):
        self.discourse_username = self.request.session.get('discourse_username')
        return super(BaseMobileView, self).dispatch(*args, **kwargs)

    def discourse_client(self, username=None):
        # get a discourse client impersonating this user, or
        # anonymous if they're not logged in
        username = username or self.discourse_username
        anon = not username

        return discourse_client(
                anonymous=anon,
                username=username)


class TopicListView(BaseMobileView):
    template_name = 'mobile/topic_list.html'

    def get_context_data(self, *args, **kwargs):
        page_context = {}
        page_context['categories'] = self.get_categories()

        return page_context

    def get_categories(self):
        cats = self.discourse_client().categories()
        parse_timestamps(cats)
        return cats


class TopicView(BaseMobileView):
    template_name = 'mobile/topic.html'

    def post(self, request, topic_id):
        # TODO: handle reply

        # TODO: authenticate user
        reply = request.POST.get('text', '')

        try:
            resp = self.discourse_client().create_post(reply, topic_id=topic_id)
            log.info('Posted reply: %s' % resp)
        except DiscourseClientError as e:
            log.info('Discourse rejected the reply: %s' % e.message, exc_info=e)
            messages.error(self.request, e.message)

        return redirect('m-topic', topic_id)

    def get(self, request, topic_id):
        self.context = {}

        topic = self.get_topic(topic_id)
        post_stream = topic['post_stream']
        posts_by_id = dict((p['id'], p) for p in post_stream['posts'])
        posts = [posts_by_id[p] for p in post_stream['stream']]
        posts = [p for p in posts if not p['hidden']]

        self.context['topic'] = topic
        self.context['posts'] = posts

        return self.render_to_response(self.context)

    def get_topic(self, topic_id):
        cats = self.discourse_client().topic('', topic_id)
        parse_timestamps(cats)
        return cats

class UserLoginView(BaseMobileView):
    template_name = 'mobile/user/login.html'

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            # authenticated
            request.session['discourse_username'] = form.discourse_username
            messages.info(request, 'Welcome back, %s' % form.discourse_username)
            print form.cleaned_data
            return redirect(form.cleaned_data['next'] or '/')

        return self.render_to_response({'form': form})


    def get(self, request):
        if request.session.get('discourse_username'):
            return redirect(request.GET.get('next', '/'))

        form = LoginForm()
        form.initial['next'] = request.GET.get('next', '/')

        return self.render_to_response({'form': form})
