import Div from "../../core/Div.mjs"

export default class CBR__Content__Placeholder extends Div {
    constructor({id, ...kwargs}={}) {
        kwargs.class = `content-placeholder ${kwargs.class || ''}`
        super({id, ...kwargs})

        const div_container = new Div({ id: 'placeholder-container', class: 'placeholder-container'                                    })

        this.add_element(div_container)


    }

    static css_rules() {
        return {
            ".placeholder-container": { height          : '100%',
                                        width           : '100%',
                                        backgroundColor : "#eef5f9",                          // Light base color
                                        boxShadow       : "inset 10px 20px 30px rgba(0,0,0,0.07)",  // Soft shadow
            }
        }
    }
}