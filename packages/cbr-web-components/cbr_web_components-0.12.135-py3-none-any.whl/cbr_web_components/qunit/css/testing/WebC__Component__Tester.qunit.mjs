import WebC__Target_Div         from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component            from '../../../js/core/Web_Component.mjs'
import WebC__Component__Tester  from '../../../js/css/testing/WebC__Component__Tester.mjs'
import { Mock_Fetch }           from '../../../js/testing/Mock_Fetch.mjs'

const { module, test, only } = QUnit

// todo: finish adding the tests (commented below) that test the support for web sockets

module('WebC__Component__Tester', hooks => {
    let target_div
    let tester
    let mock_fetch
    let original_import
    let ws_mock

    hooks.before(async () => {
        // Setup mocks
        //mock_fetch = Mock_Fetch.apply_mock()
        original_import = window.import
        ws_mock = {
            close: () => {},
            send:  () => {}
        }

        // Mock WebSocket
        // global.WebSocket = function() {
        //     return ws_mock
        // }

        // Setup component
        target_div = WebC__Target_Div.add_to_body()
        tester = await target_div.append_child(WebC__Component__Tester)
        await tester.wait_for__component_ready()
    })

    hooks.after(() => {
        window.import = original_import
        tester.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(tester.tagName.toLowerCase()         , 'webc-component-tester' , 'Has correct tag name')
        assert.equal(tester.constructor.element_name      , 'webc-component-tester' , 'Has correct element name')
        assert.equal(tester.constructor.name              , 'WebC__Component__Tester', 'Has correct class name')

        assert.ok(tester.shadowRoot                                                 , 'Has shadow root')
        assert.ok(tester.base_path                                                 , 'Has base path')
        assert.ok(Array.isArray(tester.presets)                                    , 'Has presets array')

        assert.ok(tester instanceof Web_Component                                   , 'Extends Web_Component')
        assert.ok(tester instanceof HTMLElement                                     , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = tester.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                , 'Has CSS rules')
        assert.ok(css_rules['.tester-container']                                   , 'Has container styles')
        assert.ok(css_rules['.controls']                                          , 'Has controls styles')
        assert.ok(css_rules['.host-container']                                     , 'Has host styles')
    })

    test('renders initial structure correctly', assert => {
        const container = tester.query_selector('.tester-container')
        assert.ok(container                                                        , 'Main container exists')

        const controls = tester.query_selector('.controls')
        assert.ok(controls                                                         , 'Controls section exists')

        const path_input = controls.querySelector('.path-input')
        assert.ok(path_input                                                       , 'Path input exists')
        assert.equal(path_input.value, tester.presets[0].path                     , 'Sets default path')

        const select = controls.querySelector('select')
        assert.ok(select                                                          , 'Preset select exists')
        assert.equal(select.children.length, tester.presets.length                , 'Has all presets')

        const host = tester.query_selector('#component-host')
        assert.ok(host                                                            , 'Component host exists')
    })

    // test('handles component loading', async assert => {
    //     assert.expect(2)
    //     const test_path = 'test/component.mjs'
    //
    //     // Mock dynamic import
    //     window.import = async () => {
    //         return {
    //             default: class TestComponent extends HTMLElement {
    //                 static define() { return true }
    //             }
    //         }
    //     }
    //
    //     await tester.load_component(test_path)
    //     const status = tester.query_selector('.status-text')
    //
    //     assert.ok(status.textContent.includes('successfully')                      , 'Shows success message')
    //     assert.ok(tester.script_path === test_path                                , 'Updates script path')
    // })

    // test('handles loading errors gracefully', async assert => {
    //     assert.expect(2)
    //
    //     // Mock failed import
    //     window.import = async () => {
    //         throw new Error('Test error')
    //     }
    //
    //     await tester.load_component('invalid/path.mjs')
    //     const error_div = tester.query_selector('.alert-error')
    //     const status = tester.query_selector('.status-text')
    //
    //     assert.ok(error_div.textContent.includes('Test error')                    , 'Shows error message')
    //     assert.ok(status.textContent.includes('Failed')                          , 'Updates status')
    // })

    test('handles auto-reload toggle', async assert => {
        const auto_reload = tester.query_selector('#auto-reload')
        const container = tester.query_selector('.tester-container')

        let reload_triggered = false
        tester.refresh_component = () => { reload_triggered = true }

        // Test without auto-reload
        container.dispatchEvent(new Event('mouseenter'))
        assert.notOk(reload_triggered                                             , 'No reload when disabled')

        // Enable auto-reload
        auto_reload.checked = true
        container.dispatchEvent(new Event('mouseenter'))
        assert.ok(reload_triggered                                                , 'Reloads when enabled')
    })

    // test('handles WebSocket server check', async assert => {
    //     const server_check = tester.query_selector('#server-check')
    //     let connection_started = false
    //     let connection_stopped = false
    //
    //     // Mock WebSocket methods
    //     ws_mock.close = () => { connection_stopped = true }
    //
    //     // Enable server check
    //     server_check.checked = true
    //     server_check.dispatchEvent(new Event('change'))
    //     assert.ok(tester.ws_connection                                            , 'Starts WebSocket connection')
    //
    //     // Disable server check
    //     server_check.checked = false
    //     server_check.dispatchEvent(new Event('change'))
    //     assert.ok(connection_stopped                                              , 'Stops WebSocket connection')
    // })

    test('generates correct component name', assert => {
        assert.equal(tester.get_component_name('Test_Component')                  , 'test-component'    , 'Handles basic name')
        assert.equal(tester.get_component_name('Multiple__Underscores')          , 'multiple-underscores', 'Handles multiple underscores')
        assert.equal(tester.get_component_name('UPPERCASE_NAME')                  , 'uppercase-name'    , 'Handles uppercase')
    })

    test('updates status correctly', assert => {
        tester.update_status('Test message', 'success')
        const status = tester.query_selector('.status-text')
        const timestamp = status.nextElementSibling

        assert.ok(status.classList.contains('color-success')                      , 'Applies correct color class')
        assert.equal(status.textContent                     , 'Test message'      , 'Shows correct message')
        assert.ok(timestamp.textContent.match(/\d{1,2}:\d{2}:\d{2}/)            , 'Shows timestamp')
    })
})