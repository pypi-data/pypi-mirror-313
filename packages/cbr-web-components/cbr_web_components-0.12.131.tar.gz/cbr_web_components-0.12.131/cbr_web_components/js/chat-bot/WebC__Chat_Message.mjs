import Web_Component        from "../core/Web_Component.mjs";
import Tag                  from "../core/Tag.mjs";
import Div                  from "../core/Div.mjs";


export default class WebC__Chat_Message extends Web_Component {

    constructor() {
        super();
        this.message_raw  = ''
        this.message_html = ''
        this.type         = ''
        this.duration     = ''
        this.channel      = this.getAttribute('channel' )       || null
        this.platform     = this.getAttribute('platform')       || 'platform'
        this.provider     = this.getAttribute('provider')       || 'provider'
        this.model        = this.getAttribute('model'   )       || 'model'
        if (this.channel) { this.channels.push(this.channel) }
        this.channels.push('WebC__Chat_Message')
        this.edit_message  = this.edit_message.bind(this);
        this.save_message  = this.save_message.bind(this);
        this.clear_message = this.clear_message.bind(this);
        this.edit_mode     = false

    }
    apply_css() {
        this.add_css_rules (this.css_messages())
    }

    load_attributes() {
        this.type = this.attributes.type?.value
    }

    add_event_listeners() {
        this.style.display = 'inherit'              // need to add this so that align-self works ('contents' seems a better value, but 'inherit'
        if (this.edit_mode && this.type !== 'initial') {
            this.shadowRoot.querySelector("#edit_button" ).addEventListener('click', this.edit_message )
            this.shadowRoot.querySelector("#save_button" ).addEventListener('click', this.save_message )
            this.shadowRoot.querySelector("#clear_button").addEventListener('click', this.clear_message)
        }
    }

    append(message) {
        this.message_raw += message
        this.update_text_area(this.message_raw)
        this.show_message()
        return this
    }
    save_message () {
        let text_area = this.shadowRoot.querySelector('#message_text_area')
        let message_area = this.shadowRoot.querySelector('slot')
        let edit_button = this.shadowRoot.querySelector('#edit_button')
        let save_button = this.shadowRoot.querySelector('#save_button')
        //let message_area = this.querySelector('slot')
        text_area.style.display = 'none'
        message_area.style.display = 'block'
        edit_button.style.display = 'block'
        save_button.style.display = 'none'
        this.message_raw = text_area.value

        this.show_message()
    }
    edit_message () {
        let text_area = this.shadowRoot.querySelector('#message_text_area')
        let message_area = this.shadowRoot.querySelector('slot')
        let edit_button = this.shadowRoot.querySelector('#edit_button')
        let save_button = this.shadowRoot.querySelector('#save_button')
        text_area.style.display = 'block'
        message_area.style.display = 'none'
        edit_button.style.display = 'none'
        save_button.style.display = 'block'
        text_area.style.height = text_area.scrollHeight + 'px'
        let text_area_width = $(message_area).width() /1.7
        if (text_area_width < 100) {
            text_area_width = 250
        }
        text_area.style.width = text_area_width +  'px'
    }

    clear_message () {
        let text_area = this.shadowRoot.querySelector('#message_text_area')
        text_area.value = ''
        this.message_raw = ''
        this.show_message()
    }

    update_text_area(value) {
        let text_area = this.shadowRoot.querySelector('#message_text_area')
        if (text_area) {
            text_area.style.height = text_area.scrollHeight + 'px'
            text_area.value = value
        }


    }
    create_message_html(message) {
        if (window.marked === undefined) {
            return message.replace(/\n/g, '<br>');
        }
        else {
            return marked.marked(message)
        }

    }

    source_ui_text() {
        return `${this.platform} | ${this.provider} | ${this.model}` // | ${this.duration} `
    }

