import Web_Component   from '../../core/Web_Component.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import HR              from '../../core/HR.mjs';
import Text            from '../../core/Text.mjs';
import CSS__Grid       from '../grid/CSS__Grid.mjs';
import CSS__Typography from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__Grid extends Web_Component {
    load_attributes() {
        this.css_grid = new CSS__Grid(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    css_rules__demo() {
        return {
            "#grid-demo .col, #grid-demo [class*='col-']": {
                backgroundColor: "#1a73e8",
                color: "#ffffff",
                padding: "1rem",
                marginBottom: "1rem",
                textAlign: "center",
                borderRadius: "0.25rem"
            },
            "#grid-demo .col-alt": {
                backgroundColor: "#5f6368"
            },
            "#grid-demo .col-accent": {
                backgroundColor: "#6200ee"
            },
            "#grid-demo .alignment-box": {
                minHeight: "200px",
                backgroundColor: "rgba(0,0,0,0.05)",
                borderRadius: "0.25rem",
                marginBottom: "1rem"
            }
        }
    }

    render() {
        let div_root = new Div({ id: 'grid-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Grid System Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Basic Grid
        let h_basic = new H({ level: 2, value: 'Basic Grid' })
        let basic_grid = new Div({ class: 'container' }).add_elements(
            new Div({ class: 'row' }).add_elements(
                new Div({ class: 'col-4', value: 'Column 1' }),
                new Div({ class: 'col-4 col-alt', value: 'Column 2' }),
                new Div({ class: 'col-4', value: 'Column 3' })
            )
        )

        // Responsive Grid
        let h_responsive = new H({ level: 2, value: 'Responsive Grid' })
        let responsive_grid = new Div({ class: 'container' }).add_elements(
            new Div({ class: 'row' }).add_elements(
                new Div({ class: 'col-12 col-md-6 col-lg-3', value: 'Col 1' }),
                new Div({ class: 'col-12 col-md-6 col-lg-3 col-alt', value: 'Col 2' }),
                new Div({ class: 'col-12 col-md-6 col-lg-3 col-accent', value: 'Col 3' }),
                new Div({ class: 'col-12 col-md-6 col-lg-3', value: 'Col 4' })
            )
        )

        // Auto-width Columns
        let h_auto = new H({ level: 2, value: 'Auto-width Columns' })
        let auto_grid = new Div({ class: 'container' }).add_elements(
            new Div({ class: 'row' }).add_elements(
                new Div({ class: 'col', value: 'Auto Column' }),
                new Div({ class: 'col col-alt', value: 'Auto Column' }),
                new Div({ class: 'col col-accent', value: 'Auto Column' })
            )
        )

        // Mixed Column Sizes
        let h_mixed = new H({ level: 2, value: 'Mixed Column Sizes' })
        let mixed_grid = new Div({ class: 'container' }).add_elements(
            new Div({ class: 'row' }).add_elements(
                new Div({ class: 'col-6', value: 'Half Width' }),
                new Div({ class: 'col-3 col-alt', value: 'Quarter' }),
                new Div({ class: 'col-3 col-accent', value: 'Quarter' })
            )
        )

        // Alignment
        let h_alignment = new H({ level: 2, value: 'Alignment' })
        let alignment_grid = new Div({ class: 'container' }).add_elements(
            new Div({ class: 'row justify-center align-center alignment-box' }).add_elements(
                new Div({ class: 'col-4', value: 'Centered Content' })
            )
        )

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_basic, basic_grid,
            h_responsive, responsive_grid,
            h_auto, auto_grid,
            h_mixed, mixed_grid,
            h_alignment, alignment_grid
        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_grid.apply_framework()
            this.css_typography.apply_framework()
            this.add_css_rules(this.css_rules__demo())
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Grid.define()