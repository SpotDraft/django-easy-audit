from __future__ import unicode_literals
from django.utils.encoding import smart_text
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import NOT_PROVIDED, DateTimeField
from django.utils import timezone
from ipware import get_client_ip as _get_client_ip
from user_agents import parse


def get_field_value(obj, field):
    """
    Gets the value of a given model instance field.
    :param obj: The model instance.
    :type obj: Model
    :param field: The field you want to find the value of.
    :type field: Any
    :return: The value of the field as a string.
    :rtype: str
    """
    if isinstance(field, DateTimeField):
        # DateTimeFields are timezone-aware, so we need to convert the field
        # to its naive form before we can accuratly compare them for changes.
        try:
            value = field.to_python(getattr(obj, field.name, None))
            if value is not None and settings.USE_TZ and not timezone.is_naive(value):
                value = timezone.make_naive(value, timezone=timezone.utc)
        except ObjectDoesNotExist:
            value = field.default if field.default is not NOT_PROVIDED else None
    else:
        try:
            value = smart_text(getattr(obj, field.name, None))
        except ObjectDoesNotExist:
            value = field.default if field.default is not NOT_PROVIDED else None

    return value


def model_delta(old_model, new_model):
    """
    Provides delta/difference between two models
    :param old: The old state of the model instance.
    :type old: Model
    :param new: The new state of the model instance.
    :type new: Model
    :return: A dictionary with the names of the changed fields as keys and a
             two tuple of the old and new field values
             as value.
    :rtype: dict
    """

    delta = {}
    fields = new_model._meta.fields
    for field in fields:
        old_value = get_field_value(old_model, field)
        new_value = get_field_value(new_model, field)
        if old_value != new_value:
            delta[field.name] = [smart_text(old_value),
                                 smart_text(new_value)]

    if len(delta) == 0:
        delta = None

    return delta


def get_client_ip(request):
    if not request:
        return None
    return _get_client_ip(request)[0]

def get_client_browser_info(request):
    """
    Returns user browser info in following format :
    name-version
    """
    if not request:
        return None
    user_agent_string = request.META['HTTP_USER_AGENT']
    parsed_user_agent_string = parse(user_agent_string)

    return '-'.join([parsed_user_agent_string.browser.family, parsed_user_agent_string.browser.version_string])


def get_client_operating_system_info(request):
    """
    Returns User Operating System info in following format :
    name-version
    """
    if not request:
        return None
    user_agent_string = request.META['HTTP_USER_AGENT']
    parsed_user_agent_string = parse(user_agent_string)

    return ' '.join([parsed_user_agent_string.os.family, parsed_user_agent_string.os.version_string])
