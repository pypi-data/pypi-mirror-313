import A    from "../../core/A.mjs"
import Div  from "../../core/Div.mjs"
import Icon from "../../css/icons/Icon.mjs"

export default class CBR__Left_Footer extends Div {

    href__settings = '/web/user/profile'
    href__logout = '/web/sign-out'

    constructor({id, version, ...kwargs}={}) {
        kwargs.class = `left-footer ${kwargs.class || ''}`
        super({id, ...kwargs})
        this.version = version || 'NA'
        this.build()
    }
    build() {
        const div_footer      = new Div ({ class: 'footer-container'                                               })
        const div_icons       = new Div ({ class: 'icons-container'                                                })
        const div_version     = new Div ({ class: 'version-container'                                              })
        const a_settings      = new A   ({ class: 'link-icon'       , href: this.href__settings                    })
        const a_logout        = new A   ({ class: 'link-icon'       , href: this.href__logout                      })
        const icon_settings   = new Icon({ class: 'footer-icon'     , icon: 'settings'                             })
        const icon_logout     = new Icon({ class: 'footer-icon'     , icon: 'logout'                               })
        const text_version    = new Div ({ class: 'version-text'    , value: `© Cyber Boardroom - ${this.version}` })

        a_settings  .add_element (icon_settings          )
        a_logout    .add_element (icon_logout            )
        div_icons  .add_elements (a_settings, a_logout   )
        div_version.add_element  (text_version           )
        div_footer .add_elements (div_icons, div_version )

        this.add_element(div_footer)
    }

    static css_rules() {
        return {
            ".left-footer": {
                display: "flex",
                alignItems: "center",
                padding: "0 1rem",
            },

            ".footer-container": {
                display: "flex",
                flexDirection: "column",                    // Stack containers vertically
                width: "100%"
            },

            ".icons-container": {
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                width: "100%",
                color: "#6c757d"                           // Medium gray for icons and text
            },

            ".version-container": {
                display: "flex",
                alignItems: "center",
                justifyContent: "center",                  // Center the version text
            },

            ".version-text": {
                fontSize: "0.875rem",
                fontWeight: "300",
                color: "#495057",                          // Slightly darker for better readability
            },

            ".footer-icon": {
                fontSize: "1.5rem",
                padding: "0.5rem"
            },

            ".footer-icon:hover": {
                color: "#495057"                           // Darker on hover
            },
            ".link-icon": {
                marginBottom: "0.5rem",
                textDecoration: "none",              // Remove underline
                color: "inherit",                    // Use parent's color
                display: "flex",                     // Ensure icon alignment
                alignItems: "center"
            }
        }
    }
}