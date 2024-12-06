#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_auth_remote.plugin module

This module provides the remote user authentication plugin.
"""

import logging

from pyams_security.credential import Credentials
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.plugin import ICredentialsPlugin
from pyams_utils.registry import query_utility, utility_config
from pyams_utils.wsgi import wsgi_environ_cache

from pyams_auth_remote import _


LOGGER = logging.getLogger('PyAMS (remote auth)')

CREDENTIALS_ENVIRONMENT_MODE = 'environment'
CREDENTIALS_HEADER_MODE = 'header'

CREDENTIALS_MODE_KEY = 'pyams_auth_remote.mode'
CREDENTIALS_MODE_DEFAULT = 'environment'

CREDENTIALS_ENVIRON_KEY = 'pyams_auth_remote.environment_var_name'
CREDENTIALS_ENVIRON_DEFAULT = 'REMOTE_USER'

CREDENTIALS_HEADER_KEY = 'pyams_auth_remote.header_var_name'
CREDENTIALS_HEADER_DEFAULT = 'X-SSL-Client-CN'

PARSED_CREDENTIALS_ENVKEY = 'pyams_auth_remote.user_id'


@utility_config(name='remote-user', provides=ICredentialsPlugin)
class RemoteUserCredentialsPlugin:
    """Remote user credentials plug-in

    This credentials plug-in is used to extract REMOTE_USER variable
    from request environment.
    """

    prefix = 'remote'
    title = _("Remote user authentication")
    enabled = True

    @wsgi_environ_cache(PARSED_CREDENTIALS_ENVKEY, store_none=False)
    def extract_credentials(self, request, **kwargs):
        """Extract remote user ID from request environment

        Note that extracted principal ID must match a local principal login.
        """
        settings = request.registry.settings
        mode = settings.get(CREDENTIALS_MODE_KEY, CREDENTIALS_MODE_DEFAULT)
        if mode == CREDENTIALS_ENVIRONMENT_MODE:
            var_name = settings.get(CREDENTIALS_ENVIRON_KEY, CREDENTIALS_ENVIRON_DEFAULT)
            principal_id = request.environ.get(var_name)
        elif mode == CREDENTIALS_HEADER_MODE:
            var_name = settings.get(CREDENTIALS_HEADER_KEY, CREDENTIALS_HEADER_DEFAULT)
            principal_id = request.headers.get(var_name)
        else:
            principal_id = None
        if principal_id is not None:
            sm = query_utility(ISecurityManager)
            if sm is not None:
                principals = sm.find_principals(principal_id, exact_match=True)
                if len(principals) == 1:
                    principal = principals[0]
                    return Credentials(self.prefix, principal.id,
                                       pre_authenticated=True)
                if len(principals) > 1:
                    LOGGER.warning(f"Ambiguous principal ID {principal_id}: multiple match!")
        return None
