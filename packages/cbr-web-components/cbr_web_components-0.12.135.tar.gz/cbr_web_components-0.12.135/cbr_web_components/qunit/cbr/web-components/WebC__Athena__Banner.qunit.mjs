import WebC__Target_Div     from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component        from '../../../js/core/Web_Component.mjs'
import WebC__Athena__Banner from '../../../js/cbr/web-components/WebC__Athena__Banner.mjs'
import CBR__Paths           from "../../../js/cbr/CBR__Paths.mjs";

import {
    add_padding_to_string, add_mock_markdown_path ,
    MOCK_RAW_HTML, MOCK_MARKDOWN_METADATA
} from '../../../js/testing/Mock_API__Data.mjs'



const { module, test, only } = QUnit

module('WebC__Athena__Banner', hooks => {
    let target_div
    let banner

    hooks.before(async () => {
        add_mock_markdown_path(CBR__Paths.FILE__CONTENT__SITE__ATHENA__BANNER)

        target_div = WebC__Target_Div.add_to_body()
        banner     = await target_div.append_child(WebC__Athena__Banner)
        await banner.wait_for__component_ready()
    })

    hooks.after(() => {
        banner    .remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(banner.tagName.toLowerCase()        , 'webc-athena-banner'   , 'Has correct tag name'     )        // Test component registration and naming
        assert.equal(banner.constructor.element_name     , 'webc-athena-banner'   , 'Has correct element name' )
        assert.equal(banner.constructor.name             , 'WebC__Athena__Banner' , 'Has correct class name'   )

        assert.ok(banner.shadowRoot                                               , 'Has shadow root'          )        // Test shadow DOM// Test component structure and composition
        assert.ok(banner.api_markdown                                             , 'Has API__Markdown'        )

        assert.equal(typeof banner.connectedCallback     , 'function'             , 'Has Web Component methods')        // Test inheritance through method presence
        assert.equal(typeof banner.load_data             , 'function'             , 'Has Banner methods'       )

        assert.ok(banner instanceof Web_Component                                 , 'Extends Web_Component'    )        // Test inheritance through prototype chain
        assert.ok(banner instanceof HTMLElement                                   , 'Is HTML Element'          )
        assert.ok(banner.api_markdown                                             , 'Has API__Markdown'        )
    })

    test('loads and applies CSS frameworks', assert => {
        // Assert CSS frameworks are loaded
        const css_rules = banner.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0             , 'Has CSS rules'           )
        assert.ok(css_rules['.card']                            , 'Has card styles'         )
        assert.ok(css_rules['.card-body']                       , 'Has card body styles'    )
        assert.ok(css_rules['.card-title']                      , 'Has card title styles'   )
    })

    test('renders content correctly', async assert => {
        // Assert DOM structure
        const card       = banner.query_selector('.card'      )
        const card_body  = banner.query_selector('.card-body' )
        const title      = banner.query_selector('.card-title')
        const content    = banner.query_selector('.card-text' )

        assert.ok(card         , 'Card exists'                )
        assert.ok(card_body    , 'Card body exists'           )
        assert.ok(title        , 'Title exists'               )
        assert.ok(content      , 'Content exists'             )

        // Assert content
        assert.equal(title  .textContent, MOCK_MARKDOWN_METADATA.title                   , 'Correct title'  )
        assert.ok  (content.innerHTML.includes(add_padding_to_string(MOCK_RAW_HTML,12))  , 'Correct content')
    })

    test('updates content dynamically', async assert => {

        // Act - Update content
        banner.content = {
            metadata : { title: 'New Title' },
            html    : '<p>New content</p>'
        }
        banner.render()

        // Assert
        const title   = banner.query_selector('.card-title').textContent
        const content = banner.query_selector('.card-text' ).innerHTML.trim()

        assert.equal(title  , 'New Title'              , 'Title updated'            )
        assert.equal(content, '<p>New content</p>'     , 'Content updated'         )
    })

    test('handles empty content', async assert => {
        // Arrange - set empty content
        banner.content = null
        banner.render()

        // Assert error handling
        const card_body = banner.query_selector('.card-body')
        assert.ok(card_body                            , 'Still renders card'    )
        assert.ok(card_body.textContent.trim() === ''  , 'Shows empty content'   )

    })
})