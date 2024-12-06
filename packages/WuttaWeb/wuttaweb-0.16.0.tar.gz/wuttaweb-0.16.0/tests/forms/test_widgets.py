# -*- coding: utf-8; -*-

from unittest.mock import patch

import colander
import deform
from pyramid import testing

from wuttaweb.forms import widgets as mod
from wuttaweb.forms.schema import FileDownload, PersonRef, RoleRefs, UserRefs, Permissions
from tests.util import WebTestCase


class TestObjectRefWidget(WebTestCase):

    def make_field(self, node, **kwargs):
        # TODO: not sure why default renderer is in use even though
        # pyramid_deform was included in setup?  but this works..
        kwargs.setdefault('renderer', deform.Form.default_renderer)
        return deform.Field(node, **kwargs)

    def make_widget(self, **kwargs):
        return mod.ObjectRefWidget(self.request, **kwargs)

    def test_serialize(self):
        model = self.app.model
        person = model.Person(full_name="Betty Boop")
        self.session.add(person)
        self.session.commit()

        # standard (editable)
        node = colander.SchemaNode(PersonRef(self.request, session=self.session))
        widget = self.make_widget()
        field = self.make_field(node)
        html = widget.serialize(field, person.uuid)
        self.assertIn('<b-select ', html)

        # readonly
        node = colander.SchemaNode(PersonRef(self.request, session=self.session))
        node.model_instance = person
        widget = self.make_widget()
        field = self.make_field(node)
        html = widget.serialize(field, person.uuid, readonly=True)
        self.assertIn('Betty Boop', html)
        self.assertNotIn('<a', html)

        # with hyperlink
        node = colander.SchemaNode(PersonRef(self.request, session=self.session))
        node.model_instance = person
        widget = self.make_widget(url=lambda p: '/foo')
        field = self.make_field(node)
        html = widget.serialize(field, person.uuid, readonly=True)
        self.assertIn('Betty Boop', html)
        self.assertIn('<a', html)
        self.assertIn('href="/foo"', html)

    def test_get_template_values(self):
        model = self.app.model
        person = model.Person(full_name="Betty Boop")
        self.session.add(person)
        self.session.commit()

        node = colander.SchemaNode(PersonRef(self.request, session=self.session))
        widget = self.make_widget()
        field = self.make_field(node)
        values = widget.get_template_values(field, person.uuid, {})
        self.assertIn('cstruct', values)
        self.assertNotIn('url', values)


class TestFileDownloadWidget(WebTestCase):

    def make_field(self, node, **kwargs):
        # TODO: not sure why default renderer is in use even though
        # pyramid_deform was included in setup?  but this works..
        kwargs.setdefault('renderer', deform.Form.default_renderer)
        return deform.Field(node, **kwargs)

    def test_serialize(self):

        # nb. we let the field construct the widget via our type
        # (nb. at first we do not provide a url)
        node = colander.SchemaNode(FileDownload(self.request))
        field = self.make_field(node)
        widget = field.widget

        # null value
        html = widget.serialize(field, None, readonly=True)
        self.assertNotIn('<a ', html)
        self.assertIn('<span>', html)

        # path to nonexistent file
        html = widget.serialize(field, '/this/path/does/not/exist', readonly=True)
        self.assertNotIn('<a ', html)
        self.assertIn('<span>', html)

        # path to actual file
        datfile = self.write_file('data.txt', "hello\n" * 1000)
        html = widget.serialize(field, datfile, readonly=True)
        self.assertNotIn('<a ', html)
        self.assertIn('<span>', html)
        self.assertIn('data.txt', html)
        self.assertIn('kB)', html)

        # path to file, w/ url
        node = colander.SchemaNode(FileDownload(self.request, url='/download/blarg'))
        field = self.make_field(node)
        widget = field.widget
        html = widget.serialize(field, datfile, readonly=True)
        self.assertNotIn('<span>', html)
        self.assertIn('<a href="/download/blarg">', html)
        self.assertIn('data.txt', html)
        self.assertIn('kB)', html)

        # nb. same readonly output even if we ask for editable
        html2 = widget.serialize(field, datfile, readonly=False)
        self.assertEqual(html2, html)


