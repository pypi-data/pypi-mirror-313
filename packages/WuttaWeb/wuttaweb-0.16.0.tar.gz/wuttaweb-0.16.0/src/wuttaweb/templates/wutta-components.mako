
<%def name="make_wutta_components()">
  ${self.make_wutta_request_mixin()}
  ${self.make_wutta_button_component()}
  ${self.make_wutta_filter_component()}
  ${self.make_wutta_filter_value_component()}
</%def>

<%def name="make_wutta_request_mixin()">
  <script>

    const WuttaRequestMixin = {
        methods: {

            wuttaGET(url, params, success, failure) {

                this.$http.get(url, {params: params}).then(response => {

                    if (response.data.error) {
                        this.$buefy.toast.open({
                            message: `Request failed:  ${'$'}{response.data.error}`,
                            type: 'is-danger',
                            duration: 4000, // 4 seconds
                        })
                        if (failure) {
                            failure(response)
                        }

                    } else {
                        success(response)
                    }

                }, response => {
                    this.$buefy.toast.open({
                        message: "Request failed:  (unknown server error)",
                        type: 'is-danger',
                        duration: 4000, // 4 seconds
                    })
                    if (failure) {
                        failure(response)
                    }
                })

            },

            wuttaPOST(action, params, success, failure) {

                const csrftoken = ${json.dumps(h.get_csrf_token(request))|n}
                const headers = {'X-CSRF-TOKEN': csrftoken}

                this.$http.post(action, params, {headers: headers}).then(response => {

                    if (response.data.error) {
                        this.$buefy.toast.open({
                            message: "Submit failed:  " + (response.data.error ||
                                                           "(unknown error)"),
                            type: 'is-danger',
                            duration: 4000, // 4 seconds
                        })
                        if (failure) {
                            failure(response)
                        }

                    } else {
                        success(response)
                    }

                }, response => {
                    this.$buefy.toast.open({
                        message: "Submit failed!  (unknown server error)",
                        type: 'is-danger',
                        duration: 4000, // 4 seconds
                    })
                    if (failure) {
                        failure(response)
                    }
                })
            },
        },
    }

  </script>
</%def>

<%def name="make_wutta_button_component()">
  <script type="text/x-template" id="wutta-button-template">
    <b-button :type="type"
              :native-type="nativeType"
              :tag="tag"
              :href="href"
              :title="title"
              :disabled="buttonDisabled"
              @click="clicked"
              icon-pack="fas"
              :icon-left="iconLeft">
      {{ buttonLabel }}
    </b-button>
  </script>
  <script>
    const WuttaButton = {
        template: '#wutta-button-template',
        props: {
            type: String,
            nativeType: String,
            tag: String,
            href: String,
            label: String,
            title: String,
            iconLeft: String,
            working: String,
            workingLabel: String,
            disabled: Boolean,
            once: Boolean,
        },
        data() {
            return {
                currentLabel: null,
                currentDisabled: null,
            }
        },
        computed: {
            buttonLabel: function() {
                return this.currentLabel || this.label
            },
            buttonDisabled: function() {
                if (this.currentDisabled !== null) {
                    return this.currentDisabled
                }
                return this.disabled
            },
        },
        methods: {

            clicked(event) {
                if (this.once) {
                    this.currentDisabled = true
                    if (this.workingLabel) {
                        this.currentLabel = this.workingLabel
                    } else if (this.working) {
                        this.currentLabel = this.working + ", please wait..."
                    } else {
                        this.currentLabel = "Working, please wait..."
                    }
                }
            }
        },
    }
    Vue.component('wutta-button', WuttaButton)
  </script>
</%def>

