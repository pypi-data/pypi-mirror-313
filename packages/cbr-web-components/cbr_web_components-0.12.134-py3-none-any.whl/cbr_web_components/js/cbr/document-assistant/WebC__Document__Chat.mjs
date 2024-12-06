// WebC__Document__Chat.mjs

import Web_Component from '../../core/Web_Component.mjs'
import CSS__Forms     from '../../css/CSS__Forms.mjs'
import CSS__Buttons   from '../../css/CSS__Buttons.mjs'
import CSS__Cards     from '../../css/CSS__Cards.mjs'
import CSS__Icons     from '../../css/icons/CSS__Icons.mjs'
import API__Invoke    from '../../data/API__Invoke.mjs'
import Div            from '../../core/Div.mjs'
import Textarea       from '../../core/Textarea.mjs'
import Button         from '../../core/Button.mjs'
import Icon           from '../../css/icons/Icon.mjs'
import Raw_Html       from '../../core/Raw_Html.mjs'
import CBR_Events from "../CBR_Events.mjs";

export default class WebC__Document__Chat extends Web_Component {
    constructor() {
        super();
        this.api_invoke  = new API__Invoke()
        this.messages    = []
        this.chat_id     = this.random_uuid()
        this.streaming   = false
    }
    apply_css() {
        new CSS__Forms   (this).apply_framework()
        new CSS__Buttons (this).apply_framework()
        new CSS__Cards   (this).apply_framework()
        new CSS__Icons   (this).apply_framework()
        this.add_css_rules(this.css_rules())
    }

    load_attributes() {
        this.file_id     = this.getAttribute('file-id')
        this.content     = this.getAttribute('content') || ''
    }

    async component_ready() {
        this.add_initial_messages()
    }

    add_event_listeners() {
        this.add_window_event_listener('document-updated', this.handle__on_document_updated)
    }

    add_event_handlers() {
        this.add_event__on('keydown', '.chat-input'  , this.handle__on_keydown__chat_input)
        this.add_event__on('click'  , '.send-button' , this.handle__on_click__send_button )
    }

