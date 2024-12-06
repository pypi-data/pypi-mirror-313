import WebC__Target_Div                             from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                                from '../../../js/core/Web_Component.mjs'
import WebC__Document__Editor                       from '../../../js/cbr/document-assistant/WebC__Document__Editor.mjs'
import { setup_mock_responses, set_mock_response }  from '../../../js/testing/Mock_API__Data.mjs'

const { module, test , only} = QUnit

const MOCK_CONTENT = '# Test Document\nThis is test content.'
const MOCK_FILE_ID = 'test-file-123'

module('WebC__Document__Editor', hooks => {
    let target_div
    let editor
    let original_marked

    hooks.before(async (assert) => {
        assert.timeout(10)
        setup_mock_responses()

        // Mock marked library
        original_marked = window.marked
        window.marked = { marked: (text) => `<p>${text}</p>` }

        target_div = WebC__Target_Div.add_to_body()
        editor = await target_div.append_child(WebC__Document__Editor, {'file-id': MOCK_FILE_ID, 'content': MOCK_CONTENT})
        await editor.wait_for__component_ready()
    })

    hooks.after(() => {
        window.marked = original_marked
        editor.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {

        assert.equal(editor.tagName.toLowerCase()        , 'webc-document-editor'    , 'Has correct tag name')
        assert.equal(editor.constructor.name             , 'WebC__Document__Editor'  , 'Has correct class name')

        assert.ok(editor.shadowRoot                                                  , 'Has shadow root')
        assert.ok(editor.api_invoke                                                  , 'Has API__Invoke')
        assert.equal(editor.file_id                      , MOCK_FILE_ID              , 'Sets file_id')
        assert.equal(editor.content                      , MOCK_CONTENT              , 'Sets content')
        assert.equal(editor.version                      , 1                         , 'Initial version is 1')
        assert.notOk(editor.unsaved_changes                                         , 'No initial unsaved changes')

        assert.ok(editor instanceof Web_Component                                    , 'Extends Web_Component')
        assert.ok(editor instanceof HTMLElement                                      , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = editor.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                 , 'Has CSS rules')
        assert.ok(css_rules['.editor-container']                                    , 'Has container styles')
        assert.ok(css_rules['.markdown-editor']                                     , 'Has editor styles')
        assert.ok(css_rules['.markdown-preview']                                    , 'Has preview styles')
    })

    test('renders initial state correctly', assert => {
        const container = editor.query_selector('.editor-container')
        const toolbar = editor.query_selector('.editor-toolbar')
        const editor_area = editor.query_selector('.editor-area')
        const text_editor = editor.query_selector('.markdown-editor')
        const preview = editor.query_selector('.markdown-preview')

        assert.ok(container   , 'Container exists'  )
        assert.ok(toolbar     , 'Toolbar exists'    )
        assert.ok(editor_area , 'Editor area exists')
        assert.ok(text_editor , 'Editor exists'     )
        assert.ok(preview     , 'Preview exists'    )

        assert.equal(text_editor.value  , MOCK_CONTENT                                              )
        assert.equal(preview.innerHTML ,'&lt;p&gt;# Test Document\nThis is test content.&lt;/p&gt;' )
    })

    test('handles content changes', async assert => {
        const editor_element = editor.query_selector('.markdown-editor')
        const preview = editor.query_selector('.markdown-preview')

        const new_content = '# Updated Content'
        editor_element.value = new_content
        editor_element.dispatchEvent(new Event('input'))

        assert.equal(editor.content                      , new_content              , 'Updates content')
        assert.ok(editor.unsaved_changes                                           , 'Marks changes as unsaved')
        assert.equal(preview.innerHTML                   , '<p>' + new_content + '</p>', 'Updates preview')
    })

    test('handles save operation', async assert => {
        assert.expect(6)
        const done = assert.async()

        editor.content = '# New Content'
        editor.unsaved_changes = true

        editor.addEventListener('document-saved', (event) => {
            assert.equal(event.detail.content            , '# New Content'          , 'Event has correct content')
            assert.equal(event.detail.version            , 2                        , 'Event has correct version')
            assert.notOk(editor.unsaved_changes                                    , 'Clears unsaved changes')
            assert.equal(editor.version                  , 2                        , 'Increments version')
            done()
        }, { once: true })

        await editor.save_content()

        editor.unsaved_changes = false
        await editor.save_content()

        assert.equal(editor.query_selector('.editor-status').textContent, 'All changes saved')

        editor.unsaved_changes = true
        set_mock_response('/api/user-data/files/update-file' , 'PUT', null)
        await editor.save_content()
        assert.equal(editor.query_selector('.editor-status').textContent, 'Error saving changes')

        set_mock_response('/api/user-data/files/update-file', 'PUT', { success: true, data   : { status: 'updated'    }})
    })

    test('handles preview toggle', assert => {
        const preview_btn = editor.query_selector('.preview-btn')
        const editor_area = editor.query_selector('.editor-area')

        preview_btn.click()
        assert.ok(editor_area.classList.contains('show-preview')                    , 'Shows preview')

        preview_btn.click()
        assert.notOk(editor_area.classList.contains('show-preview')                 , 'Hides preview')
    })

    test('handles tab key in editor', async assert => {
        const editor_element = editor.query_selector('.markdown-editor')
        editor_element.value = 'test'
        editor_element.selectionStart = editor_element.selectionEnd = 4

        const tab_event = new KeyboardEvent('keydown', { key: 'Tab' })
        editor_element.dispatchEvent(tab_event)

        assert.equal(editor_element.value               , 'test    '                , 'Inserts spaces for tab')
        assert.equal(editor_element.selectionStart      , 8                         , 'Moves cursor correctly')
    })

    test('handle__save_click - triggers document save', async assert => {
        assert.expect(1)
        //const done = assert.async()

        editor.addEventListener('document-saved', () => { assert.ok(true, 'Auto-save triggered') }, { once: true })

        editor.content = '# save test'
        editor.unsaved_changes = true
        await editor.handle__save_click()
    })

    test('updates status display', assert => {
        const status = editor.query_selector('.editor-status')
        const toolbar = editor.query_selector('.editor-toolbar')

        editor.update_status('document-saved')
        assert.equal(status.textContent                 , 'All changes saved'       , 'Shows saved status')
        assert.ok(status.classList.contains('status-success')                      , 'Applies success style')

        editor.update_status('save-error')
        assert.equal(status.textContent                 , 'Error saving changes'    , 'Shows error status')
        assert.ok(status.classList.contains('status-error')                        , 'Applies error style')

        editor.update_status('unsaved')
        assert.equal(status.textContent                 , 'Unsaved changes'         , 'Shows unsaved status')
        assert.ok(status.classList.contains('status-warning')                      , 'Applies warning style')
        assert.ok(toolbar.classList.contains('unsaved')                            , 'Marks toolbar as unsaved')
    })

    test('accepts changes from diff view', async assert => {
        const new_content = '# Updated via diff'

        window.dispatchEvent(new CustomEvent('changes:accept', {detail: { changes: true, new_version: new_content }}))

        const editor_element = editor.query_selector('.markdown-editor')
        assert.equal(editor.content                     , new_content              , 'Updates content')
        assert.equal(editor_element.value               , new_content              , 'Updates editor')
        assert.ok(editor.unsaved_changes                                          , 'Marks as unsaved')
    })

    test('handles version reset', async assert => {
        const reset_content = '# Reset Content'

        window.dispatchEvent(new CustomEvent('version:reset', {detail: { content: reset_content,version: 3 } }))

        // await editor.wait_for(100)

        assert.equal(editor.content                     , reset_content            , 'Updates content')
        assert.equal(editor.version                     , 3                        , 'Updates version')
    })
})