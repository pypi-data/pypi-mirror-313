## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="page_content()">
  % if form is not Undefined:
      <div class="wutta-form-wrapper">
        ${form.render_vue_tag()}
      </div>
  % endif
</%def>

<%def name="render_vue_template_form()">
  % if form is not Undefined:
      ${form.render_vue_template()}
  % endif
</%def>

<%def name="render_vue_templates()">
  ${parent.render_vue_templates()}
  ${self.render_vue_template_form()}
</%def>

<%def name="make_vue_components()">
  ${parent.make_vue_components()}
  % if form is not Undefined:
      ${form.render_vue_finalize()}
  % endif
</%def>
