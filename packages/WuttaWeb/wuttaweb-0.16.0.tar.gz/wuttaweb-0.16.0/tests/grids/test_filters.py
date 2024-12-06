# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import patch

from wuttaweb.grids import filters as mod
from tests.util import WebTestCase


class TestGridFilter(WebTestCase):

    def setUp(self):
        self.setup_web()

        model = self.app.model
        self.sample_data = [
            {'name': 'foo1', 'value': 'ONE'},
            {'name': 'foo2', 'value': 'two'},
            {'name': 'foo3', 'value': 'ggg'},
            {'name': 'foo4', 'value': 'ggg'},
            {'name': 'foo5', 'value': 'ggg'},
            {'name': 'foo6', 'value': 'six'},
            {'name': 'foo7', 'value': 'seven'},
            {'name': 'foo8', 'value': 'eight'},
            {'name': 'foo9', 'value': 'nine'},
        ]
        for setting in self.sample_data:
            self.app.save_setting(self.session, setting['name'], setting['value'])
        self.session.commit()
        self.sample_query = self.session.query(model.Setting)

    def make_filter(self, model_property, **kwargs):
        factory = kwargs.pop('factory', mod.GridFilter)
        kwargs['model_property'] = model_property
        return factory(self.request, model_property.key, **kwargs)

    def test_constructor(self):
        model = self.app.model

        # verbs is not set by default, but can be set
        filtr = self.make_filter(model.Setting.name)
        self.assertFalse(hasattr(filtr, 'verbs'))
        filtr = self.make_filter(model.Setting.name, verbs=['foo', 'bar'])
        self.assertEqual(filtr.verbs, ['foo', 'bar'])

        # verb is not set by default, but can be set
        filtr = self.make_filter(model.Setting.name)
        self.assertFalse(hasattr(filtr, 'verb'))
        filtr = self.make_filter(model.Setting.name, verb='foo')
        self.assertEqual(filtr.verb, 'foo')

        # default verb is not set by default, but can be set
        filtr = self.make_filter(model.Setting.name)
        self.assertFalse(hasattr(filtr, 'default_verb'))
        filtr = self.make_filter(model.Setting.name, default_verb='foo')
        self.assertEqual(filtr.default_verb, 'foo')

    def test_repr(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.name, factory=mod.GridFilter)
        self.assertEqual(repr(filtr), "GridFilter(key='name', active=False, verb=None, value=None)")

    def test_get_verbs(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.name, factory=mod.AlchemyFilter)
        self.assertFalse(hasattr(filtr, 'verbs'))
        self.assertEqual(filtr.default_verbs, ['equal', 'not_equal'])

        # by default, returns default verbs (plus 'is_any')
        self.assertEqual(filtr.get_verbs(), ['equal', 'not_equal', 'is_any'])

        # default verbs can be a callable
        filtr.default_verbs = lambda: ['foo', 'bar']
        self.assertEqual(filtr.get_verbs(), ['foo', 'bar', 'is_any'])

        # uses filtr.verbs if set
        filtr.verbs = ['is_true', 'is_false']
        self.assertEqual(filtr.get_verbs(), ['is_true', 'is_false', 'is_any'])

        # may add is/null verbs
        filtr = self.make_filter(model.Setting.name, factory=mod.AlchemyFilter,
                                 nullable=True)
        self.assertEqual(filtr.get_verbs(), ['equal', 'not_equal',
                                             'is_null', 'is_not_null',
                                             'is_any'])

        # filtr.verbs can be a callable
        filtr.nullable = False
        filtr.verbs = lambda: ['baz', 'blarg']
        self.assertEqual(filtr.get_verbs(), ['baz', 'blarg', 'is_any'])

    def test_get_default_verb(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.name, factory=mod.AlchemyFilter)
        self.assertFalse(hasattr(filtr, 'verbs'))
        self.assertEqual(filtr.default_verbs, ['equal', 'not_equal'])
        self.assertEqual(filtr.get_verbs(), ['equal', 'not_equal', 'is_any'])

        # returns first verb by default
        self.assertEqual(filtr.get_default_verb(), 'equal')

        # returns filtr.verb if set
        filtr.verb = 'foo'
        self.assertEqual(filtr.get_default_verb(), 'foo')

        # returns filtr.default_verb if set
        # (nb. this overrides filtr.verb since the point of this
        # method is to return the *default* verb)
        filtr.default_verb = 'bar'
        self.assertEqual(filtr.get_default_verb(), 'bar')

    def test_get_verb_labels(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.name, factory=mod.AlchemyFilter)
        self.assertFalse(hasattr(filtr, 'verbs'))
        self.assertEqual(filtr.get_verbs(), ['equal', 'not_equal', 'is_any'])

        labels = filtr.get_verb_labels()
        self.assertIsInstance(labels, dict)
        self.assertEqual(labels['equal'], "equal to")
        self.assertEqual(labels['not_equal'], "not equal to")
        self.assertEqual(labels['is_any'], "is any")

    def test_get_valueless_verbs(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.name, factory=mod.AlchemyFilter)
        self.assertFalse(hasattr(filtr, 'verbs'))
        self.assertEqual(filtr.get_verbs(), ['equal', 'not_equal', 'is_any'])

        verbs = filtr.get_valueless_verbs()
        self.assertIsInstance(verbs, list)
        self.assertIn('is_any', verbs)

    def test_apply_filter(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.value, factory=mod.StringAlchemyFilter)

        # default verb used as fallback
        # self.assertEqual(filtr.default_verb, 'contains')
        filtr.default_verb = 'contains'
        filtr.verb = None
        with patch.object(filtr, 'filter_contains', side_effect=lambda q, v: q) as filter_contains:
            filtered_query = filtr.apply_filter(self.sample_query, value='foo')
            filter_contains.assert_called_once_with(self.sample_query, 'foo')
        self.assertIsNone(filtr.verb)

        # filter verb used as fallback
        filtr.verb = 'equal'
        with patch.object(filtr, 'filter_equal', create=True, side_effect=lambda q, v: q) as filter_equal:
            filtered_query = filtr.apply_filter(self.sample_query, value='foo')
            filter_equal.assert_called_once_with(self.sample_query, 'foo')

        # filter value used as fallback
        filtr.verb = 'contains'
        filtr.value = 'blarg'
        with patch.object(filtr, 'filter_contains', side_effect=lambda q, v: q) as filter_contains:
            filtered_query = filtr.apply_filter(self.sample_query)
            filter_contains.assert_called_once_with(self.sample_query, 'blarg')

        # error if invalid verb
        self.assertRaises(mod.VerbNotSupported, filtr.apply_filter,
                          self.sample_query, verb='doesnotexist')
        filtr.verbs = ['doesnotexist']
        self.assertRaises(mod.VerbNotSupported, filtr.apply_filter,
                          self.sample_query, verb='doesnotexist')

    def test_filter_is_any(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.value)
        self.assertEqual(self.sample_query.count(), 9)

        # nb. value None is ignored
        filtered_query = filtr.filter_is_any(self.sample_query, None)
        self.assertIs(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 9)


