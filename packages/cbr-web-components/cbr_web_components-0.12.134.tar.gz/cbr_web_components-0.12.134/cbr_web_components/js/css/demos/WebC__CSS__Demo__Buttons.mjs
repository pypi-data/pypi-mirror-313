import Web_Component    from '../../core/Web_Component.mjs';
import Button           from '../../core/Button.mjs';
import Div              from '../../core/Div.mjs';
import H                from '../../core/H.mjs';
import HR               from '../../core/HR.mjs';
import Text             from '../../core/Text.mjs';
import CSS__Buttons     from '../CSS__Buttons.mjs';
import CSS__Typography  from "../CSS__Typography.mjs";

export default class WebC__CSS__Demo__Buttons extends Web_Component {
    load_attributes() {
        this.css_buttons    = new CSS__Buttons(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css      = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'buttons-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Buttons Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Basic Buttons with all variants
        let h_basic = new H({ level: 2, value: 'Button Variants' })
        let basic_buttons = [
            new Button({ class: 'btn btn-primary', value: 'Primary' }),
            new Button({ class: 'btn btn-secondary', value: 'Secondary' }),
            new Button({ class: 'btn btn-success', value: 'Success' }),
            new Button({ class: 'btn btn-danger', value: 'Danger' }),
            new Button({ class: 'btn btn-warning', value: 'Warning' }),
            new Button({ class: 'btn btn-info', value: 'Info' }),
            new Button({ class: 'btn btn-light', value: 'Light' }),
            new Button({ class: 'btn btn-dark', value: 'Dark' }),
            new Button({ class: 'btn btn-link', value: 'Link' })
        ]

        // Outline Buttons
        let h_outline = new H({ level: 2, value: 'Outline Buttons' })
        let outline_buttons = [
            new Button({ class: 'btn btn-outline-primary', value: 'Primary' }),
            new Button({ class: 'btn btn-outline-secondary', value: 'Secondary' }),
            new Button({ class: 'btn btn-outline-success', value: 'Success' }),
            new Button({ class: 'btn btn-outline-danger', value: 'Danger' }),
            new Button({ class: 'btn btn-outline-warning', value: 'Warning' }),
            new Button({ class: 'btn btn-outline-info', value: 'Info' }),
            new Button({ class: 'btn btn-outline-light', value: 'Light' }),
            new Button({ class: 'btn btn-outline-dark', value: 'Dark' })
        ]

        // Button Sizes
        let h_sizes = new H({ level: 2, value: 'Button Sizes' })
        let size_buttons = [
            new Button({ class: 'btn btn-primary btn-sm', value: 'Small' }),
            new Button({ class: 'btn btn-primary', value: 'Default' }),
            new Button({ class: 'btn btn-primary btn-lg', value: 'Large' })
        ]

        // Text Buttons
        let h_text = new H({ level: 2, value: 'Text Buttons' })
        let text_buttons = [
            new Button({ class: 'btn btn-text', value: 'Text Button' })
        ]

        // Status Buttons
        let h_status = new H({ level: 2, value: 'Status Buttons' })
        let status_buttons = [
            new Button({ class: 'btn btn-success', value: 'Success' }),
            new Button({ class: 'btn btn-error', value: 'Error' }),
            new Button({ class: 'btn btn-warning', value: 'Warning' })
        ]

        // Disabled State
        let h_disabled = new H({ level: 2, value: 'Disabled State' })
        let disabled_buttons = [
            new Button({ class: 'btn btn-primary disabled', value: 'Disabled Primary' }),
            new Button({ class: 'btn btn-secondary', value: 'Disabled Secondary', attributes: { disabled: true } })
        ]

        // Loading State
        let h_loading = new H({ level: 2, value: 'Loading State' })
        let loading_buttons = [
            new Button({ class: 'btn btn-primary btn-loading', value: 'Loading' })
        ]

        // Block Button
        let h_block = new H({ level: 2, value: 'Block Button' })
        let block_buttons = [
            new Button({ class: 'btn btn-primary btn-block', value: 'Block Button' })
        ]

        // Button Groups
        let h_groups = new H({ level: 2, value: 'Button Groups' })
        let groups = [
            new Div({ class: 'btn-group' }).add_elements(
                new Button({ class: 'btn btn-primary', value: 'Left' }),
                new Button({ class: 'btn btn-primary', value: 'Middle' }),
                new Button({ class: 'btn btn-primary', value: 'Right' })
            )
        ]

        // Button Toolbar
        let h_toolbar = new H({ level: 2, value: 'Button Toolbar' })
        let toolbar = [
            new Div({ class: 'btn-toolbar' }).add_elements(
                new Div({ class: 'btn-group' }).add_elements(
                    new Button({ class: 'btn btn-primary', value: '1' }),
                    new Button({ class: 'btn btn-primary', value: '2' }),
                    new Button({ class: 'btn btn-primary', value: '3' })
                ),
                new Div({ class: 'btn-group' }).add_elements(
                    new Button({ class: 'btn btn-secondary', value: '4' }),
                    new Button({ class: 'btn btn-secondary', value: '5' })
                ),
                new Button({ class: 'btn btn-accent', value: '6' })
            )
        ]

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_basic, ...basic_buttons,
            h_outline, ...outline_buttons,
            h_sizes, ...size_buttons,
            h_text, ...text_buttons,
            h_status, ...status_buttons,
            h_disabled, ...disabled_buttons,
            h_loading, ...loading_buttons,
            h_block, ...block_buttons,
            h_groups, ...groups,
            h_toolbar, ...toolbar
        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_buttons.apply_framework()
            this.css_typography.apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Buttons.define()