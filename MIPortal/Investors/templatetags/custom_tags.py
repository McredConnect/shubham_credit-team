from datetime import datetime, date
from django import template

register = template.Library()


@register.filter
def days_until(date1):
    delta = date1 - date.today()
    return delta.days


@register.filter(name='subtract')
def subtract(value, arg):
    return round((value - arg), 2)