<%def name="make_wutta_filter_component()">
  <script type="text/x-template" id="wutta-filter-template">
    <div v-show="filter.visible"
         class="wutta-filter">

      <b-button @click="filter.active = !filter.active"
                class="filter-toggle"
                icon-pack="fas"
                :icon-left="filter.active ? 'check' : null"
                :size="isSmall ? 'is-small' : null">
        {{ filter.label }}
      </b-button>

      <div v-show="filter.active"
           style="display: flex; gap: 0.5rem;">

        <b-button v-if="verbKnown"
                  class="filter-verb"
                  @click="verbChoiceInit()"
                  :size="isSmall ? 'is-small' : null">
          {{ verbLabel }}
        </b-button>

        <b-autocomplete v-if="!verbKnown"
                        ref="verbAutocomplete"
                        :data="verbOptions"
                        v-model="verbTerm"
                        field="verb"
                        :custom-formatter="formatVerb"
                        open-on-focus
                        keep-first
                        clearable
                        clear-on-select
                        @select="verbChoiceSelect"
                        icon-pack="fas"
                        :size="isSmall ? 'is-small' : null" />

        <wutta-filter-value v-model="filter.value"
                            ref="filterValue"
                            v-show="valuedVerb()"
                            :is-small="isSmall" />

      </div>
    </div>
  </script>
  <script>

    const WuttaFilter = {
        template: '#wutta-filter-template',
        props: {
            filter: Object,
            isSmall: Boolean,
        },

        data() {
            return {
                verbKnown: !!this.filter.verb,
                verbLabel: this.filter.verb_labels[this.filter.verb],
                verbTerm: '',
            }
        },

        computed: {

            verbOptions() {

                // construct list of options
                const options = []
                for (let verb of this.filter.verbs) {
                    options.push({
                        verb,
                        label: this.filter.verb_labels[verb],
                    })
                }

                // parse list of search terms
                const terms = []
                for (let term of this.verbTerm.toLowerCase().split(' ')) {
                    term = term.trim()
                    if (term) {
                        terms.push(term)
                    }
                }

                // show all if no search terms
                if (!terms.length) {
                    return options
                }

                // only show filters matching all search terms
                return options.filter(option => {
                    let label = option.label.toLowerCase()
                    for (let term of terms) {
                        if (label.indexOf(term) < 0) {
                            return false
                        }
                    }
                    return true
                })

                return options
            },
        },

        methods: {

            focusValue() {
                this.$refs.filterValue.focus()
            },

            formatVerb(option) {
                return option.label || option.verb
            },

            verbChoiceInit(option) {
                this.verbKnown = false
                this.$nextTick(() => {
                    this.$refs.verbAutocomplete.focus()
                })
            },

            verbChoiceSelect(option) {
                this.filter.verb = option.verb
                this.verbLabel = option.label
                this.verbKnown = true
                this.verbTerm = ''
                this.focusValue()
            },

            valuedVerb() {
                /* return true if the current verb should expose value input(s) */

                // if filter has no "valueless" verbs, then all verbs should expose value inputs
                if (!this.filter.valueless_verbs) {
                    return true
                }

                // if filter *does* have valueless verbs, check if "current" verb is valueless
                if (this.filter.valueless_verbs.includes(this.filter.verb)) {
                    return false
                }

                // current verb is *not* valueless
                return true
            },
        }
    }

    Vue.component('wutta-filter', WuttaFilter)

  </script>
</%def>

<%def name="make_wutta_filter_value_component()">
  <script type="text/x-template" id="wutta-filter-value-template">
    <div class="wutta-filter-value">

      <b-input v-model="inputValue"
               ref="valueInput"
               @input="val => $emit('input', val)"
               :size="isSmall ? 'is-small' : null" />

    </div>
  </script>
  <script>

    const WuttaFilterValue = {
        template: '#wutta-filter-value-template',
        props: {
            value: String,
            isSmall: Boolean,
        },

        data() {
            return {
                inputValue: this.value,
            }
        },

        methods: {

            focus: function() {
                this.$refs.valueInput.focus()
            }
        },
    }

    Vue.component('wutta-filter-value', WuttaFilterValue)

  </script>
</%def>
