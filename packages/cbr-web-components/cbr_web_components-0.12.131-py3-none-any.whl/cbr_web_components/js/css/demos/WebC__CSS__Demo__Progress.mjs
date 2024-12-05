import Web_Component   from '../../core/Web_Component.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import HR              from '../../core/HR.mjs';
import Text            from '../../core/Text.mjs';
import CSS__Progress   from '../CSS__Progress.mjs';
import CSS__Typography from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__Progress extends Web_Component {
    load_attributes() {
        this.css_progress   = new CSS__Progress  (this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'progress-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Progress Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Basic Progress
        let h_basic    = new H({ level: 2, value: 'Basic Progress' })
        let basic_prog = new Div({ class: 'progress' }).add_elements(new Div({ class: 'progress-bar', style: 'width: 25%', value: '25%' }))

        // Progress with Label
        let h_label    = new H({ level: 2, value: 'Progress with Label' })
        let label_prog = new Div({ class: 'progress progress-lg' }).add_elements(new Div({ class: 'progress-bar', style: 'width: 50%', value: '50% Complete' }))

        // Multiple Bars
        let h_multiple = new H({ level: 2, value: 'Multiple Progress Bars' })
        let multi_prog = new Div({ class: 'progress' }).add_elements(new Div({ class: 'progress-bar'           , style: 'width: 15%', value: '15%' }),
                                                                     new Div({ class: 'progress-bar bg-success'  , style: 'width: 30%', value: '30%' }),
                                                                     new Div({ class: 'progress-bar bg-info'     , style: 'width: 20%', value: '20%' }))

        // Striped Bars
        let h_striped    = new H({ level: 2, value: 'Striped Progress' })
        let striped_prog = new Div({ class: 'progress' }).add_elements(new Div({ class: 'progress-bar progress-bar-striped', style: 'width: 40%', value: '40%' }))

        // Animated Striped
        let h_animated    = new H({ level: 2, value: 'Animated Striped Progress' })
        let animated_prog = new Div({ class: 'progress' }).add_elements(new Div({ class: 'progress-bar progress-bar-striped progress-bar-animated', style: 'width: 75%', value: '75%' }))

        // Different Heights
        let h_heights = new H({ level: 2, value: 'Different Heights' })
        let sm_prog   = new Div({ class: 'progress progress-sm' }).add_elements(new Div({ class: 'progress-bar', style: 'width: 25%', value: '25%' }))
        let def_prog  = new Div({ class: 'progress'             }).add_elements(         new Div({ class: 'progress-bar', style: 'width: 50%', value: '50%' }))
        let lg_prog   = new Div({ class: 'progress progress-lg' }).add_elements(new Div({ class: 'progress-bar', style: 'width: 75%', value: '75%' }))

        // Contextual Alternatives
        let h_contexts = new H({ level: 2, value: 'Contextual Alternatives' })
        let ctx_prog1  = new Div({ class: 'progress' }).add_elements(new Div({ class: 'progress-bar progress-bar-success', style: 'width: 25%', value: 'Success' }))
        let ctx_prog2  = new Div({ class: 'progress' }).add_elements(new Div({ class: 'progress-bar progress-bar-info'   , style: 'width: 50%', value: 'Info' }))
        let ctx_prog3  = new Div({ class: 'progress' }).add_elements(new Div({ class: 'progress-bar progress-bar-warning', style: 'width: 75%', value: 'Warning' }))
        let ctx_prog4  = new Div({ class: 'progress' }).add_elements(new Div({ class: 'progress-bar progress-bar-error'  , style: 'width: 100%', value: 'Error' }))

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_basic, basic_prog,
            h_label, label_prog,
            h_multiple, multi_prog,
            h_striped, striped_prog,
            h_animated, animated_prog,
            h_heights, sm_prog, def_prog, lg_prog,
            h_contexts, ctx_prog1, ctx_prog2, ctx_prog3, ctx_prog4
        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_progress   .apply_framework()
            this.css_typography .apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Progress.define()