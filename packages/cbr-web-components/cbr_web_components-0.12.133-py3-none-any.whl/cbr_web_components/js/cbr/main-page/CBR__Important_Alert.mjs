import Div from "../../core/Div.mjs"

export default class CBR__Important_Alert extends Div {
    constructor({id, ...kwargs}={}) {
        kwargs.class = `important-alert ${kwargs.class || ''}`
        super({id, ...kwargs})

        const div_notice   = new Div({ class: 'alert alert-success alert-important-note'                 })
        const div_content  = new Div({ class: 'alert-content'                                            })
        const text_title   = new Div({ class: 'alert-heading', value: 'Important Note'                   })
        const text_content = new Div({ value: "Don't use any private or confidential data in the chats. " +
                                            "There is no control over what happens inside the LLM " +
                                            "platforms used, and all chat thread content is publicly available."})

        div_content.add_elements(text_title, text_content              )
        div_notice .add_element (div_content                           )

        this.add_element(div_notice)
    }

    static css_rules() {
        return {
            ".important-alert": {
                padding: "1rem",
                fontWeight: 100,

            },
            ".alert-heading": {
                fontWeight: 300,
            },
            ".alert-content > div": {
                lineHeight: "1.4",                         // Improve text readability
                fontSize: "0.875rem",
            },
            ".alert-important-note": {
              backgroundColor: "rgba(38, 198, 218, 0.1)",
            }
        }
    }
}