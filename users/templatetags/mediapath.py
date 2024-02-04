from django import template

register = template.Library()


@register.filter()
def mediapath(values):
    if values:
        return f'/media/{values}'
