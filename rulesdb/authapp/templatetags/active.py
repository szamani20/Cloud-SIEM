from django import template

register = template.Library()


@register.simple_tag
def active(request, url_name):
    from django.urls import resolve
    return 'is-active' if resolve(request.path_info).url_name == url_name else ''
