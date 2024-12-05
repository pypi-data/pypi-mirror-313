from django import template

register = template.Library()

@register.simple_tag
def split_filter_value(value):
    # Teilt den String am letzten Leerzeichen vor der Klammer
    parts = value.rsplit(' ', 1)
    if len(parts) == 2 and parts[1].startswith('(') and parts[1].endswith(')'):
        # Entfernt die Klammern aus dem zweiten Teil
        parts[1] = parts[1][1:-1]
        return parts
    return value, ''