    handle__on_keydown__chat_input({event}) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault()
            this.send_message_if_valid()
        }
    }

    async handle__on_click__send_button() {
        await this.send_message_if_valid()
    }

    async send_message_if_valid() {
        const input     = this.query_selector('.chat-input'  )
        const send_btn  = this.query_selector('.send-button' )
        const message   = input.value.trim()

        if (message && !this.streaming) {
            input.value     = ''
            input.disabled  = true
            send_btn.disabled = true
            send_btn.innerHTML = 'Processing...'
            await this.send_message(message)
        }
    }

    handle__on_document_updated(event) {
        if (event.detail.file_id === this.file_id) {
            this.content = event.detail.content
            this.add_system_message('Document updated. I have the latest version.')
        }
    }

    add_initial_messages() {
        this.add_system_message('Hello! I\'m here to help improve your document. Here are some ways I can help:')

        const suggestions = [
            "💡 Improve clarity and readability",
            "✍️ Enhance formatting and structure",
            "🔍 Fix grammar and style issues",
            "📝 Add missing sections or details",
            "🎯 Make content more concise"
        ]

        const suggestion_html = suggestions.join('\n')
        this.add_system_message(suggestion_html)
    }

    async send_message(message) {
        if (this.streaming) return

        this.add_user_message(message)
        this.streaming = true
        this.current_message = this.add_assistant_message('Processing request...')

        try {
            const server = 'https://osbot-llms.dev.aws.cyber-boardroom.com'
            const url = server + '/json-prompt/improve-document'
            const response = await this.api_invoke.invoke_api(url, 'POST',
                {
                    current_content: this.content,
                    improvement_request: message
                }
            )

            if (response.status === 'ok' && response.data?.response_json) {
                const result = response.data.response_json

                // Update assistant's message with change summary
                let message_content = `**Changes Summary:**\n${result.document.summary}\n\n`

                // Add detailed changes
                message_content += '**Proposed Changes:**\n'
                result.document.changes.forEach((change, index) => {
                    message_content += `\n${index + 1}. ${change.type.toUpperCase()}\n`
                    message_content += `   - ${change.reason}\n`
                })

                // Add action buttons to message
                this.current_message.update_content(message_content)
                //this.add_action_buttons(result)

                // Raise event to show diff view
                this.raise_event_global('diff:show')
                this.raise_event_global('update-diff-view', {
                    file_id: this.file_id,
                    changes: result
                })
            } else {
                this.current_message.update_content('Error: Invalid response format')
                await this.raise_event_global(CBR_Events.CBR__LLM__REQUEST__ERROR)
            }
        } catch (error) {
            this.current_message.update_content('Error: Failed to get response')
            await this.raise_event_global(CBR_Events.CBR__LLM__REQUEST__ERROR)
        } finally {
            this.streaming = false
        }
    }

    // add_action_buttons(result) {
    //     const actions = new Div({ class: 'message-actions' })
    //
    //     const preview_btn = new Button({
    //         class: 'btn btn-primary btn-sm preview-btn',
    //         value: 'Preview Changes'
    //     })
    //     preview_btn.add_element(new Icon({ icon: 'eye', size: 'sm', spacing: 'right' }))
    //
    //     const accept_btn = new Button({
    //         class: 'btn btn-success btn-sm accept-btn',
    //         value: 'Accept All'
    //     })
    //     accept_btn.add_element(new Icon({ icon: 'check', size: 'sm', spacing: 'right' }))
    //
    //     const reject_btn = new Button({
    //         class: 'btn btn-danger btn-sm reject-btn',
    //         value: 'Reject'
    //     })
    //     reject_btn.add_element(new Icon({ icon: 'cross', size: 'sm', spacing: 'right' }))
    //
    //     actions.add_elements(preview_btn, accept_btn, reject_btn)
    //
    //     const msg_element = this.query_selector(`#msg-${this.current_message.id}`)
    //     msg_element.appendChild(actions.dom_create())
    //
    //     // Add event listeners
    //     preview_btn.dom_create().addEventListener('click', () => this.raise_event_global('diff:show'))
    //     accept_btn.dom_create().addEventListener('click', () => this.raise_event_global('changes:accept', { changes: result.document }))
    //     reject_btn.dom_create().addEventListener('click', () => this.raise_event_global('changes:reject'))
    // }

    add_message(content, type) {
        const message = { id: this.random_uuid(), type, content, timestamp: new Date() }
        this.messages.push(message)
        this.render_message(message)
        this.scroll_to_bottom()
        return message
    }

    add_user_message(content) {
        return this.add_message(content, 'user')
    }

    add_system_message(content) {
        return this.add_message(content, 'system')
    }

    add_assistant_message(content) {
        const message = this.add_message(content, 'assistant')
        return {
            id: message.id,
            update_content: (new_content) => {
                message.content = new_content
                const msg_element = this.query_selector(`#msg-${message.id} .message-content`)
                if (msg_element) {
                    msg_element.innerHTML = marked.marked(new_content)
                }
            }
        }
    }

    render_message(message) {
        const messages_container = this.query_selector('.chat-messages')
        const msg_div = document.createElement('div')
        msg_div.id = `msg-${message.id}`
        msg_div.className = `message message-${message.type}`

        const content_div = document.createElement('div')
        content_div.className = 'message-content'
        content_div.innerHTML = marked.marked(message.content)

        msg_div.appendChild(content_div)
        messages_container.appendChild(msg_div)
    }

    scroll_to_bottom() {
        const messages = this.query_selector('.chat-messages')
        messages.scrollTop = messages.scrollHeight
    }

    html() {
        const container = new Div({ class: 'chat-container' })

        // Chat header
        const header = new Div({ class: 'chat-header' })
        header.add_elements(
            new Icon({ icon: 'robot', size: 'md', spacing: 'right' }),
            new Div({ class: 'header-text', value: 'Document Assistant' })
        )

        // Messages area
        const messages = new Div({ class: 'chat-messages' })

        // Input area
        const input_container = new Div({ class: 'chat-input-container' })
        const input = new Textarea({
            tag: 'textarea',
            class: 'chat-input',
            value      : 'add 2',
            attributes: {
                placeholder: 'Ask me to help improve the document...',
                rows       : '3',
            }
        })

        const send_btn = new Button({
            class: 'btn btn-primary send-button',
            value: 'Send'
        })
        send_btn.add_element(new Icon({ icon: 'arrow-right', size: 'sm', spacing: 'right' }))

        input_container.add_elements(input, send_btn)

        container.add_elements(header, messages, input_container)
        return container

    }


    css_rules() {
        return {
            ".chat-container"      : { display         : "flex"                      ,         // Main container
                                     flexDirection    : "column"                    ,
                                     height          : "100%"                      ,
                                     backgroundColor : "#fff"                      },

            ".chat-header"         : { display         : "flex"                      ,         // Header
                                     alignItems      : "center"                    ,
                                     padding         : "1rem"                      ,
                                     borderBottom    : "1px solid #dee2e6"         ,
                                     backgroundColor : "#f8f9fa"                   ,
                                     gap             : "0.5rem"                    },

            ".header-text"         : { fontSize        : "1rem"                      ,         // Header text
                                     fontWeight      : "500"                       ,
                                     color           : "#212529"                   },

            ".chat-messages"       : { flex            : "1"                         ,         // Messages container
                                     overflow        : "auto"                      ,
                                     padding         : "1rem"                      ,
                                     display         : "flex"                      ,
                                     flexDirection   : "column"                    ,
                                     gap             : "1rem"                      },

            ".message"             : { maxWidth        : "90%"                       ,         // Message bubbles
                                     padding         : "0.75rem"                   ,
                                     borderRadius    : "0.5rem"                    ,
                                     fontSize        : "0.875rem"                  ,
                                     lineHeight      : "1.5"                      },

            ".message-user"        : { alignSelf       : "flex-end"                  ,         // User messages
                                     backgroundColor : "#0d6efd"                   ,
                                     color           : "#fff"                      },

            ".message-assistant"   : { alignSelf       : "flex-start"                ,         // Assistant messages
                                     backgroundColor : "#f8f9fa"                   ,
                                     color           : "#212529"                   },

            ".message-system"      : { alignSelf       : "center"                    ,         // System messages
                                     backgroundColor : "#e9ecef"                   ,
                                     color           : "#6c757d"                   ,
                                     fontSize        : "0.75rem"                   ,
                                     textAlign       : "center"                    },

            ".message-content"     : { "& p"           : { margin: "0 0 0.5rem 0" }  ,         // Message content
                                     "& p:last-child" : { margin: "0"            }  },

            ".message-actions"     : { display         : "flex"                      ,         // Action buttons
                                     gap             : "0.5rem"                    ,
                                     marginTop       : "0.75rem"                   },

            ".chat-input-container": { display         : "flex"                      ,         // Input container
                                     flexDirection    : "column"                    ,
                                     gap             : "0.5rem"                    ,
                                     padding         : "1rem"                      ,
                                     borderTop       : "1px solid #dee2e6"         ,
                                     backgroundColor : "#f8f9fa"                   },

            ".chat-input"          : { width           : "100%"                      ,         // Input field
                                     padding         : "0.5rem"                    ,
                                     fontSize        : "0.875rem"                  ,
                                     lineHeight      : "1.5"                      ,
                                     border          : "1px solid #dee2e6"         ,
                                     borderRadius    : "0.375rem"                  ,
                                     resize          : "none"                      },

            ".send-button"         : { alignSelf       : "flex-end"                  }         // Send button
        }
    }
}

WebC__Document__Chat.define()