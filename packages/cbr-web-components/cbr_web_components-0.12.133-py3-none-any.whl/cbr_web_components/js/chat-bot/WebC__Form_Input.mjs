import Web_Component from "../core/Web_Component.mjs";
import Tag           from "../core/Tag.mjs";

export default class WebC__Form_Input extends Web_Component {

    constructor() {
        super();
        this.channels.push('WebC__Form_Input'     )
    }

    // connection methods
    add_event_listeners() {
        this.text_area.addEventListener                    ('input'       , this.on_input  );
        this.text_area.addEventListener                    ('keydown'     , this.on_keydown);
        this.text_area.addEventListener                    ('paste'       , this.on_paste  );
        //this.events_utils.events_receive.add_event_listener('keydown'     , this.channel, this.keydown   );
        this.events_utils.events_receive.add_event_listener('set_value'   , this.channel, this.on_set_value   );
        this.events_utils.events_receive.add_event_listener('append_value', this.channel, this.on_append_value);
    }

    apply_css() {
        this.add_css_rules(this.css_rules__chat_input())
    }


    remove_event_listeners() {
        if (this.text_area) {
            this.text_area.removeEventListener('input', this.on_input)
            this.text_area.removeEventListener('keydown', this.on_keydown)
        }
    }

    // events

    on_input = () => {
        this.text_area_resize()
    }

    on_keydown = (keyboard_event) => {
        this.events_utils.events_dispatch.send_to_channel('keydown', this.channel, { keyboard_event: keyboard_event})
    }

    on_paste = (paste_event) => {
        this.events_utils.events_dispatch.send_to_channel('paste', this.channel, { paste_event: paste_event})
    }

    on_append_value = (event) => {
        let value = event.event_data.value
        this.text_area.value += value
        this.text_area_trigger_input_event()
    }

    on_set_value = (event) => {
        let value = event.event_data.value
        this.text_area.value = value
        this.text_area_resize()
    }

    // methods

    css_rules__chat_input() {
        return { "#form_input": { "display"        : "flex"              ,
                                  "align-items"    : "center"            ,
                                  "border"         : "1px solid #ccc"    ,      // purple border
                                  "border-radius"  : "10px"              ,
                                  "padding"        : "2px"               ,
                                  "width"          : "100%"              ,
                                  "box-sizing"     : "border-box"        },     // ensures padding is included in the width

                 "#text_area" : { "width"          : "100%"              ,
                                  "border"         : "none"              ,
                                  "outline"        : "none"              ,
                                  "resize"         : "none"              ,      // removes the bottom right corner resize handle
                                  "font-size"      : "16px"              ,
                                  "line-height"    : "25px"              ,
                                  "font-family"    : 'Arial, sans-serif;',
                                  "padding"        : "10px"              ,
                                  "border-radius"  : "10px"              ,      // same border radius as parent for a uniform look
                                  "box-sizing"     : "border-box"        },

                "#text_area::placeholder": { "color"          : "#9e9e9e",      // grey placeholder text
                                             "font-size"      : "16px"   }}
    }
    html() {
        const div__form_input    = new Tag({tag: 'div'    , id: 'form_input'})
        const text_area          = new Tag({tag:'textarea', id: 'text_area', value:'', attributes:{rows: '1'}})
        div__form_input.add(text_area)
        return div__form_input
    }

    text_area_trigger_input_event() {
        const input_event = new InputEvent('input', { bubbles: true,  cancelable: true, });
        this.text_area.dispatchEvent(input_event)
    }

    text_area_new_height() {
        const line_height  = 25                             // size of text & line height
        const max_height = line_height * 8;                 // current css values this will give about 8 lines
        const new_height = Math.min(this.text_area.scrollHeight, max_height)
        return new_height
    }

    text_area_resize = () =>{
        this.text_area.style.height = 'auto';               // Reset height to auto to shrink when needed
        const new_height = this.text_area_new_height()
        this.text_area.style.height = new_height + 'px'; // Set height to scrollHeight
    }

    // properties
    get text_area() {
        return this.query_selector('#text_area')
    }


}

WebC__Form_Input.define()