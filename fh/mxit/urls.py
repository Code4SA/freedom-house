from django.conf.urls import url, patterns, include
from django.conf import settings

from fh.mxit.views import HomepageView

urlpatterns = patterns('',
    url(
        regex   = '^$',
        view    = HomepageView.as_view(),
        kwargs  = {},
        name    = 'mxit-home',
    ),
)
