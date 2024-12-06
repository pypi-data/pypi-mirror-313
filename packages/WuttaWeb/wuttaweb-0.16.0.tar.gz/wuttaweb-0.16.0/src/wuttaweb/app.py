# -*- coding: utf-8; -*-
################################################################################
#
#  wuttaweb -- Web App for Wutta Framework
#  Copyright © 2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Application
"""

import os

from wuttjamaican.app import AppProvider
from wuttjamaican.conf import make_config

from pyramid.config import Configurator

import wuttaweb.db
from wuttaweb.auth import WuttaSecurityPolicy


class WebAppProvider(AppProvider):
    """
    The :term:`app provider` for WuttaWeb.  This adds some methods to
    the :term:`app handler`, which are specific to web apps.
    """
    email_templates = 'wuttaweb:email/templates'

    def get_web_handler(self, **kwargs):
        """
        Get the configured "web" handler for the app.

        Specify a custom handler in your config file like this:

        .. code-block:: ini

           [wutta]
           web.handler_spec = poser.web.handler:PoserWebHandler

        :returns: Instance of :class:`~wuttaweb.handler.WebHandler`.
        """
        if 'web_handler' not in self.__dict__:
            spec = self.config.get(f'{self.appname}.web.handler_spec',
                                   default='wuttaweb.handler:WebHandler')
            self.web_handler = self.app.load_object(spec)(self.config)
        return self.web_handler


def make_wutta_config(settings, config_maker=None, **kwargs):
    """
    Make a WuttaConfig object from the given settings.

    Note that ``settings`` dict will (typically) correspond to the
    ``[app:main]`` section of your config file.

    Regardless, the ``settings`` must contain a special key/value
    which is needed to identify the location of the config file.
    Assuming the typical scenario then, your config file should have
    an entry like this:

    .. code-block:: ini

       [app:main]
       wutta.config = %(__file__)s

    The ``%(__file__)s`` is auto-replaced with the config file path,
    so ultimately ``settings`` would contain something like (at
    minimum)::

       {'wutta.config': '/path/to/config/file'}

    If this config file path cannot be discovered, an error is raised.
    """
    # validate config file path
    path = settings.get('wutta.config')
    if not path or not os.path.exists(path):
        raise ValueError("Please set 'wutta.config' in [app:main] "
                         "section of config to the path of your "
                         "config file.  Lame, but necessary.")

    # make config, add to settings
    config_maker = config_maker or make_config
    wutta_config = config_maker(path, **kwargs)
    settings['wutta_config'] = wutta_config

    # configure database sessions
    if hasattr(wutta_config, 'appdb_engine'):
        wuttaweb.db.Session.configure(bind=wutta_config.appdb_engine)

    return wutta_config


def make_pyramid_config(settings):
    """
    Make and return a Pyramid config object from the given settings.

    The config is initialized with certain features deemed useful for
    all apps.

    :returns: Instance of
       :class:`pyramid:pyramid.config.Configurator`.
    """
    settings.setdefault('fanstatic.versioning', 'true')
    settings.setdefault('mako.directories', ['wuttaweb:templates'])
    settings.setdefault('pyramid_deform.template_search_path',
                        'wuttaweb:templates/deform')

    pyramid_config = Configurator(settings=settings)

    # configure user authorization / authentication
    pyramid_config.set_security_policy(WuttaSecurityPolicy())

    # require CSRF token for POST
    pyramid_config.set_default_csrf_options(require_csrf=True,
                                            token='_csrf',
                                            header='X-CSRF-TOKEN')

    pyramid_config.include('pyramid_beaker')
    pyramid_config.include('pyramid_deform')
    pyramid_config.include('pyramid_fanstatic')
    pyramid_config.include('pyramid_mako')
    pyramid_config.include('pyramid_tm')

    # add some permissions magic
    pyramid_config.add_directive('add_wutta_permission_group',
                                 'wuttaweb.auth.add_permission_group')
    pyramid_config.add_directive('add_wutta_permission',
                                 'wuttaweb.auth.add_permission')

    return pyramid_config


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.

    Typically there is no need to call this function directly, but it
    may be configured as the web app entry point like so:

    .. code-block:: ini

       [app:main]
       use = egg:wuttaweb

    The app returned by this function is quite minimal, so most apps
    will need to define their own ``main()`` function, and use that
    instead.
    """
    wutta_config = make_wutta_config(settings)
    pyramid_config = make_pyramid_config(settings)

    pyramid_config.include('wuttaweb.static')
    pyramid_config.include('wuttaweb.subscribers')
    pyramid_config.include('wuttaweb.views')

    return pyramid_config.make_wsgi_app()
