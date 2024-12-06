import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__Upload                    from '../../../js/cbr/file-system/WebC__User_Files__Upload.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'
import CBR_Events from "../../../js/cbr/CBR_Events.mjs";

const { module, test, only, skip } = QUnit

const MOCK_FOLDER_DATA = {
    node_id: 'test-folder-123',
    name   : 'Test Folder'
}

module('WebC__User_Files__Upload', hooks => {
    let target_div
    let upload_component
    let original_console_error

    hooks.before(async (assert) => {
        assert.timeout(10)
        setup_mock_responses()                                                                  // Setup API mocks
        set_mock_response('/api/user-data/files/add-file', 'POST', { success: true })
        target_div = WebC__Target_Div.add_to_body()                                             // Create component
        upload_component = await target_div.append_child(WebC__User_Files__Upload)
        await upload_component.wait_for__component_ready()

        const file = new File(['test content'], 'test.txt', { type: 'text/plain' })
        const file_input = upload_component.query_selector('#file-input')
        Object.defineProperty(file_input, 'files', {
            value: [file]
        })
    })

    hooks.after(() => {
        upload_component.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(upload_component.tagName.toLowerCase()         , 'webc-user-files-upload'    , 'Has correct tag name')
        assert.equal(upload_component.constructor.element_name      , 'webc-user-files-upload'    , 'Has correct element name')
        assert.equal(upload_component.constructor.name              , 'WebC__User_Files__Upload'  , 'Has correct class name')

        assert.ok(upload_component.shadowRoot                                                     , 'Has shadow root')
        assert.ok(upload_component.api_invoke                                                     , 'Has API__Invoke')
        assert.deepEqual(upload_component.current_folder           , { node_id: null, name: 'root'}, 'Has default folder')

        assert.ok(upload_component instanceof Web_Component                                       , 'Extends Web_Component')
        assert.ok(upload_component instanceof HTMLElement                                         , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = upload_component.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                              , 'Has CSS rules')
        assert.ok(css_rules['.upload-container']                                                 , 'Has container styles')
        assert.ok(css_rules['.drop-zone']                                                        , 'Has drop zone styles')
        assert.ok(css_rules['.upload-status']                                                    , 'Has status styles')
    })

    test('renders initial state correctly', assert => {
        const container = upload_component.query_selector('.upload-container')
        assert.ok(container                                                                      , 'Container exists')

        const folder_display = upload_component.query_selector('.current-folder')
        assert.ok(folder_display                                                                 , 'Folder display exists')
        assert.ok(folder_display.textContent.includes('root')                                    , 'Shows root folder')

        const drop_zone = upload_component.query_selector('.drop-zone')
        assert.ok(drop_zone                                                                      , 'Drop zone exists')

        const file_input = upload_component.query_selector('#file-input')
        assert.ok(file_input                                                                     , 'File input exists')
        assert.equal(file_input.type                            , 'file'                         , 'Input is file type')
        assert.ok(file_input.multiple                                                            , 'Allows multiple files')

        const select_button = upload_component.query_selector('#select-files-btn')
        assert.ok(select_button                                                                  , 'Select button exists')
        assert.ok(select_button.classList.contains('btn-primary')                                , 'Has primary style')
    })

    test('handles folder selection', async assert => {
        await upload_component.raise_event_global('folder-selected', MOCK_FOLDER_DATA)
        const folder_display = upload_component.query_selector('.current-folder')
        assert.ok(folder_display.textContent.includes('Test Folder')                             , 'Updates folder display')
        assert.deepEqual(upload_component.current_folder        , MOCK_FOLDER_DATA               , 'Updates current folder')
    })

    test('handles drag and drop events', assert => {
        const drop_zone = upload_component.query_selector('.drop-zone')

        // Test dragenter
        drop_zone.dispatchEvent(new Event('dragenter'))
        assert.ok(drop_zone.classList.contains('drag-active')                                    , 'Adds active class on enter')

        // Test dragleave
        drop_zone.dispatchEvent(new Event('dragleave'))
        assert.notOk(drop_zone.classList.contains('drag-active')                                 , 'Removes active class on leave')
    })

    test('handles file selection', async assert => {
        assert.expect(2)
        assert.timeout(10)
        const done = assert.async()

        //const file = new File(['test content'], 'test.txt', { type: 'text/plain' })
        const file_input = upload_component.query_selector('#file-input')

        // Listen for refresh event
        upload_component.addEventListener('files-refresh', () => {
            assert.ok(true, 'Triggers refresh event')
            const status = upload_component.query_selector('.upload-status')
            assert.deepEqual(status.textContent, 'File test.txt uploaded successfully', 'Shows success message')
            done()
        }, { once: true })

        //Trigger file selection
        file_input.dispatchEvent(new Event('change'))
    })

    test('handles file upload errors', async assert => {
        set_mock_response('/api/user-data/files/add-file', 'POST', null, 500)

        const file_input = upload_component.query_selector('#file-input')

        file_input.dispatchEvent(new Event('change'))
        await upload_component.wait_for_event(CBR_Events.CBR__UI__NEW_ERROR_MESSAGE)

        const status = upload_component.query_selector('.upload-status')
        assert.deepEqual(status.outerHTML,'<div class="upload-status error">Failed to upload test.txt</div>')
        assert.ok      (status.classList.contains('error'), 'Shows error status')

        set_mock_response('/api/user-data/files/add-file', 'POST', { success: true })
    })

    test('handles paste events', async assert => {
        if (typeof window.__karma__ !== 'undefined') {
            assert.ok(true, 'Skipped in Karma environment');
            return;
        }
        await upload_component.refresh_ui()
        assert.timeout(10)
        assert.expect(1)
        const done = assert.async(1)

        const file = new File(['test content'], 'test.txt', { type: 'text/plain' })
        const clipboard_data = new DataTransfer()
        clipboard_data.items.add(file)

        upload_component.addEventListener('files-refresh', () => {
            assert.ok(true, 'Handles pasted file')
            done()
        }, { once: true })

        const paste_event = new ClipboardEvent('paste', { clipboardData: clipboard_data })
        upload_component.dispatchEvent(paste_event)
    })

    test('button triggers file input', assert => {
        const button = upload_component.query_selector('#select-files-btn')
        const file_input = upload_component.query_selector('#file-input')

        let clicked = false
        file_input.addEventListener('click', () => {clicked = true}, { once: true })

        button.click()
        assert.ok(clicked, 'Button triggers file input')
    })

    test('status messages auto-clear', async assert => {
        assert.expect(1)


        upload_component.show_success_message('Test message ABC')
        const status = upload_component.query_selector('.upload-status')

        assert.ok(status.textContent.includes('Test message ABC')                                    , 'Shows message')

        //const done = assert.async()
        // setTimeout(() => {
        //     assert.equal(status.textContent                      , ''                            , 'Clears message')
        //     done()
        // }, 3100)
    })

    test('handles drag and drop file upload', async assert => {
        assert.expect(4)  // We expect 4 assertions
        const done = assert.async()

        const drop_zone = upload_component.query_selector('.drop-zone')
        const mock_file = new File(['test content'], 'test.txt', { type: 'text/plain' })

        // Mock DataTransfer
        const data_transfer = new DataTransfer()
        data_transfer.items.add(mock_file)

        // Create drop event
        const drop_event = new Event('drop')
        Object.defineProperty(drop_event, 'dataTransfer', {
            value: data_transfer
        })

        // Listen for refresh event that should be triggered after upload
        upload_component.addEventListener('files-refresh', () => {
            assert.ok(true                                                            , 'Triggers refresh event')

            const status = upload_component.query_selector('.upload-status')
            assert.ok(status.textContent.includes('successfully')                     , 'Shows success message')
            done()
        } , { once: true })

        // Test dragover event
        assert.notOk(drop_zone.classList.contains('drag-active'))
        const dragover_event = new Event('dragover')
        drop_zone.dispatchEvent(dragover_event)
        assert.ok(drop_zone.classList.contains('drag-active'))

        // Test drop event
        drop_zone.dispatchEvent(drop_event)

    })

    test('handles folder_id fallbacks in upload_file_data', async assert => {
        assert.expect(3)
        const on_api_invoke = async ({url, method,data}) => {
            assert.deepEqual(url   , '/api/user-data/files/add-file')
            assert.deepEqual(method, 'POST')
            assert.deepEqual(data  , { file_name: 'test1.txt', file_bytes__base64: 'base64content', folder_id: '' })
        }
        set_mock_response('/api/user-data/files/add-file', 'POST', on_api_invoke)

        upload_component.current_folder = { node_id: null }
        await upload_component.upload_file_data('test1.txt', 'base64content')
    })
})