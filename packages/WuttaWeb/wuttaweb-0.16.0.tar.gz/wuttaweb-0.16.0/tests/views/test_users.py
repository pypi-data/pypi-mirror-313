# -*- coding: utf-8; -*-

from unittest.mock import patch

from sqlalchemy import orm

import colander

from wuttaweb.views import users as mod
from tests.util import WebTestCase


class TestUserView(WebTestCase):

    def make_view(self):
        return mod.UserView(self.request)

    def test_includeme(self):
        self.pyramid_config.include('wuttaweb.views.users')

    def test_get_query(self):
        view = self.make_view()
        query = view.get_query(session=self.session)
        self.assertIsInstance(query, orm.Query)

    def test_configure_grid(self):
        model = self.app.model
        view = self.make_view()
        grid = view.make_grid(model_class=model.User)
        self.assertFalse(grid.is_linked('person'))
        view.configure_grid(grid)
        self.assertTrue(grid.is_linked('person'))

    def test_grid_row_class(self):
        model = self.app.model
        user = model.User(username='barney', active=True)
        data = dict(user)
        view = self.make_view()

        self.assertIsNone(view.grid_row_class(user, data, 1))

        user.active = False
        self.assertEqual(view.grid_row_class(user, data, 1), 'has-background-warning')

    def test_is_editable(self):
        model = self.app.model
        view = self.make_view()

        # active user is editable
        user = model.User(username='barney', active=True)
        self.assertTrue(view.is_editable(user))

        # inactive also editable
        user = model.User(username='barney', active=False)
        self.assertTrue(view.is_editable(user))

        # but not if prevent_edit flag is set
        user = model.User(username='barney', prevent_edit=True)
        self.assertFalse(view.is_editable(user))

        # unless request user is root
        self.request.is_root = True
        self.assertTrue(view.is_editable(user))

    def test_configure_form(self):
        model = self.app.model
        barney = model.User(username='barney')
        self.session.add(barney)
        self.session.commit()
        view = self.make_view()

        # person is *not* required
        with patch.object(view, 'creating', new=True):
            form = view.make_form(model_class=model.User)
            self.assertIsNone(form.is_required('person'))
            view.configure_form(form)
            self.assertFalse(form.is_required('person'))

        # password removed (always, for now)
        with patch.object(view, 'viewing', new=True):
            form = view.make_form(model_instance=barney)
            self.assertIn('password', form)
            view.configure_form(form)
            self.assertNotIn('password', form)
        with patch.object(view, 'editing', new=True):
            form = view.make_form(model_instance=barney)
            self.assertIn('password', form)
            view.configure_form(form)
            self.assertNotIn('password', form)

    def test_unique_username(self):
        model = self.app.model
        view = self.make_view()

        user = model.User(username='foo')
        self.session.add(user)
        self.session.commit()

        with patch.object(mod, 'Session', return_value=self.session):

            # invalid if same username in data
            node = colander.SchemaNode(colander.String(), name='username')
            self.assertRaises(colander.Invalid, view.unique_username, node, 'foo')

            # but not if username belongs to current user
            view.editing = True
            self.request.matchdict = {'uuid': user.uuid}
            node = colander.SchemaNode(colander.String(), name='username')
            self.assertIsNone(view.unique_username(node, 'foo'))

    def test_objectify(self):
        model = self.app.model
        auth = self.app.get_auth_handler()
        blokes = model.Role(name="Blokes")
        self.session.add(blokes)
        others = model.Role(name="Others")
        self.session.add(others)
        barney = model.User(username='barney')
        auth.set_user_password(barney, 'testpass')
        barney.roles.append(blokes)
        self.session.add(barney)
        self.session.commit()
        view = self.make_view()
        view.editing = True
        self.request.matchdict = {'uuid': barney.uuid}

        # sanity check, user is just in 'blokes' role
        self.session.refresh(barney)
        self.assertEqual(len(barney.roles), 1)
        self.assertEqual(barney.roles[0].name, "Blokes")

        # form can update user password
        self.assertTrue(auth.check_user_password(barney, 'testpass'))
        form = view.make_model_form(model_instance=barney)
        form.validated = {'username': 'barney', 'set_password': 'testpass2'}
        user = view.objectify(form, session=self.session)
        self.assertIs(user, barney)
        self.assertTrue(auth.check_user_password(barney, 'testpass2'))

        # form can update user roles
        form = view.make_model_form(model_instance=barney)
        form.validated = {'username': 'barney', 'roles': {others.uuid}}
        user = view.objectify(form, session=self.session)
        self.assertIs(user, barney)
        self.assertEqual(len(user.roles), 1)
        self.assertEqual(user.roles[0].name, "Others")

    def test_update_roles(self):
        model = self.app.model
        auth = self.app.get_auth_handler()
        admin = auth.get_role_administrator(self.session)
        authed = auth.get_role_authenticated(self.session)
        anon = auth.get_role_anonymous(self.session)
        blokes = model.Role(name="Blokes")
        self.session.add(blokes)
        others = model.Role(name="Others")
        self.session.add(others)
        barney = model.User(username='barney')
        barney.roles.append(blokes)
        self.session.add(barney)
        self.session.commit()
        view = self.make_view()
        view.editing = True
        self.request.matchdict = {'uuid': barney.uuid}

        # no error if data is missing roles
        form = view.make_model_form(model_instance=barney)
        form.validated = {'username': 'barneyx'}
        user = view.objectify(form, session=self.session)
        self.assertIs(user, barney)
        self.assertEqual(barney.username, 'barneyx')

        # sanity check, user is just in 'blokes' role
        self.session.refresh(barney)
        self.assertEqual(len(barney.roles), 1)
        self.assertEqual(barney.roles[0].name, "Blokes")

        # let's test a bunch at once to ensure:
        # - user roles are updated
        # - authed / anon roles are not added
        # - admin role not added if current user is not root
        form = view.make_model_form(model_instance=barney)
        form.validated = {'username': 'barney',
                          'roles': {admin.uuid, authed.uuid, anon.uuid, others.uuid}}
        user = view.objectify(form, session=self.session)
        self.assertIs(user, barney)
        self.assertEqual(len(user.roles), 1)
        self.assertEqual(user.roles[0].name, "Others")

        # let's test a bunch at once to ensure:
        # - user roles are updated
        # - admin role is added if current user is root
        self.request.is_root = True
        form = view.make_model_form(model_instance=barney)
        form.validated = {'username': 'barney',
                          'roles': {admin.uuid, blokes.uuid, others.uuid}}
        user = view.objectify(form, session=self.session)
        self.assertIs(user, barney)
        self.assertEqual(len(user.roles), 3)
        role_uuids = set([role.uuid for role in user.roles])
        self.assertEqual(role_uuids, {admin.uuid, blokes.uuid, others.uuid})

        # admin role not removed if current user is not root
        self.request.is_root = False
        form = view.make_model_form(model_instance=barney)
        form.validated = {'username': 'barney',
                          'roles': {blokes.uuid, others.uuid}}
        user = view.objectify(form, session=self.session)
        self.assertIs(user, barney)
        self.assertEqual(len(user.roles), 3)

        # admin role is removed if current user is root
        self.request.is_root = True
        form = view.make_model_form(model_instance=barney)
        form.validated = {'username': 'barney',
                          'roles': {blokes.uuid, others.uuid}}
        user = view.objectify(form, session=self.session)
        self.assertIs(user, barney)
        self.assertEqual(len(user.roles), 2)
