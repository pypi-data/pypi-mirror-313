
import requests
from django import template
from django.contrib.admin.views.main import PAGE_VAR
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from milea_base import MILEA_VARS

register = template.Library()


@register.simple_tag
def get_setting(name: str):
    """
    Prüft ob die übergebene variable in den core settings existiert
    und gibt den value aus den settings zurück.

    :param name: name of setting variable
    :return: value of setting variable
    """

    split = name.split(".")

    try:
        return MILEA_VARS[split[0]][split[1]]
    except KeyError:
        return None
    except Exception as e:
        raise e

@register.simple_tag
def milea_paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == cl.paginator.ELLIPSIS:
        return format_html("{} ", cl.paginator.ELLIPSIS)
    else:
        return format_html(
            '<li class="page-item {}"><a class="page-link" href="{}"{}>{}</a></li>',
            'active' if i == cl.page_num else '',
            cl.get_query_string({PAGE_VAR: i}),
            mark_safe(' class="end"' if i == cl.paginator.num_pages else ""),
            i,
        )

@register.simple_tag
def setvar(val=None):
    return val

@register.simple_tag
def get_random_quote():
    """
    Funktion, die das zufällige Zitat von zenquotes.io abruft

    :return: dict with quote of the day
    """
    response = requests.get("https://zenquotes.io/api/random")
    if response.status_code == 200:
        data = response.json()
        return data[0]  # return dict with q (quote) and a (author)
    else:
        return "Willkommen"
