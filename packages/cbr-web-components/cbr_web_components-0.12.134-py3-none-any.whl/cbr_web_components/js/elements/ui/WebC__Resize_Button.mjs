import Web_Component from '../../core/Web_Component.mjs'
import Button       from '../../core/Button.mjs'


export default class WebC__Resize_Button extends Web_Component {

    default__resize__breakpoint = 768
    default__resize__event_name = 'resize-event'

    load_attributes() {
        this.breakpoint = parseInt(this.getAttribute('resize_breakpoint')) || this.default__resize__breakpoint
        this.event_name =          this.getAttribute('resize_event_name')  || this.default__resize__event_name
        this.add_css_rules(this.css_rules())
        this.dispatch_resize_event()
   }

   add_event_listeners() {
        this.add_event_listener('.toggle-button', 'click', () => this.toggle_size())
        window.addEventListener('resize'       , () => this.handle_resize())
   }

    handle_resize() {
        if (window.innerWidth < this.breakpoint && !this.minimized) {
            this.minimize()
        } else if (window.innerWidth >= this.breakpoint && this.minimized) {
            this.expand()
        }
    }

    minimize() {
       this.minimized = true
       this.query_selector('.toggle-button').innerHTML = '→'
       this.dispatch_resize_event()
   }

   expand() {
       this.minimized = false
       this.query_selector('.toggle-button').innerHTML = '←'
       this.dispatch_resize_event()
   }

    toggle_size() {
       this.minimized ? this.expand() : this.minimize()
    }

    dispatch_resize_event() {
        const event = new CustomEvent(this.event_name, { bubbles  : true                        ,
                                                         composed : true                        ,
                                                         detail   : { minimized: this.minimized }})
        this.dispatchEvent(event)
   }

   html() {
       return new Button({class: 'toggle-button', value: this.minimized ? '→' : '←'})
   }

   css_rules() {
       return {
           ".resize-main"         : { transition    : "width 0.3s ease-in-out" ,
                                    position        : "relative"               },


           ".resize-minimized"    : { paddingTop      : "10px"                 ,
                                      overflow        : "hidden"               },

           ".toggle-button"       : { position        : "absolute"             ,
                                    top             : "0px"                    ,
                                    padding         : "5px"                    ,
                                    cursor          : "pointer"                ,
                                    backgroundColor : "transparent"            ,
                                    border          : "none"                   ,
                                    color           : "#666"                   },

           ".toggle-button:hover" : { color           : "#000"                 }
       }
   }
}

WebC__Resize_Button.define()