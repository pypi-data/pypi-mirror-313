import API__Invoke          from "../../../js/data/API__Invoke.mjs"
import CSS__Side_Menu       from "../../css/menus/CSS__Side_Menu.mjs"
import Left_Menu            from "../../css/menus/Left_Menu.mjs"
import CSS__Alerts          from "../../css/CSS__Alerts.mjs";
import CSS__Typography      from '../../css/CSS__Typography.mjs'
import Div                  from "../../core/Div.mjs"
import Web_Component        from '../../core/Web_Component.mjs'
import WebC__Resize_Button  from "../../elements/ui/WebC__Resize_Button.mjs";
import CBR_Events           from "../CBR_Events.mjs";
import CBR__Left_Logo       from "./CBR__Left_Logo.mjs"
import CBR__Important_Alert from "./CBR__Important_Alert.mjs"


export default class WebC__CBR__Left_Menu extends Web_Component {

    left_menu__resize__breakpoint = 768
    left_menu__resize__event_name = CBR_Events.CBR__UI__LEFT_MENU_TOGGLE

    constructor() {
        super()
        this.base_path  = '/'
        this.api_invoke = new API__Invoke()
        this.menu_data  = null
    }

    // Web_Component overrides

    apply_css() {
        new CSS__Alerts    (this).apply_framework()
        new CSS__Side_Menu (this).apply_framework()
        new CSS__Typography(this).apply_framework()

        this.add_css_rules(CBR__Left_Logo      .css_rules())
        this.add_css_rules(CBR__Important_Alert.css_rules())
        this.add_css_rules(this.css_rules())
    }

    async load_data() {
        await this.fetch_menu_items()
    }

    load_attributes() {
        this.base_path    = this.getAttribute('base_path') || this.base_path
    }

    add_event_listeners() {
        this.add_window_event_listener(CBR_Events.CBR__UI__LEFT_MENU_TOGGLE, this.on_left_menu_toggle)
    }

    add_web_components() {
        let params = { resize_breakpoint : this.left_menu__resize__breakpoint ,
                       resize_event_name : this.left_menu__resize__event_name }
        this.add_web_component(WebC__Resize_Button, params )
    }

    // API methods

    async fetch_menu_items() {
        try {
            const response = await this.api_invoke.invoke_api('/api/user-data/ui/left-menu', 'GET')
            this.menu_data = response.menu_items
        } catch (error) {
            //console.error('Error fetching menu items:', error)
            this.menu_data = {}  // Set empty object on error
        }
    }

    // component methods



    on_left_menu_toggle (event) {
        const minimized = event.detail.minimized
        if (minimized) {
            this.div__left_menu_main.add_class   ('left-menu-minimized')
        } else {
            this.div__left_menu_main.remove_class('left-menu-minimized')
        }
    }

    html() {
        const div_left_menu       = new Div       ({ class: 'left-menu-main'       })
        const cbr_left_menu       = new Left_Menu ({ menu_items: this.menu_items() })
        const cbr_left_logo       = new CBR__Left_Logo()
        const cbr_important_alert = new CBR__Important_Alert()

        div_left_menu.add_elements(cbr_left_logo, cbr_left_menu, cbr_important_alert)
        return div_left_menu
    }

    menu_items() {
        if (!this.menu_data) return []

        return Object.entries(this.menu_data).map(([key, item]) => {
            const link_attributes = {
                'data-target-type'   : item.web_component ? 'web_component' : 'link' , // Add target type attribute
                'data-component-path': item.web_component_path || ''                 ,
                icon                 : item.icon                                     ,
                label                : item.label                                    ,
            }

            if (item.web_component) {
                link_attributes['data-component'] = item.web_component             // Add data-component attribute for web components
                link_attributes['href'] = `${this.base_path}/${key}`                 // Use key as path for history
            } else {
                link_attributes['href'] = `${this.base_path}/${key}/index`          // Regular path navigation
            }
            return link_attributes
        })
    }

    // GETTERS
    get div__left_menu_main() { return this.query_selector('.left-menu-main')  }

    // CSS RULES
    css_rules() {
        return {
            ".left-menu-main"                       : { transition : "width 0.3s ease-in-out"    ,
                                                        position   : "relative"                  },
            ".left-menu-minimized"                  : { width      : "60px"                      ,
                                                        paddingTop : "10px"                      ,
                                                        overflow   : "hidden"                    },
            ".left-menu-minimized .logo-container"  : { display    : "none"                      },
            ".left-menu-minimized .important-alert" : { display    : "none"                      },
        }
    }
}

WebC__CBR__Left_Menu.define()