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
Web Handler

This defines the :term:`handler` for the web layer.
"""

from wuttjamaican.app import GenericHandler


class WebHandler(GenericHandler):
    """
    Base class and default implementation for the "web" :term:`handler`.

    This is responsible for determining the "menu handler" and
    (eventually) possibly other things.
    """

    def get_menu_handler(self, **kwargs):
        """
        Get the configured "menu" handler for the web app.

        Specify a custom handler in your config file like this:

        .. code-block:: ini

           [wutta.web]
           menus.handler_spec = poser.web.menus:PoserMenuHandler

        :returns: Instance of :class:`~wuttaweb.menus.MenuHandler`.
        """
        if not hasattr(self, 'menu_handler'):
            spec = self.config.get(f'{self.appname}.web.menus.handler_spec',
                                   default='wuttaweb.menus:MenuHandler')
            self.menu_handler = self.app.load_object(spec)(self.config)
        return self.menu_handler
