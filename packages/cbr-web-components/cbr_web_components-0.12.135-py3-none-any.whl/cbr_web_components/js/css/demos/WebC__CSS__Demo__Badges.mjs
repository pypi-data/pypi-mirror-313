import Web_Component    from '../../core/Web_Component.mjs';
import Span             from '../../core/Span.mjs';
import Button           from '../../core/Button.mjs';
import Div              from '../../core/Div.mjs';
import H                from '../../core/H.mjs';
import HR               from '../../core/HR.mjs';
import Text             from '../../core/Text.mjs';
import CSS__Badges      from '../CSS__Badges.mjs';
import CSS__Buttons     from '../CSS__Buttons.mjs';
import CSS__Typography  from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__Badges extends Web_Component {
    load_attributes() {
        this.css_badges      = new CSS__Badges    (this)
        this.css_buttons     = new CSS__Buttons   (this)
        this.css_typography  = new CSS__Typography(this)
        this.apply_css       = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'badges-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Badges Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Background Colors
        let h_colors = new H({ level: 2, value: 'Background Colors' })
        let color_badges = [new Span({ class: 'badge badge-primary'  , value: 'Primary'   }),
                            new Span({ class: 'badge badge-secondary', value: 'Secondary' }),
                            new Span({ class: 'badge badge-success'  , value: 'Success'   }),
                            new Span({ class: 'badge badge-danger'   , value: 'Danger'    }),
                            new Span({ class: 'badge badge-warning'  , value: 'Warning'   }),
                            new Span({ class: 'badge badge-info'     , value: 'Info'      }),
                            new Span({ class: 'badge badge-light'    , value: 'Light'     }),
                            new Span({ class: 'badge badge-dark'     , value: 'Dark'      })]

        // Pill Badges
        let h_pills = new H({ level: 2, value: 'Pill Badges' })
        let pill_badges = [new Span({ class: 'badge badge-pill badge-primary'  , value: 'Primary'   }),
                           new Span({ class: 'badge badge-pill badge-secondary', value: 'Secondary' }),
                           new Span({ class: 'badge badge-pill badge-success'  , value: 'Success'   }),
                           new Span({ class: 'badge badge-pill badge-danger'   , value: 'Danger'    }),
                           new Span({ class: 'badge badge-pill badge-warning'  , value: 'Warning'   }),
                           new Span({ class: 'badge badge-pill badge-info'     , value: 'Info'      }),
                           new Span({ class: 'badge badge-pill badge-light'    , value: 'Light'     }),
                           new Span({ class: 'badge badge-pill badge-dark'     , value: 'Dark'      })]

        // Buttons with Badges
        let h_buttons = new H({ level: 2, value: 'Buttons with Badges' })
        let button_badges = [new Button({ class: 'btn btn-primary'  }).add_elements(new Text({ value: 'Notifications ' }),
                                                                                    new Span({ class: 'badge badge-light', value: '4' })),
                             new Button({ class: 'btn btn-secondary' }).add_elements(new Text({ value: 'Messages ' }),
                                                                                     new Span({ class: 'badge badge-light', value: '8' }))]

        // Positioned Badges
        let h_positioned = new H({ level: 2, value: 'Positioned Badges' })
        let positioned_badges = [new Button({ class: 'btn btn-primary position-relative', type: 'button'                              }).add_elements(new Text({ value: 'Inbox ' }),
                                                                                                                                                      new Span({class: 'position-absolute top-0 start-100 translate-middle badge badge-danger badge-pill',  value: '99+'}),
                                                                                                                                                      new Span({ class: 'visually-hidden', value: 'unread messages' })),
                                 new Button({ class: 'btn btn-primary position-relative', type: 'button', style: 'margin-left: 2rem;' }).add_elements(new Text({ value: 'Profile ' }),
                                                                                                                                                      new Span({class: 'position-absolute top-0 start-100 translate-middle badge badge-danger rounded-pill',  style: 'padding: 0.4em 0.4em;'}),
                                                                                                                                                      new Span({ class: 'visually-hidden', value: 'New alerts' }))]
        // Add all sections to root
        div_root.add_elements(...header   ,
                              h_colors    , ...color_badges     ,
                              h_pills     , ...pill_badges      ,
                              h_buttons   , ...button_badges    ,
                              h_positioned, ...positioned_badges)

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_badges    .apply_framework()
            this.css_buttons   .apply_framework()
            this.css_typography.apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Badges.define()