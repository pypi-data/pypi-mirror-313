# -*- coding: utf-8; -*-

from unittest import TestCase

from wuttjamaican.testing import FileConfigTestCase

from pyramid.config import Configurator
from pyramid.router import Router

from wuttaweb import app as mod
from wuttjamaican.conf import WuttaConfig


class TestWebAppProvider(TestCase):

    def test_basic(self):
        # nb. just normal usage here, confirm it does the one thing we
        # need it to..
        config = WuttaConfig()
        app = config.get_app()
        handler = app.get_web_handler()


class TestMakeWuttaConfig(FileConfigTestCase):

    def test_config_path_required(self):

        # settings must define config path, else error
        settings = {}
        self.assertRaises(ValueError, mod.make_wutta_config, settings)

    def test_basic(self):

        # mock path to config file
        myconf = self.write_file('my.conf', '')
        settings = {'wutta.config': myconf}

        # can make a config okay
        config = mod.make_wutta_config(settings)

        # and that config is also stored in settings
        self.assertIn('wutta_config', settings)
        self.assertIs(settings['wutta_config'], config)


class TestMakePyramidConfig(TestCase):

    def test_basic(self):
        settings = {}
        config = mod.make_pyramid_config(settings)
        self.assertIsInstance(config, Configurator)


class TestMain(FileConfigTestCase):

    def test_basic(self):
        global_config = None
        myconf = self.write_file('my.conf', '')
        settings = {'wutta.config': myconf}
        app = mod.main(global_config, **settings)
        self.assertIsInstance(app, Router)