class TestRoleRefsWidget(WebTestCase):

    def make_field(self, node, **kwargs):
        # TODO: not sure why default renderer is in use even though
        # pyramid_deform was included in setup?  but this works..
        kwargs.setdefault('renderer', deform.Form.default_renderer)
        return deform.Field(node, **kwargs)

    def test_serialize(self):
        self.pyramid_config.add_route('roles.view', '/roles/{uuid}')
        model = self.app.model
        auth = self.app.get_auth_handler()
        admin = auth.get_role_administrator(self.session)
        blokes = model.Role(name="Blokes")
        self.session.add(blokes)
        self.session.commit()

        # nb. we let the field construct the widget via our type
        node = colander.SchemaNode(RoleRefs(self.request, session=self.session))
        field = self.make_field(node)
        widget = field.widget

        # readonly values list includes admin
        html = widget.serialize(field, {admin.uuid, blokes.uuid}, readonly=True)
        self.assertIn(admin.name, html)
        self.assertIn(blokes.name, html)

        # editable values list *excludes* admin (by default)
        html = widget.serialize(field, {admin.uuid, blokes.uuid})
        self.assertNotIn(admin.uuid, html)
        self.assertIn(blokes.uuid, html)

        # but admin is included for root user
        self.request.is_root = True
        html = widget.serialize(field, {admin.uuid, blokes.uuid})
        self.assertIn(admin.uuid, html)
        self.assertIn(blokes.uuid, html)


class TestUserRefsWidget(WebTestCase):

    def make_field(self, node, **kwargs):
        # TODO: not sure why default renderer is in use even though
        # pyramid_deform was included in setup?  but this works..
        kwargs.setdefault('renderer', deform.Form.default_renderer)
        return deform.Field(node, **kwargs)

    def test_serialize(self):
        model = self.app.model

        # nb. we let the field construct the widget via our type
        node = colander.SchemaNode(UserRefs(self.request, session=self.session))
        field = self.make_field(node)
        widget = field.widget

        # readonly is required
        self.assertRaises(NotImplementedError, widget.serialize, field, set())
        self.assertRaises(NotImplementedError, widget.serialize, field, set(), readonly=False)

        # empty
        html = widget.serialize(field, set(), readonly=True)
        self.assertEqual(html, '<span></span>')

        # with data, no actions
        user = model.User(username='barney')
        self.session.add(user)
        self.session.commit()
        html = widget.serialize(field, {user.uuid}, readonly=True)
        self.assertIn('<b-table ', html)
        self.assertNotIn('Actions', html)
        self.assertNotIn('View', html)
        self.assertNotIn('Edit', html)

        # with view/edit actions
        with patch.object(self.request, 'is_root', new=True):
            html = widget.serialize(field, {user.uuid}, readonly=True)
        self.assertIn('<b-table ', html)
        self.assertIn('Actions', html)
        self.assertIn('View', html)
        self.assertIn('Edit', html)


class TestPermissionsWidget(WebTestCase):

    def make_field(self, node, **kwargs):
        # TODO: not sure why default renderer is in use even though
        # pyramid_deform was included in setup?  but this works..
        kwargs.setdefault('renderer', deform.Form.default_renderer)
        return deform.Field(node, **kwargs)

    def test_serialize(self):
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

        # nb. we let the field construct the widget via our type
        node = colander.SchemaNode(Permissions(self.request, permissions, session=self.session))
        field = self.make_field(node)
        widget = field.widget

        # readonly output does *not* include the perm by default
        html = widget.serialize(field, set(), readonly=True)
        self.assertNotIn("Polish the widgets", html)

        # readonly output includes the perm if set
        html = widget.serialize(field, {'widgets.polish'}, readonly=True)
        self.assertIn("Polish the widgets", html)

        # editable output always includes the perm
        html = widget.serialize(field, set())
        self.assertIn("Polish the widgets", html)
