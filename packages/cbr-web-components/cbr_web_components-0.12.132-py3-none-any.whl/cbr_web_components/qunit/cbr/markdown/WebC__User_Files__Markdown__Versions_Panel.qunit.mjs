import WebC__Target_Div                             from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                                from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__Markdown__Versions_Panel   from '../../../js/cbr/markdown-editor/WebC__User_Files__Markdown__Versions_Panel.mjs'
import { setup_mock_responses, set_mock_response }  from '../../../js/testing/Mock_API__Data.mjs'
import CBR_Events                                   from "../../../js/cbr/CBR_Events.mjs"

const { module, test, only, skip} = QUnit

const MOCK_FILE_ID = 'test-file-123'
const MOCK_VERSIONS = [
    {
        version_id       : 'v1'                ,
        version_number   : 1                   ,
        file_size       : 1024                ,
        created_date    : '2024-01-01'        ,
        created_time    : '10:00:00'          ,
        is_latest_version: true
    },
    {
        version_id       : 'v2'                ,
        version_number   : 2                   ,
        file_size       : 2048                ,
        created_date    : '2024-01-02'        ,
        created_time    : '11:00:00'          ,
        is_latest_version: false
    }
]

module('WebC__User_Files__Markdown__Versions_Panel', hooks => {
    let target_div
    let versions_panel

    hooks.before(async (assert) => {
        assert.timeout(10)
        setup_mock_responses()
        set_mock_response(`/api/user-data/files/file-versions?file_id=${MOCK_FILE_ID}`, 'GET', {'data':  MOCK_VERSIONS})

        target_div = WebC__Target_Div.add_to_body()
        versions_panel = await target_div.append_child(WebC__User_Files__Markdown__Versions_Panel,
            { file_id: MOCK_FILE_ID })
        await versions_panel.wait_for__component_ready()
    })

    hooks.after(() => {
        versions_panel.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(versions_panel.tagName.toLowerCase()     , 'webc-user-files-markdown-versions-panel', 'Has correct tag name')
        assert.equal(versions_panel.constructor.element_name  , 'webc-user-files-markdown-versions-panel', 'Has correct element name')
        assert.equal(versions_panel.constructor.name          , 'WebC__User_Files__Markdown__Versions_Panel', 'Has correct class name')

        assert.ok(versions_panel.shadowRoot                                                              , 'Has shadow root')
        assert.ok(versions_panel.api                                                                     , 'Has API instance')
        assert.equal(versions_panel.file_id                   , null                                     , 'File ID initially null')
        assert.deepEqual(versions_panel.versions              , []                                       , 'Versions initially empty')
        assert.equal(versions_panel.current_version           , null                                     , 'No current version')

        assert.ok(versions_panel instanceof Web_Component                                                , 'Extends Web_Component')
        assert.ok(versions_panel instanceof HTMLElement                                                  , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = versions_panel.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                                     , 'Has CSS rules')
        assert.ok(css_rules['.versions-panel']                                                          , 'Has panel styles')
        assert.ok(css_rules['.versions-list']                                                           , 'Has list styles')
        assert.ok(css_rules['.version-item']                                                            , 'Has item styles')
    })

    test('loads versions on file load', async assert => {
        versions_panel.raise_event_global(CBR_Events.CBR__FILE__LOADED, { file_id: MOCK_FILE_ID })
        await versions_panel.wait_for__component_ready()


        const versions_list = versions_panel.query_selector('.versions-list')
        assert.ok(versions_list                                                                         , 'Shows versions list')

        const version_items = versions_panel.query_selector_all('.version-item')
        assert.equal(version_items.length                     , 2                                       , 'Shows all versions')
    })

    test('renders version item correctly', async assert => {
        versions_panel.raise_event_global(CBR_Events.CBR__FILE__LOADED, { file_id: MOCK_FILE_ID })
        await versions_panel.wait_for__component_ready()

        const version_item = versions_panel.query_selector('.version-item')
        assert.ok(version_item                                                                          , 'Version item exists')

        // Version info
        const info = version_item.querySelector('.version-info')
        assert.ok(info                                                                                  , 'Has info section')
        assert.ok(info.textContent.includes('Version 1')                                                , 'Shows version number')
        assert.ok(info.textContent.includes('(Latest)')                                                 , 'Shows latest status')

        // Date and time
        const date_time = version_item.querySelector('.version-datetime')
        assert.ok(date_time                                                                             , 'Has date/time section')
        assert.ok(date_time.textContent.includes('2024-01-01')                                          , 'Shows date')
        assert.ok(date_time.textContent.includes('10:00:00')                                            , 'Shows time')

        // Action buttons
        const actions = version_item.querySelector('.version-actions')
        assert.ok(actions                                                                               , 'Has actions section')
        assert.ok(actions.querySelector('.view-btn')                                                    , 'Has view button')
        assert.ok(actions.querySelector('.restore-btn')                                                 , 'Has restore button')
    })

    test('handles version selection', async assert => {
        versions_panel.raise_event_global(CBR_Events.CBR__FILE__LOADED, { file_id: MOCK_FILE_ID })
        await versions_panel.wait_for__component_ready()

        versions_panel.raise_event_global('version-selected', { file_id: MOCK_FILE_ID, version_id: 'v1' })

        const selected_item = versions_panel.query_selector('.version-item.current')
        assert.ok(selected_item                           , 'Shows selected version')
        assert.equal(versions_panel.current_version, 'v1' , 'Updates current version')
    })

    test('raises version events on button clicks', async assert => {
        assert.expect(2)
        const done = assert.async(2)

        versions_panel.raise_event_global(CBR_Events.CBR__FILE__LOADED, { file_id: MOCK_FILE_ID })
        await versions_panel.wait_for__component_ready()

        // Setup event listeners
        window.addEventListener('version-view', (event) => {
            assert.equal(event.detail.version_id              , 'v1'                                    , 'Raises view event')
            done()
        }, { once: true })

        window.addEventListener('version-restore', (event) => {
            assert.equal(event.detail.version_id              , 'v1'                                    , 'Raises restore event')
            done()
        }, { once: true })

        // Trigger button clicks
        const view_btn = versions_panel.query_selector('.view-btn')
        const restore_btn = versions_panel.query_selector('.restore-btn')

        view_btn.click()
        restore_btn.click()
    })

    test('handles versions loading error', async assert => {
        set_mock_response(`/api/user-data/files/file-versions?file_id=${MOCK_FILE_ID}`, 'GET', null)

        versions_panel.raise_event_global(CBR_Events.CBR__FILE__LOADED, { file_id: MOCK_FILE_ID })
        await versions_panel.wait_for__component_ready()

        assert.deepEqual(versions_panel.versions              , []                                      , 'Uses empty array on error')
    })

    test('css rules are properly structured', assert => {
        const css_rules = versions_panel.css_rules()

        assert.deepEqual(css_rules['.versions-list'], {
            display        : "flex"                       ,
            flexDirection : "column"                     ,
            gap           : "0.75rem"
        }, 'List rules are correct')

        assert.deepEqual(css_rules['.version-item'], {
            padding        : "1rem"                      ,
            backgroundColor: "#f8f9fa"                   ,
            borderRadius   : "0.375rem"                  ,
            border        : "1px solid #dee2e6"          ,
            display       : "flex"                       ,
            justifyContent: "space-between"              ,
            alignItems    : "center"
        }, 'Item rules are correct')
    })

    test('handle__versions_update updates versions when file IDs match', async assert => {
        assert.expect(3)

        const new_versions = [
            { version_id: 'new-v1', version_number: 3 },
            { version_id: 'new-v2', version_number: 4 }
        ]

        // Set file_id so we can test matching
        versions_panel.file_id = MOCK_FILE_ID

        // Store original render method to verify it's called
        let render_called = false
        const original_render = versions_panel.render
        versions_panel.render = () => { render_called = true }

        // Test matching file ID
        versions_panel.handle__versions_update({
            detail: {
                file_id  : MOCK_FILE_ID,
                versions : new_versions
            }
        })

        assert.deepEqual(versions_panel.versions, new_versions          , 'Updates versions array')
        assert.ok(render_called                                        , 'Triggers render')

        // Test non-matching file ID
        versions_panel.handle__versions_update({
            detail: {
                file_id  : 'different-id',
                versions : ['should', 'not', 'update']
            }
        })

        assert.deepEqual(versions_panel.versions, new_versions         , 'Ignores updates for different file ID')

        // Restore original render
        versions_panel.render = original_render
    })
})