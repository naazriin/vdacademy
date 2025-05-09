from django import template
register = template.Library()

@register.filter
def star_rating(value):
    try:
        value = int(value) 
        stars = '★' * value + '☆' * (5 - value)  
        return stars
    except (ValueError, TypeError):
        return '☆' * 5 
    

@register.filter(name='trim')
def trim(value):

    if isinstance(value, str):
        return value.strip()
    return value


