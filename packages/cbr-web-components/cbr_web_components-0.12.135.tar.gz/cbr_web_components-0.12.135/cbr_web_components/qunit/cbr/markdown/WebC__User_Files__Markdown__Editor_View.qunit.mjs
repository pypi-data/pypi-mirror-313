import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__Markdown__Editor_View     from '../../../js/cbr/markdown-editor/WebC__User_Files__Markdown__Editor_View.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'
import CBR_Events                                  from "../../../js/cbr/CBR_Events.mjs"

const { module, test, only } = QUnit

const MOCK_CONTENT = '# Test Content\n\nThis is test markdown content'
const MOCK_FILE_ID = 'test-file-123'

module('WebC__User_Files__Markdown__Editor_View', hooks => {
    let target_div
    let editor_view
    let original_marked

    hooks.beforeEach(async () => {
        setup_mock_responses()

        // Setup marked mock
        original_marked = window.marked
        window.marked = { marked: text => `<div>${text}</div>` }

        target_div = WebC__Target_Div.add_to_body()
        editor_view = await target_div.append_child(WebC__User_Files__Markdown__Editor_View,
            { file_id: MOCK_FILE_ID })
        await editor_view.wait_for__component_ready()
    })

    hooks.afterEach(() => {
        window.marked = original_marked
        editor_view.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(editor_view.tagName.toLowerCase()        , 'webc-user-files-markdown-editor-view', 'Has correct tag name')
        assert.equal(editor_view.constructor.element_name     , 'webc-user-files-markdown-editor-view', 'Has correct element name')
        assert.equal(editor_view.constructor.name             , 'WebC__User_Files__Markdown__Editor_View', 'Has correct class name')

        assert.ok(editor_view.shadowRoot                                                               , 'Has shadow root')
        assert.equal(editor_view.content                      , ''                                     , 'Initializes empty content')

        assert.ok(editor_view instanceof Web_Component                                                 , 'Extends Web_Component')
        assert.ok(editor_view instanceof HTMLElement                                                   , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = editor_view.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                                   , 'Has CSS rules')
        assert.ok(css_rules['.editor-view-container']                                                 , 'Has container styles')
        assert.ok(css_rules['.split-view']                                                            , 'Has split view styles')
        assert.ok(css_rules['.markdown-editor']                                                       , 'Has editor styles')
        assert.ok(css_rules['.markdown-preview']                                                      , 'Has preview styles')
    })

    test('renders initial structure correctly', assert => {
        const container = editor_view.query_selector('.editor-view-container')
        assert.ok(container                                                    , 'Container exists')

        const split_view = editor_view.query_selector('.split-view')
        assert.ok(split_view                                                   , 'Split view exists')
        assert.notOk(split_view.classList.contains('viewer-only')              , 'Not in viewer-only mode')

        const editor = editor_view.query_selector('.markdown-editor')
        assert.ok(editor                                                       , 'Editor exists')
        assert.equal(editor.value.trim(), ''                                   , 'Editor starts empty')
        const preview = editor_view.query_selector('.markdown-preview')
        assert.ok(preview                                                      , 'Preview exists')
    })

    test('handles file loading', async assert => {
        editor_view.raise_event_global(CBR_Events.CBR__FILE__LOADED, {
            file_id: MOCK_FILE_ID,
            content: MOCK_CONTENT
        })

        const editor = editor_view.query_selector('.markdown-editor')
        const preview = editor_view.query_selector('.markdown-preview')

        assert.equal(editor.value                         , MOCK_CONTENT                              , 'Editor shows content')
        assert.equal(preview.innerHTML                    , `<div>${MOCK_CONTENT}</div>`              , 'Preview shows rendered content')
        assert.equal(editor_view.file_id                  , MOCK_FILE_ID                              , 'Sets file ID')
    })

    test('handles edit mode toggle', assert => {
        const editor = editor_view.div_markdown_editor
        const preview = editor_view.div_markdown_preview
        const split_view = editor_view.div_split_view

        // Test view mode
        editor_view.raise_event_global(CBR_Events.CBR__FILE__VIEW_MODE)
        assert.equal(editor.style.display                 , 'none'                                    , 'Hides editor in view mode')
        assert.notOk(editor.is_visible ())
        assert.ok   (preview.is_visible())
        assert.equal(preview.style.display                , ''                                   , 'Shows preview in view mode')
        assert.ok(split_view.classList.contains('viewer-only')                                        , 'Adds viewer-only class')

        // Test edit mode
        editor_view.raise_event_global(CBR_Events.CBR__FILE__EDIT_MODE)
        assert.ok(editor.is_visible ())
        assert.ok(preview.is_visible())
        assert.notOk(split_view.classList.contains('viewer-only')                                     , 'Removes viewer-only class')
    })

    test('handles content changes', async assert => {
        assert.expect(2)

        const editor = editor_view.query_selector('.markdown-editor')

        editor_view.addEventListener(CBR_Events.CBR__FILE__CHANGED, (event) => {
            assert.equal(event.detail.content             , 'New content'                             , 'Emits change event')
        })

        // Simulate input
        editor.value = 'New content'
        editor.dispatchEvent(new Event('input'))

        const preview = editor_view.query_selector('.markdown-preview')
        assert.equal(preview.innerHTML                    , '<div>New content</div>'                  , 'Updates preview')
    })

    test('responds to get content request', assert => {
        editor_view.content = 'Test content'

        const detail = {}
        editor_view.raise_event_global(CBR_Events.CBR__FILE__GET_CONTENT, detail)

        assert.equal(detail.content                       , 'Test content'                            , 'Provides current content')
    })

    test('css rules are properly structured', assert => {
        const css_rules = editor_view.css_rules()

        assert.deepEqual(css_rules['.split-view'], {
            display           : "grid"                      ,
            gridTemplateColumns: "1fr 1fr"                  ,
            gap               : "1rem"                      ,
            height            : "calc(100vh - 200px)"       ,
            minHeight         : "400px"
        }, 'Split view rules are correct')

        assert.deepEqual(css_rules['.markdown-editor'], {
            width            : "100%"                      ,
            padding         : "1rem"                      ,
            fontSize        : "0.875rem"                  ,
            fontFamily      : "monospace"                 ,
            lineHeight      : "1.5"                       ,
            border          : "1px solid #dee2e6"         ,
            borderRadius    : "0.375rem"                  ,
            resize          : "none"                      ,
            outline         : "none"                      ,
            backgroundColor : "#f8f9fa"                   ,
            color           : "#212529"
        }, 'Editor rules are correct')
    })

    test('handles refresh content', assert => {
        editor_view.content = '# Title\n\nContent'
        editor_view.refresh_content()

        const editor = editor_view.query_selector('.markdown-editor')
        const preview = editor_view.query_selector('.markdown-preview')

        assert.equal(editor.value                         , '# Title\n\nContent'                      , 'Editor updates')
        assert.equal(preview.innerHTML                    , '<div># Title\n\nContent</div>'           , 'Preview updates')
    })

    test('version bar rendering', assert => {
        const version_bar = editor_view.render_version_bar()
        const dom = version_bar.dom_create()

        assert.ok(dom.classList.contains('version-bar')                                               , 'Has correct class')
        assert.ok(dom.querySelector('.version-message')                                               , 'Has message')
        assert.ok(dom.querySelector('.restore-version-btn')                                           , 'Has restore button')
        assert.ok(dom.querySelector('.return-current-btn')                                            , 'Has return button')
    })
})