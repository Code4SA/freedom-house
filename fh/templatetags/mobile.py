from datetime import date, datetime

from django import template
from django.utils.timesince import timesince

from fh.settings import SPEAKUP_DISCOURSE_URL

register = template.Library()

@register.filter(name='avatar_url')
def avatar_url(url_template, size=20):
    return SPEAKUP_DISCOURSE_URL + url_template.replace('{size}', str(size))
