import Web_Component           from '../../core/Web_Component.mjs'
import CSS__Grid               from '../../css/grid/CSS__Grid.mjs'
import CSS__Icons              from '../../css/icons/CSS__Icons.mjs'
import Icon                    from '../../css/icons/Icon.mjs'
import Div                     from '../../core/Div.mjs'
import WebC__CBR__User_Session from "../session/WebC__CBR__User_Session.mjs";

export default class WebC__CBR__Top_Banner extends Web_Component {

    apply_css() {
        new CSS__Grid (this).apply_framework()
        new CSS__Icons(this).apply_framework()
        this.add_css_rules(this.css_rules())
    }

    async add_web_components() {
        super.add_web_component_to('.user-session', WebC__CBR__User_Session)
    }

    add_event_handlers() {
        this.add_event__on('click', '.menu-icon', this.handle__on__toggle_menu)
    }

    handle__on__toggle_menu() {
        this.raise_event_global('toggle-menu', { opened: true })
    }
    html() {
        const container    = new Div ({ class: 'top-banner'                       })    // parent div
        const menu_icon    = new Icon({ class: 'menu-icon icon-lg', icon : 'menu' })    // hamburger menu
        const user_session = new Div ({ class: 'user-session'                     })    // user session component

        container.add_elements(menu_icon, user_session)
        return container
    }

    css_rules() {
        return {
            ".top-banner"     : { display         : "flex"                      ,      // Main banner container
                                  justifyContent   : "space-between"             ,
                                  alignItems       : "center"                    ,
                                  padding          : "0 1rem"                    ,
                                  height           : "100%"                      ,
                                  backgroundColor  : "#1e88e5"                   ,
                                  color            : "#ffffff"                   ,
                                  position         : "relative"                  },

            ".menu-icon"      : { color           : "#ffffff"                   ,      // Menu icon styling
                                  cursor          : "pointer"                    ,
                                  fontSize        : "1.75rem"                    ,
                                  padding         : "0.5rem"                     ,
                                  marginLeft      : "-0.5rem"                    },

            ".menu-icon:hover": { backgroundColor : "rgba(255, 255, 255, 0.1)" ,      // Menu icon hover effect
                                  borderRadius    : "4px"                        } ,
            ".user-session"   : { backgroundColor: "red"                        }      // User session text
        }
    }
}

WebC__CBR__Top_Banner.define()