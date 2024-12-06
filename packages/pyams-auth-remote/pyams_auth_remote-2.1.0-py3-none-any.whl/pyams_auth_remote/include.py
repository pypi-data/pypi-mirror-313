#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS remote authentication.include module

This module is used for Pyramid integration
"""

import re
import os.path

import pyams_auth_remote


__docformat__ = 'restructuredtext'


def include_package(config):
    """Pyramid package include"""

    # add translations
    config.add_translation_dirs('pyams_auth_remote:locales')

    try:
        import pyams_zmi  # pylint: disable=import-outside-toplevel,unused-import
    except ImportError:
        config.scan(ignore=[re.compile(r'pyams_auth_remote\..*\.zmi\.?.*').search])
    else:
        config.scan()

    if hasattr(config, 'load_zcml'):
        zcml_name = os.path.join(pyams_auth_remote.__path__[0], 'configure.zcml')
        if os.path.exists(zcml_name):
            config.load_zcml(zcml_name)
