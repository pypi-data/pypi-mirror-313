import Web_Component    from '../../core/Web_Component.mjs';
import A                from '../../core/A.mjs';
import Div              from '../../core/Div.mjs';
import H                from '../../core/H.mjs';
import HR               from '../../core/HR.mjs';
import Text             from '../../core/Text.mjs';
import CSS__List_Groups from '../CSS__List_Groups.mjs';
import CSS__Typography  from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__List_Groups extends Web_Component {
    load_attributes() {
        this.css_list_groups = new CSS__List_Groups(this)
        this.css_typography  = new CSS__Typography(this)
        this.apply_css       = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'list-groups-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'List Groups Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Basic List Group
        let h_basic = new H({ level: 2, value: 'Basic List Group' })
        let basic_list = new Div({ class: 'list-group' }).add_elements(
            new Div({ class: 'list-group-item', value: 'An item' }),
            new Div({ class: 'list-group-item', value: 'A second item' }),
            new Div({ class: 'list-group-item', value: 'A third item' }),
            new Div({ class: 'list-group-item', value: 'A fourth item' }),
            new Div({ class: 'list-group-item', value: 'And a fifth one' })
        )

        // Active/Disabled States
        let h_states = new H({ level: 2, value: 'Active and Disabled States' })
        let states_list = new Div({ class: 'list-group' }).add_elements(
            new Div({ class: 'list-group-item active', value: 'Active item' }),
            new Div({ class: 'list-group-item', value: 'Regular item' }),
            new Div({ class: 'list-group-item disabled', value: 'Disabled item' }),
            new Div({ class: 'list-group-item', value: 'Another regular item' })
        )

        // Actionable Items
        let h_actions = new H({ level: 2, value: 'Actionable Items' })
        let action_list = new Div({ class: 'list-group' }).add_elements(
            new A({ href: '#', class: 'list-group-item list-group-item-action active', value: 'Active link' }),
            new A({ href: '#', class: 'list-group-item list-group-item-action', value: 'Regular link' }),
            new A({ href: '#', class: 'list-group-item list-group-item-action', value: 'Another link' })
        )

        // Contextual Classes
        let h_contextual = new H({ level: 2, value: 'Contextual Classes' })
        let contextual_list = new Div({ class: 'list-group' }).add_elements(
            new Div({ class: 'list-group-item list-group-item-primary', value: 'Primary list item' }),
            new Div({ class: 'list-group-item list-group-item-secondary', value: 'Secondary list item' }),
            new Div({ class: 'list-group-item list-group-item-success', value: 'Success list item' }),
            new Div({ class: 'list-group-item list-group-item-error', value: 'Error list item' }),
            new Div({ class: 'list-group-item list-group-item-warning', value: 'Warning list item' }),
            new Div({ class: 'list-group-item list-group-item-info', value: 'Info list item' })
        )

        // Horizontal List Group
        let h_horizontal = new H({ level: 2, value: 'Horizontal List Group' })
        let horizontal_list = new Div({ class: 'list-group list-group-horizontal' }).add_elements(
            new Div({ class: 'list-group-item', value: 'First item' }),
            new Div({ class: 'list-group-item', value: 'Second item' }),
            new Div({ class: 'list-group-item', value: 'Third item' })
        )

        // Flush List Group
        let h_flush = new H({ level: 2, value: 'Flush List Group' })
        let flush_list = new Div({ class: 'list-group list-group-flush' }).add_elements(
            new Div({ class: 'list-group-item', value: 'Flush item one' }),
            new Div({ class: 'list-group-item', value: 'Flush item two' }),
            new Div({ class: 'list-group-item', value: 'Flush item three' })
        )

        // Numbered List Group
        let h_numbered = new H({ level: 2, value: 'Numbered List Group' })
        let numbered_list = new Div({ class: 'list-group list-group-numbered' }).add_elements(
            new Div({ class: 'list-group-item', value: 'First numbered item' }),
            new Div({ class: 'list-group-item', value: 'Second numbered item' }),
            new Div({ class: 'list-group-item', value: 'Third numbered item' })
        )

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_basic, basic_list,
            h_states, states_list,
            h_actions, action_list,
            h_contextual, contextual_list,
            h_horizontal, horizontal_list,
            h_flush, flush_list,
            h_numbered, numbered_list
        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_list_groups.apply_framework()
            this.css_typography.apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__List_Groups.define()