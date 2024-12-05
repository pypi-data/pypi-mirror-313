import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__CBR__Left_Menu                        from '../../../js/cbr/main-page/WebC__CBR__Left_Menu.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'
import CBR_Events                                  from "../../../js/cbr/CBR_Events.mjs";

const { module, test , only} = QUnit

const MOCK_MENU_DATA = {
    menu_items: {
        dashboard: {
            icon          : 'dashboard',
            label         : 'Dashboard',
            web_component : 'WebC__Dashboard'
        },
        files: {
            icon  : 'folder',
            label : 'Files'
        }
    }
}

module('WebC__CBR__Left_Menu', hooks => {
    let target_div
    let left_menu

    hooks.beforeEach(async () => {
        setup_mock_responses()
        set_mock_response('/api/user-data/ui/left-menu', 'GET', MOCK_MENU_DATA)

        target_div = WebC__Target_Div.add_to_body()
        left_menu  = await target_div.append_child(WebC__CBR__Left_Menu)
        await left_menu.wait_for__component_ready()
    })

    hooks.afterEach(() => {
        left_menu.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(left_menu.tagName.toLowerCase()         , 'webc-cbr-left-menu'    , 'Has correct tag name'      )
        assert.equal(left_menu.constructor.element_name      , 'webc-cbr-left-menu'    , 'Has correct element name'  )
        assert.equal(left_menu.constructor.name              , 'WebC__CBR__Left_Menu'  , 'Has correct class name'    )

        assert.ok(left_menu.shadowRoot                                                 , 'Has shadow root'           )
        assert.ok(left_menu.api_invoke                                                 , 'Has API invoke'            )
        assert.ok(left_menu instanceof Web_Component                                   , 'Extends Web_Component'     )
        assert.ok(left_menu instanceof HTMLElement                                     , 'Is HTML Element'           )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = left_menu.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                   , 'Has CSS rules'             )
        assert.ok(css_rules['.left-menu-main']                                        , 'Has main menu styles'      )
        assert.ok(css_rules['.left-menu-minimized']                                   , 'Has minimized styles'      )
    })

    test('handles menu toggle events', async assert => {
        const main_menu = left_menu.div__left_menu_main

        assert.notOk(main_menu.classList.contains('left-menu-minimized')              , 'Initially not minimized'   )

        left_menu.raise_event_global(CBR_Events.CBR__UI__LEFT_MENU_TOGGLE, { minimized: true })

        assert.ok(main_menu.classList.contains('left-menu-minimized')                 , 'Minimizes on event'        )

        left_menu.raise_event_global(CBR_Events.CBR__UI__LEFT_MENU_TOGGLE,{ minimized: false })
        assert.notOk(main_menu.classList.contains('left-menu-minimized')              , 'Expands on event'          )
    })

    test('generates correct menu items', assert => {
        const menu_items = left_menu.menu_items()

        assert.equal(menu_items.length                       , 2                       , 'Creates correct number of items')

        const dashboard_item = menu_items[0]
        assert.equal(dashboard_item.icon                     , 'dashboard'             , 'Has correct icon'          )
        assert.equal(dashboard_item.label                    , 'Dashboard'             , 'Has correct label'         )
        assert.equal(dashboard_item['data-target-type']      , 'web_component'         , 'Has correct target type'   )
        assert.equal(dashboard_item['data-component']        , 'WebC__Dashboard'       , 'Has component data'        )

        const files_item = menu_items[1]
        assert.equal(files_item['data-target-type']          , 'link'                  , 'Regular link type'         )
        assert.ok(files_item.href.includes('files/index')                              , 'Has correct link path'     )

        left_menu.menu_data = null
        assert.deepEqual(left_menu.menu_items()              , []                       , 'Returns empty array when menu_data is empty')
    })

    test('handles API errors gracefully', async assert => {
        set_mock_response('/api/user-data/ui/left-menu', 'GET', null)

        await left_menu.fetch_menu_items()
        const menu_items = left_menu.menu_items()

        assert.deepEqual(menu_items                         , []                       , 'Returns empty array on error')


    })

    test('respects base path configuration', async (assert) => {
        const custom_base = '/custom'
        const custom_menu = WebC__CBR__Left_Menu.create({ base_path: custom_base })
        custom_menu.menu_data = MOCK_MENU_DATA.menu_items

        await custom_menu.connectedCallback()
        const menu_items = custom_menu.menu_items()
        assert.ok(menu_items[0].href.startsWith(custom_base)                          , 'Uses custom base path'     )
        await custom_menu.disconnectedCallback()


    })
    //
    // test('creates correct HTML structure', async assert => {
    //     const main_container = left_menu.query_selector('.left-menu-main')
    //
    //     assert.ok(main_container                                                      , 'Creates main container'    )
    //     assert.ok(main_container.querySelector('webc-cbr-left-logo')                 , 'Includes logo component'   )
    //     assert.ok(main_container.querySelector('webc-resize-button')                 , 'Includes resize button'    )
    //     assert.ok(main_container.querySelector('webc-cbr-important-alert')           , 'Includes alert component' )
    // })

    test('css_rules return correct styles', assert => {
        const rules = left_menu.css_rules()

        assert.deepEqual(rules['.left-menu-main'], {
            transition: "width 0.3s ease-in-out"    ,
            position : "relative"
        }, 'Main menu styles are correct')

        assert.deepEqual(rules['.left-menu-minimized'], {
            width     : "60px"                       ,
            paddingTop: "10px"                       ,
            overflow  : "hidden"
        }, 'Minimized styles are correct')
    })
})