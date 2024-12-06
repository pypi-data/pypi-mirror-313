import Web_Component from '../../core/Web_Component.mjs'
import CSS__Forms    from '../../css/CSS__Forms.mjs'
import CSS__Cards    from '../../css/CSS__Cards.mjs'
import CSS__Buttons  from '../../css/CSS__Buttons.mjs'
import API__Invoke   from '../../data/API__Invoke.mjs'
import Div           from '../../core/Div.mjs'
import Button        from '../../core/Button.mjs'

export default class WebC__User_Files__Content__Chat extends Web_Component {

    async apply_css() {
        this.add_css_rules (this.css_rules())
    }


    load_attributes() {
        new CSS__Forms  (this).apply_framework()
        new CSS__Cards  (this).apply_framework()
        new CSS__Buttons(this).apply_framework()
        this.api_invoke = new API__Invoke()
        this.file_id    = this.getAttribute('file_id')
        this.chat_mode  = 'content'                                    // Can be 'content' or 'summary'
    }

    async load_data() {
        const path         = `/api/user-data/files/file-contents?file_id=${this.file_id}`
        const response     = await this.api_invoke.invoke_api(path)
        this.file_data     = response.data.file_data
        this.file_summary  = JSON.parse(response.data.file_summary)
        this.content_bytes = response.data.file_bytes__base64
        const decoded      = atob(this.content_bytes)                                                            // Decode content for chat context
        this.content       = new TextDecoder().decode(new Uint8Array([...decoded].map(c => c.charCodeAt(0))))
    }

    toggle_chat_mode = async () => {
        this.chat_mode = this.chat_mode === 'content' ? 'summary' : 'content'
        await this.refresh_ui()
    }

    render_toolbar() {
        const toolbar   = new Div({ class: 'chat-toolbar' })
        const btn_class = this.chat_mode === 'content' ? 'btn-primary' : 'btn-outline-primary'
        const mode_btn  = new Button({class: `btn ${btn_class} mode-btn`,
                                     value: `Chat with ${this.chat_mode === 'content' ? 'Summary' : 'Content'}`})

        toolbar.add_element(mode_btn)
        return toolbar
    }

    render_chat() {
        const chat_container = new Div({ class: 'chat-container' })

        chat_container.add_tag({                                                        // Add chatbot component with appropriate context
            tag: 'chatbot-openai',
            attributes: { channel        : `file-chat-${this.file_id}`                                         ,
                          name           : `File ${this.chat_mode === 'content' ? 'Content' : 'Summary'} Chat` ,
                          edit_mode      : 'false'                                                             ,
                          url            : '/api/llms/chat/completion'                                         ,
                          initial_message: `I'm ready to discuss the file's ${this.chat_mode}`                 ,
                          system_prompt  : this.get_system_prompt()                                            }})

        return chat_container
    }

    get_system_prompt() {

        if (this.chat_mode === 'content') {
            return `You are a helpful assistant discussing a file's content. Here is the file content:
                ${this.content}
                
                Please help answer questions about this content.`
        } else {
            return `You are a helpful assistant discussing a file's summary. Here is the file summary:
                ${this.file_summary}
                
                Please help answer questions about this summary.`
        }
    }

    html() {
        const container = new Div({ class: 'content-chat-container' })

        container.add_elements(this.render_toolbar(), this.render_chat() )

        return container
    }

    add_event_handlers() {
        const mode_btn = this.query_selector('.chat-toolbar .btn')                          // Mode toggle button
        if (mode_btn) {
            mode_btn.addEventListener('click', this.toggle_chat_mode)
        }
    }

    remove_event_handlers() {
        const mode_btn = this.query_selector('.chat-toolbar .btn');
        if (mode_btn) {
            mode_btn.removeEventListener('click', this.toggle_chat_mode);
        }
    }

    css_rules() {
        return {
            ".view-tabs"             : { display          : "flex"                      ,           // View tabs styling
                                       gap              : "0.5rem"                     ,
                                       marginBottom      : "1rem"                      ,
                                       padding          : "0.5rem 0"                   ,
                                       borderBottom      : "1px solid #dee2e6"         },

            ".content-view"          : { flex             : "1"                         ,
                                       display           : "flex"                      ,
                                       flexDirection     : "column"                    ,
                                       gap              : "1rem"                      },

            ".chat-view"             : { flex             : "1"                         ,
                                       display           : "flex"                      ,
                                       flexDirection     : "column"                    ,
                                       minHeight         : "400px"                     },
            ".content-chat-container" : { padding          : "1rem"                      ,
                                        backgroundColor   : "#fff"                      ,
                                        borderRadius      : "0.375rem"                  ,
                                        boxShadow         : "0 2px 4px rgba(0,0,0,0.1)" ,
                                        display           : "flex"                      ,
                                        flexDirection     : "column"                    ,
                                        gap              : "1rem"                      ,
                                        height            : "100%"                      },

            ".chat-toolbar"           : { display          : "flex"                      ,
                                        justifyContent    : "flex-end"                  ,
                                        padding          : "0.5rem"                     ,
                                        borderBottom      : "1px solid #dee2e6"         },

            ".chat-container"         : { flex             : "1"                         ,
                                        minHeight         : "0"                         ,
                                        display           : "flex"                      ,
                                        flexDirection     : "column"                    },

            "chatbot-openai"          : { flex             : "1"                         ,
                                        minHeight         : "0"                         },

            ".error-message"          : { color            : "#dc3545"                   ,
                                        fontSize          : "0.875rem"                  ,
                                        padding          : "0.5rem"                     },

            // Chat interface customization
            ".chat-interface"         : { display          : "flex"                      ,
                                        flexDirection     : "column"                    ,
                                        gap              : "1rem"                      ,
                                        padding          : "1rem"                      },

            ".chat-messages"          : { flex             : "1"                         ,
                                        overflowY         : "auto"                      ,
                                        padding          : "1rem"                      ,
                                        backgroundColor   : "#f8f9fa"                   ,
                                        borderRadius      : "0.375rem"                  }
        }
    }
}

WebC__User_Files__Content__Chat.define()