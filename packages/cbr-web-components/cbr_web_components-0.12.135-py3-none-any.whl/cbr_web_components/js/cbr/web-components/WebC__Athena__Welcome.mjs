import Web_Component                from '../../core/Web_Component.mjs';
import CSS__Cards                   from '../../css/CSS__Cards.mjs';
import CSS__Typography              from '../../css/CSS__Typography.mjs';
import API__Invoke                  from '../../data/API__Invoke.mjs';
import LLM__Handler                 from "../llms/LLM__Handler.mjs";
import Div                          from '../../core/Div.mjs';
import Raw_Html                     from '../../core/Raw_Html.mjs';
import CSS__Grid                    from "../../css/grid/CSS__Grid.mjs";
import CBR__Session__Event__Handler from "../session/CBR__Session__Event__Handler.mjs";


export default class WebC__Athena__Welcome extends Web_Component {
    load_attributes() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        this.event_handler = new CBR__Session__Event__Handler()
        this.api_invoke    = new API__Invoke()
        this.welcome_message = ''
    }

    add_event_listeners() {
        this.event_handler.subscribe(this.event_handler.events.ACTIVE_SESSION_CHANGED, this.handle__active_session_changed)
    }

    async component_ready() {
        await this.generate_welcome()
    }

    async fetch_user_data() {
        try {
            return await this.api_invoke.invoke_api('/api/user-data/user/user-profile', 'GET')
        } catch (error) {
            //console.error('Error fetching user data:', error)
            return null
        }
    }

    async generate_welcome() {
        const user_data = await this.fetch_user_data()
        if (!user_data) return

        const user_prompt   = "Generate a one-paragraph (max 100 words) personalized welcome message for this user, based on their profile preferences. " +
                             "reply as if speaking directly to the user, don't start your answer with quotes"
        const system_prompt = `You are called Athena, here is what you know about this user: ${JSON.stringify(user_data)}`

        try {
            const llm_handler = new LLM__Handler()
            await llm_handler.stream_response(
                user_prompt,
                [system_prompt],
                { onChunk: (message) => this.show_message(message) }
            )
        } catch (error) {
            //console.log(error)
            this.show_message('Error generating welcome message')
        }
    }

    handle__active_session_changed = async () => {
        await this.generate_welcome()
    }

    show_message(message) {
        if (typeof marked !== 'undefined' && marked) {                          /* global marked */
            const marked_message = marked.marked(message)
            this.welcome_message = marked_message
        }
        else {
            this.welcome_message = message
        }
        this.render()
    }

    html() {
        const card = new Div({ class: 'card h-100 m-1' })
        const body = new Div({ class: 'card-body' })
        //const title = new H({ level: 3, class: 'card-title mb-3', value: 'Welcome' })
        const content = new Raw_Html({ class: 'card-text', value: this.welcome_message })

        body.add_elements(content)
        card.add_element(body)

        return card
    }
}

WebC__Athena__Welcome.define()