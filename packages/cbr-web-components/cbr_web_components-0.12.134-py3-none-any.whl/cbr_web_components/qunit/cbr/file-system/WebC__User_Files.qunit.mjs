import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__User_Files                           from '../../../js/cbr/file-system/WebC__User_Files.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test, only } = QUnit

module('WebC__User_Files', hooks => {
    let target_div
    let user_files

    hooks.before(async () => {
        setup_mock_responses()
        set_mock_response('/api/user-data/files/folder?folder_id=test-folder'                               , 'GET' , {})
        set_mock_response('/api/user-data/file-to-llms/folder-summary?folder_id=test-folder&re_create=false', 'POST', {})
        target_div = WebC__Target_Div.add_to_body()
        user_files = await target_div.append_child(WebC__User_Files)
        await user_files.wait_for__component_ready()
    })

    hooks.after(() => {
        user_files.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(user_files.tagName.toLowerCase()         , 'webc-user-files'           , 'Has correct tag name')
        assert.equal(user_files.constructor.element_name      , 'webc-user-files'           , 'Has correct element name')
        assert.equal(user_files.constructor.name              , 'WebC__User_Files'          , 'Has correct class name')

        assert.ok(user_files.shadowRoot                                                     , 'Has shadow root')
        assert.ok(user_files.api_invoke                                                     , 'Has API__Invoke')

        assert.ok(user_files instanceof Web_Component                                       , 'Extends Web_Component')
        assert.ok(user_files instanceof HTMLElement                                         , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = user_files.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                        , 'Has CSS rules')
        assert.ok(css_rules['.files-container']                                            , 'Has container styles')
        assert.ok(css_rules['.files-panel']                                                , 'Has panel styles')
        assert.ok(css_rules['.left-panel']                                                 , 'Has left panel styles')
        assert.ok(css_rules['.right-panel']                                                , 'Has right panel styles')
    })

    test('renders initial structure correctly', assert => {
        const container = user_files.query_selector('.files-container')
        assert.ok(container                                                                , 'Container exists')

        const left_panel = user_files.query_selector('.left-panel')
        assert.ok(left_panel                                                               , 'Left panel exists')
        assert.equal(getComputedStyle(left_panel).width, '350px'                          , 'Left panel has correct width')

        const right_panel = user_files.query_selector('.right-panel')
        assert.ok(right_panel                                                              , 'Right panel exists')

        const preview_section = right_panel.querySelector('.preview-section')
        assert.ok(preview_section                                                          , 'Preview section exists')
    })

    test('adds child web components', assert => {
        // Test presence of child components
        assert.ok(user_files.query_selector('webc-resize-button')                         , 'Resize button exists')
        assert.ok(user_files.query_selector('webc-user-files-tree-view')                  , 'Tree view exists')
        assert.ok(user_files.query_selector('webc-user-files-actions')                    , 'Actions exists')
        assert.ok(user_files.query_selector('webc-user-files-upload')                     , 'Upload exists')
        assert.ok(user_files.query_selector('webc-user-files-file-viewer')                , 'File viewer exists')
        assert.ok(user_files.query_selector('webc-user-files-folder-viewer')              , 'Folder viewer exists')
    })

    test('handles left panel resize', async assert => {
        const left_panel = user_files.div__left_panel

        // Test minimizing
        user_files.dispatchEvent(new CustomEvent('resize-user-files-left-panel', {
            detail: { minimized: true }
        }))

        assert.ok(left_panel.classList.contains('left-panel-minimized')                    , 'Panel gets minimized class')
        assert.equal(getComputedStyle(left_panel).width, '0px'                            , 'Panel width becomes 0')

        // Test maximizing
        user_files.dispatchEvent(new CustomEvent('resize-user-files-left-panel', {
            detail: { minimized: false }
        }))

        assert.notOk(left_panel.classList.contains('left-panel-minimized')                 , 'Minimized class removed')
        assert.equal(getComputedStyle(left_panel).width, '350px'                          , 'Panel returns to original width')
    })


    test('handles folder selection', async assert => {
        const file_viewer = user_files.query_selector('webc-user-files-file-viewer')
        const folder_viewer = user_files.query_selector('webc-user-files-folder-viewer')

        document.dispatchEvent(new CustomEvent('folder-selected', {
            detail: { node_id: 'test-folder', name: 'Test Folder' }
        }))

        assert.equal(file_viewer.style.display    , 'none'                                , 'File viewer becomes hidden')
        assert.equal(folder_viewer.style.display  , 'block'                               , 'Folder viewer becomes visible')
    })

    test('handles file selection', async assert => {
        const file_viewer = user_files.query_selector('webc-user-files-file-viewer')
        const folder_viewer = user_files.query_selector('webc-user-files-folder-viewer')

        document.dispatchEvent(new CustomEvent('file-selected', {
            detail: { node_id: 'test-file', name: 'test.txt' }
        }))

        assert.equal(file_viewer.style.display    , 'block'                               , 'File viewer becomes visible')
        assert.equal(folder_viewer.style.display  , 'none'                                , 'Folder viewer becomes hidden')
    })

    test('reloads components on session change', async assert => {
        let tree_view_refreshed = false
        const tree_view = user_files.query_selector('webc-user-files-tree-view')
        tree_view.refresh = () => { tree_view_refreshed = true }

        const file_viewer = user_files.query_selector('webc-user-files-file-viewer')
        let viewer_cleared = false
        file_viewer.clear_viewer = () => { viewer_cleared = true }

        // Add a selection to test clearing
        const selected_element = document.createElement('div')
        selected_element.classList.add('selected')
        user_files.shadowRoot.appendChild(selected_element)

        document.dispatchEvent(new Event('active_session_changed'))

        assert.ok(tree_view_refreshed                                                     , 'Tree view refreshes')
        assert.ok(viewer_cleared                                                          , 'File viewer clears')
        assert.notOk(selected_element.classList.contains('selected')                      , 'Selections are cleared')
    })

    test('handles files refresh event', assert => {
        let tree_view_refreshed = false
        const tree_view = user_files.query_selector('webc-user-files-tree-view')
        tree_view.refresh = () => { tree_view_refreshed = true }

        user_files.shadowRoot.dispatchEvent(new Event('files-refresh'))

        assert.ok(tree_view_refreshed                                                     , 'Tree view refreshes on event')
    })

    test('css rules are properly structured', assert => {
        const css_rules = user_files.css_rules()

        // Test host rules
        assert.deepEqual(css_rules[':host'], {
            display          : "block"                      ,
            width           : "100%"                       ,
            height          : "100%"                       ,
            minHeight       : "0"
        }, 'Host rules are correct')

        // Test container rules
        assert.deepEqual(css_rules['.files-container'], {
            display         : "flex"                       ,
            width          : "100%"                       ,
            height         : "100%"                       ,
            gap            : "1rem"                       ,
            padding        : "1rem"                       ,
            backgroundColor: "#f8f9fa"                    ,
            position       : "absolute"                   ,
            top            : "0"                          ,
            left           : "0"                          ,
            right          : "0"                          ,
            bottom         : "0"                          ,
            overflow       : "auto"
        }, 'Container rules are correct')

        // Test panel rules
        assert.deepEqual(css_rules['.left-panel'], {
            width          : "350px"                      ,
            minWidth       : "350px"                      ,
            display        : "flex"                       ,
            flexDirection  : "column"                     ,
            gap            : "1rem"                       ,
            flexShrink     : "0"
        }, 'Left panel rules are correct')
    })
})