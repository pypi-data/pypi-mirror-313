import WebC__Target_Div                             from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                                from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__Markdown                   from '../../../js/cbr/markdown-editor/WebC__User_Files__Markdown.mjs'
import { setup_mock_responses, set_mock_response }  from '../../../js/testing/Mock_API__Data.mjs'
import CBR_Events                                   from "../../../js/cbr/CBR_Events.mjs"

const { module, test, only } = QUnit

const MOCK_FILE_ID = 'test-file-123'

module('WebC__User_Files__Markdown', hooks => {
    let target_div
    let markdown_component

    hooks.before(async () => {
        setup_mock_responses()
        target_div = WebC__Target_Div.add_to_body()
        markdown_component = await target_div.append_child(WebC__User_Files__Markdown, { file_id: MOCK_FILE_ID })
        await markdown_component.wait_for__component_ready()
    })

    hooks.after(() => {
        markdown_component.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(markdown_component.tagName.toLowerCase()    , 'webc-user-files-markdown' , 'Has correct tag name'     )
        assert.equal(markdown_component.constructor.element_name , 'webc-user-files-markdown' , 'Has correct element name' )
        assert.equal(markdown_component.constructor.name         , 'WebC__User_Files__Markdown', 'Has correct class name'  )

        assert.ok(markdown_component.shadowRoot                                               , 'Has shadow root'          )
        assert.equal(markdown_component.file_id                  , MOCK_FILE_ID               , 'Sets file_id from attrs' )

        assert.ok(markdown_component instanceof Web_Component                                 , 'Extends Web_Component'    )
        assert.ok(markdown_component instanceof HTMLElement                                   , 'Is HTML Element'          )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = markdown_component.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                          , 'Has CSS rules'            )
        assert.ok(css_rules['.markdown-container']                                           , 'Has container styles'     )
        assert.ok(css_rules['.editor-container']                                             , 'Has editor styles'        )
        assert.ok(css_rules['.preview-and-versions']                                         , 'Has preview styles'       )
    })

    test('renders initial structure correctly', assert => {
        const container = markdown_component.query_selector('.markdown-container')
        assert.ok(container                                                                  , 'Container exists'         )

        const editor_toolbar = markdown_component.query_selector('.editor-toolbar')
        assert.ok(editor_toolbar                                                             , 'Toolbar exists'           )

        const viewer_editor = markdown_component.query_selector('.viewer-and-editor')
        assert.ok(viewer_editor                                                              , 'Editor exists'            )

        const versions_container = markdown_component.query_selector('.versions-container')
        assert.ok(versions_container                                                         , 'Versions panel exists'    )

        assert.notOk(versions_container.is_visible())
        assert.ok   (versions_container.is_hidden ())
        assert.equal(versions_container.style.display, 'none'                                , 'Versions hidden by default')
    })

    test('adds child web components', assert => {
        assert.ok(markdown_component.query_selector('webc-user-files-markdown-versions-panel'), 'Versions panel added'    )
        assert.ok(markdown_component.query_selector('webc-user-files-markdown-toolbar')       , 'Toolbar added'          )
        assert.ok(markdown_component.query_selector('webc-user-files-markdown-editor-view')   , 'Editor view added'      )
    })

    test('handles show/hide history', assert => {
        const versions_container = markdown_component.query_selector('.versions-container')
        assert.ok   (versions_container.is_hidden ())
        assert.notOk(versions_container.is_visible())
        // Test show history
        markdown_component.raise_event_global(CBR_Events.CBR__FILE__SHOW_HISTORY)
        assert.notOk(versions_container.is_hidden ())
        assert.ok   (versions_container.is_visible())

        // Test hide history
        markdown_component.raise_event_global(CBR_Events.CBR__FILE__HIDE_HISTORY)
        assert.ok   (versions_container.is_hidden ())
        assert.notOk   (versions_container.is_visible())
    })

    test('handles file cancel', assert => {
        assert.expect(1)

        markdown_component.addEventListener(CBR_Events.CBR__FILE__VIEW_MODE, () => {
            assert.ok(true                                                                    , 'Triggers view mode event')
        })

        markdown_component.raise_event_global(CBR_Events.CBR__FILE__CANCEL)
    })

    test('css rules are properly structured', assert => {
        const css_rules = markdown_component.css_rules()

        // Test container rules
        assert.deepEqual(css_rules['.markdown-container'], {
            height          : "100%"                       ,
            display        : "flex"                       ,
            flexDirection  : "column"                     ,
            backgroundColor: "#fff"                       ,
            borderRadius   : "0.375rem"                   ,
            boxShadow      : "0 2px 4px rgba(0,0,0,0.1)"
        }, 'Container rules are correct')

        // Test editor container rules
        assert.deepEqual(css_rules['.editor-container'], {
            flex           : "1"                          ,
            display       : "flex"                       ,
            flexDirection : "column"                     ,
            padding       : "1rem"                       ,
            gap           : "1rem"
        }, 'Editor container rules are correct')

        // Test preview and versions rules
        assert.deepEqual(css_rules['.preview-and-versions'], {
            display       : "flex"                       ,
            flexDirection: "row"                        ,
            padding      : "10px"
        }, 'Preview and versions rules are correct')
    })

    test('handles child component params', assert => {
        const versions_panel = markdown_component.query_selector('webc-user-files-markdown-versions-panel')
        const editor_view   = markdown_component.query_selector('webc-user-files-markdown-editor-view')

        assert.equal(versions_panel.getAttribute('file_id'), MOCK_FILE_ID                    , 'Passes file_id to versions')
        assert.equal(editor_view.getAttribute('file_id')   , MOCK_FILE_ID                    , 'Passes file_id to editor' )
    })
})