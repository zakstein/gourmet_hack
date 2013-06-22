from django.shortcuts import render_to_response as real_render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template.context import RequestContext
from django.http import HttpRequest
from django.conf import settings

@csrf_protect
def render_to_response(*args, **kwargs):
    if len(args) > 0 and not isinstance(args[0], HttpRequest):
        return real_render_to_response(*args, **kwargs)
    if not kwargs.get('context_instance', None):
        kwargs['context_instance'] = RequestContext(args[0])

    # Add common vars to dictionary
    if isinstance(args[-1], dict):
        # args[-1]['JS_ROOT'] = settings.JS_ROOT
        # args[-1]['CSS_ROOT'] = settings.CSS_ROOT
        pass

    return real_render_to_response(*args[1:], **kwargs)
