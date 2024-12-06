===================================
PyAMS remote authentication package
===================================


Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.
It's an extension to PyAMS_security, which allows extraction of user's credentials from REMOTE_USER
environment variable, which can be set for example by Apache mod_ssl module from incoming
client certificate.

    >>> import pprint

    >>> from pyramid.testing import tearDown, DummyRequest
    >>> from pyams_security.tests import setup_tests_registry
    >>> config = setup_tests_registry()
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_mail import includeme as include_mail
    >>> include_mail(config)
    >>> from pyams_site import includeme as include_site
    >>> include_site(config)
    >>> from pyams_security import includeme as include_security
    >>> include_security(config)
    >>> from pyams_auth_remote import includeme as include_auth_remote
    >>> include_auth_remote(config)

    >>> from pyams_utils.registry import get_utility, set_local_registry
    >>> registry = config.registry
    >>> set_local_registry(registry)

    >>> from pyams_site.generations import upgrade_site
    >>> request = DummyRequest()
    >>> app = upgrade_site(request)
    Upgrading PyAMS timezone to generation 1...
    Upgrading PyAMS security to generation 2...

    >>> from zope.traversing.interfaces import BeforeTraverseEvent
    >>> from pyams_utils.registry import handle_site_before_traverse
    >>> handle_site_before_traverse(BeforeTraverseEvent(app, request))

    >>> from pyams_security.interfaces import ISecurityManager
    >>> sm = get_utility(ISecurityManager)

    >>> from pyams_security.interfaces.plugin import ICredentialsPlugin
    >>> plugin = get_utility(ICredentialsPlugin, name='remote-user')


Using PyAMS security policy
---------------------------

The plugin should be included correctly into PyAMS security policy:

    >>> from pyams_security.policy import PyAMSSecurityPolicy
    >>> policy = PyAMSSecurityPolicy(secret='my secret',
    ...                              http_only=True,
    ...                              secure=False)
    >>> config.set_security_policy(policy)

Getting effective principals via security policy require a Beaker cache:

    >>> from beaker.cache import CacheManager, cache_regions
    >>> cache = CacheManager(**{'cache.type': 'memory'})
    >>> cache_regions.update({'short': {'type': 'memory', 'expire': 0}})
    >>> cache_regions.update({'long': {'type': 'memory', 'expire': 0}})

    >>> plugin in sm.credentials_plugins
    True
    >>> plugin in sm.authentication_plugins
    False
    >>> plugin in sm.directory_plugins
    False


Extracting credentials from request
-----------------------------------

The main feature of this plugin is to extract credentials from request environment:

    >>> import base64

    >>> request = DummyRequest(environ={'REMOTE_USER': 'system:admin'}, registry=config.registry)
    >>> policy.authenticated_userid(request) is None
    True

Why the remote user principal isn't authenticated? Because it must match with another principal
available into one of our security manager directory plugins!

    >>> request = DummyRequest(environ={'REMOTE_USER': 'admin'}, registry=config.registry)
    >>> creds = plugin.extract_credentials(request, authenticate=False)
    >>> creds
    <pyams_security.credential.Credentials object at 0x...>
    >>> creds.prefix
    'remote'
    >>> creds.id
    'system:admin'
    >>> creds.attributes
    {'pre_authenticated': True}

Providing a request without authorization, or a bad encoded authorization header, should return
None:

    >>> request = DummyRequest()
    >>> creds = plugin.extract_credentials(request)
    >>> creds is None
    True

    >>> request = DummyRequest(headers={'Authorization': 'Basic not encoded'})
    >>> creds = plugin.extract_credentials(request)
    >>> creds is None
    True

You can also store the certificate CN into a request header, for example using Apache *mod_header* extension:

    >>> from pyams_auth_remote.plugin import CREDENTIALS_MODE_KEY, CREDENTIALS_HEADER_MODE, CREDENTIALS_HEADER_DEFAULT

    >>> config.registry.settings[CREDENTIALS_MODE_KEY] = CREDENTIALS_HEADER_MODE
    >>> request = DummyRequest(headers={CREDENTIALS_HEADER_DEFAULT: 'admin'}, registry=config.registry)

    >>> creds = plugin.extract_credentials(request, authenticate=False)
    >>> creds is None
    False
    >>> creds.id
    'system:admin'
    >>> creds.attributes
    {'pre_authenticated': True}


Tests cleanup:

    >>> tearDown()
