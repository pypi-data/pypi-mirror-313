import Web_Component    from '../../core/Web_Component.mjs';
import Nav              from '../../core/Nav.mjs';
import Ol               from '../../core/Ol.mjs';
import Li               from '../../core/Li.mjs';
import A                from '../../core/A.mjs';
import Div              from '../../core/Div.mjs';
import H                from '../../core/H.mjs';
import HR               from '../../core/HR.mjs';
import Text             from '../../core/Text.mjs';
import CSS__Breadcrumbs from '../CSS__Breadcrumbs.mjs';
import CSS__Typography from "../CSS__Typography.mjs";

export default class WebC__CSS__Demo__Breadcrumbs extends Web_Component {
    load_attributes() {
        this.css_breadcrumbs = new CSS__Breadcrumbs(this)
        this.css_typography  = new CSS__Typography(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'breadcrumbs-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Breadcrumbs Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Simple Breadcrumb
        let h_simple = new H({ level: 2, value: 'Simple Breadcrumb' })
        let simple_breadcrumb = [
            new Nav({ class: 'nav-breadcrumb', attributes: { 'aria-label': 'breadcrumb' } }).add_elements(
                new Ol({ class: 'nav-breadcrumb-list' }).add_elements(
                    new Li({ class: 'nav-breadcrumb-item nav-breadcrumb-item-current',
                           attributes: { 'aria-current': 'page' } }).add_elements(
                        new Text({ value: 'Home' })
                    )
                )
            )
        ]

        // Two-Level Breadcrumb
        let h_two_level = new H({ level: 2, value: 'Two-Level Breadcrumb' })
        let two_level_breadcrumb = [
            new Nav({ class: 'nav-breadcrumb', attributes: { 'aria-label': 'breadcrumb' } }).add_elements(
                new Ol({ class: 'nav-breadcrumb-list' }).add_elements(
                    new Li({ class: 'nav-breadcrumb-item' }).add_elements(
                        new A({ class: 'nav-breadcrumb-link', href: '#', value: 'Home' })
                    ),
                    new Li({ class: 'nav-breadcrumb-item nav-breadcrumb-item-current',
                           attributes: { 'aria-current': 'page' } }).add_elements(
                        new Text({ value: 'Library' })
                    )
                )
            )
        ]

        // Three-Level Breadcrumb
        let h_three_level = new H({ level: 2, value: 'Three-Level Breadcrumb' })
        let three_level_breadcrumb = [
            new Nav({ class: 'nav-breadcrumb', attributes: { 'aria-label': 'breadcrumb' } }).add_elements(
                new Ol({ class: 'nav-breadcrumb-list' }).add_elements(
                    new Li({ class: 'nav-breadcrumb-item' }).add_elements(
                        new A({ class: 'nav-breadcrumb-link', href: '#', value: 'Home' })
                    ),
                    new Li({ class: 'nav-breadcrumb-item' }).add_elements(
                        new A({ class: 'nav-breadcrumb-link', href: '#', value: 'Library' })
                    ),
                    new Li({ class: 'nav-breadcrumb-item nav-breadcrumb-item-current',
                           attributes: { 'aria-current': 'page' } }).add_elements(
                        new Text({ value: 'Data' })
                    )
                )
            )
        ]

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_simple, ...simple_breadcrumb,
            h_two_level, ...two_level_breadcrumb,
            h_three_level, ...three_level_breadcrumb
        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_breadcrumbs.apply_framework()
            this.css_typography .apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Breadcrumbs.define()