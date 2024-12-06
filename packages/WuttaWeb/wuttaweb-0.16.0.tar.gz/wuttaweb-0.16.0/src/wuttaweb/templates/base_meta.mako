## -*- coding: utf-8; -*-

<%def name="global_title()">${app.get_node_title()}</%def>

<%def name="extra_styles()"></%def>

<%def name="favicon()">
  <link rel="icon" type="image/x-icon" href="${config.get('wuttaweb.favicon_url', default=request.static_url('wuttaweb:static/img/favicon.ico'))}" />
</%def>

<%def name="header_logo()">
  ${h.image(config.get('wuttaweb.header_logo_url', default=request.static_url('wuttaweb:static/img/favicon.ico')), "Header Logo", style="height: 49px;")}
</%def>

<%def name="full_logo(image_url=None)">
  ${h.image(image_url or config.get('wuttaweb.logo_url', default=request.static_url('wuttaweb:static/img/logo.png')), f"{app.get_title()} logo")}
</%def>

<%def name="footer()">
  <p class="has-text-centered">
    powered by ${h.link_to("WuttaWeb", 'https://wuttaproject.org/', target='_blank')}
  </p>
</%def>
