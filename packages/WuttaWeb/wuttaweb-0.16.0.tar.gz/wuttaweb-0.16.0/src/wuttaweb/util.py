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
Web Utilities
"""

import importlib
import json
import logging
import warnings

import sqlalchemy as sa

import colander
from webhelpers2.html import HTML, tags


log = logging.getLogger(__name__)


class FieldList(list):
    """
    Convenience wrapper for a form's field list.  This is a subclass
    of :class:`python:list`.

    You normally would not need to instantiate this yourself, but it
    is used under the hood for
    :attr:`~wuttaweb.forms.base.Form.fields` as well as
    :attr:`~wuttaweb.grids.base.Grid.columns`.
    """

    def insert_before(self, field, newfield):
        """
        Insert a new field, before an existing field.

        :param field: String name for the existing field.

        :param newfield: String name for the new field, to be inserted
           just before the existing ``field``.
        """
        if field in self:
            i = self.index(field)
            self.insert(i, newfield)
        else:
            log.warning("field '%s' not found, will append new field: %s",
                        field, newfield)
            self.append(newfield)

    def insert_after(self, field, newfield):
        """
        Insert a new field, after an existing field.

        :param field: String name for the existing field.

        :param newfield: String name for the new field, to be inserted
           just after the existing ``field``.
        """
        if field in self:
            i = self.index(field)
            self.insert(i + 1, newfield)
        else:
            log.warning("field '%s' not found, will append new field: %s",
                        field, newfield)
            self.append(newfield)

    def set_sequence(self, fields):
        """
        Sort the list such that it matches the same sequence as the
        given fields list.

        This does not add or remove any elements, it just
        (potentially) rearranges the internal list elements.
        Therefore you do not need to explicitly declare *all* fields;
        just the ones you care about.

        The resulting field list will have the requested fields in
        order, at the *beginning* of the list.  Any unrequested fields
        will remain in the same order as they were previously, but
        will be placed *after* the requested fields.

        :param fields: List of fields in the desired order.
        """
        unimportant = len(self) + 1

        def getkey(field):
            if field in fields:
                return fields.index(field)
            return unimportant

        self.sort(key=getkey)


def get_form_data(request):
    """
    Returns the effective form data for the given request.

    Mostly this is a convenience, which simply returns one of the
    following, depending on various attributes of the request.

    * :attr:`pyramid:pyramid.request.Request.POST`
    * :attr:`pyramid:pyramid.request.Request.json_body`
    """
    # nb. we prefer JSON only if no POST is present
    # TODO: this seems to work for our use case at least, but perhaps
    # there is a better way?  see also
    # https://docs.pylonsproject.org/projects/pyramid/en/latest/api/request.html#pyramid.request.Request.is_xhr
    if not request.POST and (
            getattr(request, 'is_xhr', False)
            or getattr(request, 'content_type', None) == 'application/json'):
        return request.json_body
    return request.POST


def get_libver(
        request,
        key,
        configured_only=False,
        default_only=False,
        prefix='wuttaweb',
):
    """
    Return the appropriate version string for the web resource library
    identified by ``key``.

    WuttaWeb makes certain assumptions about which libraries would be
    used on the frontend, and which versions for each would be used by
    default.  But it should also be possible to customize which
    versions are used, hence this function.

    Each library has a built-in default version but your config can
    override them, e.g.:

    .. code-block:: ini

       [wuttaweb]
       libver.bb_vue = 3.4.29

    :param request: Current request.

    :param key: Unique key for the library, as string.  Possibilities
       are the same as for :func:`get_liburl()`.

    :param configured_only: Pass ``True`` here if you only want the
       configured version and ignore the default version.

    :param default_only: Pass ``True`` here if you only want the
       default version and ignore the configured version.

    :param prefix: If specified, will override the prefix used for
       config lookups.

       .. warning::

          This ``prefix`` param is for backward compatibility and may
          be removed in the future.

    :returns: The appropriate version string, e.g. ``'1.2.3'`` or
       ``'latest'`` etc.  Can also return ``None`` in some cases.
    """
    config = request.wutta_config

    # nb. we prefer a setting to be named like:  wuttaweb.libver.vue
    # but for back-compat this also can work:    tailbone.libver.vue
    # and for more back-compat this can work:    wuttaweb.vue_version
    # however that compat only works for some of the settings...

    if not default_only:

        # nb. new/preferred setting
        version = config.get(f'wuttaweb.libver.{key}')
        if version:
            return version

        # fallback to caller-specified prefix
        if prefix != 'wuttaweb':
            version = config.get(f'{prefix}.libver.{key}')
            if version:
                warnings.warn(f"config for {prefix}.libver.{key} is deprecated; "
                              f"please set wuttaweb.libver.{key} instead",
                              DeprecationWarning)
                return version

    if key == 'buefy':
        if not default_only:
            # nb. old/legacy setting
            version = config.get(f'{prefix}.buefy_version')
            if version:
                warnings.warn(f"config for {prefix}.buefy_version is deprecated; "
                              "please set wuttaweb.libver.buefy instead",
                              DeprecationWarning)
                return version
        if not configured_only:
            return '0.9.25'

    elif key == 'buefy.css':
        # nb. this always returns something
        return get_libver(request, 'buefy',
                          default_only=default_only,
                          configured_only=configured_only)

    elif key == 'vue':
        if not default_only:
            # nb. old/legacy setting
            version = config.get(f'{prefix}.vue_version')
            if version:
                warnings.warn(f"config for {prefix}.vue_version is deprecated; "
                              "please set wuttaweb.libver.vue instead",
                              DeprecationWarning)
                return version
        if not configured_only:
            return '2.6.14'

    elif key == 'vue_resource':
        if not configured_only:
            return '1.5.3'

    elif key == 'fontawesome':
        if not configured_only:
            return '5.3.1'

    elif key == 'bb_vue':
        if not configured_only:
            return '3.4.31'

    elif key == 'bb_oruga':
        if not configured_only:
            return '0.8.12'

    elif key in ('bb_oruga_bulma', 'bb_oruga_bulma_css'):
        if not configured_only:
            return '0.3.0'

    elif key == 'bb_fontawesome_svg_core':
        if not configured_only:
            return '6.5.2'

    elif key == 'bb_free_solid_svg_icons':
        if not configured_only:
            return '6.5.2'

    elif key == 'bb_vue_fontawesome':
        if not configured_only:
            return '3.0.6'


def get_liburl(
        request,
        key,
        configured_only=False,
        default_only=False,
        prefix='wuttaweb',
):
    """
    Return the appropriate URL for the web resource library identified
    by ``key``.

    WuttaWeb makes certain assumptions about which libraries would be
    used on the frontend, and which versions for each would be used by
    default.  But ultimately a URL must be determined for each, hence
    this function.

    Each library has a built-in default URL which references a public
    Internet (i.e. CDN) resource, but your config can override the
    final URL in two ways:

    The simplest way is to just override the *version* but otherwise
    let the default logic construct the URL.  See :func:`get_libver()`
    for more on that approach.

    The most flexible way is to override the URL explicitly, e.g.:

    .. code-block:: ini

       [wuttaweb]
       liburl.bb_vue = https://example.com/cache/vue-3.4.31.js

    :param request: Current request.

    :param key: Unique key for the library, as string.  Possibilities
       are:

       Vue 2 + Buefy

       * ``vue``
       * ``vue_resource``
       * ``buefy``
       * ``buefy.css``
       * ``fontawesome``

       Vue 3 + Oruga

       * ``bb_vue``
       * ``bb_oruga``
       * ``bb_oruga_bulma``
       * ``bb_oruga_bulma_css``
       * ``bb_fontawesome_svg_core``
       * ``bb_free_solid_svg_icons``
       * ``bb_vue_fontawesome``

    :param configured_only: Pass ``True`` here if you only want the
       configured URL and ignore the default URL.

    :param default_only: Pass ``True`` here if you only want the
       default URL and ignore the configured URL.

    :param prefix: If specified, will override the prefix used for
       config lookups.

       .. warning::

          This ``prefix`` param is for backward compatibility and may
          be removed in the future.

    :returns: The appropriate URL as string.  Can also return ``None``
       in some cases.
    """
    config = request.wutta_config

    if not default_only:

        # nb. new/preferred setting
        url = config.get(f'wuttaweb.liburl.{key}')
        if url:
            return url

        # fallback to caller-specified prefix
        url = config.get(f'{prefix}.liburl.{key}')
        if url:
            warnings.warn(f"config for {prefix}.liburl.{key} is deprecated; "
                          f"please set wuttaweb.liburl.{key} instead",
                          DeprecationWarning)
            return url

    if configured_only:
        return

    version = get_libver(request, key, prefix=prefix,
                         configured_only=False,
                         default_only=default_only)

    # load fanstatic libcache if configured
    static = config.get('wuttaweb.static_libcache.module')
    if not static:
        static = config.get(f'{prefix}.static_libcache.module')
        if static:
            warnings.warn(f"config for {prefix}.static_libcache.module is deprecated; "
                          "please set wuttaweb.static_libcache.module instead",
                          DeprecationWarning)
    if static:
        static = importlib.import_module(static)
        needed = request.environ['fanstatic.needed']
        liburl = needed.library_url(static.libcache) + '/'
        # nb. add custom url prefix if needed, e.g. /wutta
        if request.script_name:
            liburl = request.script_name + liburl

    if key == 'buefy':
        if static and hasattr(static, 'buefy_js'):
            return liburl + static.buefy_js.relpath
        return f'https://unpkg.com/buefy@{version}/dist/buefy.min.js'

    elif key == 'buefy.css':
        if static and hasattr(static, 'buefy_css'):
            return liburl + static.buefy_css.relpath
        return f'https://unpkg.com/buefy@{version}/dist/buefy.min.css'

    elif key == 'vue':
        if static and hasattr(static, 'vue_js'):
            return liburl + static.vue_js.relpath
        return f'https://unpkg.com/vue@{version}/dist/vue.min.js'

    elif key == 'vue_resource':
        if static and hasattr(static, 'vue_resource_js'):
            return liburl + static.vue_resource_js.relpath
        return f'https://cdn.jsdelivr.net/npm/vue-resource@{version}'

    elif key == 'fontawesome':
        if static and hasattr(static, 'fontawesome_js'):
            return liburl + static.fontawesome_js.relpath
        return f'https://use.fontawesome.com/releases/v{version}/js/all.js'

    elif key == 'bb_vue':
        if static and hasattr(static, 'bb_vue_js'):
            return liburl + static.bb_vue_js.relpath
        return f'https://unpkg.com/vue@{version}/dist/vue.esm-browser.prod.js'

    elif key == 'bb_oruga':
        if static and hasattr(static, 'bb_oruga_js'):
            return liburl + static.bb_oruga_js.relpath
        return f'https://unpkg.com/@oruga-ui/oruga-next@{version}/dist/oruga.mjs'

    elif key == 'bb_oruga_bulma':
        if static and hasattr(static, 'bb_oruga_bulma_js'):
            return liburl + static.bb_oruga_bulma_js.relpath
        return f'https://unpkg.com/@oruga-ui/theme-bulma@{version}/dist/bulma.mjs'

    elif key == 'bb_oruga_bulma_css':
        if static and hasattr(static, 'bb_oruga_bulma_css'):
            return liburl + static.bb_oruga_bulma_css.relpath
        return f'https://unpkg.com/@oruga-ui/theme-bulma@{version}/dist/bulma.css'

    elif key == 'bb_fontawesome_svg_core':
        if static and hasattr(static, 'bb_fontawesome_svg_core_js'):
            return liburl + static.bb_fontawesome_svg_core_js.relpath
        return f'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-svg-core@{version}/+esm'

    elif key == 'bb_free_solid_svg_icons':
        if static and hasattr(static, 'bb_free_solid_svg_icons_js'):
            return liburl + static.bb_free_solid_svg_icons_js.relpath
        return f'https://cdn.jsdelivr.net/npm/@fortawesome/free-solid-svg-icons@{version}/+esm'

    elif key == 'bb_vue_fontawesome':
        if static and hasattr(static, 'bb_vue_fontawesome_js'):
            return liburl + static.bb_vue_fontawesome_js.relpath
        return f'https://cdn.jsdelivr.net/npm/@fortawesome/vue-fontawesome@{version}/+esm'


def get_csrf_token(request):
    """
    Convenience function, returns the effective CSRF token (raw
    string) for the given request.

    See also :func:`render_csrf_token()`.
    """
    token = request.session.get_csrf_token()
    if token is None:
        token = request.session.new_csrf_token()
    return token


def render_csrf_token(request, name='_csrf'):
    """
    Convenience function, returns CSRF hidden input inside hidden div,
    e.g.:

    .. code-block:: html

       <div style="display: none;">
          <input type="hidden" name="_csrf" value="TOKEN" />
       </div>

    This function is part of :mod:`wuttaweb.helpers` (as
    :func:`~wuttaweb.helpers.csrf_token()`) which means you can do
    this in page templates:

    .. code-block:: mako

       ${h.form(request.current_route_url())}
       ${h.csrf_token(request)}
       <!-- other fields etc. -->
       ${h.end_form()}

    See also :func:`get_csrf_token()`.
    """
    token = get_csrf_token(request)
    return HTML.tag('div', tags.hidden(name, value=token, id=None), style='display:none;')


def get_model_fields(config, model_class=None):
    """
    Convenience function to return a list of field names for the given
    model class.

    This logic only supports SQLAlchemy mapped classes and will use
    that to determine the field listing if applicable.  Otherwise this
    returns ``None``.
    """
    if not model_class:
        return

    try:
        mapper = sa.inspect(model_class)
    except sa.exc.NoInspectionAvailable:
        return

    fields = [prop.key for prop in mapper.iterate_properties]

    # nb. we never want the continuum 'versions' prop
    app = config.get_app()
    if app.continuum_is_enabled() and 'versions' in fields:
        fields.remove('versions')

    return fields


def make_json_safe(value, key=None, warn=True):
    """
    Convert a Python value as needed, to ensure it is compatible with
    :func:`python:json.dumps()`.

    :param value: Python value.

    :param key: Optional key for the value, if known.  This is used
       when logging warnings, if applicable.

    :param warn: Whether warnings should be logged if the value is not
       already JSON-compatible.

    :returns: A (possibly new) Python value which is guaranteed to be
       JSON-serializable.
    """

    # convert null => None
    if value is colander.null:
        return None

    # recursively convert dict
    if isinstance(value, dict):
        parent = dict(value)
        for key, value in parent.items():
            parent[key] = make_json_safe(value, key=key, warn=warn)
        value = parent

    # ensure JSON-compatibility, warn if problems
    try:
        json.dumps(value)
    except TypeError as error:
        if warn:
            prefix = "value"
            if key:
                prefix += f" for '{key}'"
            log.warning("%s is not json-friendly: %s", prefix, repr(value))
        value = str(value)
        if warn:
            log.warning("forced value to: %s", value)

    return value
