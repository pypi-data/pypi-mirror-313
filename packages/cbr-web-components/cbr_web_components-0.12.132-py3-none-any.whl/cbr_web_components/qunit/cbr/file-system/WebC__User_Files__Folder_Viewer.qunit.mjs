import WebC__Target_Div                                                 from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                                                    from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__Folder_Viewer                                  from '../../../js/cbr/file-system/WebC__User_Files__Folder_Viewer.mjs'
import {setup_mock_responses, set_mock_response, add_padding_to_string} from '../../../js/testing/Mock_API__Data.mjs'

const { module, test, only , skip} = QUnit

const MOCK_FOLDER_ID = 'test-folder-123'
const MOCK_FOLDER_DATA = {
    folder_name: 'Test Folder',
    metadata: {
        timestamp__created: '2024-01-01T10:00:00',
        timestamp__updated: '2024-01-02T15:30:00'
    },
    files: ['file1', 'file2'],
    folders: ['subfolder1']
}

const MOCK_FOLDER_SUMMARY = '## Folder Contents\n- Important documents\n- Project files'

module('WebC__User_Files__Folder_Viewer', hooks => {
    let target_div
    let folder_viewer
    let original_marked

    hooks.before(async () => {
        setup_mock_responses()
        set_mock_response(`/api/user-data/files/folder?folder_id=${MOCK_FOLDER_ID}`                               , 'GET' , { data: MOCK_FOLDER_DATA   })
        set_mock_response(`/api/user-data/file-to-llms/folder-summary?folder_id=${MOCK_FOLDER_ID}&re_create=false`, 'POST', { data: MOCK_FOLDER_SUMMARY})

        original_marked = window.marked                                         // Store original marked function
        window.marked = { marked: (text) => `<p>${text}</p>` }

        target_div = WebC__Target_Div.add_to_body()
        folder_viewer = await target_div.append_child(WebC__User_Files__Folder_Viewer)
        await folder_viewer.wait_for__component_ready()
    })

    hooks.after(() => {
        window.marked = original_marked                                     // Restore original marked function

        folder_viewer.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(folder_viewer.tagName.toLowerCase()        , 'webc-user-files-folder-viewer', 'Has correct tag name')
        assert.equal(folder_viewer.constructor.element_name     , 'webc-user-files-folder-viewer', 'Has correct element name')
        assert.equal(folder_viewer.constructor.name             , 'WebC__User_Files__Folder_Viewer', 'Has correct class name')

        assert.ok(folder_viewer.shadowRoot                                                        , 'Has shadow root')
        assert.ok(folder_viewer.api_invoke                                                        , 'Has API__Invoke')
        assert.equal(folder_viewer.current_folder               , null                            , 'Initial folder is null')

        assert.ok(folder_viewer instanceof Web_Component                                          , 'Extends Web_Component')
        assert.ok(folder_viewer instanceof HTMLElement                                            , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = folder_viewer.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                              , 'Has CSS rules')
        assert.ok(css_rules['.viewer-container']                                                 , 'Has container styles')
        assert.ok(css_rules['.folder-header']                                                    , 'Has header styles')
        assert.ok(css_rules['.summary-container']                                                , 'Has summary styles')
    })

    test('handles folder selection', async assert => {
        folder_viewer.raise_event_global('folder-selected', { node_id: MOCK_FOLDER_ID, name: 'Test Folder' }) // Simulate folder selection
        await folder_viewer.wait_for__component_ready()

        const folder_name = folder_viewer.query_selector    ('.folder-name')
        const folder_meta = folder_viewer.query_selector_all('.folder-meta')
        const summary     = folder_viewer.query_selector    ('.summary-content')

        assert.deepEqual(folder_name.textContent   , 'Test Folder'                           )
        assert.deepEqual(folder_meta.length        , 4                                       )
        assert.ok       (folder_meta[0].textContent.startsWith('Created   : ')               )
        assert.ok       (folder_meta[1].textContent.startsWith('Updated   : ')               )
        assert.deepEqual(folder_meta[2].textContent, 'Files     : 2'                         )
        assert.deepEqual(folder_meta[3].textContent, 'Subfolders: 1'                         )
        assert.ok(summary.textContent.includes(add_padding_to_string(MOCK_FOLDER_SUMMARY,12)))
    })

    test('formats dates correctly', assert => {
        const timestamp = '2024-01-01T10:00:00'
        const formatted = folder_viewer.format_date(timestamp)

        assert.ok(formatted.includes('2024')                                                     , 'Includes year')
        assert.ok(formatted.includes('10:00')                                                    , 'Includes time')
    })

    test('handles summary creation', async assert => {
        set_mock_response(`/api/user-data/file-to-llms/folder-summary?folder_id=${MOCK_FOLDER_ID}&re_create=true`, 'POST', {
            data: 'New summary'
        })

        // Select folder first
        folder_viewer.current_folder = { node_id: MOCK_FOLDER_ID }
        await folder_viewer.load_folder_data()
        //await folder_viewer.render_folder_viewer()

        const create_btn = folder_viewer.query_selector('.btn-primary')
        assert.ok(create_btn                                                                     , 'Create button exists')

        // Click create summary button
        await create_btn.click()

        assert.ok(create_btn.textContent.includes('Create Summary')                              , 'Button text reset')
    })

    test('clears viewer correctly', async assert => {
        folder_viewer.raise_event_global('folder-selected', { node_id: MOCK_FOLDER_ID, name: 'Test Folder' }) // Simulate folder selection
        await folder_viewer.wait_for__component_ready()

        assert.ok(folder_viewer.query_selector('.folder-name'), 'Initially shows folder')

        // Clear viewer
        folder_viewer.clear_viewer()

        assert.equal(folder_viewer.current_folder , null, 'Clears current folder')
        assert.equal(folder_viewer.folder_data    , null, 'Clears folder data')
        assert.equal(folder_viewer.folder_summary , null, 'Clears folder summary')
    })

    test('summary section rendering', async assert => {
        folder_viewer.folder_summary = null
        let summary_div = folder_viewer.render_summary_section()
        assert.equal(summary_div.elements.length, 0, 'Empty when no summary')

        // Test with summary
        folder_viewer.folder_summary = MOCK_FOLDER_SUMMARY
        summary_div = folder_viewer.render_summary_section()
        const dom__summary_div = summary_div.dom_create()
        assert.ok(dom__summary_div.querySelector('.summary-title'   ), 'Has summary title')
        assert.ok(dom__summary_div.querySelector('.summary-content' ), 'Has summary content')
    })

    // todo: find a way to show empty state
    //
    // test('renders empty state correctly', async assert => {
    //
    //     const container     = folder_viewer.query_selector('.viewer-container')
    //     const empty_message = folder_viewer.query_selector('.viewer-empty')
    //
    //     assert.ok(container                                                                      , 'Container exists')
    //     assert.ok(empty_message                                                                  , 'Empty message exists')
    //     assert.equal(empty_message.textContent.trim()          , 'Select a folder to view its contents', 'Shows correct message')
    // })

    // todo: find a better way to show error messages
    //
    // test('error message display', async assert => {
    //     //await folder_viewer.render_folder_viewer()
    //
    //     folder_viewer.show_error_message('Test error')
    //     const status = folder_viewer.query_selector('.viewer-status')
    //
    //     // console.log(status)
    //     // assert.ok(1)
    //     // return
    //     assert.ok(status                                                                        , 'Status element exists')
    //     assert.equal(status.textContent                      , 'Test error'                     , 'Shows error message')
    //
    //     // Wait for message to clear
    //     //await folder_viewer.wait_for(3100)        // todo: find a way to test this without waiting
    //     assert.equal(status.textContent                      , ''                               , 'Clears error message')
    // })
})