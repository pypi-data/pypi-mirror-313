import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__CBR__Main_Page                       from '../../../js/cbr/main-page/WebC__CBR__Main_Page.mjs'
import { setup_mock_responses, set_mock_response ,
          } from '../../../js/testing/Mock_API__Data.mjs'
import CBR_Events from "../../../js/cbr/CBR_Events.mjs";

const { module, test , only, skip} = QUnit

module('WebC__CBR__Main_Page', hooks => {
    let target_div
    let main_page

    hooks.before(async () => {
        setup_mock_responses()

        target_div = WebC__Target_Div.add_to_body()
        main_page = await target_div.append_child(WebC__CBR__Main_Page)
        await main_page.wait_for__component_ready()
    })

    hooks.after(() => {
        main_page.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(main_page.tagName.toLowerCase()         , 'webc-cbr-main-page'    , 'Has correct tag name'     )
        assert.equal(main_page.constructor.element_name      , 'webc-cbr-main-page'    , 'Has correct element name' )
        assert.equal(main_page.constructor.name              , 'WebC__CBR__Main_Page'  , 'Has correct class name'   )

        assert.ok(main_page.shadowRoot                                                 , 'Has shadow root'          )
        assert.ok(main_page.routeContent                                              , 'Has route content'        )
        assert.ok(main_page.routeHandler                                              , 'Has route handler'        )
        assert.ok(main_page instanceof Web_Component                                   , 'Extends Web_Component'    )
    })

    test('route handler initialization', assert => {
        assert.equal(main_page.routeHandler.base_path       , main_page.base_path     , 'Sets handler base path'  )
    })

    test('handles menu toggle events', async assert => {
        const layout_col = main_page.query_selector('#layout-col-left')
        const left_footer = main_page.query_selector('#left-footer')
        main_page.raise_event_global(CBR_Events.CBR__UI__LEFT_MENU_TOGGLE, { minimized: false })            // make sure we are not minimised

        assert.ok(layout_col.classList.contains('w-250px')                            , 'Initially expanded'       )
        assert.notOk(layout_col.classList.contains('w-50px')                          , 'Not minimized'           )

        main_page.raise_event_global(CBR_Events.CBR__UI__LEFT_MENU_TOGGLE, { minimized: true })

        assert.ok(layout_col.classList.contains('w-50px')                             , 'Minimizes correctly'      )
        assert.notOk(layout_col.classList.contains('w-250px')                         , 'Removes expanded class'   )
        //assert.notOk(left_footer.style.display
        assert.ok(left_footer.is_hidden()                                            ,  'Hides footer'            )

        main_page.raise_event_global(CBR_Events.CBR__UI__LEFT_MENU_TOGGLE, { minimized: false })
        assert.ok(layout_col.classList.contains('w-250px')                            , 'Expands correctly'        )
        assert.notOk(layout_col.classList.contains('w-50px')                          , 'Removes minimized class' )
        assert.ok(left_footer.is_visible()                                            ,  'Hides footer'            )
    })

    test('extracts base path and version', assert => {
        // Test with full path
        window.history.pushState({}, '', '/ui/dev/dashboard')
        main_page.extract_base_path_and_version()
        assert.equal(main_page.version                      , 'dev'                   , 'Extracts version'         )
        assert.equal(main_page.base_path                    , '/ui/dev'               , 'Sets correct base path'   )

        window.history.pushState({}, '', '/ui')                 // Test with minimal path
        main_page.extract_base_path_and_version()

        assert.equal(main_page.version                      , 'latest'                , 'Uses default version'     )
        assert.equal(main_page.base_path                    , '/ui/latest'            , 'Sets default base path'   )

        window.history.pushState({}, '', '/ui/v1.2.3')                 // Test with path with version
        main_page.extract_base_path_and_version()

        assert.equal(main_page.version                      , 'v1.2.3'                , 'Uses default version'     )
        assert.equal(main_page.base_path                    , '/ui/v1.2.3'            , 'Sets default base path'   )
    })

    test('creates correct HTML structure', assert => {
        const main_container = main_page.query_selector('#main-page')

        assert.ok(main_container                                                      , 'Creates main container'   )
        assert.ok(main_page.query_selector('#top-banner')                            , 'Has banner section'       )
        assert.ok(main_page.query_selector('#left-menu')                             , 'Has left menu'           )
        assert.ok(main_page.query_selector('#content')                               , 'Has content section'      )
        assert.ok(main_page.query_selector('#left-footer')                           , 'Has footer section'       )
    })

    test('initializes web components', assert => {
        assert.ok(main_page.query_selector('webc-cbr-top-banner')                    , 'Adds top banner'          )
        assert.ok(main_page.query_selector('webc-cbr-left-menu')                     , 'Adds left menu'          )
    })


    test('layout structure', assert => {
        const layout = main_page.query_selector('#main-page')

        assert.ok(layout.classList.contains('h-100vh')                               , 'Full height layout'       )
        assert.ok(layout.classList.contains('p-0')                                   , 'No padding'               )

        const content_row = main_page.query_selector('#layout-col-left').parentElement
        assert.ok(content_row.classList.contains('flex-fill')                        , 'Flexible content row'     )
        assert.ok(content_row.classList.contains('flex-nowrap')                      , 'No wrapping'             )
    })
})