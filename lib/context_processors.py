import urllib

from django.conf import settings
from django.core.urlresolvers import reverse

def google_analytics(request):
    """
    Add the Google Analytics tracking ID and domain to the context for use when
    rendering tracking code.
    """
    ga_tracking_id = getattr(settings, 'GOOGLE_ANALYTICS_TRACKING_ID', False)
    ga_domain = getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', False)
    if not settings.DEBUG and ga_tracking_id and ga_domain:
        return {
            'GOOGLE_ANALYTICS_TRACKING_ID': ga_tracking_id,
            'GOOGLE_ANALYTICS_DOMAIN': ga_domain,
        }
    return {}

def speakup(request):
    """
    Add Speak Up Mzansi related config into the context.
    """
    return {
        'SPEAKUP_DISCOURSE_URL': getattr(settings, 'SPEAKUP_DISCOURSE_URL', '/'),
        'SPEAKUP_INFO_URL': getattr(settings, 'SPEAKUP_INFO_URL', '/'),
    }

def mobile(request):
    """
    Add Mobile-related config to the context.
    """
    return {
        'is_logged_in': request.session.get('discourse_username') is not None,
        'discourse_username': request.session.get('discourse_username'),
        'login_url': reverse('m-login') + '?' + urllib.urlencode({'next': request.path})
    }
