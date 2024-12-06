import Web_Component    from '../../core/Web_Component.mjs';
import Layout          from '../../css/grid/Layout.mjs';
import CSS__Grid       from '../../css/grid/CSS__Grid.mjs';
import CSS__Typography from '../../css/CSS__Typography.mjs';
import CSS__Cards      from '../../css/CSS__Cards.mjs';
import CSS__Buttons    from '../../css/CSS__Buttons.mjs';
import API__Invoke     from '../../data/API__Invoke.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import Button          from '../../core/Button.mjs';
import CBR__Session__Event__Handler from "../session/CBR__Session__Event__Handler.mjs";
import CBR_Events from "../CBR_Events.mjs";

export default class WebC__Personas__Container extends Web_Component {

    constructor() {
        super();
        this.api_invoke    = new API__Invoke()
        this.event_handler = new CBR__Session__Event__Handler()
    }
    apply_css() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Buttons   (this).apply_framework()
    }

    async load_data() {
        await this.load_personas()
    }

    add_event_listeners() {
            this.add_window_event_listener(CBR_Events.CBR__SESSION__PERSONA__CHANGED, this.handle__persona_session_changed)
    }

    add_event_handlers() {
        if (this.query_selector('.login-button')) {
            this.add_event__on('click', '.login-button', this.handle__login_button_click)
        }
    }

    handle__login_button_click = ({event}) => {
        const persona_id = event.target.dataset.guestId
        this.event_handler.dispatch( this.event_handler.events.LOGIN_AS_PERSONA,  { persona_id })
    }

    handle__persona_session_changed = (event) => {
        const state = event.detail.state
        if (state.persona_session) {
            this.update_persona_buttons(state.persona_session.user_name)
        }
    }

    update_persona_buttons(active_persona) {
        const buttons = this.shadowRoot.querySelectorAll('.login-button')
        buttons.forEach(button => {
            const persona_id = button.dataset.guestId
            const card = button.closest('.card')
            const persona_name = card.querySelector('.persona-name').textContent

            if (persona_name === active_persona) {
                button.textContent = 'Current Persona'
                button.classList.remove('btn-outline-primary')
                button.classList.add('btn-success')
                button.disabled = true
            } else {
                button.textContent = 'Login as this persona'
                button.classList.remove('btn-success')
                button.classList.add('btn-outline-primary')
                button.disabled = false
            }
        })
    }

    async load_personas() {
        try {
            const personas = await this.api_invoke.invoke_api('/api/user-session/guests/data', 'GET')
            this.personas = personas
            //this.render()
        } catch (error) {
            //console.error('Error loading personas:', error)
        }
    }

    async handle_login_click(event) {
        if (event.target.matches('.login-button')) {
            const guest_id = event.target.dataset.guestId                           // todo refactor this into a separate class and make it event driven
            const path = `/api/user-session/guest/login-as-persona?persona_id=${guest_id}`
            await this.api_invoke.invoke_api(path, 'POST')
                await this.navigate_to_personas_page()
        }
    }
     /* istanbul ignore next */
    async navigate_to_personas_page() {
        window.location.href = '/webc/cbr-webc-dev/personas/index'
    }

    create_persona_card(guest_id, persona) {
        const { user_data } = persona

        const card = new Div({ class: 'card bg-white mb-4 m-1' })
        const body = new Div({ class: 'card-body p-4' })

        // Name
        const name = new H({
            level: 2,
            class: 'persona-name',
            value: `${user_data.first_name} ${user_data.last_name}`
        })

        // Role - using blue color
        const role = new Div({
            class: 'persona-role',
            value: user_data.role
        })

        // Organization details
        const details = new Div({ class: 'persona-details' })
        details.add_elements(
            new Div({ value: user_data.organisation }),
            new Div({ value: `${user_data.sector} Sector` }),
            new Div({ value: user_data.size_of_organisation }),
            new Div({ value: user_data.country })
        )

        // Interaction Preferences
        const preferences = new Div({ class: 'preferences-section' })
        const pref_title = new Div({
            class: 'preferences-title',
            value: 'Interaction Preferences'
        })
        const pref_text = new Div({
            class: 'preferences-text',
            value: user_data.additional_system_prompt
        })
        preferences.add_elements(pref_title, pref_text)

        // Login button - using CSS__Buttons classes
        const login_button = new Button({
            class: 'btn btn-outline-primary btn-block login-button',
            value: 'Login as this persona',
            'data-guest-id': guest_id
        })

        body.add_elements(name, role, details, preferences, login_button)
        card.add_element(body)

        return card
    }

    render() {
        const layout = new Layout({ class: 'container' })

        // Header
        const header = new Div({ class: 'header' })
        const title = new H({
            level: 1,
            class: 'main-title',
            value: 'Personas'
        })
        const subtitle = new Div({
            class: 'subtitle',
            value: 'Select a persona to experience Athena from different perspectives'
        })
        header.add_elements(title, subtitle)

        // Personas container
        const cards_container = new Div({ class: 'personas-container d-flex' })

        if (this.personas) {
            Object.entries(this.personas).forEach(([guest_id, persona]) => {
                cards_container.add_element(
                    this.create_persona_card(guest_id, persona)
                )
            })
        }

        layout.add_elements(header, cards_container)
        this.set_inner_html(layout.html())
        this.add_css_rules(this.css_rules())
    }

    css_rules() {
        return {
            ".container": {
                padding: "2rem"
            },
            ".header": {
                marginBottom: "2rem"
            },
            ".main-title": {
                fontSize: "2rem",
                fontWeight: "500",
                marginBottom: "0.5rem"
            },
            ".subtitle": {
                fontSize: "1rem",
                color: "#666",
                marginBottom: "2rem"
            },
            ".card": {
                border: "1px solid #eee",
                borderRadius: "8px",
                marginBottom: "1rem",
                backgroundColor: "#ffffff",
                boxShadow: "0 1px 3px rgba(0,0,0,0.1)"
            },
            ".persona-name": {
                fontSize: "1.5rem",
                fontWeight: "500",
                marginBottom: "0.5rem"
            },
            ".persona-role": {
                fontSize: "1.125rem",
                color: "#4A90E2",
                marginBottom: "1rem"
            },
            ".persona-details": {
                marginBottom: "1.5rem",
                lineHeight: "1.6"
            },
            ".preferences-section": {
                marginBottom: "1.5rem"
            },
            ".preferences-title": {
                fontSize: "1rem",
                fontWeight: "500",
                marginBottom: "0.5rem"
            },
            ".preferences-text": {
                fontStyle: "italic",
                color: "#666"
            },
            // Removed custom button styles as we're now using CSS__Buttons
            ".btn-block": {
                width: "100%"
            }
        }
    }
}

WebC__Personas__Container.define()