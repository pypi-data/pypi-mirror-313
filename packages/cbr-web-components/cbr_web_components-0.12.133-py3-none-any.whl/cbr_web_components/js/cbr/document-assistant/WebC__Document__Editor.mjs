// WebC__Document__Editor.mjs

import Web_Component from '../../core/Web_Component.mjs'
import CSS__Forms     from '../../css/CSS__Forms.mjs'
import CSS__Buttons   from '../../css/CSS__Buttons.mjs'
import CSS__Icons     from '../../css/icons/CSS__Icons.mjs'
import API__Invoke    from '../../data/API__Invoke.mjs'
import Div            from '../../core/Div.mjs'
import Button         from '../../core/Button.mjs'
import Icon           from '../../css/icons/Icon.mjs'
import Raw_Html       from '../../core/Raw_Html.mjs'

export default class WebC__Document__Editor extends Web_Component {

    constructor() {
        super()
        this.api_invoke  = new API__Invoke()
        this.version     = 1
        this.unsaved_changes = false
    }

    apply_css() {
        new CSS__Forms   (this).apply_framework()
        new CSS__Buttons (this).apply_framework()
        new CSS__Icons   (this).apply_framework()
        this.add_css_rules(this.css_rules())
    }
    load_attributes() {
        this.file_id     = this.getAttribute('file-id')
        this.content     = this.getAttribute('content')
    }


    add_event_listeners() {
        this.add_window_event_listener('changes:accept' , this.handle__changes_accept  )
        this.add_window_event_listener('version:reset'  , this.handle__version_reset   )
        this.add_window_event_listener('content-changed', this.handle__content_changed )
    }

    add_event_handlers() {
        this.add_event__on('input'   , '.markdown-editor', this.handle__editor_input  )
        this.add_event__on('click'   , '.save-btn'      , this.handle__save_click     )
        this.add_event__on('click'   , '.preview-btn'   , this.handle__preview_toggle )
        this.add_event__on('keydown' , '.markdown-editor', this.handle__editor_keydown )
    }

    handle__editor_input({event}) {                                                     // Handle editor content changes
        this.content = event.target.value
        this.update_status('unsaved')
        this.update_preview()
        this.raise_event_global('content-changed', { content: this.content })
    }

    async handle__save_click() {                                                             // Handle manual save button click
        await this.save_content()
    }

    handle__preview_toggle() {                                                         // Handle preview mode toggle
        const editor_area = this.query_selector('.editor-area')
        editor_area.classList.toggle('show-preview')

        const preview_btn = this.query_selector('.preview-btn')
        preview_btn.innerHTML = editor_area.classList.contains('show-preview')
            ? this.html__edit_button()
            : this.html__preview_button()
    }

    handle__editor_keydown({event}) {                                                  // Handle tab key in editor
        if (event.key === 'Tab') {
            event.preventDefault()
            const editor         = event.target
            const start         = editor.selectionStart
            const end           = editor.selectionEnd
            editor.value        = editor.value.substring(0, start) +
                                 '    ' +
                                 editor.value.substring(end)
            editor.selectionStart = editor.selectionEnd = start + 4
        }
    }

    html__edit_button() {
        return '<i class="icon">✎</i> Edit'
    }

    html__preview_button() {
        return '<i class="icon">👁</i> Preview'
    }

    async handle__changes_accept(event) {
        if (event.detail.changes) {
            this.content          = event.detail.new_version
            this.unsaved_changes = true
            await this.update_editor()
            await this.save_content()
        }
    }

    async handle__version_reset(event) {
        if (event.detail.content) {
            this.content         = event.detail.content
            this.version        = event.detail.version
            await this.update_editor()
        }
    }

    handle__content_changed() {
        this.unsaved_changes = true
        //if (this.save_timer) { clearTimeout(this.save_timer) }
        //this.save_timer = setTimeout(() => this.save_content(), 2000)                 // Auto-save after 2 seconds
    }

