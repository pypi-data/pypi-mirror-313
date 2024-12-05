import Web_Component        from "../../core/Web_Component.mjs";
import API__Invoke          from "../../data/API__Invoke.mjs";
import Div                  from "../../core/Div.mjs";
import Raw_Html             from "../../core/Raw_Html.mjs";
import Load_Libraries__CSS  from "../../utils/Load_Libraries__CSS.mjs";

export default class WebC__API_Markdown_To_Html extends Web_Component {
    static url__cdn_files                              = 'https://static.dev.aws.cyber-boardroom.com/cbr-content/latest/'
    static url__api_markdown_file_to_html_and_metadata = '/markdown/render/markdown-file-to-html-and-metadata?path='
    static class__markdown_section                     = 'markdown_section'
    static class__markdown_html                        = 'markdown_html'
    static class__markdown_metadata                    = 'markdown_metadata'
    static class__markdown_error                       = 'markdown_error'
    static class__markdown_title                       = 'markdown_title'
    static class__markdown_sub_title                   = 'markdown_sub_title'
    static class__markdown_description                 = 'markdown_description'
    static on_error_return_value                       = { html:'(error loading markdown content)', metadata:{}}

    // base class methods overrides

    async apply_css() {
        if (this.should_apply_css) {                                                   // todo: find a better place to put this logic
            this.add_css_rules(this.css_rules())
        }
    }

    async load_data() {
        const mock_responses                   = JSON.parse(this.getAttribute('mock_responses'))
        this.markdown_metadata                 = null
        this.markdown_html                     = null
        this.api_invoke                        = new API__Invoke()
        this.api_invoke.on_error_return_value  = WebC__API_Markdown_To_Html.on_error_return_value
        await this.load_html_content_and_metadata()

        this.load_libraries__css               = new Load_Libraries__CSS({target:this})      // todo: legacy, not needed anymore in the new pure WebC model
    }

    async component_ready() {
        this.raise_event('build-complete')
    }

    load_attributes() {
        super.load_attributes()
        this.content_path                      = this.getAttribute('content-path')
        this.should_apply_css                  = this.hasAttribute('apply-css'   )                   // todo: fix this clash of attribute name 'should_apply_css', with override should_apply_css in Web_Component
        this.use_cdn_for_markdown_file_content = this.hasAttribute('disable-cdn' ) === false
    }

    // class methods

    html() {
        const div_markdown    = new Div     ({class: WebC__API_Markdown_To_Html.class__markdown_section     })
        const div_html        = new Raw_Html({class: WebC__API_Markdown_To_Html.class__markdown_html        })
        const div_metadata    = new Div     ({class: WebC__API_Markdown_To_Html.class__markdown_metadata    })
        const div_error       = new Div     ({class: WebC__API_Markdown_To_Html.class__markdown_error       })
        const div_title       = new Div     ({class: WebC__API_Markdown_To_Html.class__markdown_title       })
        const div_sub_title   = new Div     ({class: WebC__API_Markdown_To_Html.class__markdown_sub_title   })
        const div_description = new Div     ({class: WebC__API_Markdown_To_Html.class__markdown_description })


        div_html.raw_html     = this.markdown_html

        if (this.markdown_metadata) {
            div_error      .value = this.markdown_metadata.error
            div_title      .value = this.markdown_metadata.title
            div_sub_title  .value = this.markdown_metadata.sub_title
            div_description.value = this.markdown_metadata.description

            if (this.markdown_metadata.error      ) { div_metadata.add_element(div_error      ) }
            if (this.markdown_metadata.title      ) { div_metadata.add_element(div_title      ) }
            if (this.markdown_metadata.sub_title  ) { div_metadata.add_element(div_sub_title  ) }
            if (this.markdown_metadata.description) { div_metadata.add_element(div_description) }

            div_markdown.add_element(div_metadata)
        }
        div_markdown.add_element(div_html)

        return div_markdown
    }

    css_rules() {
        return {    [`.${WebC__API_Markdown_To_Html.class__markdown_section}`    ] : { 'background-color' : '#fff'           ,
                                                                                       'margin'           : '10px'              ,
                                                                                       'border'           : '1px solid #ddd'      ,
                                                                                       'border-radius'    : '8px'                 ,
                                                                                       'padding'          : '10px'              },
                    [`.${WebC__API_Markdown_To_Html.class__markdown_title}`      ] : { 'font-size'        : '24px'              ,
                                                                                       'font-weight'      : 'bold'              ,
                                                                                       'margin-bottom'    : '8px'               },
                    [`.${WebC__API_Markdown_To_Html.class__markdown_sub_title}`  ] : { 'font-size'        : '20px'              ,
                                                                                       'font-weight'     : 'normal'             ,
                                                                                       'color'           : '#555'               ,
                                                                                       'margin-bottom'   : '6px'                },
                    [`.${WebC__API_Markdown_To_Html.class__markdown_description}`] : { 'font-size'        : '16px'              ,
                                                                                       'font-style'      : 'italic'             ,
                                                                                       'color'           : '#666'               ,
                                                                                       'margin-bottom'   : '12px'               },
                    [`.${WebC__API_Markdown_To_Html.class__markdown_error}`      ] : { 'font-size'        : '16px'              ,
                                                                                       'font-style'      : 'italic'             ,
                                                                                       'color'           : 'red'                },
                    [`.${WebC__API_Markdown_To_Html.class__markdown_html}`       ] : { },

                    // extra class which will need to be moved somewhere else since these are inspired by Bootstrap and will be very useful in other modules
                    [`.alert`                                                    ] : { 'padding'         : '20px'                 ,
                                                                                       'margin-bottom'   : '20px'                 ,
                                                                                       'border'          : '1px solid transparent',
                                                                                       'border-radius'   : '4px'                  ,
                                                                                       'font-family'     : 'Arial, sans-serif'    },

                    [`.alert-warning`                                            ] : { 'background-color': '#fff0d5'              ,
                                                                                       'border-color'    : '#ffe8bf'              ,
                                                                                       'color'           : '#664711'              },
                    [`.alert .alert-heading`                                     ] : { 'font-size'       : '1.5em'                ,
                                                                                       'margin-top'      : '0'                    ,
                                                                                       'margin-bottom'   : '10px'                 ,
                                                                                       'color'           : '#664711'              },
                    [`.alert p`                                                  ] : { 'margin'          : '0'                    ,
                                                                                       'font-size'       : '1em'                  },
                }
    }

    async load_html_content_and_metadata() {
        if (!this.content_path) { return }
        const method           = 'GET'
        const  target_url      = this.resolve_target_url()
        const html_and_metadata = await this.api_invoke.invoke_api(target_url, method)
        this.markdown_html     = html_and_metadata.html
        this.markdown_metadata = html_and_metadata.metadata
    }

    resolve_target_url() {
        if (this.use_cdn_for_markdown_file_content) {
            return WebC__API_Markdown_To_Html.url__cdn_files + this.content_path + '.json'
        } else {
            return WebC__API_Markdown_To_Html.url__api_markdown_file_to_html_and_metadata + this.content_path
        }
    }
}

WebC__API_Markdown_To_Html.define()