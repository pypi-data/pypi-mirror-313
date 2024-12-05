import Web_Component            from '../../core/Web_Component.mjs';
import Layout                   from '../../css/grid/Layout.mjs';
import CSS__Grid                from '../../css/grid/CSS__Grid.mjs';
import CSS__Typography          from '../../css/CSS__Typography.mjs';
import API__Invoke              from '../../data/API__Invoke.mjs';
import Chatbot_OpenAI           from "../../chat-bot/Chatbot_OpenAI.mjs";
import WebC__Athena__Banner     from "./WebC__Athena__Banner.mjs";
import WebC__Athena__Welcome    from "./WebC__Athena__Welcome.mjs";
import WebC__Athena__Examples   from "./WebC__Athena__Examples.mjs";
import WebC__Athena__Config     from "./WebC__Athena__Config.mjs";

export default class WebC__Athena__Container extends Web_Component {

    constructor(){
        super()
        this.api_invoke = new API__Invoke()
    }

    load_attributes() {
        this.channel    = this.getAttribute('channel') || `athena_${this.random_id()}`
        // Get initial config from localStorage
        this.show_system_prompt = localStorage.getItem('athena_show_system_prompt') === 'true'
        this.edit_mode          = localStorage.getItem('athena_edit_mode') === 'true'
    }

    async apply_css() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Typography(this).apply_framework()
    }

    async load_data() {
        this.system_prompt = await this.build_system_prompt()
    }

    add_event_listeners() {
        window.addEventListener('config-update', this.handle_config_update.bind(this))
    }

    handle_config_update(event) {
        if (event.detail.channel === this.channel) {
            this.show_system_prompt = event.detail.show_system_prompt
            this.edit_mode = event.detail.edit_mode
            this.render()
        }
    }

    // Format user data into system prompt format
    format_user_data(user_data) {
        if (!user_data) return ''

        const intro = "We have asked the user to provide some information and included below is the data provided, please customise the answers as much as possible to these user preferences:\n"
        const lines = [intro]

        for (const [key, value] of Object.entries(user_data)) {
            if (value) {
                // Pad key to 32 characters (30 + 2 for alignment)
                const padded_key = key.padEnd(32)
                lines.push(`- ${padded_key}: ${value}`)
            }
        }
        return lines.join(' \n ')
    }

    // Fetch user data from API
    async fetch_user_data() {
        try {
            return await this.api_invoke.invoke_api('/api/user-data/user/user-profile', 'GET')
        } catch (error) {
            //console.error('Error fetching user data:', error)
            return null
        }
    }

    // Fetch Athena prompt markdown content
    async fetch_athena_prompt() {
        try {
            const content = await this.api_invoke.invoke_api(
                '/markdown/static_content/content-file?path=en/site/athena/athena-prompt.md',
                'GET'
            )
            return content
        } catch (error) {
            //console.error('Error fetching Athena prompt:', error)
            return ''
        }
    }

    // Combine both prompts
    async build_system_prompt() {
        const [user_data, athena_prompt] = await Promise.all([
            this.fetch_user_data(),
            this.fetch_athena_prompt()
        ])
        const formatted_user_data = this.format_user_data(user_data)
        return `${athena_prompt}\n\n${formatted_user_data}`.trim()          // Combine the prompts, with Athena prompt first
    }

    async add_web_components() {

        const params__chat_bot = { initial_message   : 'Hello, I am Athena. How can I help you?' ,
                                   channel           : this.channel                              ,
                                   edit_mode         : String(this.edit_mode)                    ,
                                   name              : 'Athena'                                  ,
                                   url               : '/api/open_ai/prompt_with_system__stream' ,
                                   system_prompt     : this.system_prompt                        ,
                                   show_system_prompt: String(this.show_system_prompt)           }

        const params__channel  = { channel: this.channel }
        this.add_web_component_to('#athena-banner'  , WebC__Athena__Banner                      )
        this.add_web_component_to('#athena-welcome' , WebC__Athena__Welcome                     )
        this.add_web_component_to('#athena-chatbot' , Chatbot_OpenAI         , params__chat_bot )
        this.add_web_component_to('#athena-examples', WebC__Athena__Examples , params__channel  )
        this.add_web_component_to('#athena-config'  , WebC__Athena__Config   , params__channel  )
    }

    html() {

        const layout = new Layout({
            id: 'athena-page',
            class: 'h-100pc d-flex flex-column'
        })

        // Banner row
        const row_banner = layout.add_row({ id: 'athena-row', class: 'm-1' })

        // Banner column (left side)

        row_banner.add_col({id: 'athena-banner', class: 'col-6' })

        // Welcome message column (right side)
        row_banner.add_col({id: 'athena-welcome', class: 'col-6' })

        // Content row
        const row_content = layout.add_row({ class: 'flex-fill m-1' })
        row_content.add_col({id: 'athena-chatbot', class: 'col-9'})                 // Chat column

        const right_col = row_content.add_col({ class: 'col-3' })                   // Right column with examples and config


        right_col.add_col({id: 'athena-examples', class: 'mb-3' })                  // Examples section
        right_col.add_col({id: 'athena-config'  , class: 'mb-3' })                  // Config section


        return layout
    }
}

WebC__Athena__Container.define()