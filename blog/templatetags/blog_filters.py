from django import template

register = template.Library()

@register.filter(name='truncate_at_dot')
def truncate_at_dot(value):

    if isinstance(value, str):  
        return value.split('.')[0]
    return value  
