from django.conf.urls import url, patterns, include
from django.conf import settings

import fh.mobile.views as views

urlpatterns = patterns('',
    url(
        regex   = '^$',
        view    = views.TopicListView.as_view(),
        kwargs  = {},
        name    = 'm-topics',
    ),
    url(
        regex   = '^t/(?P<topic_id>[0-9]+)$',
        view    = views.TopicView.as_view(),
        kwargs  = {},
        name    = 'm-topic',
    ),

    # user management
    #url(
    #    regex   = '^user/new$',
    #    view    = views.UserSignupView.as_view(),
    #    kwargs  = {},
    #    name    = 'm-new-user',
    #),
    url(
        regex   = '^user/login$',
        view    = views.UserLoginView.as_view(),
        kwargs  = {},
        name    = 'm-login',
    ),
    #url(
    #    regex   = '^user/logout$',
    #    view    = views.UserLoginView.as_view(),
    #    kwargs  = {},
    #    name    = 'm-topic',
    #),
    #url('^auth/callback$', OAuthView.as_view()),
)
