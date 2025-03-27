from django import template

register = template.Library()

@register.filter
def modulo(value, arg):
    try:
        return int(value) % int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divisibleby(value, arg):
    try:
        return int(int(value) / int(arg))
    except (ValueError, TypeError):
        return 0