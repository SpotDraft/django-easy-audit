from django.contrib import admin

try: # Django 2.0
    from django.urls import reverse
except: # Django < 2.0
    from django.core.urlresolvers import reverse

from django.utils.safestring import mark_safe
from . import settings
from .models import CRUDEvent, LoginEvent, RequestEvent
from .admin_helpers import prettify_json, EasyAuditModelAdmin


# CRUD events
class CRUDEventAdmin(EasyAuditModelAdmin):
    list_display = ['get_event_type_display', 'content_type', 'object_id', 'object_repr_link', 'user_link', 'datetime', 'remote_ip', 'browser', 'operating_system']
    date_hierarchy = 'datetime'
    list_filter = ['event_type', 'content_type', 'user', 'datetime', ]
    search_fields = ['=object_id', 'object_json_repr', ]
    readonly_fields = ['event_type', 'object_id', 'content_type',
                       'object_repr', 'object_json_repr_prettified', 'user',
                       'user_pk_as_string', 'datetime', 'changed_fields_prettified', 'remote_ip', 'browser', 'operating_system']
    exclude = ['object_json_repr', 'changed_fields']

    def object_repr_link(self, obj):
        if obj.event_type == CRUDEvent.DELETE:
            html = obj.object_repr
        else:
            try:
                url = reverse("admin:%s_%s_change" % (
                    obj.content_type.app_label,
                    obj.content_type.model,
                ), args=(obj.object_id,))
                html = '<a href="%s">%s</a>' % (url, obj.object_repr)
            except:
                html = obj.object_repr
        return mark_safe(html)

    object_repr_link.short_description = 'object repr'

    def object_json_repr_prettified(self, obj):
        return prettify_json(obj.object_json_repr)

    object_json_repr_prettified.short_description = 'object json repr'

    def changed_fields_prettified(self, obj):
        return prettify_json(obj.changed_fields)

    changed_fields_prettified.short_description = 'changed fields'


if settings.ADMIN_SHOW_MODEL_EVENTS:
    admin.site.register(CRUDEvent, CRUDEventAdmin)


# Login events
class LoginEventAdmin(EasyAuditModelAdmin):
    list_display = ['datetime', 'get_login_type_display', 'user_link', 'username', 'remote_ip', 'browser', 'operating_system']
    date_hierarchy = 'datetime'
    list_filter = ['login_type', 'user', 'datetime', ]
    search_fields = ['=remote_ip', 'username', ]
    readonly_fields = ['login_type', 'username', 'user', 'remote_ip', 'datetime',  'browser', 'operating_system']


if settings.ADMIN_SHOW_AUTH_EVENTS:
    admin.site.register(LoginEvent, LoginEventAdmin)


# Request events
class RequestEventAdmin(EasyAuditModelAdmin):
    list_display = ['datetime', 'user_link', 'method', 'url', 'remote_ip' , 'browser', 'operating_system']
    date_hierarchy = 'datetime'
    list_filter = ['method', 'user', 'datetime', ]
    search_fields = ['=remote_ip', 'username', 'url', 'query_string', ]
    readonly_fields = ['url', 'method', 'query_string', 'user', 'remote_ip', 'datetime' , 'browser', 'operating_system']


if settings.ADMIN_SHOW_REQUEST_EVENTS:
    admin.site.register(RequestEvent, RequestEventAdmin)
