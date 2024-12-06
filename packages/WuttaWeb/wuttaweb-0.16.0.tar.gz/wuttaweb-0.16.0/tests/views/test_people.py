# -*- coding: utf-8; -*-

from unittest.mock import patch

from sqlalchemy import orm

from pyramid.httpexceptions import HTTPNotFound

from wuttaweb.views import people
from tests.util import WebTestCase


class TestPersonView(WebTestCase):

    def make_view(self):
        return people.PersonView(self.request)

    def test_includeme(self):
        self.pyramid_config.include('wuttaweb.views.people')

    def test_get_query(self):
        view = self.make_view()
        query = view.get_query(session=self.session)
        self.assertIsInstance(query, orm.Query)

    def test_configure_grid(self):
        model = self.app.model
        view = self.make_view()
        grid = view.make_grid(model_class=model.Setting)
        self.assertEqual(grid.linked_columns, [])
        view.configure_grid(grid)
        self.assertIn('full_name', grid.linked_columns)

    def test_configure_form(self):
        model = self.app.model
        view = self.make_view()
        form = view.make_form(model_class=model.Person)

        # required fields
        with patch.object(view, 'creating', new=True):
            form.set_fields(form.get_model_fields())
            self.assertEqual(form.required_fields, {})
            view.configure_form(form)
            self.assertTrue(form.required_fields)
            self.assertFalse(form.required_fields['middle_name'])

        person = model.Person(full_name="Barney Rubble")
        user = model.User(username='barney', person=person)
        self.session.add(user)
        self.session.commit()

        # users field
        with patch.object(view, 'viewing', new=True):
            form = view.make_form(model_instance=person)
            self.assertEqual(form.defaults, {})
            view.configure_form(form)
            self.assertIn('_users', form.defaults)

    def test_autocomplete_query(self):
        model = self.app.model

        person1 = model.Person(full_name="George Jones")
        self.session.add(person1)
        person2 = model.Person(full_name="George Strait")
        self.session.add(person2)
        self.session.commit()

        view = self.make_view()
        with patch.object(view, 'Session', return_value=self.session):

            # both people match
            query = view.autocomplete_query('george')
            self.assertEqual(query.count(), 2)

            # just 1 match
            query = view.autocomplete_query('jones')
            self.assertEqual(query.count(), 1)

            # no matches
            query = view.autocomplete_query('sally')
            self.assertEqual(query.count(), 0)

    def test_view_profile(self):
        self.pyramid_config.include('wuttaweb.views.common')
        self.pyramid_config.include('wuttaweb.views.auth')
        self.pyramid_config.add_route('people', '/people/')

        model = self.app.model
        person = model.Person(full_name="Barney Rubble")
        self.session.add(person)
        self.session.commit()

        # sanity check
        view = self.make_view()
        self.request.matchdict = {'uuid': person.uuid}
        response = view.view_profile(session=self.session)
        self.assertEqual(response.status_code, 200)

    def test_make_user(self):
        self.pyramid_config.include('wuttaweb.views.common')

        model = self.app.model
        person = model.Person(full_name="Barney Rubble")
        self.session.add(person)
        self.session.commit()

        # sanity check
        view = self.make_view()
        self.request.matchdict = {'uuid': person.uuid}
        response = view.make_user()
        # nb. this always redirects for now
        self.assertEqual(response.status_code, 302)
