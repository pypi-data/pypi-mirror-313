import Web_Component from '../../core/Web_Component.mjs'
import CSS__Cards    from '../../css/CSS__Cards.mjs'
import CSS__Grid     from '../../css/grid/CSS__Grid.mjs'
import API__Invoke   from '../../data/API__Invoke.mjs'
import Div           from '../../core/Div.mjs'
import Raw_Html      from '../../core/Raw_Html.mjs'
import LLM__Handler  from '../llms/LLM__Handler.mjs'

export default class WebC__PastChats__Welcome extends Web_Component {

    constructor() {
        super()
        this.api_invoke     = new API__Invoke()
    }
    async apply_css() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Cards     (this).apply_framework()
    }

    load_data() {
        this.welcome_message = ''
    }

    async component_ready() {
        await this.generate_welcome()
    }

    async fetch_user_data() {
        try {
            const [profile, chats] = await Promise.all([
                this.api_invoke.invoke_api('/api/user-data/user/user-profile', 'GET'),
                this.api_invoke.invoke_api('/api/user-data/chats/chats'      , 'GET')
            ])
            return { profile, chats: chats?.saved_chats }
        } catch (error) {
            //console.error('Error fetching data:', error)
            return null
        }
    }

    analyze_chat_history(chats) {
        const total_chats          = Object.keys(chats).length
        const total_messages       = Object.values(chats).reduce((sum, chat) => sum + (chat.history_size || 0), 0)
        const prompts              = Object.values(chats).map(chat => chat.last_user_prompt).filter(Boolean)
        const topics               = [...new Set(prompts)].filter(Boolean)
        const total_prompts_size   = Object.values(chats).reduce((sum, chat) => sum + (chat.prompts_size || 0), 0)
        const total_responses_size = Object.values(chats).reduce((sum, chat) => sum + (chat.responses_size || 0), 0)

        return { total_chats, total_messages, topics, total_prompts_size, total_responses_size }
    }

    async generate_welcome() {
        const data = await this.fetch_user_data()
        if (!data) return

        const { profile, chats } = data
        const analytics = this.analyze_chat_history(chats)

        const user_prompt = `Create a personalized welcome message for a user's chat history page. Here are the key statistics:
            - Total conversations: ${analytics.total_chats}
            - Total messages exchanged: ${analytics.total_messages}
            - Recent topics discussed: ${analytics.topics.slice(0, 3).join(', ')}
            - Total data exchanged: ${((analytics.total_prompts_size + analytics.total_responses_size) / 1024).toFixed(1)}KB

            Please create a friendly, engaging message that:
            1. Acknowledges their level of engagement
            2. References their recent topics of interest
            3. Encourages continued interaction
            Keep it concise (max 100 words) and conversational.`

        const system_prompt = `You are Athena, analyzing chat history for ${profile.first_name}. 
                             Focus on being encouraging and highlight the value of their conversations.
                             Your role is to help them understand their engagement patterns.`

        try {
            const llm_handler = new LLM__Handler()
            await llm_handler.stream_response(
                user_prompt,
                [system_prompt],
                { onChunk: (message) => this.show_message(message) }
            )
        } catch (error) {
            //console.error('Error generating welcome:', error)
            this.show_message('')
        }
    }

    show_message(message) {
        if (typeof marked !== 'undefined' && marked) {                          /* global marked */
            const marked_message = marked.marked(message)
            this.welcome_message = marked_message
        } else {
            this.welcome_message = message
        }
        this.render()
    }

    html() {
        const card = new Div({ class: 'card mb-4 m-1' })
        const body = new Div({ class: 'card-body' })
        const content = new Raw_Html({
            class: 'card-text welcome-message',
            value: this.welcome_message
        })

        body.add_element(content)
        card.add_element(body)
        return card
    }

    css_rules() {
        return {
            ".card"            : { backgroundColor: "#ffffff"                      ,         // Card container
                                  borderRadius   : "8px"                           },

            ".welcome-message" : { fontSize      : "1.1rem"                       ,         // Message styling
                                  lineHeight    : "1.5"                           ,
                                  color         : "#2c3e50"                       },

            ".welcome-message p": { margin       : "0"                            }          // Remove paragraph margins
        }
    }
}

WebC__PastChats__Welcome.define()