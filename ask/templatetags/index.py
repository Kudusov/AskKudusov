from django import template
import re
register = template.Library()


@register.filter
def index(List, i):
    return List[int(i)]


@register.filter
def catslug(line):
    result = re.findall(r'\d+', line)
    return result[-1]


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)
