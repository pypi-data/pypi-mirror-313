import Web_Component    from '../../core/Web_Component.mjs';
import Layout          from '../../css/grid/Layout.mjs';
import CSS__Grid       from '../../css/grid/CSS__Grid.mjs';
import CSS__Typography from '../../css/CSS__Typography.mjs';
import CSS__Forms      from '../../css/CSS__Forms.mjs';
import CSS__Cards      from '../../css/CSS__Cards.mjs';
import API__Invoke     from '../../data/API__Invoke.mjs';
import Div             from '../../core/Div.mjs';
import Form            from '../../core/Form.mjs';
import Input           from '../../core/Input.mjs';
import Label           from '../../core/Label.mjs';
import Textarea        from '../../core/Textarea.mjs';
import Button          from '../../core/Button.mjs';
import H               from '../../core/H.mjs';
import API__Web__Forms from "../api/API__Web__Forms.mjs";
import Chatbot_OpenAI from "../../chat-bot/Chatbot_OpenAI.mjs";

export default class WebC__Profile__Container extends Web_Component {
    constructor() {
        super();
        this.api_invoke      = new API__Invoke()
        this.api_web_forms  = new API__Web__Forms()
    }

    apply_css () {
        new CSS__Grid      (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        new CSS__Forms     (this).apply_framework()
        new CSS__Cards     (this).apply_framework()
    }

    load_attributes() {
        super.load_attributes();
        this.channel = `profile_${this.random_id()}`
    }

    async load_data() {
        await this.load_profile()
    }


    add_event_listeners() {
        this.handle_form_submit    = this.handle_form_submit.bind(this);

        this.shadowRoot.addEventListener('submit', this.handle_form_submit)
        //this.shadowRoot.addEventListener('input', this.handle_form_change.bind(this))
    }

    add_web_components() {
        this.add_web_component_to('.chat-container', Chatbot_OpenAI, {
            channel           : this.channel                   ,
            edit_mode        : 'false'                        ,
            name             : 'Profile Assistant'             ,
            url              : '/api/open_ai/prompt_with_system__stream',
            initial_message  : "I'm your profile assistant. Try updating your profile and I'll adjust my responses to match your preferences and role.",
            initial_prompt   : 'Hi, what do you know about me?',
            show_system_prompt: 'true'                         ,
            system_prompt    : this.create_profile_prompt()
        })
    }

    disconnectedCallback() {
        super.disconnectedCallback()
        this.remove_event_listeners()
    }

    remove_event_listeners() {
        this.shadowRoot.removeEventListener('submit', this.handle_form_submit)
    }

    async load_profile() {
        try {
            const profile = await this.api_invoke.invoke_api('/api/user-data/user/user-profile', 'GET')
            this.current_profile = profile
            this.render()
        } catch (error) {
            //console.error('Error loading profile:', error)
        }
    }

    async handle_form_submit(event) {
        event.preventDefault()
        const form = event.target
        const form_data = new FormData(form)

        try {
            await this.api_web_forms.submit_form(form_data, '/web/user/profile')
            this.notify_chatbot_profile_updated()
        } catch (error) {
            //console.error('Error updating profile:', error)
        }
    }


    // handle_form_change(event) {
    //     clearTimeout(this.update_timeout)
    //     this.update_timeout = setTimeout(() => {
    //         const form = this.shadowRoot.querySelector('form')
    //         const form_data = new FormData(form)
    //         this.current_profile = Object.fromEntries(form_data.entries())
    //         this.notify_chatbot_profile_updated()
    //     }, 1000)
    // }

    notify_chatbot_profile_updated() {
        const event = new CustomEvent('profile-update', {
            bubbles: true,
            composed: true,
            detail: {
                channel: this.channel,
                profile: this.current_profile
            }
        })
        this.dispatchEvent(event)
        this.reload_page()
    }

    /* istanbul ignore next */
    reload_page() {
        document.location.reload()
    }



    create_form() {
        const form = new Form({ class: 'card' })
        const body = new Div({ class: 'card-body' })
        const title = new H({ level: 2, class: 'card-title mb-4', value: 'Update Profile' })
        const fields = [
            { name: 'first_name', label: 'First name', type: 'text' },
            { name: 'last_name', label: 'Last name', type: 'text' },
            { name: 'role', label: 'Role', type: 'text' },
            { name: 'organisation', label: 'Organisation', type: 'text' },
            { name: 'sector', label: 'Sector', type: 'text' },
            { name: 'size_of_organisation', label: 'Size of organisation', type: 'text' },
            { name: 'country', label: 'Country', type: 'text' },
            { name: 'linkedin', label: 'LinkedIn', type: 'url', placeholder: 'https://linkedin.com/in/username' }
        ]

        // Create form groups using CSS__Forms patterns
        const form_groups = fields.map(field => {
            const group = new Div({ class: 'field-group' })

            const label = new Label({
                class: 'label',
                value: field.label,
                attributes: { for: field.name }
            })

            const input = new Input({ class      : 'input',
                                      type       : field.type,
                                      id         : field.name,
                                      name       : field.name,
                                      value      : this.current_profile?.[field.name] || '',
                                      placeholder: field.placeholder || ''})

            group.add_elements(label, input)
            return group
        })

        // Additional system prompt textarea
        const prompt_group = new Div({ class: 'field-group' })
        const prompt_label = new Label({
            class: 'label',
            value: 'Additional preferences',
            for: 'additional_system_prompt'
        })
        const prompt_help = new Div({
            class: 'help',
            value: 'Customize how Athena interacts with you. For example: "I prefer bullet points" or "Focus on technical details"'
        })
        const prompt_input = new Textarea({
            class: 'input',
            id: 'additional_system_prompt',
            name: 'additional_system_prompt',
            rows: '4',
            value: this.current_profile?.additional_system_prompt || ''
        })
        prompt_group.add_elements(prompt_label, prompt_input, prompt_help)

        // Submit button using CSS__Forms button styling
        const submit = new Button({ class: 'button button-primary',
                                    value: 'Update Profile'       ,
                                    type: 'submit'                })

        body.add_elements(title, ...form_groups, prompt_group, submit)
        form.add_element(body)
        return form
    }


    html() {
        const layout = new Layout({
            id: 'profile-page',
            class: 'h-100pc d-flex flex-column'
        })

        // Content row
        const row_content = layout.add_row({ class: 'flex-fill m-1' })

        // Form column (left side)
        const col_form = row_content.add_col({ class: 'col-6 m-1' })
        col_form.add_element(this.create_form())

        const col_chat = row_content.add_col({ class: 'col-5 m-1' })
        const div_chat = new Div({ class: 'chat-container' })
        col_chat.add_element(div_chat)

        return layout
    }


    create_profile_prompt() {

        if (!this.current_profile) return ''

        const lines = []
        for (const [key, value] of Object.entries(this.current_profile)) {
            if (value) {
                // Pad key to 32 characters (30 + 2 for alignment)
                const padded_key = key.padEnd(32)
                lines.push(`- ${padded_key}: ${value}`)
            }
        }
        const profile_data =  lines.join(' \n ')

        return `
Here is the profile of the user that is talking to you:
${profile_data}
                
Please address the user by name, explain what you know about the user, and how the profile data helps 
in creating personalized and customised experiences.`
    }
}

WebC__Profile__Container.define()