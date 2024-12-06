import Web_Component   from '../../core/Web_Component.mjs';
import Div             from '../../core/Div.mjs';
import Row             from '../grid/Row.mjs';
import H               from '../../core/H.mjs';
import HR              from '../../core/HR.mjs';
import Text            from '../../core/Text.mjs';
import CSS__Grid       from '../grid/CSS__Grid.mjs';
import CSS__Typography from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__Row extends Web_Component {
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
        let container = new Div({ class: 'container' })
        let row1 = new Row()
        row1.add_col({ size: 4, value: 'Column 1' })
        row1.add_col({ size: 4, class: 'col-alt', value: 'Column 2' })
        row1.add_col({ size: 4, value: 'Column 3' })
        container.add_element(row1)

        // Responsive Grid
        let h_responsive = new H({ level: 2, value: 'Responsive Grid' })
        let container2 = new Div({ class: 'container' })
        let row2 = new Row()
        row2.add_col({ class: 'col-12 col-md-6 col-lg-3', value: 'Col 1' })
        row2.add_col({ class: 'col-12 col-md-6 col-lg-3 col-alt', value: 'Col 2' })
        row2.add_col({ class: 'col-12 col-md-6 col-lg-3 col-accent', value: 'Col 3' })
        row2.add_col({ class: 'col-12 col-md-6 col-lg-3', value: 'Col 4' })
        container2.add_element(row2)

        // Auto-width Columns
        let h_auto = new H({ level: 2, value: 'Auto-width Columns' })
        let container3 = new Div({ class: 'container' })
        let row3 = new Row()
        row3.add_col({ value: 'Auto Column' })
        row3.add_col({ class: 'col-alt', value: 'Auto Column' })
        row3.add_col({ class: 'col-accent', value: 'Auto Column' })
        container3.add_element(row3)

        // Mixed Column Sizes
        let h_mixed = new H({ level: 2, value: 'Mixed Column Sizes' })
        let container4 = new Div({ class: 'container' })
        let row4 = new Row()
        row4.add_col({ size: 6, value: 'Half Width' })
        row4.add_col({ size: 3, class: 'col-alt', value: 'Quarter' })
        row4.add_col({ size: 3, class: 'col-accent', value: 'Quarter' })
        container4.add_element(row4)

        // Alignment
        let h_alignment = new H({ level: 2, value: 'Alignment' })
        let container5 = new Div({ class: 'container' })
        let row5 = new Row({ class: 'justify-center align-center alignment-box' })
        row5.add_col({ size: 4, value: 'Centered Content' })
        container5.add_element(row5)

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_basic, container,
            h_responsive, container2,
            h_auto, container3,
            h_mixed, container4,
            h_alignment, container5
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

WebC__CSS__Demo__Row.define()