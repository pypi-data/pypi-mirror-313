import "../../prototypes/html-elements.mjs"
import "../../prototypes/global-event-registry.mjs"

import Web_Component             from '../../core/Web_Component.mjs'
import Layout                    from '../../css/grid/Layout.mjs'
import CSS__Alerts               from "../../css/CSS__Alerts.mjs"
import CSS__Grid                 from '../../css/grid/CSS__Grid.mjs'
import CSS__Typography           from '../../css/CSS__Typography.mjs'
import CSS__Side_Menu            from "../../css/menus/CSS__Side_Menu.mjs"
import CSS__CBR__Layout__Default from "./CSS__CBR__Layout__Default.mjs";
import CBR__Left_Footer          from "../elements/CBR__Left_Footer.mjs"
import CBR__Top_Banner           from "../elements/CBR__Top_Banner.mjs"
import CBR__Content__Placeholder from "../elements/CBR__Content__Placeholder.mjs"
import CBR__Route__Handler       from "../router/CBR__Route__Handler.mjs"
import CBR__Route__Content       from "../router/CBR__Route__Content.mjs"
import API__Invoke               from "../../data/API__Invoke.mjs";
import WebC__CBR__Left_Menu      from "../main-page/WebC__CBR__Left_Menu.mjs";
import CBR_Events                from "../CBR_Events.mjs";
import WebC__CBR__Top_Banner     from "./WebC__CBR__Top_Banner.mjs";

export default class WebC__CBR__Main_Page extends Web_Component {
    constructor() {
        super()
        this.routeContent   = new CBR__Route__Content()
        this.routeHandler   = new CBR__Route__Handler(this)
        this.api_invoke     = new API__Invoke()
        this.base_path      = '/'
    }

    // Web_Component overrides

    apply_css() {
        new CSS__Alerts              (this).apply_framework()
        new CSS__Grid                (this).apply_framework()
        new CSS__Typography          (this).apply_framework()
        new CSS__Side_Menu           (this).apply_framework()
        new CSS__CBR__Layout__Default(this).apply_framework()

        this.add_css_rules(CBR__Top_Banner          .css_rules())
        this.add_css_rules(CBR__Left_Footer         .css_rules())
        this.add_css_rules(CBR__Content__Placeholder.css_rules())
    }

    add_web_components() {
        this.add_web_component_to('#top-banner', WebC__CBR__Top_Banner, {})
        this.add_web_component_to('#left-menu' , WebC__CBR__Left_Menu , {base_path : this.base_path})

        setTimeout(() => { window.dispatchEvent(new Event('resize')) }, 1)
    }

    add_event_listeners() {
       this.add_window_event_listener(CBR_Events.CBR__UI__LEFT_MENU_TOGGLE , this.on_left_menu_toggle   )
    }

    load_data() {
        this.extract_base_path_and_version()
    }

    async component_ready() {
        this.routeHandler.set_base_path(this.base_path)
        await this.handle_first_route()
    }
    // EVENT HANDLERS

    on_left_menu_toggle(event) {
        const minimized   = event.detail.minimized
        const layout_col  = this.query_selector('#layout-col-left' )
        const left_footer = this.query_selector('#left-footer'     )
        if (minimized) {
            layout_col .add_class('w-50px' ).remove_class('w-250px')
            left_footer.hide()
        } else {
            layout_col .add_class('w-250px').remove_class('w-50px' )
            left_footer.show()
        }
   }



    async render() {
        super.render()
    }

    async handle_first_route() {
        //await this.routeHandler.handle_route(window.location.pathname)          // todo refactor to new menu structure (where the menu data is dynamically fetched )
    }

    extract_base_path_and_version() {
        const path_parts = window.location.pathname.split('/');

        if (path_parts.length >= 2 && path_parts[2]) {
            this.version = path_parts[2];             // Version is the second part of the path (e.g., dev, prod, v0.1.100)
        } else {
            this.version = 'latest';                 // Default version
        }

        this.base_path = `/ui/${this.version}`;      // Use this.version
    }

    html() {
        let layout, row_banner, row_content

        layout      = new Layout({ id:'main-page', class: 'h-100vh p-0' })
        row_banner  = layout.add_row()
        row_content = layout.add_row({class: 'flex-fill flex-nowrap'                           })

        row_banner .add_col({ id: 'top-banner'      , class: 'h-75px'                               })
        row_content.add_col({ id: 'layout-col-left' , class: 'w-250px flex-column d-flex'           })
                   .add_col({ id: 'left-menu'       , class: 'flex-fill bg-white'                   }).parent()
                   .add_col({ id: 'left-footer'     , class: 'h-75px bg-light-gray'                 })
        row_content.add_col({ id: 'content'         , class: 'd-flex bg-light-gray m-1'             })

        layout     .with_id('left-footer').add_element(new CBR__Left_Footer         ({version:this.version}))
        //layout     .with_id('top-banner' ).add_element(new CBR__Top_Banner          ()                      )
        layout     .with_id('content'    ).add_element(new CBR__Content__Placeholder()                      )

        return layout.html()

    }
}


WebC__CBR__Main_Page.define()