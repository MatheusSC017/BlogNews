from django import template

register = template.Library()


@register.filter()
def to_int(value):
    try:
        return int(value)
    except TypeError:
        return 0
