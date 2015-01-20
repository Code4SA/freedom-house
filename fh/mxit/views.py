from django.views.generic import View, TemplateView
from django.shortcuts import redirect
from django.http import HttpResponse
from mxit import Mxit

from fh.discourse import discourse_client, parse_timestamps
from fh.templatetags.mxit import discourse_url
from fh.settings import MXIT_CLIENT_ID, MXIT_SECRET

import logging
log = logging.getLogger(__name__)

MXIT_SCOPE = 'profile/private'

def mxit_client(state=None):
    return Mxit(MXIT_CLIENT_ID, MXIT_SECRET, state=state, redirect_uri='http://mxit.speakupmzansi.org.za/auth/callback')


class OAuthView(View):
    def get(self, request):
        """ OAuth callback after asking for perms to view user profile. """
        error = self.request.GET.get('error')
        code = self.request.GET.get('code')

        if error:
            # something went wrong, or the user said no
            log.info("OAuth request error: %s -- %s" % (request.GET.get('error'),
                                                        request.GET.get('error_description')))

        elif code:
            # authorized, get the auth token from mxit
            code = self.request.GET.get('code')
            self.auth_token = mxit_client().oauth.get_user_token(MXIT_SCOPE, code)
            self.create_mxit_user()

        url = self.request.session.get('after-oauth', '/')
        return redirect(url)

    def create_mxit_user(self):
        mxit_id = self.request.META.get('HTTP_X_MXIT_USERID_R')
        if not mxit_id:
            log.warn("No MXIT_USERID_R header, not authenticating.")
            return

        # get the full profile from mxit
        profile = mxit_client().users.get_full_profile(mxit_id, self.auth_token)
        name = '%s %s' % (profile.get('FirstName', ''), profile.get('LastName', ''))

        log.info("Creating MXIT user: %s" % profile)

        # create the discourse user linked to this mxit id
        user = discourse_client().create_mxit_user({
            'name': name,
            'email': profile['Email'],
            'username': profile['DisplayName'],
            'mxit_userid': mxit_id,
            })


class HomepageView(TemplateView):
    template_name = 'mxit/home.html'

    def get_context_data(self, *args, **kwargs):
        log.debug(self.request.META)

        page_context = {}
        page_context['categories'] = self.get_categories()

        return page_context

    def get_categories(self):
        cats = discourse_client(anonymous=True).categories()
        parse_timestamps(cats)
        return cats


class TopicView(TemplateView):
    template_name = 'mxit/topic.html'

    def get(self, request, topic_id):
        self.topic_id = topic_id
        self.context = {}

        log.debug(self.request.META)

        # is the user trying to post a reply?
        user_input = self.request.META.get('HTTP_X_MXIT_USER_INPUT', '').strip()
        if user_input:
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
        # check if they're a registered user
        mxit_id = self.request.META.get('HTTP_X_MXIT_USERID_R')
        user = discourse_client().mxit_user(mxit_id)
        if not user:
            # go through the user creation flow
            return self.auth_and_create_mxit_user(mxit_id)

        # TODO: check if they're allowed to post, they might be too new, etc.
        # TODO: if we're checking they're too new, they need to browse around more

        # validate the quality of the post
        if len(user_input) < 20:
            self.context['flash'] = 'Please type at least 20 characters in your reply.'
        else:
            # TODO: post the reply
            pass

        # TODO: do a redirect?
        return self.show_topic()

    def auth_and_create_mxit_user(self, mxit_id):
        # authorize with mxit
        self.request.session['after-oauth'] = self.request.path
        self.request.session['mxit-input'] = self.request.META.get('HTTP_X_MXIT_USER_INPUT')
        return redirect(mxit_client().oauth.auth_url(MXIT_SCOPE))


    def get_topic(self, topic_id):
        cats = discourse_client(anonymous=True).topic('', topic_id)
        parse_timestamps(cats)
        return cats
