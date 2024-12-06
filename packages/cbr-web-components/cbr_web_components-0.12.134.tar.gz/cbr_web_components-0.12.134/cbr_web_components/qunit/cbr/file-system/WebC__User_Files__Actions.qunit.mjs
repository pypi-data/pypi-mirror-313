import WebC__Target_Div          from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component             from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__Actions from '../../../js/cbr/file-system/WebC__User_Files__Actions.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test , only, skip} = QUnit

const MOCK_FOLDER_DATA = {
    node_id: 'test-folder-123',
    name   : 'Test Folder'
}

module('WebC__User_Files__Actions', hooks => {
    let target_div
    let actions
    let api_calls = []

    hooks.before(async () => {
        setup_mock_responses()

        // Track API calls
        api_calls = []
        set_mock_response('/api/user-data/files/add-folder'                               , 'POST'  , { success: true })
        set_mock_response('/api/user-data/files/add-file'                                 , 'POST'  , { success: true })
        set_mock_response('/api/user-data/files/folder-rename'                            , 'POST'  , { success: true })
        set_mock_response('/api/user-data/files/delete-folder'                            , 'DELETE', { success: true })
        set_mock_response('/api/user-data/files/delete-folder?folder_id=test-folder-123'  , 'DELETE', { success: true })

        target_div = WebC__Target_Div.add_to_body()
        actions = await target_div.append_child(WebC__User_Files__Actions)
        await actions.wait_for__component_ready()
    })

    hooks.after(() => {
        actions.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        // Test component registration and naming
        assert.equal(actions.tagName.toLowerCase()        , 'webc-user-files-actions', 'Has correct tag name'     )
        assert.equal(actions.constructor.element_name     , 'webc-user-files-actions', 'Has correct element name' )
        assert.equal(actions.constructor.name             , 'WebC__User_Files__Actions', 'Has correct class name' )

        // Test shadow DOM and API
        assert.ok(actions.shadowRoot                                                  , 'Has shadow root'         )
        assert.ok(actions.api_invoke                                                  , 'Has API__Invoke'        )

        // Test inheritance
        assert.ok(actions instanceof Web_Component                                    , 'Extends Web_Component'   )
        assert.ok(actions instanceof HTMLElement                                      , 'Is HTML Element'         )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = actions.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                  , 'Has CSS rules'           )
        assert.ok(css_rules['.actions-container']                                    , 'Has container styles'    )
        assert.ok(css_rules['.folder-info']                                         , 'Has folder info styles'  )
        assert.ok(css_rules['.action-button']                                       , 'Has button styles'       )
    })

    test('renders initial state correctly', async assert => {
        // Test container structure
        const container = actions.query_selector('.actions-container')
        assert.ok(container                                                          , 'Container exists'        )

        // Test folder info section
        const folder_info = actions.query_selector('.folder-info')
        assert.ok(folder_info                                                        , 'Folder info exists'      )
        assert.ok(folder_info.textContent.includes('root')                          , 'Shows root folder'       )

        // Test form elements
        assert.ok(actions.query_selector('.new-folder-input')                       , 'New folder input exists' )
        assert.ok(actions.query_selector('.new-markdown-input')                     , 'Markdown input exists'   )
        assert.ok(actions.query_selector('.new-folder-btn')                         , 'Add folder button exists')
        assert.ok(actions.query_selector('.new-markdown-btn')                       , 'Add markdown button exists')
    })

    test('handles folder selection', async assert => {
        // Simulate folder selection
        const folder_event = new CustomEvent('folder-selected', {
            detail: MOCK_FOLDER_DATA
        })
        document.dispatchEvent(folder_event)

        const folder_name = actions.query_selector('.folder-name')
        assert.equal(folder_name.textContent                     , 'Test Folder'    , 'Updates folder name'     )

        // Test rename/delete elements appear
        assert.ok(actions.query_selector('.rename-input')                           , 'Rename input appears'    )
        assert.ok(actions.query_selector('.action-button.rename')                   , 'Rename button appears'   )
        assert.ok(actions.query_selector('.action-button.delete')                   , 'Delete button appears'   )
    })

    test('adds new folder', async assert => {
        assert.expect(1)
        assert.timeout(100)
        const done = assert.async()
        const input             = actions.query_selector('.new-folder-input')
        const button            = actions.query_selector('.new-folder-btn')
        const on__files_refresh = () => {
            assert.ok(true , 'Triggers refresh event'  )
            done()
        }

        input.value = 'New Test Folder'
        actions.addEventListener('files-refresh', on__files_refresh , { once: true })
        button.click()
    })

    test('creates markdown file', async assert => {                                     // todo: this test doesn't check if: creates markdown file
        assert.expect(1)
        assert.timeout(100)
        const done = assert.async()
        const input             = actions.query_selector('.new-markdown-input')
        const button            = actions.query_selector('.new-markdown-btn')
        const on__files_refresh = () => {
            assert.ok(true , 'Triggers refresh event'  )
            done()
        }
        input.value = 'test-doc.md'

        actions.addEventListener('files-refresh', on__files_refresh, { once: true })
        button.click()
    })

    test('handles rename operation', async assert => {
        assert.expect(1)
        assert.timeout(100)
        const done              = assert.async()
        const on__files_refresh = () => {
            assert.ok(true , 'Triggers refresh event'  )
            done()
        }

        document.dispatchEvent(new CustomEvent('folder-selected', { detail: MOCK_FOLDER_DATA }))        // change folder so that we can rename it
        await actions.wait_for__component_ready()

        actions.addEventListener('files-refresh', on__files_refresh, { once: true })
        const input = actions.query_selector ('.rename-input'        )
        const button = actions.query_selector('.action-button.rename')

        input.value = 'Renamed Folder'                                                                  // change folder value
        button.click()                                                                                  // and then trigger the rename
    })

    test('handles delete operation', async assert => {
        assert.expect(1)
        assert.timeout(100)
        const done              = assert.async()
        const on__files_refresh = () => {
            assert.ok(true , 'Triggers refresh event'  )
            done()
        }

        document.dispatchEvent(new CustomEvent('folder-selected', { detail: MOCK_FOLDER_DATA }))            // Setup folder selection first (since we can't delete root)
        await actions.wait_for__component_ready()

        const original_confirm = window.confirm                                                             // Mock confirm to return true
        window.confirm = () => true

        actions.addEventListener('files-refresh', on__files_refresh, { once: true })
        const delete_button = actions.query_selector('.action-button.delete')       // get delete button
        delete_button.click()                                                       // and click on it

        window.confirm = original_confirm                                           // Restore original confirm
    })

    test('prevents root folder operations', async assert => {
        // Setup root folder
        actions.current_folder = {
            node_id: null,
            name   : 'root'
        }
        actions.render()

        assert.ok(actions.query_selector('.action-button.rename')               , 'rename button for root')  // todo: add test to see if it is visible
        assert.ok(actions.query_selector('.action-button.delete')               , 'delete button for root')
    })

    test('appends .md extension if needed', async assert => {
        const done = assert.async();                                    // Async test
        assert.timeout(100)

        await actions.refresh_ui()

        const input  = actions.query_selector('.new-markdown-input')
        input.value = 'test-doc'  // No extension

        assert.expect(1)                                     // BUG this should
        const on_files_refresh_1 = () => {
            assert.ok(true , 'Adds .md and refreshes'  )
            done()
        }

        actions.addEventListener('files-refresh', on_files_refresh_1, { once: true })
        const button_1 = actions.query_selector('.new-markdown-btn')
        button_1.click()
    })

    test('handles API errors gracefully', async assert => {
        set_mock_response('/api/user-data/files/add-folder', 'POST', null, 500)                                         // Setup error responses

        const input = actions.query_selector('.new-folder-input')
        const button = actions.query_selector('.new-folder-btn')

        input.value = 'Error Test'
        button.click()
        assert.ok(true, 'Handles error without crashing')
    })

     test('logs errors when deleting folder fails', async assert => {
        // Track console.error calls
        const error_logs = []
        const original_console_error = console.error
        console.error = (...args) => error_logs.push(args)

        // Setup folder and error response
        actions.current_folder = MOCK_FOLDER_DATA
        set_mock_response('/api/user-data/files/delete-folder?folder_id=test-folder-123', 'DELETE', null, 500)

        // Mock confirm to return true
        const original_confirm = window.confirm
        window.confirm = () => true

        // Attempt delete
        await actions.delete_current_folder()

        // Verify error was logged
        assert.equal(error_logs.length                     , 1                     , 'Logs one error'          )
        assert.equal(error_logs[0][0]                      , 'Error deleting folder:', 'Correct error message' )
        assert.ok(error_logs[0][1] instanceof Error                                , 'Includes error object'   )

        // Restore mocks
        console.error = original_console_error
        window.confirm = original_confirm
    })

    test('logs errors when renaming folder fails', async assert => {
        // Track console.error calls
        const error_logs = []
        const original_console_error = console.error
        console.error = (...args) => error_logs.push(args)

        // Setup folder and error response
        actions.current_folder = MOCK_FOLDER_DATA
        set_mock_response('/api/user-data/files/folder-rename', 'POST', null, 500)

        // Attempt rename
        await actions.rename_current_folder('new name')

        // Verify error was logged
        assert.equal(error_logs.length                     , 1                     , 'Logs one error'          )
        assert.equal(error_logs[0][0]                      , 'Error renaming folder:', 'Correct error message' )
        assert.ok(error_logs[0][1] instanceof Error                                , 'Includes error object'   )

        // Restore mock
        console.error = original_console_error
    })

    test('prevents operations on root folder', async assert => {
        // Mock alert to track calls
        const alert_messages = []
        const original_alert = window.alert
        window.alert = (msg) => alert_messages.push(msg)

        // Attempt operations on root folder
        actions.current_folder = { node_id: null, name: 'root' }

        await actions.delete_current_folder()
        assert.equal(alert_messages[0]                     , 'Cannot delete root folder', 'Shows delete alert' )

        await actions.rename_current_folder('new name')
        assert.equal(alert_messages[1]                     , 'Cannot rename root folder', 'Shows rename alert' )

        // Restore mock
        window.alert = original_alert
    })


})