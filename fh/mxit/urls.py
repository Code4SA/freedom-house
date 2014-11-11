from django.conf.urls import url, patterns, include
from django.conf import settings

from fh.mxit.views import HomepageView, TopicView

urlpatterns = patterns('',
    url(
        regex   = '^$',
        view    = HomepageView.as_view(),
        kwargs  = {},
        name    = 'mxit-home',
    ),
    url(
        regex   = '^t/(?P<topic_id>[0-9]+)$',
        view    = TopicView.as_view(),
        kwargs  = {},
        name    = 'mxit-topic',
    ),
)
