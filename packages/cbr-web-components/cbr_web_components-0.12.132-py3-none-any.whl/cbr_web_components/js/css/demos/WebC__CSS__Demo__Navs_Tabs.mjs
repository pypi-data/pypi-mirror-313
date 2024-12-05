import Web_Component from '../../core/Web_Component.mjs';
import A from '../../core/A.mjs';
import Button from '../../core/Button.mjs';
import Div from '../../core/Div.mjs';
import H from '../../core/H.mjs';
import HR from '../../core/HR.mjs';
import Nav from '../../core/Nav.mjs';
import Text from '../../core/Text.mjs';
import CSS__NavsTabs from '../CSS__Navs_Tabs.mjs';
import CSS__Typography from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__Navs_Tabs extends Web_Component {
    load_attributes() {
        this.css_navs_tabs = new CSS__NavsTabs(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'navs-tabs-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Navs & Tabs Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Basic Nav
        let h_basic = new H({ level: 2, value: 'Basic Nav' })
        let basic_nav = new Nav({ class: 'nav' }).add_elements(
            new A({ class: 'nav-link active', href: '#', value: 'Active' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link disabled', href: '#', value: 'Disabled' })
        )

        // Tabs
        let h_tabs = new H({ level: 2, value: 'Tabs' })
        let tabs_nav = new Nav({ class: 'nav nav-tabs' }).add_elements(
            new A({ class: 'nav-link active', href: '#', value: 'Active' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link disabled', href: '#', value: 'Disabled' })
        )

        // Pills
        let h_pills = new H({ level: 2, value: 'Pills' })
        let pills_nav = new Nav({ class: 'nav nav-pills' }).add_elements(
            new A({ class: 'nav-link active', href: '#', value: 'Active' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link disabled', href: '#', value: 'Disabled' })
        )

        // Fill
        let h_fill = new H({ level: 2, value: 'Fill' })
        let fill_nav = new Nav({ class: 'nav nav-pills nav-fill' }).add_elements(
            new A({ class: 'nav-link active', href: '#', value: 'Active' }),
            new A({ class: 'nav-link', href: '#', value: 'Much longer nav link' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link disabled', href: '#', value: 'Disabled' })
        )

        // Justified
        let h_justified = new H({ level: 2, value: 'Justified' })
        let justified_nav = new Nav({ class: 'nav nav-pills nav-justified' }).add_elements(
            new A({ class: 'nav-link active', href: '#', value: 'Active' }),
            new A({ class: 'nav-link', href: '#', value: 'Much longer nav link' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link disabled', href: '#', value: 'Disabled' })
        )

        // Vertical
        let h_vertical = new H({ level: 2, value: 'Vertical' })
        let vertical_nav = new Nav({ class: 'nav nav-pills nav-vertical' }).add_elements(
            new A({ class: 'nav-link active', href: '#', value: 'Active' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link disabled', href: '#', value: 'Disabled' })
        )

        // Underline style
        let h_underline = new H({ level: 2, value: 'Underline Style' })
        let underline_nav = new Nav({ class: 'nav nav-underline' }).add_elements(
            new A({ class: 'nav-link active', href: '#', value: 'Active' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link', href: '#', value: 'Link' }),
            new A({ class: 'nav-link disabled', href: '#', value: 'Disabled' })
        )

        // Tab panels example
        let h_tab_panels = new H({ level: 2, value: 'Tab Panels' })
        let tab_panels = new Div({ class: 'tabs-example' }).add_elements(
            new Nav({ class: 'nav nav-tabs' }).add_elements(
                new A({ class: 'nav-link active', href: '#home', value: 'Home' }),
                new A({ class: 'nav-link', href: '#profile', value: 'Profile' }),
                new A({ class: 'nav-link', href: '#contact', value: 'Contact' })
            ),
            new Div({ class: 'tab-content' }).add_elements(
                new Div({ class: 'tab-pane active', id: 'home' }).add_elements(
                    new Text({ value: 'This is the home tab content panel.' })
                ),
                new Div({ class: 'tab-pane', id: 'profile' }).add_elements(
                    new Text({ value: 'This is the profile tab content panel.' })
                ),
                new Div({ class: 'tab-pane', id: 'contact' }).add_elements(
                    new Text({ value: 'This is the contact tab content panel.' })
                )
            )
        )

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_basic, basic_nav,
            h_tabs, tabs_nav,
            h_pills, pills_nav,
            h_fill, fill_nav,
            h_justified, justified_nav,
            h_vertical, vertical_nav,
            h_underline, underline_nav,
            h_tab_panels, tab_panels
        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_navs_tabs.apply_framework()
            this.css_typography.apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Navs_Tabs.define()