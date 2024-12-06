import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__File_Viewer               from '../../../js/cbr/file-system/WebC__User_Files__File_Viewer.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'
import CBR_Events from "../../../js/cbr/CBR_Events.mjs";

const { module, test, only } = QUnit

const MOCK_FILE_ID = 'test-file-123'
const MOCK_FILE_DATA = {
    file_data: {
        file_name      : 'test.txt'            ,
        file_type      : '.txt'                ,
        file_size      : 1024                  ,
        updated__date  : '2024-01-01'          ,
        updated__time  : '10:00:00'
    },
    file_bytes__base64: btoa('Test content')   ,
    file_summary      : '"Test file summary"'
}

module('WebC__User_Files__File_Viewer', hooks => {
    let target_div
    let file_viewer
    let original_marked

    hooks.before(async (assert) => {
        assert.timeout(10)
        setup_mock_responses()
        set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`                      , 'GET'    , { data: MOCK_FILE_DATA })
        set_mock_response(`/api/user-data/files/delete-file?file_id=${MOCK_FILE_ID}`                        , 'DELETE' , { success: true        })
        set_mock_response('/api/user-data/files/rename-file'                                                , 'PUT'    , { success: true        })
        set_mock_response(`/api/user-data/file-to-llms/file-summary?re_create=true&file_id=${MOCK_FILE_ID}`, 'POST'   , { success: true        })
        //
        // Mock marked library
        original_marked = window.marked
        window.marked = { marked: (text) => `<p>${text}</p>` }

        target_div  = WebC__Target_Div.add_to_body()
        file_viewer = await target_div.append_child(WebC__User_Files__File_Viewer)
        await file_viewer.wait_for__component_ready()
    })

    hooks.after(() => {
        window.marked = original_marked
        file_viewer.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(file_viewer.tagName.toLowerCase()        , 'webc-user-files-file-viewer'  , 'Has correct tag name')
        assert.equal(file_viewer.constructor.element_name     , 'webc-user-files-file-viewer'  , 'Has correct element name')
        assert.equal(file_viewer.constructor.name             , 'WebC__User_Files__File_Viewer', 'Has correct class name')

        assert.ok(file_viewer.shadowRoot                                                     , 'Has shadow root')
        assert.ok(file_viewer.api_invoke                                                     , 'Has API__Invoke')
        assert.equal(file_viewer.current_file                 , null                          , 'Initial file is null')
        assert.equal(file_viewer.current_view                 , 'content'                     , 'Default view is content')

        assert.ok(file_viewer instanceof Web_Component                                       , 'Extends Web_Component')
        assert.ok(file_viewer instanceof HTMLElement                                         , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = file_viewer.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                         , 'Has CSS rules')
        assert.ok(css_rules['.viewer-container']                                            , 'Has container styles')
        assert.ok(css_rules['.file-header']                                                 , 'Has header styles')
        assert.ok(css_rules['.content-container']                                           , 'Has content styles')
    })


    test('handles file selection', async assert => {

        file_viewer.raise_event_global('file-selected', { node_id: MOCK_FILE_ID, name: 'test.txt' })
        await file_viewer.wait_for_event(CBR_Events.CBR__FILE__LOAD)

        const file_name    = file_viewer.query_selector    ('.file-name'   )
        const file_meta    = file_viewer.query_selector_all('.file-meta'   )
        const file_actions = file_viewer.query_selector    ('.file-actions')
        assert.equal(file_name.textContent             , 'test.txt'                         , 'Shows correct file name')
        assert.equal(file_meta.length                 , 3                                   , 'Shows all metadata')
        assert.ok(file_actions                                                              , 'Shows action buttons')
    })

    test('renders view tabs correctly', async assert => {
        // Select a file first
        file_viewer.current_file = { node_id: MOCK_FILE_ID, name: 'test.txt' }
        await file_viewer.render_file_viewer()

        const tabs        = file_viewer.query_selector('.view-tabs')
        const content_tab = file_viewer.query_selector('#content-tab')
        const chat_tab    = file_viewer.query_selector('#chat-tab')

        assert.ok(tabs                                                                      , 'Tabs container exists')
        assert.ok(content_tab                                                               , 'Content tab exists')
        assert.ok(chat_tab                                                                  , 'Chat tab exists')
        assert.ok(content_tab.classList.contains('btn-primary')                             , 'Content tab is active')
        assert.ok(chat_tab.classList.contains('btn-outline-primary')                        , 'Chat tab is inactive')
    })

    test('switches views correctly', async assert => {
        file_viewer.current_file = { node_id: MOCK_FILE_ID, name: 'test.txt' }
        await file_viewer.render_file_viewer()

        const chat_tab = file_viewer.query_selector('#chat-tab')
        chat_tab.click()
        await file_viewer.wait_for__component_ready()

        assert.equal(file_viewer.current_view         , 'chat'                              , 'Switches to chat view')
        assert.ok(file_viewer.query_selector('webc-user-files-content-chat')               , 'Shows chat component')
    })
    //
    test('renders file content correctly', async assert => {
        file_viewer.current_file = { node_id: MOCK_FILE_ID, name: 'test.txt' }
        await file_viewer.render_file_viewer()

        const content_container = file_viewer.query_selector('.content-container')
        const content_text = content_container.querySelector('.content-text')

        assert.ok(content_container                                                         , 'Content container exists')
        assert.ok(content_text                                                              , 'Text content rendered')
        assert.ok(content_text.textContent.includes('Test content')                         , 'Shows correct content')
    })

    test('formats dates and sizes correctly', assert => {
        const formatted_date = file_viewer.format_date('2024-01-01', '10:00:00')
        assert.equal(formatted_date                    , '2024-01-01 10:00:00'              , 'Formats date correctly')

        const formatted_size = file_viewer.format_size(1024)
        assert.equal(formatted_size                    , '1.0 KB'                           , 'Formats size correctly')
    })

    test('handles file actions', async assert => {
        file_viewer.raise_event_global('file-selected', { node_id: MOCK_FILE_ID, name: 'test.txt' })
        await file_viewer.wait_for__component_ready()
        assert.expect(3)
        const done = assert.async(2)

        file_viewer.current_file = { node_id: MOCK_FILE_ID, name: 'test.txt' }

        const original_confirm = window.confirm                 // Mock confirm for delete
        window.confirm = () => true

        const original_prompt = window.prompt                   // Mock prompt for rename
        window.prompt = () => 'new_name.txt'

        const on_file_listener = () => {
            assert.ok(true, 'Triggers refresh event')
            done()
        }
        file_viewer.addEventListener('files-refresh', on_file_listener)

        //Test delete
        const delete_btn = file_viewer.query_selector('.delete-file')
        delete_btn.click()


        // Test rename
        const rename_btn = file_viewer.query_selector('.rename-file')
        rename_btn.click()

        // Test create summary

        const summary_btn = file_viewer.query_selector('.create-summary')
        summary_btn.click()
        await file_viewer.wait_for__component_ready()
        assert.ok(1)                                                            // todo: add assert confirming the summary was created

        // Restore originals
        window.confirm = original_confirm
        window.prompt = original_prompt

        file_viewer.removeEventListener('files-refresh', on_file_listener)
    })


    test('renders summary section', async assert => {
        file_viewer.current_file = { node_id: MOCK_FILE_ID, name: 'test.txt' }
        await file_viewer.render_file_viewer()

        const summary_container = file_viewer.query_selector('.summary-container')
        const summary_title = file_viewer.query_selector('.summary-title')
        const summary_content = file_viewer.query_selector('.summary-content')

        assert.ok(summary_container                                                         , 'Summary container exists')
        assert.equal(summary_title.textContent         , 'File Summary'                     , 'Shows correct title')
        assert.ok(summary_content.innerHTML.includes('Test file summary')                   , 'Shows correct summary')
    })

    test('handles markdown files correctly', async assert => {
        // Setup mock data for markdown file
        const markdown_data = {
            file_data: {
                file_name: 'test.md',
                file_type: '.md',
                file_size: 1024,
                updated__date: '2024-01-01',
                updated__time: '10:00:00'
            },
            file_bytes__base64: btoa('# Test Markdown'),
            file_summary: '"Markdown summary"'
        }

        set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`, 'GET', { data: markdown_data })

        file_viewer.current_file = { node_id: MOCK_FILE_ID, name: 'test.md' }
        await file_viewer.render_file_viewer()

        const markdown_editor = file_viewer.query_selector('webc-user-files-markdown')
        assert.ok(markdown_editor, 'Renders markdown editor component')
        assert.equal(markdown_editor.getAttribute('file_id'), MOCK_FILE_ID, 'Sets correct file ID')
    })

    test('handles document files correctly', async assert => {
        // Test different document types (.doc, .docx, .xls, .xlsx, .ppt, .pptx)
        const document_types = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']

        for (const doc_type of document_types) {
            const doc_data = {
                file_data: {
                    file_name: `test${doc_type}`,
                    file_type: doc_type,
                    file_size: 1024,
                    updated__date: '2024-01-01',
                    updated__time: '10:00:00'
                },
                file_bytes__base64: btoa('test content'),
                file_summary: '"Document summary"'
            }

            set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`, 'GET', { data: doc_data })
            set_mock_response(`/api/user-data/files/file-temp-signed-url?file_id=${MOCK_FILE_ID}`, 'GET', { data: 'https://example.com/doc' })

            file_viewer.current_file = { node_id: MOCK_FILE_ID, name: `test${doc_type}` }
            await file_viewer.render_file_viewer()

            const document_viewer = file_viewer.query_selector('.content-document-viewer')
            assert.ok(document_viewer, `Renders document viewer for ${doc_type}`)
            assert.ok(document_viewer.innerHTML.includes('google.com/viewer'), 'Uses Google Viewer')
        }
    })

    test('handles image files correctly', async assert => {
        // Test different image types (.jpg, .jpeg, .png, .gif)
        const image_types = ['.jpg', '.jpeg', '.png', '.gif']

        for (const img_type of image_types) {
            const image_data = {
                file_data: {
                    file_name: `test${img_type}`,
                    file_type: img_type,
                    file_size: 1024,
                    updated__date: '2024-01-01',
                    updated__time: '10:00:00'
                },
                file_bytes__base64: btoa('fake-image-data'),
                file_summary: '"Image summary"'
            }

            set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`, 'GET', { data: image_data })

            file_viewer.current_file = { node_id: MOCK_FILE_ID, name: `test${img_type}` }
            await file_viewer.render_file_viewer()

            const image = file_viewer.query_selector('.content-image')
            assert.ok(image, `Renders image viewer for ${img_type}`)
            assert.ok(image.src.startsWith('data:image/'), 'Uses data URL for image')
        }
    })

    test('handles PDF files correctly', async assert => {
        const pdf_data = {
            file_data: {
                file_name: 'test.pdf',
                file_type: '.pdf',
                file_size: 1024,
                updated__date: '2024-01-01',
                updated__time: '10:00:00'
            },
            file_bytes__base64: btoa('fake-pdf-data'),
            file_summary: '"PDF summary"'
        }

        set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`, 'GET', { data: pdf_data })

        file_viewer.current_file = { node_id: MOCK_FILE_ID, name: 'test.pdf' }
        await file_viewer.render_file_viewer()

        const pdf_viewer = file_viewer.query_selector('.content-pdf')
        const pdf_embed = pdf_viewer.querySelector('embed')

        assert.ok(pdf_viewer, 'Renders PDF viewer')
        assert.ok(pdf_embed, 'Contains embed element')
        assert.equal(pdf_embed.type, 'application/pdf', 'Correct embed type')
        assert.ok(pdf_embed.src.startsWith('data:application/pdf;base64,'), 'Uses data URL for PDF')
    })

    test('handles default fallback for unknown file types', async assert => {
        const unknown_data = {
            file_data: {
                file_name: 'test.xyz',
                file_type: '.xyz',
                file_size: 1024,
                updated__date: '2024-01-01',
                updated__time: '10:00:00'
            },
            file_bytes__base64: btoa('test content'),
            file_summary: '"Unknown file summary"'
        }

        set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`, 'GET', { data: unknown_data })

        file_viewer.current_file = { node_id: MOCK_FILE_ID, name: 'test.xyz' }
        await file_viewer.render_file_viewer()

        // First try text display
        const content_text = file_viewer.query_selector('.content-text')

        // If text display fails, should show binary message
        const binary_message = file_viewer.query_selector('.content-binary')

        assert.ok(content_text || binary_message, 'Shows either text content or binary message')
        if (binary_message) {
            assert.ok(binary_message.textContent.includes('Binary file contents'), 'Shows correct binary message')
        }
    })

    test('handles JSON file content display correctly', async assert => {
        // Test valid JSON formatting
        const json_data = {
            file_data: {
                file_name: 'test.json',
                file_type: '.json',
                file_size: 1024,
                updated__date: '2024-01-01',
                updated__time: '10:00:00'
            },
            file_bytes__base64: btoa(JSON.stringify({ key: 'value' })),
            file_summary: '"JSON file summary"'
        }

        set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`, 'GET', { data: json_data })

        file_viewer.current_file = { node_id: MOCK_FILE_ID, name: 'test.json' }
        await file_viewer.render_file_viewer()

        const code_element = file_viewer.query_selector('.content-code')
        assert.ok(code_element, 'Renders code element for valid JSON')
        assert.ok(code_element.innerHTML.includes('<pre>'), 'Uses pre element for formatting')
        assert.ok(code_element.innerHTML.includes('"key": "value"'), 'Shows formatted JSON content')
    })

    test('handles invalid JSON content gracefully', async assert => {
        // Test invalid JSON handling
        const invalid_json_data = {
            file_data: {
                file_name: 'invalid.json',
                file_type: '.json',
                file_size: 1024,
                updated__date: '2024-01-01',
                updated__time: '10:00:00'
            },
            file_bytes__base64: btoa('{ invalid json content }'),
            file_summary: '"Invalid JSON file"'
        }

        set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`, 'GET', { data: invalid_json_data })

        file_viewer.current_file = { node_id: MOCK_FILE_ID, name: 'invalid.json' }
        await file_viewer.render_file_viewer()

        const text_element = file_viewer.query_selector('.content-text')
        assert.ok(text_element, 'Falls back to text display for invalid JSON')
        assert.ok(text_element.innerHTML.includes('invalid json content'), 'Shows raw content')
    })

    test('on_current_file__create_summary handles missing file', async assert => {
        file_viewer.current_file = null
        await file_viewer.on_current_file__create_summary()
        assert.ok(true, 'Returns early when no current file')
    })

    test('on_current_file__create_summary creates summary successfully', async assert => {
        file_viewer.current_file = { node_id: MOCK_FILE_ID }
        set_mock_response('/api/user-data/file-to-llms/file-summary', 'POST', { success: true })

        await file_viewer.on_current_file__create_summary()
        assert.ok(true, 'Successfully creates summary without errors')
    })

    test('on_current_file__delete handles missing file and data', async assert => {
        // Test with no current file
        file_viewer.current_file = null
        await file_viewer.on_current_file__delete()
        assert.ok(true, 'Returns early when no current file')

        // Test with file but no data
        file_viewer.current_file = { node_id: MOCK_FILE_ID }
        file_viewer.file_data = null
        await file_viewer.on_current_file__delete()
        assert.ok(true, 'Returns early when no file data')
    })

    test('on_current_file__delete handles successful deletion', async assert => {
        assert.expect(3)
        const done = assert.async()

        // Setup test data
        file_viewer.current_file = { node_id: MOCK_FILE_ID }
        file_viewer.file_data = { file_name: 'test.txt' }

        // Mock confirm dialog
        const original_confirm = window.confirm
        window.confirm = () => true

        // Add refresh event listener
        file_viewer.addEventListener('files-refresh', () => {
            assert.ok(true, 'Triggers refresh event')
            done()
        })

        await file_viewer.on_current_file__delete()

        assert.equal(file_viewer.current_file, null, 'Clears current file')
        assert.equal(file_viewer.file_data, null, 'Clears file data')

        // Restore original confirm
        window.confirm = original_confirm
    })

    test('on_current_file__delete handles cancellation', async assert => {
        // Setup test data
        file_viewer.current_file = { node_id: MOCK_FILE_ID }
        file_viewer.file_data = { file_name: 'test.txt' }

        // Mock confirm dialog to return false
        const original_confirm = window.confirm
        window.confirm = () => false

        await file_viewer.on_current_file__delete()

        assert.ok(file_viewer.current_file, 'Retains current file on cancel')
        assert.ok(file_viewer.file_data, 'Retains file data on cancel')

        // Restore original confirm
        window.confirm = original_confirm
    })

    test('on_current_file__create_download handles missing file', async assert => {
        file_viewer.current_file = null
        await file_viewer.on_current_file__create_download()
        assert.ok(true, 'Returns early when no current file')
    })

    test('on_current_file__create_download initiates download', async assert => {
        // Setup test data
        file_viewer.current_file = { node_id: MOCK_FILE_ID }

        // Mock reload_window_location
        const original_reload = file_viewer.reload_window_location
        let called_path = null
        file_viewer.reload_window_location = (path) => {
            called_path = path
        }

        await file_viewer.on_current_file__create_download()

        assert.ok(called_path, 'Called reload_window_location')
        assert.ok(called_path.includes('/api/user-data/files/file-download'), 'Uses correct API endpoint')
        assert.ok(called_path.includes(MOCK_FILE_ID), 'Includes file ID in path')

        // Restore original reload
        file_viewer.reload_window_location = original_reload
    })

    test('handles tab switching between content and chat views', async assert => {
        // Test content tab
        await file_viewer.on_content_tab__click()
        assert.equal(file_viewer.current_view, 'content', 'Switches to content view')

        // Test chat tab
        await file_viewer.on_chat_tab__click()
        assert.equal(file_viewer.current_view, 'chat', 'Switches to chat view')
    })
})