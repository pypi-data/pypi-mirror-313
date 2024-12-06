import Web_Component    from '../../js/core/Web_Component.mjs'
import WebC__Target_Div from '../../js/utils/WebC__Target_Div.mjs'

const { module, test, only } = QUnit

// Create a test component that extends Web_Component
class Test_Component extends Web_Component {
    css_rules() {
        return {
            ".test"          : { color           : "red"              },
            ".nested"        : { backgroundColor : "blue"             },
            "@keyframes spin": {
                "0%"        : { transform       : "rotate(0deg)"     },
                "100%"      : { transform       : "rotate(360deg)"   }
            }
        }
    }
}
Test_Component.define()

module('Web_Component', hooks => {
    let target_div
    let component

    hooks.before(async () => {
        target_div = WebC__Target_Div.add_to_body()
        component  = await target_div.append_child(Test_Component)
        await component.wait_for__component_ready()
    })

    hooks.after(() => {
        component.remove()
        target_div.remove()
    })

    test('constructor and initialization', assert => {
        assert.ok   (component.shadowRoot                                         , 'Creates shadow root'       )
        assert.ok   (component.channels.includes('Web_Component')                 , 'Sets default channel'      )
        assert.ok   (component.window_event_listeners instanceof Array            , 'Initializes event array'   )
        assert.ok   (component.events_utils                                       , 'Has event utils'           )
        assert.ok   (component.webc_id.startsWith('webc_id_')                    , 'Generates webc_id'         )
        assert.ok   (component.channel.startsWith('webc_channel_')               , 'Generates channel'         )
    })

    test('static element_name method', assert => {
        class Test__Component__Name extends Web_Component {}

        assert.equal(Test__Component__Name.element_name , 'test-component-name'  , 'Converts class name'       )
        assert.equal(Web_Component.element_name         , 'web-component'        , 'Handles base class'        )
    })

    test('static create method', assert => {
        const el = Test_Component.create({
            id         : 'test-id'                  ,
            class      : 'test-class'               ,
            inner_html : '<div>Test</div>'
        })

        assert.equal(el.tagName.toLowerCase()       , 'test-component'           , 'Creates correct element'   )
        assert.equal(el.getAttribute('id')          , 'test-id'                 , 'Sets ID attribute'         )
        assert.equal(el.getAttribute('class')       , 'test-class'             , 'Sets class attribute'      )
        assert.equal(el.innerHTML                   , '<div>Test</div>'         , 'Sets inner HTML'          )
    })

    test('connectedCallback lifecycle', async assert => {
        assert.expect(2)
        const done = assert.async()
        let called = false

        class Lifecycle_Component extends Web_Component {
            async component_ready() {
                called = true
                assert.ok(true                                                    , 'Calls component_ready'    )
            }
        }
        Lifecycle_Component.define()

        const lifecycle = await target_div.append_child(Lifecycle_Component)
        await lifecycle.wait_for__component_ready()

        assert.ok(called                                                         , 'Completes lifecycle'      )
        done()
    })

    test('event handling methods', async assert => {
        assert.expect(4)
        const done = assert.async()

        // Test regular event
        const regular_event = await component.raise_event('test-event', { data: 'test' })
        assert.notOk(regular_event.bubbles                                       , 'Regular event no bubbles' )
        assert.equal(regular_event.detail.data     , 'test'                     , 'Sets event detail'        )

        // Test global event
        const global_event = component.raise_event_global('test-global', { data: 'global' })
        assert.ok   (global_event.bubbles                                        , 'Global event bubbles'     )
        assert.equal(global_event.detail.data      , 'global'                   , 'Sets global detail'       )
        done()
    })

    test('window event listeners', async assert => {
        let callback_called = false
        const callback = () => { callback_called = true }

        component.add_window_event_listener('test-window-event', callback)
        window.dispatchEvent(new Event('test-window-event'))

        assert.ok(callback_called                                                , 'Window listener works'    )

        component.remove_window_event_listeners()
        callback_called = false
        window.dispatchEvent(new Event('test-window-event'))

        assert.notOk(callback_called                                             , 'Removes listeners'        )
    })

    test('DOM event binding', async assert => {
        assert.expect(3)

        // Setup test elements
        component.set_inner_html('<button id="test-button">Test</button>')
        const button = component.query_selector('#test-button')

        // Test click binding
        let clicked = false
        component.add_event__on_click('#test-button', () => clicked = true)
        button.click()
        assert.ok(clicked                                                        , 'Binds click event'        )

        // Test custom event binding
        let custom_called = false
        component.add_event__on('custom-event', '#test-button', () => custom_called = true)
        button.dispatchEvent(new CustomEvent('custom-event'))
        assert.ok(custom_called                                                  , 'Binds custom event'       )

        // Test cleanup
        clicked = false
        custom_called = false
        component.remove_window_event_listeners()
        button.click()
        button.dispatchEvent(new CustomEvent('custom-event'))
        assert.notOk(clicked || custom_called                                    , 'Cleans up event bindings' )
    })

    test('CSS rules handling', async assert => {
        component.add_css_rules(component.css_rules())
        const rules = component.all_css_rules()

        assert.ok   (rules['.test']                                             , 'Adds basic rules'         )
        assert.ok   (rules['.nested']                                           , 'Adds nested rules'        )
        assert.ok   (Object.keys(rules).length >= 2                             , 'Multiple rules added'     )
    })

    test('DOM manipulation methods', async assert => {
        // Test inner HTML methods
        component.set_inner_html('<div id="test">Test</div>')
        assert.ok   (component.query_selector('#test')                          , 'Sets inner HTML'          )

        component.append_inner_html('<span>Appended</span>')
        assert.ok   (component.inner_html().includes('Appended')                , 'Appends inner HTML'       )

        // Test query selectors
        const single = component.query_selector('#test')
        assert.ok   (single                                                     , 'Queries single element'   )
        assert.equal(single.textContent           , 'Test'                      , 'Gets correct element'     )

        const all = component.query_selector_all('div, span')
        assert.equal(all.length                  , 2                            , 'Queries multiple elements')
    })

    test('utility methods', async assert => {
        // Test random ID generation
        const id1 = component.random_id('test')
        const id2 = component.random_id('test')
        assert.ok   (id1.startsWith('test_')                                    , 'Adds correct prefix'      )
        assert.notEqual(id1                      , id2                          , 'Generates unique IDs'     )

        // Test UUID generation
        const uuid = component.random_uuid()
        assert.equal(uuid.length                 , 36                           , 'Generates valid UUID'     )
        assert.ok   (uuid.includes('-')                                         , 'UUID has correct format'  )
    })

    test ('wait_for_event handling', async assert => {
        assert.expect(2)
        const done = assert.async()

        // Test successful wait
        setTimeout(() => {
            component.dispatchEvent(new CustomEvent('test-wait', { detail: 'success' }))
        }, 0.0001)

        const result = await component.wait_for_event('test-wait', 0.0001)
        assert.equal(result                     , 'success'                     , 'Resolves with detail'     )

        // Test timeout
        try {
            await component.wait_for_event('never-fires', 0.0001)
            assert.ok(false                                                     , 'Should timeout'           )
        } catch (error) {
            assert.ok(error.message.includes('never-fires')                     , 'Handles timeout'          )
        }
        done()
    })
})