class TestAlchemyFilter(WebTestCase):

    def setUp(self):
        self.setup_web()

        model = self.app.model
        self.sample_data = [
            {'name': 'foo1', 'value': 'ONE'},
            {'name': 'foo2', 'value': 'two'},
            {'name': 'foo3', 'value': 'ggg'},
            {'name': 'foo4', 'value': 'ggg'},
            {'name': 'foo5', 'value': 'ggg'},
            {'name': 'foo6', 'value': 'six'},
            {'name': 'foo7', 'value': 'seven'},
            {'name': 'foo8', 'value': 'eight'},
            {'name': 'foo9', 'value': None},
        ]
        for setting in self.sample_data:
            self.app.save_setting(self.session, setting['name'], setting['value'])
        self.session.commit()
        self.sample_query = self.session.query(model.Setting)

    def make_filter(self, model_property, **kwargs):
        factory = kwargs.pop('factory', mod.AlchemyFilter)
        kwargs['model_property'] = model_property
        return factory(self.request, model_property.key, **kwargs)

    def test_filter_equal(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.value)
        self.assertEqual(self.sample_query.count(), 9)

        # not filtered for null value
        filtered_query = filtr.filter_equal(self.sample_query, None)
        self.assertIs(filtered_query, self.sample_query)

        # nb. by default, *is filtered* by empty string
        filtered_query = filtr.filter_equal(self.sample_query, '')
        self.assertIsNot(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 0)

        # filtered by value
        filtered_query = filtr.filter_equal(self.sample_query, 'ggg')
        self.assertIsNot(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 3)

    def test_filter_not_equal(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.value)
        self.assertEqual(self.sample_query.count(), 9)

        # not filtered for empty value
        filtered_query = filtr.filter_not_equal(self.sample_query, None)
        self.assertIs(filtered_query, self.sample_query)

        # nb. by default, *is filtered* by empty string
        filtered_query = filtr.filter_not_equal(self.sample_query, '')
        self.assertIsNot(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 9)

        # filtered by value
        filtered_query = filtr.filter_not_equal(self.sample_query, 'ggg')
        self.assertIsNot(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 6)

    def test_filter_is_null(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.value)
        self.assertEqual(self.sample_query.count(), 9)

        # nb. value None is ignored
        filtered_query = filtr.filter_is_null(self.sample_query, None)
        self.assertIsNot(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 1)

    def test_filter_is_not_null(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.value)
        self.assertEqual(self.sample_query.count(), 9)

        # nb. value None is ignored
        filtered_query = filtr.filter_is_not_null(self.sample_query, None)
        self.assertIsNot(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 8)