    disconnectedCallback() {
        super.disconnectedCallback()
        //if (this.save_timer) { clearTimeout(this.save_timer) }                        // Clean up timer when component is destroyed
    }

    async save_content() {
        if (!this.unsaved_changes) return

        try {
            await this.api_invoke.invoke_api(
                '/api/user-data/files/update-file',
                'PUT',
                {
                    file_id: this.file_id,
                    file_bytes__base64: btoa(this.content)
                }
            )

            this.version++
            this.unsaved_changes = false
            this.update_status('document-saved')

            // Notify parent of save
            this.raise_event('document-saved', {
                content: this.content,
                version: this.version
            })

        } catch (error) {
            //console.error('Error saving document:', error)
            this.update_status('save-error')
        }
    }

    update_status(status) {
        const status_el = this.query_selector('.editor-status')
        const toolbar = this.query_selector('.editor-toolbar')

        //if (!status_el || !toolbar) return

        switch (status) {
            case 'document-saved':
                status_el.textContent = 'All changes saved'
                status_el.className = 'editor-status status-success'
                toolbar.classList.remove('unsaved')
                break
            case 'save-error':
                status_el.textContent = 'Error saving changes'
                status_el.className = 'editor-status status-error'
                break
            case 'unsaved':
                status_el.textContent = 'Unsaved changes'
                status_el.className = 'editor-status status-warning'
                toolbar.classList.add('unsaved')
                break
        }

        // Clear success/error messages after delay
        // if (status !== 'unsaved') {
        //     setTimeout(() => {
        //         status_el.textContent = this.unsaved_changes ? 'Unsaved changes' : ''
        //         status_el.className = this.unsaved_changes ? 'editor-status status-warning' : 'editor-status'
        //     }, 3000)
        //}
    }

    async update_editor() {
        const editor = this.query_selector('.markdown-editor')
        if (editor) {
            editor.value = this.content
            this.update_preview()
            this.update_status(this.unsaved_changes ? 'unsaved' : 'document-saved')
        }
    }

    update_preview() {
        const preview = this.query_selector('.markdown-preview')
        if (preview) {
            preview.innerHTML = marked.marked(this.content)
        }
    }

    html() {
        const container = new Div({ class: 'editor-container' })

        // Toolbar
        const toolbar = new Div({ class: 'editor-toolbar' })

        // Version info and status
        const info = new Div({ class: 'editor-info' })
        info.add_elements(
            new Div({ class: 'version-info', value: `v${this.version}` }),
            new Div({ class: 'editor-status' })
        )

        // Save button
        const save_btn = new Button({
            class: 'btn btn-primary save-btn',
            value: 'Save'
        })
        save_btn.add_element(new Icon({ icon: 'save', size: 'sm', spacing: 'right' }))

        // Preview toggle
        const preview_btn = new Button({
            class: 'btn btn-secondary preview-btn',
            value: 'Preview'
        })
        preview_btn.add_element(new Icon({ icon: 'eye', size: 'sm', spacing: 'right' }))

        toolbar.add_elements(info, save_btn, preview_btn)

        // Editor area
        const editor_area = new Div({ class: 'editor-area' })

        // Main editor
        const editor = new Div({
            tag: 'textarea',
            class: 'markdown-editor',
            value: this.content,
            attributes: {
                spellcheck: 'false',
                'data-gramm': 'false'
            }
        })

        // Preview panel (hidden by default)
        const preview = new Div({ class: 'markdown-preview' })
        preview.value = marked.marked(this.content)

        editor_area.add_elements(editor, preview)
        container.add_elements(toolbar, editor_area)

        return container
    }



