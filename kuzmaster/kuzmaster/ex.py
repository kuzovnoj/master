from django import template

register = template.Library()

# здесь продолжайте программу

@register.inclusion_tag('women/mainmenu.html')
def show_list(items=None):
    return {'items': items}