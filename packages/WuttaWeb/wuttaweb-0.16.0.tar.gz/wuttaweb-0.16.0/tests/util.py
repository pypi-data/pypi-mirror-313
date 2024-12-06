# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import MagicMock

from pyramid import testing

from wuttjamaican.conf import WuttaConfig
from wuttjamaican.testing import FileConfigTestCase
from wuttaweb import subscribers
from wuttaweb.menus import MenuHandler


class DataTestCase(FileConfigTestCase):
    """
    Base class for test suites requiring a full (typical) database.
    """

    def setUp(self):
        self.setup_db()

    def setup_db(self):
        self.setup_files()
        self.config = WuttaConfig(defaults={
            'wutta.db.default.url': 'sqlite://',
        })
        self.app = self.config.get_app()

        # init db
        model = self.app.model
        model.Base.metadata.create_all(bind=self.config.appdb_engine)
        self.session = self.app.make_session()

    def tearDown(self):
        self.teardown_db()

    def teardown_db(self):
        self.teardown_files()


class WebTestCase(DataTestCase):
    """
    Base class for test suites requiring a full (typical) web app.
    """

    def setUp(self):
        self.setup_web()

    def setup_web(self):
        self.setup_db()
        self.request = self.make_request()
        self.pyramid_config = testing.setUp(request=self.request, settings={
            'wutta_config': self.config,
            'mako.directories': ['wuttaweb:templates'],
            'pyramid_deform.template_search_path': 'wuttaweb:templates/deform',
        })

        # init web
        self.pyramid_config.include('pyramid_deform')
        self.pyramid_config.include('pyramid_mako')
        self.pyramid_config.add_directive('add_wutta_permission_group',
                                          'wuttaweb.auth.add_permission_group')
        self.pyramid_config.add_directive('add_wutta_permission',
                                          'wuttaweb.auth.add_permission')
        self.pyramid_config.add_subscriber('wuttaweb.subscribers.before_render',
                                           'pyramid.events.BeforeRender')
        self.pyramid_config.include('wuttaweb.static')

        # setup new request w/ anonymous user
        event = MagicMock(request=self.request)
        subscribers.new_request(event)
        def user_getter(request, **kwargs): pass
        subscribers.new_request_set_user(event, db_session=self.session,
                                         user_getter=user_getter)

    def tearDown(self):
        self.teardown_web()

    def teardown_web(self):
        testing.tearDown()
        self.teardown_db()

    def make_request(self):
        return testing.DummyRequest()


class NullMenuHandler(MenuHandler):
    """
    Dummy menu handler for testing.
    """
    def make_menus(self, request, **kwargs):
        return []
