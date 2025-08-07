from django import template


register = template.Library()


@register.filter
def subtract(value, arg):
    try:
        return value - arg
    except:
        return None


@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except:
        return None