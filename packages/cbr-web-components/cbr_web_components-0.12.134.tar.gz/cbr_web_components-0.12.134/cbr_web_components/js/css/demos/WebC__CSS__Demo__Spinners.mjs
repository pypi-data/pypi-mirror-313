import Web_Component   from '../../core/Web_Component.mjs';
import Button          from '../../core/Button.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import HR              from '../../core/HR.mjs';
import Span            from '../../core/Span.mjs';
import Text            from '../../core/Text.mjs';
import CSS__Spinners   from '../CSS__Spinners.mjs';
import CSS__Typography from '../CSS__Typography.mjs';
import CSS__Buttons    from '../CSS__Buttons.mjs';

export default class WebC__CSS__Demo__Spinners extends Web_Component {
    load_attributes() {
        this.css_buttons    = new CSS__Buttons   (this)
        this.css_spinners   = new CSS__Spinners(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css      = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'spinners-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Spinners Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Border Spinner
        let h_border   = new H({ level: 2, value: 'Border Spinner' })
        let border_row = new Div({ class: 'demo-row' }).add_elements(new Div({ class: 'spinner spinner-primary'   }),
                                                                    new Div({ class: 'spinner spinner-secondary' }),
                                                                    new Div({ class: 'spinner spinner-success'   }),
                                                                    new Div({ class: 'spinner spinner-error'     }))

        // Growing Spinner
        let h_grow   = new H({ level: 2, value: 'Growing Spinner' })
        let grow_row = new Div({ class: 'demo-row' }).add_elements(new Div({ class: 'spinner-grow spinner-primary'   }),
                                                                  new Div({ class: 'spinner-grow spinner-secondary' }),
                                                                  new Div({ class: 'spinner-grow spinner-success'   }),
                                                                  new Div({ class: 'spinner-grow spinner-error'     }))

        // Small Spinner
        let h_small   = new H({ level: 2, value: 'Small Spinner' })
        let small_row = new Div({ class: 'demo-row' }).add_elements(new Div({ class: 'spinner spinner-sm spinner-primary'     }),
                                                                   new Div({ class: 'spinner-grow spinner-sm spinner-primary' }))

        // Button with Spinner
        let h_button   = new H({ level: 2, value: 'Button with Spinner' })
        let button_row = new Div({ class: 'demo-row' }).add_elements(new Button({ class: 'btn btn-primary' }).add_elements(new Div({ class: 'spinner spinner-sm' }),
                                                                                                                           new Text({ value: 'Loading...' })))

        // Spinner with Text
        let h_text   = new H({ level: 2, value: 'Spinner with Text' })
        let text_row = new Div({ class: 'spinner-flex' }).add_elements(new Div({ class: 'spinner spinner-primary' }),
                                                                      new Span({ class: 'spinner-text', value: 'Loading...' }))

        // Centered Spinner
        let h_center   = new H({ level: 2, value: 'Centered Spinner' })
        let center_row = new Div({ class: 'spinner-flex', style: 'height: 100px;' }).add_elements(new Div({ class: 'spinner spinner-primary' }))

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_border, border_row,
            h_grow, grow_row,
            h_small, small_row,
            h_button, button_row,
            h_text, text_row,
            h_center, center_row
        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_buttons    .apply_framework()
            this.css_spinners   .apply_framework()
            this.css_typography .apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Spinners.define()