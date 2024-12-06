import Web_Component from '../../core/Web_Component.mjs'
import CSS__Forms    from '../../css/CSS__Forms.mjs'
import CSS__Buttons  from '../../css/CSS__Buttons.mjs'
import CSS__Icons    from '../../css/icons/CSS__Icons.mjs'
import Div           from '../../core/Div.mjs'
import Button        from '../../core/Button.mjs'
import Textarea      from '../../core/Textarea.mjs'
import CBR_Events    from "../CBR_Events.mjs";
import CSS__Alerts   from "../../css/CSS__Alerts.mjs";
import CSS__Grid     from "../../css/grid/CSS__Grid.mjs";

export default class WebC__User_Files__Markdown__Editor_View extends Web_Component {

    constructor() {
        super()
        this.content = ''
    }
    apply_css() {
        new CSS__Alerts (this).apply_framework()
        new CSS__Buttons(this).apply_framework()
        new CSS__Forms  (this).apply_framework()
        new CSS__Grid   (this).apply_framework()
        new CSS__Icons  (this).apply_framework()

        this.add_css_rules(this.css_rules())
    }

    add_event_listeners() {

        this.add_window_event_listener(CBR_Events.CBR__FILE__LOADED     , this.on_file_loaded     )
        this.add_window_event_listener(CBR_Events.CBR__FILE__EDIT_MODE  , this.on_file_edit_mode  )
        this.add_window_event_listener(CBR_Events.CBR__FILE__VIEW_MODE  , this.on_file_view_mode  )
        this.add_window_event_listener(CBR_Events.CBR__FILE__GET_CONTENT, this.on_file_get_content)

        this.add_event__on('input', '.markdown-editor', this.on_input_change)

        // const editor = this.query_selector('.markdown-editor')
        // editor.addEventListener('input', (e) => this.on_input_change(e))

        // // Version bar button handlers
        // if (this.viewing_version) {
        //     this.query_selector('.restore-version-btn')?.addEventListener('click', () => {
        //         this.raise_event_global('restore-version', {
        //             version_id: this.viewing_version
        //         })
        //     })
        //
        //     this.query_selector('.return-current-btn')?.addEventListener('click', () => {
        //         this.raise_event_global('return-current')
        //     })
        // }
    }
    on_input_change({event}) {
        this.content = event.target.value
        this.refresh_content()
        this.raise_event_global(CBR_Events.CBR__FILE__CHANGED, {content: this.content})
    }

    on_file_loaded(event) {
        this.file_id      = event.detail?.file_id
        this.content      = event.detail?.content
        this.refresh_content()
        //const editor_html = this.html__editor_viewer().html()
        //this.set_inner_html(editor_html)
    }
    on_file_edit_mode() {
        this.div_markdown_editor .show()
        this.div_markdown_preview.show()
        this.div_split_view.remove_class('viewer-only')
    }
    on_file_get_content(event) {
        event.detail.content = this.content
    }

    on_file_view_mode() {
        this.div_markdown_editor .hide()
        this.div_markdown_preview.show()
        this.div_split_view.add_class('viewer-only')

    }
    refresh_content() {
        this.query_selector('.markdown-editor').value      = this.content
        this.query_selector('.markdown-preview').innerHTML = marked.marked(this.content)
    }

    render_version_bar() {
        const version_bar = new Div({ class: 'version-bar' })
        version_bar.add_elements(
            new Div({
                class: 'version-message',
                value: 'Viewing previous version'
            }),
            new Button({
                class: 'btn btn-sm btn-success restore-version-btn',
                value: 'Restore This Version'
            }),
            new Button({
                class: 'btn btn-sm btn-secondary return-current-btn',
                value: 'Return to Current'
            })
        )
        return version_bar
    }


