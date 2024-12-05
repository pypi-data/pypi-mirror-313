import WebC__Target_Div     from '../../js/utils/WebC__Target_Div.mjs'
import Web_Component        from '../../js/core/Web_Component.mjs'
import WebC__Chat_Input     from '../../js/chat-bot/WebC__Chat_Input.mjs'
import WebC__Form_Input     from '../../js/chat-bot/WebC__Form_Input.mjs'

const { module, test, only } = QUnit

module('WebC__Chat_Input', hooks => {
    let target_div
    let chat_input
    let mock_text_area

    hooks.before(async (assert) => {
        assert.timeout(10)
        target_div = WebC__Target_Div.add_to_body()
        chat_input = await target_div.append_child(WebC__Chat_Input)
        await chat_input.wait_for__component_ready()

        // Create mock text area with expected value property
        mock_text_area = document.createElement('textarea')
        mock_text_area.value = ''

        // Mock the form input's text_area getter
        const form_input = chat_input.query_selector('webc-form-input')
        Object.defineProperty(form_input, 'text_area', {
            get: () => mock_text_area
        })
    })

    hooks.after(() => {
        chat_input.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(chat_input.tagName.toLowerCase()        , 'webc-chat-input'       , 'Has correct tag name')
        assert.equal(chat_input.constructor.element_name     , 'webc-chat-input'       , 'Has correct element name')
        assert.equal(chat_input.constructor.name             , 'WebC__Chat_Input'      , 'Has correct class name')

        assert.ok(chat_input.shadowRoot                                               , 'Has shadow root')
        assert.ok(chat_input.events_utils                                            , 'Has events utils')
        assert.ok(chat_input.channels.includes('WebC__Chat_Input')                   , 'Has correct channel')

        assert.ok(chat_input instanceof Web_Component                                 , 'Extends Web_Component')
        assert.ok(chat_input instanceof HTMLElement                                  , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = chat_input.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                  , 'Has CSS rules')
        assert.ok(css_rules['.chat-input']                                          , 'Has chat input styles')
        assert.ok(css_rules['#action-button']                                       , 'Has action button styles')
        assert.ok(css_rules['#clear-button']                                        , 'Has clear button styles')
    })

    test('renders initial structure correctly', assert => {
        const images_container = chat_input.query_selector('.chat-images')
        assert.ok(images_container                                                   , 'Images container exists')

        const chat_input_div = chat_input.query_selector('.chat-input')
        assert.ok(chat_input_div                                                     , 'Chat input container exists')

        const form_input = chat_input.query_selector('webc-form-input')
        assert.ok(form_input                                                         , 'Form input component exists')

        const action_button = chat_input.query_selector('#action-button')
        assert.ok(action_button                                                      , 'Action button exists')
        assert.equal(action_button.textContent                 , 'send'              , 'Action button shows send')

        const clear_button = chat_input.query_selector('#clear-button')
        assert.ok(clear_button                                                       , 'Clear button exists')
        assert.equal(clear_button.textContent                  , 'clear'             , 'Clear button shows clear')
    })

    test('handles input keydown', async assert => {
        assert.expect(3)
        const done = assert.async()

        chat_input.addEventListener('new_input_message', event => {
            assert.equal(event.detail.user_prompt            , 'test message'        , 'Sends correct message')
            assert.equal(event.detail.channel                , chat_input.channel    , 'Includes channel')
            assert.deepEqual(event.detail.images             , []                    , 'Includes empty images array')
            done()
        }, { once: true })

        mock_text_area.value = 'test message'

        const key_event = {
            event_data: {
                keyboard_event: {
                    key: 'Enter',
                    shiftKey: false,
                    preventDefault: () => {}
                }
            }
        }

        chat_input.on_input_keydown(key_event)
    })

    test('handles action button states', assert => {
        const action_button = chat_input.action_button

        chat_input.set_action_button('stop')
        assert.equal(action_button.innerHTML                  , 'stop'               , 'Shows stop text')
        assert.equal(action_button.style.backgroundColor      , 'black'              , 'Shows stop color')

        chat_input.set_action_button('send')
        assert.equal(action_button.innerHTML                  , 'send'               , 'Shows send text')
        assert.equal(action_button.style.backgroundColor      , 'rgb(0, 123, 255)'   , 'Shows send color')
    })

    test('handles stream events', async assert => {
        const action_button = chat_input.action_button

        await chat_input.on_prompt_sent({})
        assert.equal(action_button.innerHTML                  , 'stop'               , 'Shows stop on prompt')
        assert.ok(chat_input.input.disabled                                          , 'Input disabled on prompt')

        await chat_input.on_stream_complete({})
        assert.equal(action_button.innerHTML                  , 'send'               , 'Shows send on complete')
        assert.notOk(chat_input.input.disabled                                       , 'Input enabled on complete')
    })

    test ('handles image paste', async assert => {
        const images_container = chat_input.images
        assert.equal(images_container.children.length         , 0                    , 'No initial images')

        const file_contents      = 'ABCD'
        const expected_image_data = `data:image/png;base64,${btoa(file_contents)}`
        const paste_event = {
            event_data: {
                paste_event: {
                    clipboardData: {
                        items: [{
                            type: 'image/png',
                            getAsFile: () => new File([file_contents], 'test.png', { type: 'image/png' })
                        }]
                    }
                }
            }
        }

        // Mock convertImageToBase64
        //chat_input.convertImageToBase64 = async () => mock_image_data

        await chat_input.process_paste(paste_event)

        assert.equal(images_container.children.length         , 1                    , 'Image added')
        //assert.equal(images_container.querySelector('img').src, mock_image_data      , 'Correct image source')
        assert.equal(images_container.querySelector('img').src, expected_image_data      , 'Correct image source')
    })

    test('clears messages', assert => {
        assert.expect(1)

        chat_input.addEventListener('clear_messages', event => {
            assert.equal(event.detail.channel                 , chat_input.channel   , 'Sends clear event')
        }, { once: true })

        chat_input.on_clear_button()
    })

    test('handles action button click', async assert => {
        assert.expect(2)
        const done = assert.async()

        mock_text_area.value = 'test message'

        chat_input.addEventListener('new_input_message', event => {
            assert.equal(event.detail.user_prompt            , 'test message'        , 'Sends message on click')
            assert.equal(chat_input.action_button.innerHTML  , 'stop'                , 'Updates button state')
            done()
        }, { once: true })

        chat_input.on_action_button()
    })


    test('handles keyboard event with empty input', async assert => {
        assert.expect(2)
        const key_event = {
            event_data: {
                keyboard_event: {
                    key: 'Enter',
                    _key: 'Enter',      // Test the fallback key property
                    shiftKey: false,
                    preventDefault: () => {
                        assert.ok(true, 'Prevents default on empty input')
                    }
                }
            }
        }

        chat_input.on_input_keydown(key_event)
        key_event.event_data.keyboard_event.key = null
        key_event.event_data.keyboard_event._key = 'Enter'
        chat_input.on_input_keydown(key_event)




    })

    test('handles paste event with different clipboard sources', async assert => {
        assert.expect(3)
        const done = assert.async()

        // Test regular clipboardData
        await chat_input.process_paste({
            event_data: {
                paste_event: {
                    clipboardData: {
                        items: [{ type: 'image/png', getAsFile: () => new File([''], 'test.png') }]
                    }
                }
            }
        })
        assert.ok(true, 'Handles standard clipboard')

        // Test originalEvent clipboardData
        await chat_input.process_paste({
            event_data: {
                paste_event: {
                    originalEvent: {
                        clipboardData: {
                            items: [{ type: 'image/png', getAsFile: () => new File([''], 'test.png') }]
                        }
                    }
                }
            }
        })
        assert.ok(true, 'Handles original event clipboard')

        // Test empty clipboard
        await chat_input.process_paste({
            event_data: {
                paste_event: {}
            }
        })
        assert.ok(true, 'Handles empty clipboard')
        done()
    })

    test('handles image display with size calculation', async assert => {
        chat_input.images.innerHTML = ''                                // Clear any existing images
        const mock_base64 = 'data:image/png;base64,SGVsbG8gV29ybGQ='    // "Hello World" in base64

        const size = chat_input.calculateImageSize(mock_base64)         // Test image size calculation
        assert.equal(size, 12, 'Correctly calculates base64 size')

        chat_input.displayImage(mock_base64)                            // Verify full image display process

        const displayed_img = chat_input.images.querySelector('img')
        assert.ok   (displayed_img, 'Image element created')
        assert.equal(displayed_img.src, mock_base64, 'Image has correct source')
        assert.ok   (displayed_img.style.cssText.includes('max-width: 150px'), 'Has size constraints')
    })

    test('action button handles stop/send states', assert => {
        // Test stop to start transition
        chat_input.action_button.innerHTML = 'stop'
        chat_input.on_action_button()
        assert.equal(chat_input.action_button.innerHTML, 'send', 'Changes from stop to send')
        assert.equal(chat_input.action_button.style.backgroundColor, 'rgb(0, 123, 255)', 'Updates button color')

        // Test empty input handling
        mock_text_area.value = '   '
        chat_input.on_action_button()
        assert.equal(chat_input.action_button.innerHTML, 'send', 'Stays on send for empty input')

        // Test valid input transition
        mock_text_area.value = 'test message'
        chat_input.on_action_button()
        assert.equal(chat_input.action_button.innerHTML, 'stop', 'Changes to stop for valid input')
    })
})