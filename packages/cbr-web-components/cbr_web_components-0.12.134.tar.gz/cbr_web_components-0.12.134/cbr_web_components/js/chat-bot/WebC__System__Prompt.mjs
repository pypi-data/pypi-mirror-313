import Web_Component  from "../core/Web_Component.mjs";
import Icon           from '../css/icons/Icon.mjs';
import Div            from '../core/Div.mjs';
import Icon__Mappings from "../css/icons/Icon__Mappings.mjs";

export default class WebC__System__Prompt extends Web_Component {
    constructor() {
        super();
        this.expanded = false;
        this.content = '';
    }

    load_attributes() {
        this.content = this.getAttribute('content') || '';
    }

    add_event_listeners() {
        const toggle = this.shadowRoot.querySelector('.prompt-header');
        if (toggle) {
            toggle.addEventListener('click', () => this.toggle_expansion());
        }
    }

    toggle_expansion() {
        this.expanded = !this.expanded;
        const content = this.shadowRoot.querySelector('.prompt-content');
        const toggle  = this.shadowRoot.querySelector('.icon');

        content.style.display = this.expanded ? 'block' : 'none';
        toggle.textContent = Icon__Mappings.getIcon(this.expanded ? 'triangle-down' : 'triangle-right');

        if (this.expanded) {
            content.scrollTop = 0;
        }
    }

    async apply_css() {
        this.add_css_rules (this.css_rules());
    }

    html() {
        const container = new Div({ class: 'system-prompt-container' });

        const header  = new Div({ class: 'prompt-header' });
        const toggle  = new Div({ class: 'prompt-toggle' }).add_element(new Icon({ icon: 'triangle-right', class: 'icon' }));
        const summary = new Div({class: 'prompt-summary',   value: `System Prompt (${this.calculate_size(this.content)} chars)` });
        const content = new Div({ class: 'prompt-content',  value: this.content });
        header   .add_elements(toggle, summary);
        container.add_elements(header, content);

        return container
    }

    calculate_size(content) {
        return content.length;
    }

    css_rules() {
        return {
            ".system-prompt-container" : { "background-color" : "#2a2d3e"           ,   // Softer dark blue background
                                          "border-radius"    : "8px"               ,
                                          "margin"          : "8px auto"          ,   // Center alignment
                                          "width"           : "100%"              ,
                                          "max-width"       : "80%"              ,
                                          "border"          : "1px solid #3f4259" ,   // Subtle border
                                          "box-shadow"      : "0 2px 4px rgba(0,0,0,0.1)" },

            ".prompt-header"          : { "display"         : "flex"              ,
                                          "align-items"     : "center"             ,
                                          "padding"         : "8px 12px"           ,
                                          "color"           : "#e6e6e6"            ,
                                          "border-radius"    : "8px"                ,
                                          "border-bottom"   : "1px solid #3f4259"  ,   // Separator line
                                          "cursor"          : "pointer"            },

            ".prompt-toggle"          : { "margin-right"    : "8px"               ,
                                         "cursor"          : "pointer"           ,
                                         "display"         : "flex"              ,
                                         "align-items"     : "center"            ,
                                         "color"           : "#8b8fa3"           },   // Softer icon color

            ".prompt-summary"         : { "font-size"       : "0.9rem"            ,
                                         "font-family"     : "monospace"         ,
                                         "color"           : "#c1c3cf"           },   // Softer text color

            ".prompt-content"         : { "display"         : "none"              ,
                                         "padding"         : "12px 16px"         ,
                                         "color"           : "#c1c3cf"           ,   // Softer text color
                                         "font-size"       : "0.9rem"            ,
                                         "line-height"     : "1.5"               ,
                                         "font-family"     : "monospace"         ,
                                         "max-height"      : "50vh"              ,
                                         "overflow-y"      : "auto"              ,
                                         "white-space"     : "pre-wrap"          },

            // Custom scrollbar styling
            ".prompt-content::-webkit-scrollbar"         : { "width"           : "8px"               ,
                                                            "background-color" : "transparent"        },

            ".prompt-content::-webkit-scrollbar-track"   : { "background"      : "rgba(255,255,255,0.05)" },

            ".prompt-content::-webkit-scrollbar-thumb"   : { "background"      : "rgba(255,255,255,0.2)"  ,
                                                            "border-radius"    : "4px"                     },

            ".prompt-content::-webkit-scrollbar-thumb:hover": { "background"   : "rgba(255,255,255,0.3)"  },

            ".prompt-content pre"     : { "background-color": "#363a4f"           ,   // Slightly lighter code blocks
                                         "padding"         : "8px 12px"          ,
                                         "border-radius"   : "6px"               ,
                                         "margin"          : "8px 0"             ,
                                         "border"          : "1px solid #3f4259" ,   // Subtle border
                                         "overflow-x"      : "auto"              },

            ".prompt-content code"    : { "background-color": "#363a4f"           ,   // Matching inline code style
                                         "padding"         : "2px 4px"           ,
                                         "border-radius"   : "4px"               ,
                                         "border"          : "1px solid #3f4259" }
        }
    }

}

WebC__System__Prompt.define();