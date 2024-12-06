import Web_Component        from "../core/Web_Component.mjs";
import WebC__Chat_Message   from "./WebC__Chat_Message.mjs";
import WebC__System__Prompt from './WebC__System__Prompt.mjs';

export default class WebC__Chat_Messages extends Web_Component {

    constructor() {
        super();
        this.auto_scroll        = true                        // Auto-scroll to the bottom of the chat window
        this.dom_spinner        = null
        this.current_message    = null

    }

    load_attributes() {
        this.channel            = this.getAttribute('channel'           )       || null
        this.edit_mode          = this.getAttribute('edit_mode'         ) === 'true'
        this.show_sent_messages = this.getAttribute('show_sent_messages') === 'true'
        //if (show_sent_messages == 'true'): { this.show_sent_messages = true }

        if (this.channel) { this.channels.push(this.channel) }
        this.channels.push('WebC__Chat_Messages')
    }

    is_message_to_current_channel(event_data) {
        return event_data?.channel === this.channel
    }
    handle_stream_start(event_data)  {
        if (this.is_message_to_current_channel(event_data)) {
            let initial_message = ''
            let images   = null
            let platform = event_data.platform
            let provider = event_data.provider
            let model    = event_data.model
            this.current_message = this.add_message_received(initial_message, images, platform, provider, model ) }
            this.auto_scroll = true
    }
    handle_stream_data(event_data) {
        if (this.is_message_to_current_channel(event_data)) {
            if (this.dom_spinner) {
                this.dom_spinner.remove();
                this.dom_spinner = null
            }
            let chunk = event_data.data
            this.current_message?.append(chunk)
            this.messages_div_scroll_to_end()
        }
    }
    add_event_listeners() {
        //console.log("configuring event hooks in WebC__Chat_Messages")

        //var current_message = null
        window.addEventListener('streamStart', (e)=>{
            //current_message = this.add_message_received('')
            this.handle_stream_start(e.detail)
        });

        // window.addEventListener('streamComplete', (e)=>{
        //     //console.log('>>>>> streamComplete:")', e)
        // });
        window.addEventListener('streamData', (e)=>{
            this.handle_stream_data(e.detail)
        });

        window.addEventListener('add-message', (e)=>{
            this.add_message(e.detail?.message, e.detail?.type, e.detail?.images, e.detail?.platform, e.detail?.provider, e.detail?.model);
        });

        this.messages_div().addEventListener('wheel', () => {              // Add scroll listener
            this.auto_scroll = false                                     // Disable auto-scroll on manual scroll
        })
    }

    async apply_css() {
        this.add_css_rules(this.css_rules())
    }

    html() {
        return `<div class="messages"><slot></slot></div>`
    }

    css_rules() { return { "*"         : { "font-family"    : "Verdana" },
                           ".messages" : { "display"        : "flex"    ,
                                           "flex-direction" : "column"  ,
                                           "overflow-y"     : "auto"    ,
                                           "padding"        : "10px"    }}
    }

    add_message(message, type, images, platform, provider, model) {
        const new_message_params = { type     : type    ,
                                     platform : platform || '.',
                                     provider : provider || '.',
                                     model    : model    || '.' }
        const new_message =  WebC__Chat_Message.create(new_message_params)

        new_message.edit_mode = this.edit_mode
        this.appendChild(new_message)
        new_message.message(message)
        new_message.images(images)

        this.messages_div_scroll_to_end()
        return new_message
    }

    add_message_sent    (message) {
        let message_sent = null
        if (this.show_sent_messages) {
            message_sent = this.add_message(message.user_prompt, 'sent' , message.images  )
            this.dom_spinner = message_sent.show_spinner()
        }


        const event = new CustomEvent('messageSent', {
            bubbles : true    ,                         // allows the event to bubble up through the DOM
            composed: true    ,                         // allows the event to cross shadow DOM boundaries
            detail  : { message } });
        this.dispatchEvent(event);

        return message_sent
    }

    add_message_system(message) {
        const system_prompt = WebC__System__Prompt.create();
        system_prompt.setAttribute('content', message);
        this.appendChild(system_prompt);
    }

    add_message_initial(message) {
        return this.add_message(message, 'initial')
    }

    add_message_link_thread_id(message) {
        return this.add_message(message, 'link_thread_id')
    }
    
    add_message_received(message, images, platform, provider, model) {
        return this.add_message(message, 'received', images, platform, provider, model)
    }


    on_message_sent    (callback) {
        // how to create a custom event
    }
    on_message_received(message) {

    }  // method to be overwritten by Classes that extend this one

    messages () {
        return this.childNodes                          // todo: change the logic since we really shouldn't be using the html elements here, we should have an internal data representation of the messages
    }

    messages_clear() {
        this.innerHTML = ''
        return this
    }
    messages_size() {
        return this.messages().length
    }

    messages_div () {
        return this.query_selector('.messages')

    }
    messages_div_scroll_to_end() {
        if (!this.auto_scroll) { return }
        this.scrollTop = this.scrollHeight
    }
}

WebC__Chat_Messages.define()