    css_rules() {
        return {
            ".editor-container"    : { display         : "flex"                      ,      // Main container
                                     flexDirection    : "column"                    ,
                                     height          : "100%"                      ,
                                     backgroundColor : "#fff"                      },

            ".editor-toolbar"      : { display         : "flex"                      ,      // Toolbar
                                     justifyContent  : "space-between"             ,
                                     alignItems      : "center"                    ,
                                     padding         : "0.75rem"                   ,
                                     borderBottom    : "1px solid #dee2e6"         ,
                                     backgroundColor : "#f8f9fa"                   ,
                                     gap             : "0.5rem"                    },

            ".editor-info"         : { display         : "flex"                      ,      // Version and status
                                     alignItems      : "center"                    ,
                                     gap             : "1rem"                      },

            ".version-info"        : { fontSize        : "0.75rem"                   ,      // Version number
                                     color           : "#6c757d"                   ,
                                     padding         : "0.25rem 0.5rem"            ,
                                     backgroundColor : "#e9ecef"                   ,
                                     borderRadius    : "0.25rem"                   },

            ".editor-status"       : { fontSize        : "0.75rem"                   },     // Status message

            ".status-success"      : { color           : "#198754"                   },     // Status states
            ".status-error"        : { color           : "#dc3545"                   },
            ".status-warning"      : { color           : "#ffc107"                   },

            ".editor-area"         : { display         : "flex"                    ,      // Editor/Preview container
                                     flex            : "1"                         ,
                                     minHeight       : "250px"                     ,
                                     position        : "relative"                  },

            ".markdown-editor"     : { flex            : "1"                         ,      // Editor
                                     padding         : "1rem"                      ,
                                     fontSize        : "0.875rem"                  ,
                                     fontFamily      : "Monaco, monospace"         ,
                                     lineHeight      : "1.6"                      ,
                                     border          : "none"                      ,
                                     resize          : "none"                      ,
                                     outline         : "none"                      ,
                                     backgroundColor : "#f8f9fa"                   ,
                                     color           : "#212529"                   },

            ".markdown-preview"    : { display         : "none"                      ,      // Preview panel
                                     flex            : "1"                         ,
                                     padding         : "1rem"                      ,
                                     overflow        : "auto"                      ,
                                     backgroundColor : "#fff"                      },

            // Show preview mode
            ".editor-area.show-preview .markdown-editor"  : { display: "none"       },
            ".editor-area.show-preview .markdown-preview" : { display: "block"      },

            // Preview content styling
            // ".markdown-preview"    : { "& h1"          : { marginTop    : "0"              ,
            //                                              marginBottom : "1rem"            ,
            //                                              fontSize     : "2rem"            },
            //                          "& h2"          : { marginTop    : "1.5rem"          ,
            //                                              marginBottom : "1rem"            ,
            //                                              fontSize     : "1.5rem"          },
            //                          "& h3"          : { marginTop    : "1.25rem"         ,
            //                                              marginBottom : "0.75rem"         ,
            //                                              fontSize     : "1.25rem"         },
            //                          "& p"           : { marginBottom : "1rem"            },
            //                          "& ul, & ol"    : { marginBottom : "1rem"            ,
            //                                              paddingLeft  : "2rem"            },
            //                          "& code"        : { backgroundColor: "#f8f9fa"       ,
            //                                              padding       : "0.2rem 0.4rem"   ,
            //                                              borderRadius  : "0.25rem"         },
            //                          "& pre"         : { backgroundColor: "#f8f9fa"       ,
            //                                              padding       : "1rem"            ,
            //                                              borderRadius  : "0.375rem"        ,
            //                                              marginBottom  : "1rem"            ,
            //                                              overflow      : "auto"            },
            //                          "& blockquote"  : { borderLeft     : "0.25rem solid #dee2e6",
            //                                              paddingLeft    : "1rem"            ,
            //                                              marginBottom   : "1rem"            ,
            //                                              color          : "#6c757d"         }},

            // Unsaved changes indicator
            ".editor-toolbar.unsaved": { "& .save-btn": { animation: "pulse 2s infinite" }},

            "@keyframes pulse"     : { "0%"           : { transform: "scale(1)"          },
                                     "50%"          : { transform: "scale(1.05)"        },
                                     "100%"         : { transform: "scale(1)"          }}
        }
    }
}

WebC__Document__Editor.define()