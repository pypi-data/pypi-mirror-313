from django.apps import apps
from django.template import Library
from django.utils.text import slugify

from milea_base import MILEA_VARS

register = Library()

@register.simple_tag
def app_additional_config(app):
    """
    Get additional infos from the app config and build a second level menu
    """

    menu_icon = "ti ti-package"  # Default Icon
    menu_firstlevel = list()
    menu_secondlevel = list()
    menu_others = False  # Special menu for config apps defined in MILEA_VARS
    app_config = apps.get_app_config(app['app_label'])

    # Menu icon
    if hasattr(app_config, 'menu_icon'):
        menu_icon = getattr(app_config, 'menu_icon')

    # Default Menu
    if not hasattr(app_config, 'menu_firstlvl') and not hasattr(app_config, 'menu_secondlvl'):
        menu_firstlevel = app['models']

    # First Level Menu
    if hasattr(app_config, 'menu_firstlvl'):
        for menu in getattr(app_config, 'menu_firstlvl'):
            for item in app['models']:
                if item['object_name'] in menu:
                    menu_firstlevel.append(item)

    # Second Lvl Menu
    if hasattr(app_config, 'menu_secondlvl'):
        for menu in getattr(app_config, 'menu_secondlvl'):
            menu_tmp = dict(name=menu[0], key=slugify(menu[0]), models=[])
            for item in app['models']:
                if item['object_name'] in menu[1]:
                    menu_tmp['models'].append(item)
            if len(menu_tmp['models']) > 0:
                menu_secondlevel.append(menu_tmp)

    # Config Menu
    if app_config.name in MILEA_VARS['milea_base']['MENUOTHERS']:
        menu_others = True

    r = dict(
        menu_icon=menu_icon,
        menu_firstlevel=menu_firstlevel,
        menu_secondlevel=menu_secondlevel,
        menu_others=menu_others
    )

    return r


@register.simple_tag
def sort_app_list(app_list):
    # Get the order value from settings var
    order = MILEA_VARS['milea_base']['MENUORDER']

    # Create a dictionary mapping app_labels to app_dicts
    app_dict = {app['app_label']: app for app in app_list}

    # Sort the app_list based on the 'order' list
    sorted_app_list = [app_dict[label] for label in order if label in app_dict]

    # Add apps not included in 'order' to the end of the list
    apps_not_in_order = [app for app in app_list if app['app_label'] not in order]
    sorted_app_list.extend(apps_not_in_order)

    return sorted_app_list

@register.simple_tag
def has_others(app_list):
    """Check if user has rights for apps in others menu"""
    for app in app_list:
        if app['app_label'] in MILEA_VARS['milea_base']['MENUOTHERS']:
            return True
    return False
