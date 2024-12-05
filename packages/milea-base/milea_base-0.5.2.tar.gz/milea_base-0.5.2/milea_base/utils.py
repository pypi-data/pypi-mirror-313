from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.admin.utils import construct_change_message
from django.contrib.contenttypes.models import ContentType

from milea_base import MILEA_VARS


def create_log_entry(user_id, obj, new, form=None, msg=None):
    """Creates a Log Entry in the django admin history"""

    change_message = msg if msg is not None else construct_change_message(form, None, True if new else False)
    if user_id is None:
        user_id = 1  # Default System User

    LogEntry.objects.log_action(
        user_id,
        ContentType.objects.get_for_model(obj.__class__).id,
        obj.id,
        str(obj),
        ADDITION if new else CHANGE,
        change_message
    )


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
