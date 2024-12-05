import Web_Component    from '../../core/Web_Component.mjs';
import Button           from '../../core/Button.mjs';
import Div              from '../../core/Div.mjs';
import H                from '../../core/H.mjs';
import HR               from '../../core/HR.mjs';
import P                from '../../core/P.mjs';
import A                from '../../core/A.mjs';
import Text             from '../../core/Text.mjs';
import CSS__Alerts      from '../CSS__Alerts.mjs';
import CSS__Typography  from "../CSS__Typography.mjs";

export default class WebC__CSS__Demo__Alerts extends Web_Component {
    load_attributes() {
        this.css_alerts     = new CSS__Alerts(this)
        this.apply_css      = this.hasAttribute('no-css') === false
        this.css_typography = new CSS__Typography(this)
    }

    render() {
        let div_root = new Div({ id: 'alerts-demo' })

        // Header
        let header = [new HR(),
                      new Text({ value: 'Alerts Demo' + (this.apply_css ? ' (with CSS)' : '') }),
                      new HR()]

        // Basic Alerts
        let h_basic = new H({ level: 2, value: 'Basic Alerts' })
        let basic_alerts = [new Div({ class: 'alert alert-primary'   }).add_elements(new Div({ class: 'alert-content' }).add_elements(new Text({ value: 'A simple primary alert—check it out!'   }))),
                            new Div({ class: 'alert alert-secondary' }).add_elements(new Div({ class: 'alert-content' }).add_elements(new Text({ value: 'A simple secondary alert—check it out!' }))),
                            new Div({ class: 'alert alert-success'   }).add_elements(new Div({ class: 'alert-content' }).add_elements(new Text({ value: 'A simple success alert—check it out!'   }))),
                            new Div({ class: 'alert alert-danger'    }).add_elements(new Div({ class: 'alert-content' }).add_elements(new Text({ value: 'A simple danger alert—check it out!'    }))),
                            new Div({ class: 'alert alert-warning'   }).add_elements(new Div({ class: 'alert-content' }).add_elements(new Text({ value: 'A simple warning alert—check it out!'   }))),
                            new Div({ class: 'alert alert-info'      }).add_elements(new Div({ class: 'alert-content' }).add_elements(new Text({ value: 'A simple info alert—check it out!'      }))),
                            new Div({ class: 'alert alert-light'     }).add_elements(new Div({ class: 'alert-content' }).add_elements(new Text({ value: 'A simple light alert—check it out!'     }))),
                            new Div({ class: 'alert alert-dark'      }).add_elements(new Div({ class: 'alert-content' }).add_elements(new Text({ value: 'A simple dark alert—check it out!'      })))]

        // Alerts with Links
        let h_links = new H({ level: 2, value: 'Alerts with Links' })
        let link_alerts = [new Div({ class: 'alert alert-primary'   }).add_elements(new Div({ class: 'alert-content' }).add_elements(new Text({ value: 'A simple primary alert with '   }),
                                                                                                                                     new A   ({ href : '#' , value: 'an example link'   }),
                                                                                                                                     new Text({ value: '. Give it a click if you like.' }))),
                           new Div({ class: 'alert alert-secondary' }).add_elements(new Div({ class: 'alert-content' }).add_elements(new Text({ value: 'A simple secondary alert with ' }),
                                                                                                                                     new A   ({ href : '#' , value: 'an example link'   }),
                                                                                                                                     new Text({ value: '. Give it a click if you like.' })))]
        // Additional Content
        let h_additional = new H({ level: 2, value: 'Additional Content' })
        let additional_alerts = [new Div({ class: 'alert alert-success' }).add_elements(new Div({ class: 'alert-content' }).add_elements(new P({ class: 'alert-heading', value: 'Well done!' }),
                                                                                                                                         new P({ value: 'You successfully read this important alert message. This example text is going to run a bit longer so that you can see how spacing within an alert works with this kind of content.' }),
                                                                                                                                         new P({ value: 'Whenever you need to, be sure to use margin utilities to keep things nice and tidy.' })))]
        // Add all sections to root
        div_root.add_elements(...header  ,
                              h_basic     , ...basic_alerts     ,
                              h_links     , ...link_alerts      ,
                              h_additional, ...additional_alerts)

        if (this.apply_css) {
            this.css_alerts    .apply_framework()
            this.css_typography.apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Alerts.define()