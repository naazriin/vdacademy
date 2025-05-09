from django import template

register = template.Library()

@register.filter
def to_range(value):
    return range(int(value))

@register.filter
def times(number):
    return range(number)