import CBR_Events                 from "../CBR_Events.mjs";
import Web_Component              from '../../core/Web_Component.mjs'
import CSS__Cards                 from '../../css/CSS__Cards.mjs'
import CSS__Forms                 from '../../css/CSS__Forms.mjs'
import CSS__Grid                  from '../../css/grid/CSS__Grid.mjs'
import CSS__Typography            from '../../css/CSS__Typography.mjs'
import LLM__Handler               from './LLM__Handler.mjs'
import LLM__Response__Handler     from './LLM__Response__Handler.mjs'
import Div                        from '../../core/Div.mjs'
import Button                     from '../../core/Button.mjs'
import Textarea                   from '../../core/Textarea.mjs'

export default class WebC__LLM__Test extends Web_Component {

    constructor() {
        super()
        this.llm_handler         = new LLM__Handler()
        this.response_handler    = new LLM__Response__Handler()
        this.current_response    = ''
    }
    async apply_css() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Forms     (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        this.add_css_rules(this.css_rules())
    }

    add_event_handlers() {
        this.add_event__on( 'click', '#submit-prompt', this.handle_submit)
        this.add_event__on( 'click', '#clear-form'   , this.handle_clear)
    }

    async handle_submit() {

        const system_prompt = this.query_selector('#system-prompt').value.trim()
        const user_prompt   = this.query_selector('#user-prompt'  ).value.trim()
        if (!user_prompt) return

        const response_div = this.query_selector('#response-container')
        response_div.innerHTML = '<div class="loading">Processing...</div>'

        try {
            await this.llm_handler.stream_response(
                user_prompt,
                [system_prompt],
                {
                    onChunk: (chunk) => {
                        this.current_response = chunk
                        this.update_response()
                    },
                    onError: (error) => {
                        response_div.innerHTML = `<div class="error">Error: ${error.message}</div>`
                    }
                }
            )
        } catch (error) {
            //console.error('Error processing LLM request:', error)                         // todo: add to refactored error handler
        }
    }

    handle_clear() {
        this.shadowRoot.querySelector('#system-prompt').value = ''
        this.shadowRoot.querySelector('#user-prompt').value = ''
        this.current_response = ''
        this.update_response()
    }

    update_response() {
        const response_div = this.shadowRoot.querySelector('#response-container')
        if (response_div) {
            response_div.innerHTML = this.response_handler.create_response_element(
                this.current_response,
                'response-content'
            )
        }
    }

    css_rules() {
        return {
            ".test-container"      : { padding          : "1rem"                      ,
                                     backgroundColor   : "#fff"                      ,
                                     borderRadius      : "0.5rem"                    ,
                                     boxShadow         : "0 2px 4px rgba(0,0,0,0.1)" },

            ".input-section"       : { marginBottom     : "1.5rem"                    },

            ".prompt-label"        : { display          : "block"                     ,
                                     marginBottom      : "0.5rem"                    ,
                                     fontWeight        : "500"                       },

            ".prompt-textarea"     : { width            : "100%"                      ,
                                     minHeight         : "100px"                     ,
                                     marginBottom      : "1rem"                      },

            ".button-group"        : { display          : "flex"                      ,
                                     gap              : "0.5rem"                     ,
                                     marginBottom      : "1rem"                      },

            ".response-section"    : { backgroundColor  : "#f8f9fa"                   ,
                                     padding          : "1rem"                       ,
                                     borderRadius      : "0.375rem"                  ,
                                     minHeight         : "200px"                     },

            ".response-content"    : { fontFamily       : "system-ui, sans-serif"     ,
                                     lineHeight        : "1.6"                       },

            ".loading"             : { color            : "#6c757d"                   ,
                                     fontStyle         : "italic"                     },

            ".error"               : { color            : "#dc3545"                   ,
                                     fontWeight        : "500"                       }
        }
    }

    html() {
        const container = new Div({ class: 'test-container' })

        // System Prompt Section
        const system_section = new Div({ class: 'input-section' })
        const system_textarea = new Textarea({
            id          : 'system-prompt',
            class       : 'input prompt-textarea',
            placeholder : 'Enter system prompt...'
        })

        // User Prompt Section
        const user_section = new Div({ class: 'input-section' })
        const user_textarea = new Textarea({
            id          : 'user-prompt',
            class       : 'input prompt-textarea',
            placeholder : 'Enter user prompt...'
        })

        // Buttons
        const button_group = new Div({ class: 'button-group' })
        const submit_btn = new Button({
            id      : 'submit-prompt',
            class   : 'btn btn-primary',
            value   : 'Submit'
        })
        const clear_btn = new Button({
            id      : 'clear-form',
            class   : 'btn btn-secondary',
            value   : 'Clear'
        })

        button_group.add_elements(submit_btn, clear_btn)

        // Response Section
        const response_section = new Div({ class: 'response-section' })
        const response_container = new Div({ id: 'response-container' })
        response_section.add_element(response_container)

        // Build Component
        container.add_elements(
            system_section.add_elements(
                new Div({ class: 'prompt-label', value: 'System Prompt' }),
                system_textarea
            ),
            user_section.add_elements(
                new Div({ class: 'prompt-label', value: 'User Prompt' }),
                user_textarea
            ),
            button_group,
            response_section
        )

        return container
    }
}

WebC__LLM__Test.define()