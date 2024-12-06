import Div from "../../core/Div.mjs"
import A from "../../core/A.mjs"
import Icon from "../icons/Icon.mjs"

export default class Left_Menu extends Div {
    constructor({id, menu_items, ...kwargs}={}) {
        kwargs.class = `side-menu ${kwargs.class || ''}`
        super({id, ...kwargs})

        this.menu_items = menu_items || []
        this.render_menu()
    }

    render_menu() {
        this.menu_items.forEach(item => {
            const menuItem = new Div({ class: 'side-menu-item' })
            const link = new A({
                class: 'side-menu-link',
                attributes: item
            })

            const icon = new Icon({
                icon: item.icon,
                class: 'side-menu-icon icon-md',
                color: 'muted'
            })

            const text = new Div({
                class: 'side-menu-text',
                value: item.label
            })
            // if (window.location.pathname === item.href) {
            //     menuItem.add_class('active')
            // }

            link.add_elements(icon, text)
            menuItem.add_element(link)
            this.add_element(menuItem)
        })
    }
}