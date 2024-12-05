import WebC__Target_Div      from '../../js/utils/WebC__Target_Div.mjs'
import Web_Component         from '../../js/core/Web_Component.mjs'
import WebC__Form_Input      from '../../js/chat-bot/WebC__Form_Input.mjs'
import AAA__Element_Event    from '../../js/testing/AAA__Element_Event.mjs'

const { module, test , only} = QUnit

module('WebC__Form_Input', hooks => {
    let target_div
    let form_input

    hooks.before(async () => {
        target_div = WebC__Target_Div.add_to_body()
        form_input = await target_div.append_child(WebC__Form_Input)
        await form_input.wait_for__component_ready()
    })

    hooks.after(() => {
        form_input.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(form_input.tagName.toLowerCase()         , 'webc-form-input'        , 'Has correct tag name'     )
        assert.equal(form_input.constructor.element_name      , 'webc-form-input'        , 'Has correct element name' )
        assert.equal(form_input.constructor.name              , 'WebC__Form_Input'       , 'Has correct class name'   )

        assert.ok(form_input.shadowRoot                                                   , 'Has shadow root'          )
        assert.ok(form_input.channels.includes('WebC__Form_Input')                       , 'Has correct channel'      )
        assert.ok(form_input.events_utils                                                , 'Has events utils'         )

        assert.ok(form_input instanceof Web_Component                                     , 'Extends Web_Component'    )
        assert.ok(form_input instanceof HTMLElement                                       , 'Is HTML Element'          )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = form_input.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                      , 'Has CSS rules'            )
        assert.ok(css_rules['#form_input']                                              , 'Has form input styles'    )
        assert.ok(css_rules['#text_area']                                               , 'Has text area styles'     )
        assert.ok(css_rules['#text_area::placeholder']                                  , 'Has placeholder styles'   )
    })

    test('renders initial structure correctly', assert => {
        const form_container = form_input.query_selector('#form_input')
        assert.ok(form_container                                                         , 'Form container exists'    )

        const text_area = form_input.query_selector('#text_area')
        assert.ok(text_area                                                              , 'Text area exists'         )
        assert.equal(text_area.getAttribute('rows')            , '1'                     , 'Has correct rows'         )
        assert.equal(text_area.value                          , ''                       , 'Starts empty'             )
    })

    test('handles input event and resizing', async assert => {
        assert.expect(2)
        const text_area = form_input.text_area
        const initial_height = text_area.style.height

        // Trigger input event
        text_area.value = 'Test input\nwith multiple\nlines'
        text_area.dispatchEvent(new Event('input'))

        assert.notEqual(text_area.style.height, initial_height                          , 'Height changes on input'  )
        assert.ok(parseInt(text_area.style.height) <= 25 * 8                            , 'Respects max height'      )
    })

    test('handles keydown event dispatch', async assert => {
        assert.expect(1)
        await AAA__Element_Event.test({
            element: form_input.text_area,
            event_name: 'keydown',
            assert: function(event) {
                assert.ok(event instanceof CustomEvent                                  , 'Dispatches keyboard event')
            }
        })
    })

    test('handles paste event dispatch', async assert => {
        assert.expect(1)
        await AAA__Element_Event.test({
            element: form_input.text_area,
            event_name: 'paste',
            assert: function(event) {
                assert.ok(event instanceof CustomEvent                                , 'Dispatches clipboard event')
            }
        })
    })

    test('handles set_value event', async assert => {
        const test_value = 'Test value'
        form_input.on_set_value({ event_data: { value: test_value }})

        assert.equal(form_input.text_area.value                 , test_value            , 'Sets text area value'     )
    })

    test('handles append_value event', async assert => {
        const initial_value = 'Initial '
        const append_value  = 'appended'

        form_input.text_area.value = initial_value
        form_input.on_append_value({ event_data: { value: append_value }})

        assert.equal(form_input.text_area.value                 , initial_value + append_value, 'Appends value correctly')
    })

    test('text area resize calculations', assert => {
        const text_area = form_input.text_area

        // Test single line
        text_area.value = 'Single line'
        const single_line_height = form_input.text_area_new_height()

        // Test multiple lines
        text_area.value = 'Line 1\nLine 2\nLine 3'
        const multi_line_height = form_input.text_area_new_height()

        assert.ok(multi_line_height > single_line_height                                , 'Height increases with lines')
        assert.ok(multi_line_height <= 25 * 8                                           , 'Respects maximum height'   )
    })

    test('handles input event triggering', assert => {
        assert.expect(1)
        const text_area = form_input.text_area

        text_area.addEventListener('input', () => {
            assert.ok(true                                                              , 'Input event triggered'    )
        }, { once: true })

        form_input.text_area_trigger_input_event()
    })

    test('handles text area getter', assert => {
        const text_area = form_input.text_area
        assert.ok(text_area instanceof HTMLTextAreaElement                              , 'Returns textarea element' )
        assert.equal(text_area.id                            , 'text_area'              , 'Has correct ID'           )
    })
})