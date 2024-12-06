import Div           from "../core/Div.mjs";
import Tag           from "../core/Tag.mjs";
import Web_Component from "../core/Web_Component.mjs"

export default class WebC__Target_Div extends Web_Component {
    constructor() {
        super();
    }
    // properties
    // get inner_html()      { return this.target_element.innerHTML  }
    // set inner_html(value) { this.target_element.innerHTML = value }

    // methods

    apply_css() {
        this.add_css_rules (this.css_rules())
    }

    // todo: see if we need this with unique Ids for per target-div (at the momment we can get the div via .query_selector('.target_div') )
    // get target_element() {
    //     return this.shadow_root().querySelector(".target_div")  //(`#${this.target_div_id}`)
    // }

    build({...kwargs}={}) {      // todo: change to a different  method than build
        this.add_css_rules (this.css_rules(kwargs))
        return this
    }

    css_rules({right="10px" , left=null, width=null, top="10px", bottom="10px", height=null, z_index=null}={}) {
        return { ".target_div": { border         : "3px solid #724ae8",
                                  bottom         : bottom            ,
                                  left           : left              ,
                                  overflow       : "auto"            ,
                                  position       : "fixed"           ,
                                  right          : right             ,
                                  top            : top               ,
                                  height         : height            ,
                                  width          : width || '70%'    ,
                                  zIndex         : z_index || "1000" ,
                                  backgroundColor: "white"          }}
    }

    html(chat_bot_id=null) {
        const target_div = new Div({id:chat_bot_id, class:'target_div'})
        const slot_div = new Tag({tag:'slot'})
        target_div.add(slot_div)
        slot_div.html_config.include_id = false
        return target_div.html()
    }

    style(styles) {
        const div_style = this.target_div().style;
        if (typeof styles === 'object') {
            for (const property in styles) {
                if (styles.hasOwnProperty(property)) {
                    div_style[property] = styles[property];
                }
            }
        }
        return divStyle;
    }

    target_div() {
        return this.target_element
    }

}

WebC__Target_Div.define()