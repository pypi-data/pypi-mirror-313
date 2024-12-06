import WebC__Target_Div          from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component             from '../../../js/core/Web_Component.mjs'
import WebC__Document__Assistant from '../../../js/cbr/document-assistant/WebC__Document__Assistant.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test , only} = QUnit

const MOCK_FILE_ID = '970804a2-88d8-41d6-881e-e1c5910b80f8'
const MOCK_CONTENT = '# Test Document\nThis is test content.'
const MOCK_FILE_DATA = {
    file_data: {
        name: 'test.md',
        size: 1024,
        type: 'text/markdown'
    },
    file_bytes__base64: btoa(MOCK_CONTENT)
}

module('WebC__Document__Assistant', hooks => {
    let target_div
    let assistant
    let original_marked

    hooks.before(async () => {
        setup_mock_responses()
        set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`, 'GET', { data: MOCK_FILE_DATA })

        original_marked = window.marked                             // Mock marked library
        window.marked = { marked: (text) => `<p>${text}</p>` }

        target_div = WebC__Target_Div.add_to_body()
        assistant = await target_div.append_child(WebC__Document__Assistant, { 'file-id': MOCK_FILE_ID })
        await assistant.wait_for__component_ready()
    })

    hooks.after(() => {
        window.marked = original_marked
        assistant.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(assistant.tagName.toLowerCase()        , 'webc-document-assistant'    , 'Has correct tag name')
        assert.equal(assistant.constructor.element_name     , 'webc-document-assistant'    , 'Has correct element name')
        assert.equal(assistant.constructor.name             , 'WebC__Document__Assistant'  , 'Has correct class name')

        assert.ok(assistant.shadowRoot                                                     , 'Has shadow root')
        assert.ok(assistant.api_invoke                                                     , 'Has API__Invoke')
        assert.equal(assistant.file_id                      , MOCK_FILE_ID                 , 'Sets file_id from attrs')

        assert.ok(assistant instanceof Web_Component                                       , 'Extends Web_Component')
        assert.ok(assistant instanceof HTMLElement                                         , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = assistant.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                       , 'Has CSS rules')
        assert.ok(css_rules['.document-assistant']                                        , 'Has container styles')
        assert.ok(css_rules['.chat-panel']                                               , 'Has chat panel styles')
        assert.ok(css_rules['.document-panel']                                           , 'Has document panel styles')
        assert.ok(css_rules['.diff-overlay']                                             , 'Has diff overlay styles')
    })

    test('loads document data correctly', async assert => {
        assert.ok(assistant.state.document.content                                        , 'Content is loaded')
        assert.equal(assistant.state.document.content       , MOCK_CONTENT                , 'Content matches mock')
        assert.deepEqual(assistant.file_data               , MOCK_FILE_DATA.file_data     , 'File data is stored')
    })

    test('adds web components correctly', assert => {
        const editor = assistant.query_selector('webc-document-editor')
        assert.ok(editor                                                                  , 'Editor component exists')
        assert.equal(editor.getAttribute('file-id')         , MOCK_FILE_ID                , 'Editor has correct file ID')
        assert.equal(editor.getAttribute('content')         , MOCK_CONTENT                , 'Editor has correct content')
    })

    test ('handles version control', async assert => {
        const original_content = assistant.state.document.content
        const new_content = '# Updated Content'
        await assistant.raise_event_global('version:commit')

        await assistant.raise_event_global('document:change', { content: new_content })
        await assistant.raise_event_global('version:commit')

        assert.equal(assistant.state.document.history.length, 2                           , 'Version added to history')
        assert.equal(assistant.state.document.history[1].content, new_content            , 'Version content correct')

        await assistant.raise_event_global('version:reset', { version: 1 })
        assert.equal(assistant.state.document.content, original_content                   , 'Content reset to version')
    })

    test('renders initial state correctly', async assert => {
        const container = assistant.query_selector('.document-assistant')
        assert.ok(container                                                               , 'Main container exists')

        const chat_panel = assistant.query_selector('.chat-panel')
        assert.ok(chat_panel                                                              , 'Chat panel exists')

        const document_panel = assistant.query_selector('.document-panel')
        assert.ok(document_panel                                                          , 'Document panel exists')

        const diff_overlay = assistant.query_selector('.diff-overlay')
        assert.ok(diff_overlay                                                            , 'Diff overlay exists')
        assert.notOk(diff_overlay.classList.contains('visible')                          , 'Diff overlay hidden by default')
    })

    test('handles document change events', async assert => {
        const new_content = '# Updated Content'
        assistant.raise_event_global('document:change', { content: new_content })
        assert.equal(assistant.state.document.content       , new_content                 , 'Content updated')
        assert.equal(assistant.state.document.version      , 2                           , 'Version incremented')
    })

    test('handles diff visibility events', async assert => {
        assistant.raise_event_global('diff:show')
        let diff_overlay = assistant.query_selector('.diff-overlay')
        assert.ok(diff_overlay.classList.contains('visible')                              , 'Shows diff overlay')

        assistant.raise_event_global('diff:hide')
        diff_overlay = assistant.query_selector('.diff-overlay')
        assert.notOk(diff_overlay.classList.contains('visible')                          , 'Hides diff overlay')
    })

    test('handles change acceptance', async assert => {
        const new_version = '# New Content'
        assistant.state.diff.visible = true
        assistant.state.diff.changes = ['test change']
        assistant.state.diff.selected = [0]

        assistant.raise_event_global('changes:accept', { changes: { new_version } })

        assert.equal(assistant.state.document.content       , new_version                 , 'Content updated')
        assert.notOk(assistant.state.diff.visible                                        , 'Diff overlay hidden')
        assert.equal(assistant.state.diff.changes.length   , 0                           , 'Changes cleared')
        assert.equal(assistant.state.diff.selected.length  , 0                           , 'Selected changes cleared')
    })

    test('handles change rejection', async assert => {
        assistant.state.diff.visible = true
        assistant.state.diff.changes = ['test change']
        assistant.state.diff.selected = [0]

        assistant.raise_event_global('changes:reject')

        assert.notOk(assistant.state.diff.visible                                        , 'Diff overlay hidden')
        assert.equal(assistant.state.diff.changes.length   , 0                           , 'Changes cleared')
        assert.equal(assistant.state.diff.selected.length  , 0                           , 'Selected changes cleared')
    })


    test('handles API errors gracefully', async assert => {
        assistant.state.document.content = ''
        set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`, 'GET', null, 500)

        const error_logs = []
        const original_console_error = console.error
        console.error = (...args) => error_logs.push(args)

        await assistant.load_document_data()

        assert.ok(error_logs.length > 0                                                   , 'Logs error')
        assert.equal(assistant.state.document.content       , ''                          , 'Content remains empty')

        console.error = original_console_error
    })
})