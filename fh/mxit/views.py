import urllib

from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from mxit import Mxit

from fh.discourse import discourse_client, parse_timestamps
from pydiscourse.exceptions import DiscourseClientError
from fh.templatetags.mxit import discourse_url
from fh.settings import MXIT_CLIENT_ID, MXIT_SECRET

import logging
log = logging.getLogger(__name__)

MXIT_SCOPE = 'profile/private'

def mxit_client(state=None):
    return Mxit(MXIT_CLIENT_ID, MXIT_SECRET, state=state, redirect_uri='http://mxit.speakupmzansi.org.za/auth/callback')


class MXitView(TemplateView):
    def dispatch(self, *args, **kwargs):
        self.login_mxit_user()

        log.info("MXit user id: %s" % self.mxit_id)
        log.info("MXit discourse username: %s" % self.discourse_username)
        log.info("MXit headers: %s" % self.request.META)

        # after oauth, pretend that the last page the user viewed was
        # the page they're going to go back to
        last_path = self.request.session.get('after-oauth', self.request.path)

        try:
            return super(MXitView, self).dispatch(*args, **kwargs)
        finally:
            self.request.session['last-path'] = last_path


    def login_mxit_user(self):
        """ Try to lookup the discourse userid for this mxit user, and set the
        username and user id in the session. """
        self.mxit_id = self.request.META.get('HTTP_X_MXIT_USERID_R')
        if self.mxit_id and not self.request.session.get('discourse_username'):
            user = self.discourse_client('system').mxit_user(self.mxit_id)
            if user:
                self.request.session['discourse_username'] = user['username']

        self.discourse_username = self.request.session.get('discourse_username')


    def discourse_client(self, username=None):
        # get a discourse client impersonating this user, or
        # anonymous if they're not logged in
        username = username or self.discourse_username
        anon = not username

        return discourse_client(
                anonymous=anon,
                username=username)


class OAuthView(MXitView):
    def get(self, request):
        """ OAuth callback after asking for perms to view user profile. """
        error = self.request.GET.get('error')
        code = self.request.GET.get('code')

        if error:
            # something went wrong, or the user said no
            log.info("OAuth request error: %s -- %s" % (request.GET.get('error'),
                                                        request.GET.get('error_description')))

        elif code:
            # authorized, create the mxit user
            self.create_mxit_user(code)

        try:
            url = self.request.session.pop('after-oauth')
        except KeyError:
            url = '/'

        return redirect(url)

    def create_mxit_user(self, auth_code):
        if not self.mxit_id:
            log.warn("No MXIT_USERID_R header, not authenticating.")
            return

        mxit = mxit_client()
        mxit.oauth.get_user_token(MXIT_SCOPE, auth_code)

        # get the full profile from mxit
        profile = mxit.users.get_full_profile()
        log.info("MXIT profile: %s" % profile)
        name = '%s %s' % (profile.get('FirstName', ''), profile.get('LastName', ''))

        remote_ip = self.request.META['REMOTE_ADDR']
        remote_ip = self.request.META.get('HTTP_X_FORWARDED_FOR', remote_ip).split(',')[0].strip()

        user_info = dict(
                name=name,
                email=profile['Email'],
                username=profile['DisplayName'],
                mxit_id=self.mxit_id,
                remote_ip=remote_ip,
                cellphone_number=profile['MobileNumber'])

        log.info("Creating MXit discourse user: %s" % user_info)

        # create the discourse user linked to this mxit id
        res = self.discourse_client('system').create_mxit_user(**user_info)
        log.info("Created MXIT user: %s" % res)
        if res.get('success'):
            self.login_mxit_user()


class HomepageView(MXitView):
    template_name = 'mxit/home.html'

    def get_context_data(self, *args, **kwargs):
        page_context = {}
        page_context['categories'] = self.get_categories()

        return page_context

    def get_categories(self):
        cats = self.discourse_client().categories()
        parse_timestamps(cats)
        return cats


class TopicView(MXitView):
    template_name = 'mxit/topic.html'

    def get(self, request, topic_id):
        self.topic_id = topic_id
        self.context = {}

        # is the user trying to post a reply?
        try:
            user_input = request.session.pop('mxit-input-after-oauth')
        except KeyError:
            user_input = urllib.unquote_plus(self.request.META.get('HTTP_X_MXIT_USER_INPUT', '')).strip()

        # mxit can send user input totally randomly. So ensure
        # that the last page they looked at is this topic, before
        # allowing a reply
        try:
            replies_allowed = request.path == request.session.pop('last-path')
        except KeyError:
            replies_allowed = False

        # should we care about user input?
        if replies_allowed and user_input:
            return self.handle_user_reply(user_input)

        return self.show_topic()

    def show_topic(self):
        topic = self.get_topic(self.topic_id)
        post_stream = topic['post_stream']

        posts_by_id = dict((p['id'], p) for p in post_stream['posts'])

        posts = [posts_by_id[p] for p in post_stream['stream']]
        posts = [p for p in posts if not p['hidden']]

        self.context['topic'] = topic
        self.context['posts'] = posts
        self.context['d_topic_url'] = discourse_url('/t/%s/%s' % (topic['slug'], topic['id']))

        return self.render_to_response(self.context)

    def handle_user_reply(self, reply):
        log.info("Reply: %s" % reply)

        # are they logged in?
        if not self.discourse_username:
            # go through the user creation flow
            return self.auth_and_create_mxit_user()

        # TODO: check if they're allowed to post, they might be too new, etc.
        # TODO: if we're checking they're too new, they need to browse around more

        # validate the quality of the post
        if len(reply) < 20:
            messages.error(self.request, 'Please type at least 20 characters in your reply.')
        else:
            try:
                resp = self.discourse_client().create_post(reply, topic_id=self.topic_id)
                log.info('Posted reply: %s' % resp)
            except DiscourseClientError as e:
                log.info('Discourse rejected the reply: %s' % e.message, exc_info=e)
                messages.error(self.request, e.message)

        # do a redirect to prevent re-sending the user reply data
        return redirect(self.request.path)

    def auth_and_create_mxit_user(self):
        # authorize with mxit
        self.request.session['after-oauth'] = self.request.path
        self.request.session['mxit-input-after-oauth'] = self.request.META.get('HTTP_X_MXIT_USER_INPUT')
        return redirect(mxit_client().oauth.auth_url(MXIT_SCOPE))


    def get_topic(self, topic_id):
        cats = self.discourse_client().topic('', topic_id)
        parse_timestamps(cats)
        return cats
