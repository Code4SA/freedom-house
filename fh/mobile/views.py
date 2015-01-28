import urllib
import logging

from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render

from pydiscourse.exceptions import DiscourseClientError

from fh.mobile.forms import LoginForm, SignupForm, ForgotPasswordForm
from fh.discourse import discourse_client, parse_timestamps

log = logging.getLogger(__name__)


def error404(request):
    return render(request, 'mobile/404.html')


class BaseMobileView(TemplateView):
    def dispatch(self, *args, **kwargs):
        self.discourse_username = self.request.session.get('discourse_username')
        return super(BaseMobileView, self).dispatch(*args, **kwargs)

    def login_url(self):
        # TODO: seriously? there's got to be a better way to build urls
        return reverse('m-login') + '?' + urllib.urlencode({'next': self.request.path})

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
        if not self.discourse_username:
            return redirect(self.login_url())

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
        if self.discourse_username:
            return redirect(request.GET.get('next', '/'))

        form = LoginForm(request.POST)

        if form.is_valid():
            # authenticated
            request.session['discourse_username'] = form.discourse_username
            messages.info(request, 'Welcome back %s' % form.discourse_username)
            return redirect(form.cleaned_data['next'] or '/')

        return self.render_to_response({'form': form})


    def get(self, request):
        if self.discourse_username:
            return redirect(request.GET.get('next', '/'))

        form = LoginForm()
        form.initial['next'] = request.GET.get('next', '/')

        return self.render_to_response({'form': form})

def user_logout(request):
    request.session.flush()
    messages.info(request, "You've been logged out.")
    return redirect('/')


class UserSignupView(BaseMobileView):
    template_name = 'mobile/user/new.html'

    def post(self, request):
        if self.discourse_username:
            return redirect(request.GET.get('next', '/'))

        form = SignupForm(request.POST)

        if form.is_valid():
            # created user
            request.session['discourse_username'] = form.discourse_username
            messages.info(request, 'Welcome %s' % form.discourse_username)
            return redirect(form.cleaned_data['next'] or '/')

        return self.render_to_response({'form': form})


    def get(self, request):
        if self.discourse_username:
            return redirect(request.GET.get('next', '/'))

        form = SignupForm()
        form.initial['next'] = request.GET.get('next', '/')

        return self.render_to_response({'form': form})


class ForgotPasswordView(BaseMobileView):
    template_name = 'mobile/user/forgot.html'

    def post(self, request):
        if self.discourse_username:
            return redirect('/')

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            # send request
            if self.discourse_client().forgot_password(form.cleaned_data['login']):
                messages.info(request, "We've sent you an email with instructions on how to reset your password.")
                return redirect('/')
            else:
                messages.info(request, "We couldn't find that username or email.")

        return self.render_to_response({'form': form})


    def get(self, request):
        if self.discourse_username:
            return redirect('/')

        form = ForgotPasswordForm()
        return self.render_to_response({'form': form})
