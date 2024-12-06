# -*- coding: utf-8; -*-

from unittest import TestCase

from wuttjamaican.conf import WuttaConfig

from wuttaweb import handler as mod
from wuttaweb.menus import MenuHandler


class TestWebHandler(TestCase):

    def setUp(self):
        self.config = WuttaConfig()
        self.app = self.config.get_app()
        self.handler = mod.WebHandler(self.config)

    def test_menu_handler_default(self):
        menus = self.handler.get_menu_handler()
        self.assertIsInstance(menus, MenuHandler)
