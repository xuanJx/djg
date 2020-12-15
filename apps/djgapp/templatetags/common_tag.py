import datetime
from django.conf import settings
from django.templatetags.static import StaticNode, do_static
from django import template
from ..utils import set_url_parameter

register = template.Library()

class StaticNodeRdm(StaticNode):
    @classmethod
    def handle_simple(cls, path):
        url = super().handle_simple(path)
        return set_url_parameter(url, '_v', datetime.datetime.now().timestamp())

@register.tag(name='staticCache')
def static_cache(parser, token):
    if settings.DEBUG:
        return StaticNodeRdm.handle_token(parser, token)
    return do_static(parser, token)