class TestStringAlchemyFilter(WebTestCase):

    def setUp(self):
        self.setup_web()

        model = self.app.model
        self.sample_data = [
            {'name': 'foo1', 'value': 'ONE'},
            {'name': 'foo2', 'value': 'two'},
            {'name': 'foo3', 'value': 'ggg'},
            {'name': 'foo4', 'value': 'ggg'},
            {'name': 'foo5', 'value': 'ggg'},
            {'name': 'foo6', 'value': 'six'},
            {'name': 'foo7', 'value': 'seven'},
            {'name': 'foo8', 'value': 'eight'},
            {'name': 'foo9', 'value': 'nine'},
        ]
        for setting in self.sample_data:
            self.app.save_setting(self.session, setting['name'], setting['value'])
        self.session.commit()
        self.sample_query = self.session.query(model.Setting)

    def make_filter(self, model_property, **kwargs):
        factory = kwargs.pop('factory', mod.StringAlchemyFilter)
        kwargs['model_property'] = model_property
        return factory(self.request, model_property.key, **kwargs)

    def test_filter_contains(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.value)
        self.assertEqual(self.sample_query.count(), 9)

        # not filtered for empty value
        filtered_query = filtr.filter_contains(self.sample_query, None)
        self.assertIs(filtered_query, self.sample_query)
        filtered_query = filtr.filter_contains(self.sample_query, '')
        self.assertIs(filtered_query, self.sample_query)

        # filtered by value
        filtered_query = filtr.filter_contains(self.sample_query, 'ggg')
        self.assertIsNot(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 3)

    def test_filter_does_not_contain(self):
        model = self.app.model
        filtr = self.make_filter(model.Setting.value)
        self.assertEqual(self.sample_query.count(), 9)

        # not filtered for empty value
        filtered_query = filtr.filter_does_not_contain(self.sample_query, None)
        self.assertIs(filtered_query, self.sample_query)
        filtered_query = filtr.filter_does_not_contain(self.sample_query, '')
        self.assertIs(filtered_query, self.sample_query)

        # filtered by value
        filtered_query = filtr.filter_does_not_contain(self.sample_query, 'ggg')
        self.assertIsNot(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 6)


class TestBooleanAlchemyFilter(WebTestCase):

    def setUp(self):
        self.setup_web()

        model = self.app.model
        self.sample_data = [
            {'username': 'alice', 'active': True},
            {'username': 'bob', 'active': True},
            {'username': 'charlie', 'active': False},
        ]
        for user in self.sample_data:
            user = model.User(**user)
            self.session.add(user)
        self.session.commit()
        self.sample_query = self.session.query(model.User)

    def make_filter(self, model_property, **kwargs):
        factory = kwargs.pop('factory', mod.BooleanAlchemyFilter)
        kwargs['model_property'] = model_property
        return factory(self.request, model_property.key, **kwargs)

    def test_coerce_value(self):
        model = self.app.model
        filtr = self.make_filter(model.User.active)

        self.assertIsNone(filtr.coerce_value(None))

        self.assertTrue(filtr.coerce_value(True))
        self.assertTrue(filtr.coerce_value(1))
        self.assertTrue(filtr.coerce_value('1'))

        self.assertFalse(filtr.coerce_value(False))
        self.assertFalse(filtr.coerce_value(0))
        self.assertFalse(filtr.coerce_value(''))

    def test_filter_is_true(self):
        model = self.app.model
        filtr = self.make_filter(model.User.active)
        self.assertEqual(self.sample_query.count(), 3)

        # nb. value None is ignored
        filtered_query = filtr.filter_is_true(self.sample_query, None)
        self.assertIsNot(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 2)

    def test_filter_is_false(self):
        model = self.app.model
        filtr = self.make_filter(model.User.active)
        self.assertEqual(self.sample_query.count(), 3)

        # nb. value None is ignored
        filtered_query = filtr.filter_is_false(self.sample_query, None)
        self.assertIsNot(filtered_query, self.sample_query)
        self.assertEqual(filtered_query.count(), 1)


class TestVerbNotSupported(TestCase):

    def test_basic(self):
        error = mod.VerbNotSupported('equal')
        self.assertEqual(str(error), "unknown filter verb not supported: equal")
