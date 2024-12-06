# -*- coding: utf-8; -*-

from unittest.mock import patch

import colander
from pyramid import testing

from sqlalchemy import orm

from wuttjamaican.conf import WuttaConfig
from wuttaweb.forms import schema as mod
from wuttaweb.forms import widgets
from tests.util import DataTestCase, WebTestCase


class TestObjectNode(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.request = testing.DummyRequest(wutta_config=self.config)

    def test_dictify(self):
        model = self.app.model
        person = model.Person(full_name="Betty Boop")

        # unsupported type is converted to string
        node = mod.ObjectNode(colander.String())
        value = node.dictify(person)
        self.assertEqual(value, "Betty Boop")

        # but supported type can dictify
        node = mod.ObjectNode(mod.PersonRef(self.request))
        value = node.dictify(person)
        self.assertIs(value, person)

    def test_objectify(self):
        model = self.app.model
        person = model.Person(full_name="Betty Boop")

        # unsupported type raises error
        node = mod.ObjectNode(colander.String())
        self.assertRaises(NotImplementedError, node.objectify, person)

        # but supported type can objectify
        node = mod.ObjectNode(mod.PersonRef(self.request))
        value = node.objectify(person)
        self.assertIs(value, person)


class TestWuttaEnum(WebTestCase):

    def test_widget_maker(self):
        enum = self.app.enum
        typ = mod.WuttaEnum(self.request, enum.UpgradeStatus)
        widget = typ.widget_maker()
        self.assertIsInstance(widget, widgets.SelectWidget)


class TestObjectRef(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.request = testing.DummyRequest(wutta_config=self.config)

    def test_empty_option(self):

        # null by default
        typ = mod.ObjectRef(self.request)
        self.assertIsNone(typ.empty_option)

        # passing true yields default empty option
        typ = mod.ObjectRef(self.request, empty_option=True)
        self.assertEqual(typ.empty_option, ('', "(none)"))

        # can set explicitly
        typ = mod.ObjectRef(self.request, empty_option=('foo', 'bar'))
        self.assertEqual(typ.empty_option, ('foo', 'bar'))

        # can set just a label
        typ = mod.ObjectRef(self.request, empty_option="(empty)")
        self.assertEqual(typ.empty_option, ('', "(empty)"))

    def test_model_class(self):
        typ = mod.ObjectRef(self.request)
        self.assertRaises(NotImplementedError, getattr, typ, 'model_class')

    def test_serialize(self):
        model = self.app.model
        node = colander.SchemaNode(colander.String())

        # null
        typ = mod.ObjectRef(self.request)
        value = typ.serialize(node, colander.null)
        self.assertIs(value, colander.null)

        # model instance
        person = model.Person(full_name="Betty Boop")
        self.session.add(person)
        self.session.commit()
        self.assertIsNotNone(person.uuid)
        typ = mod.ObjectRef(self.request)
        value = typ.serialize(node, person)
        self.assertEqual(value, person.uuid)

    def test_deserialize(self):
        model = self.app.model
        node = colander.SchemaNode(colander.String())

        # null
        typ = mod.ObjectRef(self.request)
        value = typ.deserialize(node, colander.null)
        self.assertIs(value, colander.null)

        # model instance
        person = model.Person(full_name="Betty Boop")
        self.session.add(person)
        self.session.commit()
        self.assertIsNotNone(person.uuid)
        with patch.object(mod.ObjectRef, 'model_class', new=model.Person):
            typ = mod.ObjectRef(self.request, session=self.session)
            value = typ.deserialize(node, person.uuid)
            self.assertIs(value, person)

    def test_dictify(self):
        model = self.app.model
        node = colander.SchemaNode(colander.String())

        # model instance
        person = model.Person(full_name="Betty Boop")
        self.session.add(person)
        self.session.commit()
        self.assertIsNotNone(person.uuid)
        typ = mod.ObjectRef(self.request)
        value = typ.dictify(person)
        self.assertIs(value, person)

    def test_objectify(self):
        model = self.app.model
        node = colander.SchemaNode(colander.String())

        # null
        typ = mod.ObjectRef(self.request)
        value = typ.objectify(None)
        self.assertIsNone(value)

        # model instance
        person = model.Person(full_name="Betty Boop")
        self.session.add(person)
        self.session.commit()
        self.assertIsNotNone(person.uuid)
        with patch.object(mod.ObjectRef, 'model_class', new=model.Person):

            # can specify as uuid
            typ = mod.ObjectRef(self.request, session=self.session)
            value = typ.objectify(person.uuid)
            self.assertIs(value, person)

            # or can specify object proper
            typ = mod.ObjectRef(self.request, session=self.session)
            value = typ.objectify(person)
            self.assertIs(value, person)

        # error if not found
        with patch.object(mod.ObjectRef, 'model_class', new=model.Person):
            typ = mod.ObjectRef(self.request, session=self.session)
            self.assertRaises(ValueError, typ.objectify, 'WRONG-UUID')

    def test_get_query(self):
        model = self.app.model
        with patch.object(mod.ObjectRef, 'model_class', new=model.Person):
            typ = mod.ObjectRef(self.request, session=self.session)
            query = typ.get_query()
            self.assertIsInstance(query, orm.Query)

    def test_sort_query(self):
        model = self.app.model
        with patch.object(mod.ObjectRef, 'model_class', new=model.Person):
            typ = mod.ObjectRef(self.request, session=self.session)
            query = typ.get_query()
            sorted_query = typ.sort_query(query)
            self.assertIs(sorted_query, query)

    def test_widget_maker(self):
        model = self.app.model
        person = model.Person(full_name="Betty Boop")
        self.session.add(person)
        self.session.commit()

        # basic
        with patch.object(mod.ObjectRef, 'model_class', new=model.Person):
            typ = mod.ObjectRef(self.request, session=self.session)
            widget = typ.widget_maker()
            self.assertEqual(len(widget.values), 1)
            self.assertEqual(widget.values[0][1], "Betty Boop")

        # empty option
        with patch.object(mod.ObjectRef, 'model_class', new=model.Person):
            typ = mod.ObjectRef(self.request, session=self.session, empty_option=True)
            widget = typ.widget_maker()
            self.assertEqual(len(widget.values), 2)
            self.assertEqual(widget.values[0][1], "(none)")
            self.assertEqual(widget.values[1][1], "Betty Boop")


class TestPersonRef(WebTestCase):

    def test_sort_query(self):
        typ = mod.PersonRef(self.request, session=self.session)
        query = typ.get_query()
        self.assertIsInstance(query, orm.Query)
        sorted_query = typ.sort_query(query)
        self.assertIsInstance(sorted_query, orm.Query)
        self.assertIsNot(sorted_query, query)

    def test_get_object_url(self):
        self.pyramid_config.add_route('people.view', '/people/{uuid}')
        model = self.app.model
        typ = mod.PersonRef(self.request, session=self.session)

        person = model.Person(full_name="Barney Rubble")
        self.session.add(person)
        self.session.commit()

        url = typ.get_object_url(person)
        self.assertIsNotNone(url)
        self.assertIn(f'/people/{person.uuid}', url)


class TestUserRef(WebTestCase):

    def test_sort_query(self):
        typ = mod.UserRef(self.request, session=self.session)
        query = typ.get_query()
        self.assertIsInstance(query, orm.Query)
        sorted_query = typ.sort_query(query)
        self.assertIsInstance(sorted_query, orm.Query)
        self.assertIsNot(sorted_query, query)

    def test_get_object_url(self):
        self.pyramid_config.add_route('users.view', '/users/{uuid}')
        model = self.app.model
        typ = mod.UserRef(self.request, session=self.session)

        user = model.User(username='barney')
        self.session.add(user)
        self.session.commit()

        url = typ.get_object_url(user)
        self.assertIsNotNone(url)
        self.assertIn(f'/users/{user.uuid}', url)


class TestUserRefs(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.request = testing.DummyRequest(wutta_config=self.config)

    def test_widget_maker(self):
        model = self.app.model
        typ = mod.UserRefs(self.request, session=self.session)
        widget = typ.widget_maker()
        self.assertIsInstance(widget, widgets.UserRefsWidget)


class TestRoleRefs(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.request = testing.DummyRequest(wutta_config=self.config)

    def test_widget_maker(self):
        model = self.app.model
        auth = self.app.get_auth_handler()
        admin = auth.get_role_administrator(self.session)
        authed = auth.get_role_authenticated(self.session)
        anon = auth.get_role_anonymous(self.session)
        blokes = model.Role(name="Blokes")
        self.session.add(blokes)
        self.session.commit()

        # default values for widget includes all but: authed, anon
        typ = mod.RoleRefs(self.request, session=self.session)
        widget = typ.widget_maker()
        self.assertEqual(len(widget.values), 2)
        self.assertEqual(widget.values[0][1], "Administrator")
        self.assertEqual(widget.values[1][1], "Blokes")


class TestPermissions(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.request = testing.DummyRequest(wutta_config=self.config)

    def test_widget_maker(self):

        # no supported permissions
        permissions = {}
        typ = mod.Permissions(self.request, permissions)
        widget = typ.widget_maker()
        self.assertEqual(len(widget.values), 0)

        # supported permissions are morphed to values
        permissions = {
            'widgets': {
                'label': "Widgets",
                'perms': {
                    'widgets.polish': {
                        'label': "Polish the widgets",
                    },
                },
            },
        }
        typ = mod.Permissions(self.request, permissions)
        widget = typ.widget_maker()
        self.assertEqual(len(widget.values), 1)
        self.assertEqual(widget.values[0], ('widgets.polish', "Polish the widgets"))


class TestFileDownload(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.request = testing.DummyRequest(wutta_config=self.config)

    def test_widget_maker(self):

        # sanity / coverage check
        typ = mod.FileDownload(self.request, url='/foo')
        widget = typ.widget_maker()
        self.assertIsInstance(widget, widgets.FileDownloadWidget)
        self.assertEqual(widget.url, '/foo')
