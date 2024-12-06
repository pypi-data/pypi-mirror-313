import Icon                 from "../../css/icons/Icon.mjs"
import Div                  from "../../core/Div.mjs"
import Tag                  from "../../core/Tag.mjs"

export default class CBR__Top_Banner extends Div {
    constructor({...kwargs}={}) {
        super({...kwargs})
        this.setup()
    }

    setup() {
        this.add_class('top-banner')

        const menu_icon    = new Icon({ class: 'menu-icon icon-lg'  , icon: 'menu' })    // Hamburger menu
        const user_session = new Tag({tag: 'webc-cbr-user-session' })

        this.add_elements(menu_icon, user_session)
    }

    static css_rules() {
        return {
            ".top-banner": {
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "0 1rem",
                height: "100%",
                backgroundColor: "#1e88e5",
                color: "#ffffff",
                position: "relative"
            },

            ".menu-icon": {
                color: "#ffffff",
                cursor: "pointer",
                fontSize: "1.75rem",
                padding: "0.5rem",
                marginLeft: "-0.5rem"
            },

            ".menu-icon:hover": {
                backgroundColor: "rgba(255, 255, 255, 0.1)",
                borderRadius: "4px"
            }
        }
    }
}