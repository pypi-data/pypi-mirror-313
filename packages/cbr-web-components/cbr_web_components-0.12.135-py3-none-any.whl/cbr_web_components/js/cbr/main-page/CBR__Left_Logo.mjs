import Div from "../../core/Div.mjs"
import Img from "../../core/Img.mjs"

export default class CBR__Left_Logo extends Div {
    constructor({id, ...kwargs}={}) {
        kwargs.class = `logo ${kwargs.class || ''}`
        super({id, ...kwargs})
        //const cbr_logo = 'assets/cbr/cbr-logo-beta.png'
        const cbr_logo = 'https://static.dev.aws.cyber-boardroom.com/cbr-static/latest/assets/cbr/cbr-logo-beta.png'
        const div_container = new Div({ class: 'logo-container'                                            })
        const div_logo      = new Div({ class: 'logo-wrapper'                                              })
        const img_logo      = new Img({ class: 'logo'      , alt: 'Cyber Boardroom Logo',  src: cbr_logo   })

        div_logo     .add_element (img_logo                            )
        div_container.add_element (div_logo                            )

        this.add_element(div_container)
    }

    static css_rules() {
        return {
            ".logo-container": {
                display: "flex",
                flexDirection: "column",
                padding: "1rem",
                backgroundColor: "#ffffff",
                borderRadius: "0.5rem"
            },

            ".logo-wrapper": {
                marginBottom: "1rem"
            },

            ".logo": {
                width: "100%",
                height: "auto"
            }
        }
    }
}