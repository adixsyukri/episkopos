from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from kotti import get_settings
from kotti.security import get_principals
from kotti.views.login import login_success_callback
from kotti.views.login import _find_user

import json
import velruse
from uuid import uuid4
from datetime import datetime
from episkopos import _

@view_config(context='velruse.AuthenticationComplete')
def login_complete_view(request):
    context = request.context
    came_from = request.session.pop('came_from')
    result = {
        'provider_type': context.provider_type,
        'provider_name': context.provider_name,
        'profile': context.profile,
        'credentials': context.credentials,
    }
    user = get_principals().search(
            email=result['profile']['verifiedEmail']).first()
    if user:
        return login_success_callback(request, user, came_from)

    request.session['velruse.credentials'] = result
    return HTTPFound(request.application_url + 
                    '/set_username?came_from=' + came_from)

@view_config(name='set_username',
            renderer='episkopos:templates/set_username.pt')
def set_username(context, request):
    came_from = request.params.get('came_from', request.resource_url(context))
    login = (request.params.get('login') or '').strip()
    if login and not get_principals().search(name=login).first():
        cred = request.session.pop('velruse.credentials')
        appstruct = {
            'name': login,
            'password': uuid4().hex,
            'title': cred['profile']['displayName'],
            'email': cred['profile']['verifiedEmail'],
            'active': True,
            'confirm_token': None,
            'groups': None
        }
        get_principals()[login] = appstruct
        return login_success_callback(request, 
                get_principals()[login], came_from)
    elif login and get_principals().search(name=login).first():
        request.session.flash(_(u"Username already taken."), 'error')
    return {'url': request.url, 'came_from': came_from}

@view_config(name='login')
def login(context, request):
    request.session['came_from'] = request.params.get(
                    'came_from', request.resource_url(context))
    return HTTPFound(velruse.login_url(request, 'google'))


@view_config(name='pwd_login', renderer='episkopos:templates/login.pt')
def pwd_login(context, request):
    """
    Login view.  Renders either the login or password forgot form templates or
    handles their form submission and redirects to came_from on success.

    :result: Either a redirect response or a dictionary passed to the template
             for rendering
    :rtype: pyramid.httpexceptions.HTTPFound or dict
    """

    principals = get_principals()

    came_from = request.params.get(
        'came_from', request.resource_url(context))
    login, password = u'', u''

    if 'submit' in request.POST:
        login = request.params['login'].lower()
        password = request.params['password']
        user = _find_user(login)

        if (user is not None and user.active and
                principals.validate_password(password, user.password)):
            return get_settings()['kotti.login_success_callback'][0](
                request, user, came_from)
        request.session.flash(_(u"Login failed."), 'error')

    if 'reset-password' in request.POST:
        login = request.params['login']
        user = _find_user(login)
        if user is not None and user.active:
            return get_settings()['kotti.reset_password_callback'][0](
                request, user)
        else:
            request.session.flash(
                _(u"That username or email is not known by this system."),
                'error')

    return {
        'url': request.application_url + '/@@pwd_login',
        'came_from': came_from,
        'login': login,
        'password': password,
    }