    html() {
        const container = new Div({ class: 'editor-view-container' })

        const split_view = new Div({ class: 'split-view' })
        split_view.add_elements( new Textarea({ class: 'markdown-editor'}),
                                 new Div     ({class: 'markdown-preview'}))
        container.add_element(split_view)
        return container

        // } else {
        //     if (this.viewing_version) {
        //         container.add_element(this.render_version_bar())
        //     }
        // }

    }

    // properties with dom elements
    get div_markdown_editor ()     { return this.query_selector('.markdown-editor' ) }
    get div_markdown_preview()     { return this.query_selector('.markdown-preview') }
    get div_split_view      ()     { return this.query_selector('.split-view'      ) }

    css_rules() {
        return {

            ".editor-view-container" : { display           : "flex"                      ,         // Main container
                                         flexDirection     : "column"                    ,
                                         height            : "100%"                      ,
                                         gap               : "1rem"                      },

            ".split-view"            : { display            : "grid"                      ,         // Edit mode view
                                         gridTemplateColumns: "1fr 1fr"                   ,
                                         gap                : "1rem"                      ,
                                         height             : "calc(100vh - 200px)"       ,
                                         minHeight          : "400px"                     },

            ".split-view.viewer-only"           : { gridTemplateColumns: "1fr"                       },

            ".markdown-editor"     : { width            : "100%"                      ,         // Editor textarea
                                      padding          : "1rem"                      ,
                                      fontSize         : "0.875rem"                  ,
                                      fontFamily       : "monospace"                 ,
                                      lineHeight       : "1.5"                       ,
                                      border           : "1px solid #dee2e6"         ,
                                      borderRadius     : "0.375rem"                  ,
                                      resize           : "none"                      ,
                                      outline          : "none"                      ,
                                      backgroundColor  : "#f8f9fa"                   ,
                                      color            : "#212529"                   },

            ".markdown-preview"    : { padding          : "1rem"                      ,         // Preview pane
                                      overflow         : "auto"                      ,
                                      fontSize         : "0.875rem"                  ,
                                      lineHeight       : "1.6"                       ,
                                      backgroundColor  : "#f8f9fa"                   ,
                                      borderRadius     : "0.375rem"                  },

            ".version-bar"         : { padding          : "0.75rem"                   ,         // Version viewing bar
                                      backgroundColor  : "#fff3cd"                   ,
                                      borderRadius     : "0.375rem"                  ,
                                      display          : "flex"                      ,
                                      alignItems       : "center"                    ,
                                      justifyContent   : "space-between"             },

            ".version-message"     : { fontSize         : "0.875rem"                  ,         // Version message
                                      color            : "#856404"                   },

            // Markdown preview styling
            ".markdown-preview h1" : { fontSize         : "1.75rem"                   ,         // Heading 1
                                      marginBottom     : "1rem"                      ,
                                      borderBottom     : "1px solid #dee2e6"         ,
                                      paddingBottom    : "0.5rem"                    },

            ".markdown-preview h2" : { fontSize         : "1.5rem"                    ,         // Heading 2
                                      marginBottom     : "1rem"                      ,
                                      borderBottom     : "1px solid #dee2e6"         ,
                                      paddingBottom    : "0.5rem"                    },

            ".markdown-preview h3" : { fontSize         : "1.25rem"                   ,         // Heading 3
                                      marginBottom     : "0.75rem"                   },

            ".markdown-preview p"  : { marginBottom     : "1rem"                      },        // Paragraphs

            ".markdown-preview code": { fontFamily      : "monospace"                 ,         // Inline code
                                      backgroundColor  : "#f1f3f5"                   ,
                                      padding          : "0.2em 0.4em"               ,
                                      borderRadius     : "0.25rem"                   },

            ".markdown-preview pre": { backgroundColor  : "#f8f9fa"                   ,         // Code blocks
                                     padding          : "1rem"                      ,
                                     borderRadius     : "0.375rem"                  ,
                                     marginBottom     : "1rem"                      ,
                                     overflow         : "auto"                      }
        }
    }
}

WebC__User_Files__Markdown__Editor_View.define()