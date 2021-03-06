from datetime import date, datetime

from django import template
from django.utils.timesince import timesince

from fh.settings import SPEAKUP_DISCOURSE_URL

register = template.Library()

@register.filter(name='avatar_url')
def avatar_url(url_template, size=20):
    return SPEAKUP_DISCOURSE_URL + url_template.replace('{size}', str(size))

@register.filter(name='short_time_ago')
def short_time_ago(value):
    if not isinstance(value, date): # datetime is a subclass of date
        return value

    value = timesince(value)
    value = value.split(',', 1)[0]
    return value\
        .replace('years', 'w')\
        .replace('year', 'y')\
        .replace('months', 'm')\
        .replace('month', 'm')\
        .replace('weeks', 'w')\
        .replace('week', 'w')\
        .replace('days', 'd')\
        .replace('day', 'd')\
        .replace('hours', 'h')\
        .replace('hour', 'h')\
        .replace('minutes', 'min')\
        .replace('minute', 'min')\
        .replace('seconds', 's')\
        .replace('second', 's')\
        .strip()

@register.filter('d_url')
def discourse_url(path, medium='mxit', campaign='mxit'):
    return SPEAKUP_DISCOURSE_URL + path + ('#utm_source=mxit&utm_medium=%s&utm_campaign=%s' % (medium, campaign))
