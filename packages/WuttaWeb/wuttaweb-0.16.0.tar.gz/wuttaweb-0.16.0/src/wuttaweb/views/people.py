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
Views for people
"""

import sqlalchemy as sa

from wuttjamaican.db.model import Person
from wuttaweb.views import MasterView
from wuttaweb.forms.schema import UserRefs


class PersonView(MasterView):
    """
    Master view for people.

    Default route prefix is ``people``.

    Notable URLs provided by this class:

    * ``/people/``
    * ``/people/new``
    * ``/people/XXX``
    * ``/people/XXX/edit``
    * ``/people/XXX/delete``
    """
    model_class = Person
    model_title_plural = "People"
    route_prefix = 'people'
    sort_defaults = 'full_name'
    has_autocomplete = True

    grid_columns = [
        'full_name',
        'first_name',
        'middle_name',
        'last_name',
    ]

    filter_defaults = {
        'full_name': {'active': True},
    }

    def configure_grid(self, g):
        """ """
        super().configure_grid(g)

        # full_name
        g.set_link('full_name')

        # first_name
        g.set_link('first_name')

        # last_name
        g.set_link('last_name')

    def configure_form(self, f):
        """ """
        super().configure_form(f)
        person = f.model_instance

        # TODO: master should handle these? (nullable column)
        f.set_required('first_name', False)
        f.set_required('middle_name', False)
        f.set_required('last_name', False)

        # users
        # nb. colanderalchemy wants to do some magic for the true
        # 'users' relationship, so we use a different field name
        f.remove('users')
        if not (self.creating or self.editing):
            f.append('_users')
            f.set_readonly('_users')
            f.set_node('_users', UserRefs(self.request))
            f.set_default('_users', [u.uuid for u in person.users])

    def autocomplete_query(self, term):
        """ """
        model = self.app.model
        session = self.Session()
        query = session.query(model.Person)
        criteria = [model.Person.full_name.ilike(f'%{word}%')
                    for word in term.split()]
        query = query.filter(sa.and_(*criteria))\
                     .order_by(model.Person.full_name)
        return query

    def view_profile(self, session=None):
        """ """
        person = self.get_instance(session=session)
        context = {
            'person': person,
            'instance': person,
        }
        return self.render_to_response('view_profile', context)

    def make_user(self):
        """ """
        self.request.session.flash("TODO: this feature is not yet supported", 'error')
        return self.redirect(self.request.get_referrer())

    @classmethod
    def defaults(cls, config):
        """ """

        # nb. Person may come from custom model
        wutta_config = config.registry.settings['wutta_config']
        app = wutta_config.get_app()
        cls.model_class = app.model.Person

        cls._defaults(config)
        cls._people_defaults(config)

    @classmethod
    def _people_defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        url_prefix = cls.get_url_prefix()
        instance_url_prefix = cls.get_instance_url_prefix()
        permission_prefix = cls.get_permission_prefix()

        # view profile
        config.add_route(f'{route_prefix}.view_profile',
                         f'{instance_url_prefix}/profile',
                         request_method='GET')
        config.add_view(cls, attr='view_profile',
                        route_name=f'{route_prefix}.view_profile',
                        permission=f'{permission_prefix}.view_profile')

        # make user for person
        config.add_route(f'{route_prefix}.make_user',
                         f'{url_prefix}/make-user',
                         request_method='POST')
        config.add_view(cls, attr='make_user',
                        route_name=f'{route_prefix}.make_user',
                        permission='users.create')


def defaults(config, **kwargs):
    base = globals()

    PersonView = kwargs.get('PersonView', base['PersonView'])
    PersonView.defaults(config)


def includeme(config):
    defaults(config)
