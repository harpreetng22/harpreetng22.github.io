from django import template

register = template.Library()
@register.simple_tag
def converter(value):
    return str(value)
