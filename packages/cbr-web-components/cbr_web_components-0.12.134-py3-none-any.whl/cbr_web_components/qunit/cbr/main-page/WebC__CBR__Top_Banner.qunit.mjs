import WebC__Target_Div     from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component        from '../../../js/core/Web_Component.mjs'
import WebC__CBR__Top_Banner from '../../../js/cbr/main-page/WebC__CBR__Top_Banner.mjs'

const { module, test , only} = QUnit

module('WebC__CBR__Top_Banner', hooks => {
    let target_div
    let top_banner

    hooks.before(async () => {
        target_div  = WebC__Target_Div.add_to_body()
        top_banner  = await target_div.append_child(WebC__CBR__Top_Banner)
        await top_banner.wait_for__component_ready()
    })

    hooks.after(() => {
        top_banner.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(top_banner.tagName.toLowerCase()        , 'webc-cbr-top-banner'    , 'Has correct tag name'     )
        assert.equal(top_banner.constructor.element_name     , 'webc-cbr-top-banner'    , 'Has correct element name' )
        assert.equal(top_banner.constructor.name             , 'WebC__CBR__Top_Banner'  , 'Has correct class name'   )

        assert.ok(top_banner.shadowRoot                                                  , 'Has shadow root'          )
        assert.ok(top_banner instanceof Web_Component                                    , 'Extends Web_Component'    )
        assert.ok(top_banner instanceof HTMLElement                                      , 'Is HTML Element'          )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = top_banner.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                     , 'Has CSS rules'            )
        assert.ok(css_rules['.top-banner']                                              , 'Has banner styles'        )
        assert.ok(css_rules['.menu-icon']                                               , 'Has menu icon styles'     )
        assert.ok(css_rules['.menu-icon:hover']                                         , 'Has hover styles'         )
    })

    test('renders initial layout correctly', assert => {
        const container    = top_banner.query_selector('.top-banner')
        const menu_icon    = top_banner.query_selector('.menu-icon')
        const user_session = top_banner.query_selector('.user-session')

        assert.ok(container                                                             , 'Container exists'         )
        assert.ok(menu_icon                                                             , 'Menu icon exists'         )
        assert.ok(user_session                                                          , 'User session exists'      )

        assert.ok(menu_icon.classList.contains('icon-lg')                               , 'Icon has correct size'    )
        assert.equal(menu_icon.textContent                    , '☰'                     , 'Shows menu icon'          )
    })

    test('handles menu icon click', async assert => {
        assert.expect(3)

        top_banner.addEventListener('toggle-menu', event => {
            assert.ok(event.detail                                                      , 'Event has detail'         )
            assert.equal(event.detail.opened                   , true                   , 'Sets opened state'        )
            assert.ok(event.bubbles && event.composed                                   , 'Event properly configured')
        }, {only: true})

        const menu_icon = top_banner.query_selector('.menu-icon')
        menu_icon.click()
    })


    test('adds web components correctly', async assert => {
        const user_session = top_banner.query_selector('webc-cbr-user-session')
        assert.ok(user_session                                                          , 'User session component added')
    })
})