    html() {
        let source        = this.source_ui_text()
        const div_class   = `message ${this.type}`
        const div_message = new Tag({tag: 'div', class: div_class})
        const text_area   = new Tag({tag: 'textarea', id:'message_text_area' , class: 'message-edit', value: this.message_raw})

        const div_slot    = new Tag({tag: 'slot'})
        const div_edit    = new Tag({tag:'button', id:'edit_button' , value: 'EDIT'})
        const div_save    = new Tag({tag:'button', id:'save_button' , value: 'OK'})
        const div_clear   = new Tag({tag:'button', id:'clear_button', value: 'X'})
        const div_source = new Div({id: 'source', value: source})
        if (this.edit_mode && this.type !== 'initial') {
                div_message.add(div_edit)
                div_message.add(div_save)
                div_message.add(div_clear)
        }
        div_message.add(div_slot)
        div_message.add(text_area)

        if (this.type === 'received') {
            if (this.model !== '.') {
                div_source.class = 'source-received'
                div_message.add(div_source)
            }
        }

        let html = div_message.html()
        html += `
<style>
.message-edit {
    display: none;
    font-size: 14px;
    width: 95%;
    padding: 5px;
    border-radius: 5px;
    margin-top: 10px;
    margin-bottom: 0px;
    box-sizing: border-box;
}

#save_button { display: none;}

.source-sent { position:relative;
          bottom: -30px;
          color : #6a42c1; }
.source-received { position:relative;
          bottom: -30px;
          color : #808080; }
.badge {
    position: absolute;
    color: white;
    padding: 5px 10px;
    border-radius: 12px;
    font-size: 7px;
}

</style>`
        return html
    }

    images(images) {
        if (images && images.length > 0) {
            const hr = document.createElement('hr');
            this.appendChild(hr)
            for (let index in images) {
                const image_url = images[index]
                //todo refactor to creating with Tag (and into utils class)
                const img = document.createElement('img');
                img.src = image_url
                img.style="width:auto; height:auto; margin:10px;max-width:350px;max-height:350px"
                this.appendChild(img)
            }
        }
    }
    //todo see if this assigment is better done using a property
    message(value) {
        if (value){
            this.message_raw = value
            this.update_text_area(value)
            this.show_message()
        }
        return this.innerHTML
    }

    show_message(){
        this.message_html = this.create_message_html(this.message_raw)
        this.innerHTML    = this.message_html
    }

    hide_spinner() {
        const dom_spinner = this.shadowRoot.querySelector('.spinner')
        if (dom_spinner) {
            dom_spinner.remove()
            return true }
        return false
    }

    show_spinner() {
        const div_spinner = new Tag({tag: 'div', class:'spinner'})
        const dom_spinner = div_spinner.dom_create()

        this.shadow_root_append(dom_spinner)

        const keyframes = [ { transform: 'rotate(0deg)' },    // Start at 0 degrees
                            { transform: 'rotate(360deg)' }];   // Rotate 360 degrees

        const options   = { duration    : 1500      ,   // Duration in milliseconds
                            iterations  : Infinity  ,   // Repeat the animation indefinitely
                            easing      : 'linear'  };  // Use a linear pacing function

        dom_spinner.animate(keyframes, options);     // Apply the animation to the element
        return dom_spinner
    }

    css_messages() { return {   ".message"      : { "margin-bottom"   : "25px"             ,
                                                    "max-width"       : "80%"              ,
                                                    "padding"         : "10px"             },
                                ".initial"      : { "background-color": "#f8f4f4"           ,
                                                    "align-self"      : "flex-start"        ,
                                                    "border-radius"   : "10px 10px 10px 0px"},
                                ".received"     : { "background-color": "#f2f2f2"           ,
                                                    "align-self"      : "flex-start"        ,
                                                    "border-radius"   : "10px 10px 10px 0px"},
                                ".sent"         : { "background-color": "#724ae8"           ,
                                                    "align-self"      : "flex-end"          ,
                                                    "color"           : "#fff"              ,
                                                    "border-radius"   : "10px 10px 0 10px"  },
                                ".spinner"      : { "border"          : "4px solid #f3f3f3" , /* Light grey */
                                                    "border-top"      : "4px solid #3498db" , /* Blue */
                                                    "border-radius"   : "50%"               ,
                                                    "width"           : "15px"              ,
                                                    "height"          : "15px"              },
    }}
}

WebC__Chat_Message.define()