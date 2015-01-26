from django.conf.urls import url, patterns, include
from django.conf import settings

from fh.mobile.views import TopicListView, TopicView#, OAuthView

urlpatterns = patterns('',
    url(
        regex   = '^$',
        view    = TopicListView.as_view(),
        kwargs  = {},
        name    = 'm-topics',
    ),
    url(
        regex   = '^t/(?P<topic_id>[0-9]+)$',
        view    = TopicView.as_view(),
        kwargs  = {},
        name    = 'm-topic',
    ),
    #url('^auth/callback$', OAuthView.as_view()),
)
