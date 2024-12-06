import WebC__Resize_Button from '../../../js/elements/ui/WebC__Resize_Button.mjs'
import WebC__Target_Div    from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component       from '../../../js/core/Web_Component.mjs'

const { module, test , only} = QUnit

module('WebC__Resize_Button', hooks => {
    let target_div
    let resize_button
    let original_inner_width

    hooks.before(async () => {
        original_inner_width = window.innerWidth
        target_div = WebC__Target_Div.add_to_body()
        resize_button = await target_div.append_child(WebC__Resize_Button)
        await resize_button.wait_for__component_ready()
    })

    hooks.after(() => {
        Object.defineProperty(window, 'innerWidth', { value: original_inner_width })
        resize_button.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(resize_button.tagName.toLowerCase()    , 'webc-resize-button'  , 'Has correct tag name'     )
        assert.equal(resize_button.constructor.element_name , 'webc-resize-button'  , 'Has correct element name' )
        assert.equal(resize_button.constructor.name        , 'WebC__Resize_Button' , 'Has correct class name'   )

        assert.ok(resize_button.shadowRoot                                          , 'Has shadow root'          )
        assert.ok(resize_button instanceof Web_Component                            , 'Extends Web_Component'    )
        assert.ok(resize_button instanceof HTMLElement                              , 'Is HTML Element'          )
    })

    test('initializes with default attributes', assert => {
        assert.equal(resize_button.breakpoint     , 768                            , 'Default breakpoint'       )
        assert.equal(resize_button.event_name     , 'resize-event'                 , 'Default event name'       )
        assert.notOk(resize_button.minimized                                       , 'Not minimized by default' )
    })

    test('handles custom attributes', async assert => {
        const custom_button = await target_div.append_child(WebC__Resize_Button, {
            resize_breakpoint: '1024',
            resize_event_name: 'custom-event'
        })

        assert.equal(custom_button.breakpoint    , 1024                            , 'Custom breakpoint'        )
        assert.equal(custom_button.event_name    , 'custom-event'                  , 'Custom event name'        )
    })

    test('toggle_size changes state', async assert => {
        assert.expect(4)

        resize_button.addEventListener('resize-event', (event) => {
            assert.ok(event.detail                                                 , 'Event contains detail'    )
            assert.ok('minimized' in event.detail                                  , 'Detail includes state'    )
        }, {once: true})

        resize_button.toggle_size()
        assert.ok(resize_button.minimized                                          , 'Becomes minimized'        )

        resize_button.toggle_size()
        assert.notOk(resize_button.minimized                                       , 'Becomes expanded'         )
    })

    test('handles window resize', async assert => {
        // Simulate window smaller than breakpoint
        Object.defineProperty(window, 'innerWidth', { value: 500 })
        resize_button.handle_resize()
        assert.ok(resize_button.minimized                                          , 'Minimizes on small window')

        // Simulate window larger than breakpoint
        Object.defineProperty(window, 'innerWidth', { value: 1000 })
        resize_button.handle_resize()
        assert.notOk(resize_button.minimized                                       , 'Expands on large window'  )
    })

    test('button appearance changes with state', async assert => {
        const button = resize_button.query_selector('.toggle-button')
        assert.equal(button.innerHTML            , '←'                             , 'Shows expand arrow'       )

        resize_button.minimize()
        assert.equal(button.innerHTML            , '→'                             , 'Shows minimize arrow'     )

        resize_button.expand()
        assert.equal(button.innerHTML            , '←'                             , 'Returns to expand arrow'  )
    })

    test('dispatches resize events', assert => {
        assert.expect(5)

        let event_count = 0
        const on_resize_event =  (event) => {
            event_count++
            assert.ok(event.bubbles                                                , 'Event bubbles'            )
            assert.ok(event.composed                                               , 'Event is composed'        )
        }
        resize_button.addEventListener('resize-event',on_resize_event)

        resize_button.minimize()
        resize_button.expand()
        assert.equal(event_count                 , 2                               , 'Fires correct events'     )

        resize_button.removeEventListener('resize-event',on_resize_event)
    })
})