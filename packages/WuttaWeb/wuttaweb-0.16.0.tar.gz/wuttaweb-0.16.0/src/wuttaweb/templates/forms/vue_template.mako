## -*- coding: utf-8; -*-

<script type="text/x-template" id="${form.vue_tagname}-template">
  ${h.form(form.action_url, method='post', enctype='multipart/form-data', **form_attrs)}
    ${h.csrf_token(request)}

    <section>
      % for fieldname in form:
          ${form.render_vue_field(fieldname)}
      % endfor
    </section>

    % if not form.readonly:
        <br />
        <div class="buttons"
             % if form.align_buttons_right:
             style="justify-content: right;"
             % endif
             >

          % if form.show_button_cancel:
              <wutta-button ${'once' if form.auto_disable_cancel else ''}
                            tag="a" href="${form.get_cancel_url()}"
                            label="${form.button_label_cancel}" />
          % endif

          % if form.show_button_reset:
              <b-button native-type="reset">
                Reset
              </b-button>
          % endif

          <b-button type="${form.button_type_submit}"
                    native-type="submit"
                    % if form.auto_disable_submit:
                        :disabled="formSubmitting"
                    % endif
                    icon-pack="fas"
                    icon-left="${form.button_icon_submit}">
            % if form.auto_disable_submit:
                {{ formSubmitting ? "Working, please wait..." : "${form.button_label_submit}" }}
            % else:
                ${form.button_label_submit}
            % endif
          </b-button>

        </div>
    % endif

  ${h.end_form()}
</script>

<script>

  let ${form.vue_component} = {
      template: '#${form.vue_tagname}-template',
      methods: {},
  }

  let ${form.vue_component}Data = {

      % if not form.readonly:

          modelData: ${json.dumps(model_data)|n},

          % if form.auto_disable_submit:
              formSubmitting: false,
          % endif

      % endif

      % if form.grid_vue_context:
          gridContext: {
              % for key, data in form.grid_vue_context.items():
                  '${key}': ${json.dumps(data)|n},
              % endfor
          },
      % endif
  }

</script>
