from collections import namedtuple
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.signals import request_started
from django.http.cookie import SimpleCookie
from django.utils import six, timezone
from django.conf import settings
from easyaudit.utils import (get_client_ip, get_client_browser_info, get_client_operating_system_info)

from easyaudit.models import RequestEvent
from easyaudit.settings import UNREGISTERED_URLS, WATCH_REQUEST_EVENTS
from easyaudit.middleware.easyaudit import get_current_request, get_current_user

import re


def should_log_url(url):
    # check if current url is blacklisted
    for unregistered_url in UNREGISTERED_URLS:
        pattern = re.compile(unregistered_url)
        if pattern.match(url):
            return False
    return True


def record(name, d):
    """
    Quick and dirty implementation to convert {'META': blah} so that 
    a.META works just like a.['META']
    """
    return namedtuple(name, d.keys())(**d)


def request_started_handler(sender, environ, **kwargs):
    if not should_log_url(environ['PATH_INFO']):
        return

    # get the user from request
    user = get_current_user()
    if user and user.is_anonymous:
        user = None

    # get the user from cookies
    if not user and environ.get('HTTP_COOKIE'):
        cookie = SimpleCookie()  # python3 compatibility
        cookie.load(environ['HTTP_COOKIE'])

        session_cookie_name = settings.SESSION_COOKIE_NAME
        if session_cookie_name in cookie:
            session_id = cookie[session_cookie_name].value

            try:
                session = Session.objects.get(session_key=session_id)
            except Session.DoesNotExist:
                session = None

            if session:
                user_id = session.get_decoded().get('_auth_user_id')
                try:
                    user = get_user_model().objects.get(id=user_id)
                except:
                    user = None

    request_event = RequestEvent.objects.create(
        url=environ['PATH_INFO'],
        method=environ['REQUEST_METHOD'],
        query_string=environ['QUERY_STRING'],
        user=user,
        remote_ip=get_client_ip(record('FakeRequest', {
            'META': environ
        })),
        browser=get_client_browser_info(record('FakeRequest', {
            'META': environ
        })), 
        operating_system=get_client_operating_system_info(record('FakeRequest', {
            'META': environ
        })),
        datetime=timezone.now())


if WATCH_REQUEST_EVENTS:
    request_started.connect(
        request_started_handler,
        dispatch_uid='easy_audit_signals_request_started')
