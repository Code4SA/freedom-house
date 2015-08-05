from django.conf.urls import *  # NOQA
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
from cms.sitemaps import CMSSitemap
from fh.views import CouncillorView

admin.autodiscover()

urlpatterns = i18n_patterns('',
    # redirect root URL back to the forums
    url(r'^$', RedirectView.as_view(url=settings.SPEAKUP_DISCOURSE_URL, permanent=True), name='home'),

    url(r'^admin/', include(admin.site.urls)),  # NOQA
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^councillor/', CouncillorView.as_view(), name='councillor'),
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  # NOQA
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ) + staticfiles_urlpatterns() + urlpatterns  # NOQA
