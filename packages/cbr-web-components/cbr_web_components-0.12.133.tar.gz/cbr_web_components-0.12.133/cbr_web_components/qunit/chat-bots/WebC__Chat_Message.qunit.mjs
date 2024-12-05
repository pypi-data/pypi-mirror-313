import WebC__Target_Div from '../../js/utils/WebC__Target_Div.mjs'
import Web_Component    from '../../js/core/Web_Component.mjs'
import WebC__Chat_Message from '../../js/chat-bot/WebC__Chat_Message.mjs'

const { module, test, only } = QUnit

module('WebC__Chat_Message', hooks => {
    let target_div
    let chat_message
    let original_marked

    hooks.before(async () => {
        original_marked = window.marked               // Store original marked
        window.marked = { marked: (text) => text }   // Mock marked

        target_div = WebC__Target_Div.add_to_body()
        chat_message = await target_div.append_child(WebC__Chat_Message, {
            type: 'sent',
            channel: 'test-channel',
            platform: 'test-platform',
            provider: 'test-provider',
            model: 'test-model'
        })
        await chat_message.wait_for__component_ready()
    })

    hooks.after(() => {
        window.marked = original_marked             // Restore original marked
        chat_message.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(chat_message.tagName.toLowerCase()        , 'webc-chat-message'      , 'Has correct tag name'     )
        assert.equal(chat_message.constructor.element_name     , 'webc-chat-message'      , 'Has correct element name' )
        assert.equal(chat_message.constructor.name             , 'WebC__Chat_Message'     , 'Has correct class name'   )

        assert.ok(chat_message.shadowRoot                                                  , 'Has shadow root'          )
        assert.equal(chat_message.type                         , 'sent'                   , 'Sets type correctly'      )
        assert.equal(chat_message.channel                      , 'test-channel'           , 'Sets channel correctly'   )
        assert.equal(chat_message.platform                     , 'test-platform'          , 'Sets platform correctly'  )
        assert.equal(chat_message.provider                     , 'test-provider'          , 'Sets provider correctly'  )
        assert.equal(chat_message.model                        , 'test-model'             , 'Sets model correctly'     )

        assert.ok(chat_message instanceof Web_Component                                    , 'Extends Web_Component'    )
        assert.ok(chat_message instanceof HTMLElement                                      , 'Is HTML Element'          )
    })

    test('loads and applies CSS rules', assert => {
        const css_rules = chat_message.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                       , 'Has CSS rules'            )
        assert.ok(css_rules['.message']                                                   , 'Has message styles'       )
        assert.ok(css_rules['.initial']                                                   , 'Has initial styles'       )
        assert.ok(css_rules['.received']                                                  , 'Has received styles'      )
        assert.ok(css_rules['.sent']                                                      , 'Has sent styles'          )
        assert.ok(css_rules['.spinner']                                                   , 'Has spinner styles'       )
    })

    test('handles message appending and display', assert => {
        chat_message.append('Hello')
        assert.equal(chat_message.message_raw          , 'Hello'                         , 'Raw message set correctly' )
        assert.equal(chat_message.innerHTML            , 'Hello'                         , 'Displays message correctly')

        chat_message.append(' World')
        assert.equal(chat_message.message_raw          , 'Hello World'                   , 'Appends to raw message'   )
        assert.equal(chat_message.innerHTML            , 'Hello World'                   , 'Updates display'          )
    })

    test('handles edit mode', async assert => {
        chat_message.edit_mode = true
        await chat_message.refresh_ui()

        const edit_button = chat_message.shadowRoot.querySelector('#edit_button')
        const save_button = chat_message.shadowRoot.querySelector('#save_button')
        const text_area = chat_message.shadowRoot.querySelector('#message_text_area')

        assert.ok(edit_button                                                             , 'Edit button exists'       )
        assert.ok(save_button                                                             , 'Save button exists'       )
        assert.ok(text_area                                                               , 'Text area exists'         )

        chat_message.message('Test message')
        edit_button.click()


        assert.equal(text_area.style.display           , 'block'                         , 'Shows text area'          )
        assert.equal(text_area.value                   , 'Test message'                  , 'Sets text area content'   )
        assert.equal(edit_button.style.display         , 'none'                          , 'Hides edit button'        )
        assert.equal(save_button.style.display         , 'block'                         , 'Shows save button'        )
    })

    test('handles save operation', async assert => {
        chat_message.edit_mode = true
        await chat_message.refresh_ui()

        const text_area = chat_message.shadowRoot.querySelector('#message_text_area')
        const save_button = chat_message.shadowRoot.querySelector('#save_button')

        text_area.value = 'Updated message'
        save_button.click()

        assert.equal(chat_message.message_raw          , 'Updated message'               , 'Updates raw message'      )
        assert.equal(chat_message.innerHTML            , 'Updated message'               , 'Updates displayed message')
        assert.equal(text_area.style.display           , 'none'                          , 'Hides text area'         )
    })

    test('handles clear operation', async assert => {
        chat_message.edit_mode = true
        await chat_message.refresh_ui()

        chat_message.message('Test message')
        const clear_button = chat_message.shadowRoot.querySelector('#clear_button')

        clear_button.click()

        assert.equal(chat_message.message_raw          , ''                              , 'Clears raw message'       )
        assert.equal(chat_message.innerHTML            , ''                              , 'Clears displayed message' )
    })

    test('handles spinner operations', assert => {
        const spinner = chat_message.show_spinner()
        assert.ok(spinner                                                                , 'Shows spinner'            )
        assert.ok(spinner.classList.contains('spinner')                                  , 'Spinner has correct class')

        const removed = chat_message.hide_spinner()
        assert.ok(removed                                                                , 'Removes spinner'          )
        assert.notOk(chat_message.shadowRoot.querySelector('.spinner')                   , 'Spinner no longer exists' )
    })

    test('handles image display', assert => {
        const images = ['test1.jpg', 'test2.jpg']
        chat_message.images(images)

        const img_elements = chat_message.querySelectorAll('img')
        assert.equal(img_elements.length              , 2                               , 'Displays all images'      )
        assert.equal(img_elements[0].src.split('/').pop(), 'test1.jpg'                 , 'Sets correct image source')
        assert.ok(chat_message.querySelector('hr')                                      , 'Adds separator'           )
    })

    test('handles source display for received messages', async assert => {
        chat_message.type = 'received'
        await chat_message.refresh_ui()
        const source_text = chat_message.shadowRoot.querySelector('#source')
        assert.ok(source_text                                                             , 'Source info exists'       )
        assert.ok(source_text.classList.contains('source-received')                       , 'Has correct class'        )
        assert.equal(source_text.textContent, 'test-platform | test-provider | test-model','Shows correct source info' )
    })

    test('markdown handling', assert => {
        window.marked = undefined
        const test_text = 'line1\nline2'

        const plain_result = chat_message.create_message_html(test_text)
        assert.equal(plain_result                    , 'line1<br>line2'                , 'Handles newlines without marked')

        window.marked = { marked: (text) => `<p>${text}</p>` }
        const markdown_result = chat_message.create_message_html(test_text)
        assert.equal(markdown_result                 , '<p>line1\nline2</p>'           , 'Uses marked when available')
    })

    test('load_attributes -defaults', assert => {
        const chat_message = new WebC__Chat_Message()
        chat_message.load_attributes()
        assert.ok(1)
        assert.equal(chat_message.type    , null        )
        assert.equal(chat_message.channel , null        )
        assert.equal(chat_message.platform, 'platform'  )
        assert.equal(chat_message.provider, 'provider'  )
        assert.equal(chat_message.model   , 'model'     )

        assert.equal(chat_message.hide_spinner(), false)
    })
})