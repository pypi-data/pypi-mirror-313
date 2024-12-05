import WebC__Target_Div      from '../../js/utils/WebC__Target_Div.mjs'
import Web_Component         from '../../js/core/Web_Component.mjs'
import WebC__Chat_Messages   from '../../js/chat-bot/WebC__Chat_Messages.mjs'
import WebC__Chat_Message    from '../../js/chat-bot/WebC__Chat_Message.mjs'
import WebC__System__Prompt  from '../../js/chat-bot/WebC__System__Prompt.mjs'

const { module, test , only} = QUnit

module('WebC__Chat_Messages', hooks => {
    let target_div
    let chat_messages

    hooks.before(async () => {
        target_div     = WebC__Target_Div.add_to_body()
        chat_messages  = await target_div.append_child(WebC__Chat_Messages)
        await chat_messages.wait_for__component_ready()
    })

    hooks.after(() => {
        chat_messages.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(chat_messages.tagName.toLowerCase()        , 'webc-chat-messages'     , 'Has correct tag name'     )
        assert.equal(chat_messages.constructor.element_name     , 'webc-chat-messages'     , 'Has correct element name' )
        assert.equal(chat_messages.constructor.name             , 'WebC__Chat_Messages'    , 'Has correct class name'   )

        assert.ok(chat_messages.shadowRoot                                                 , 'Has shadow root'          )
        assert.equal(chat_messages.auto_scroll                  , true                     , 'Auto-scroll defaults true')
        assert.equal(chat_messages.dom_spinner                  , null                     , 'Spinner starts null'      )
        assert.equal(chat_messages.current_message              , null                     , 'Current message null'     )

        assert.ok(chat_messages instanceof Web_Component                                   , 'Extends Web_Component'    )
        assert.ok(chat_messages instanceof HTMLElement                                    , 'Is HTML Element'          )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = chat_messages.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                       , 'Has CSS rules'            )
        assert.ok(css_rules['.messages']                                                  , 'Has messages container style')
    })

    test('renders initial structure correctly', assert => {
        const messages_container = chat_messages.query_selector('.messages')
        assert.ok(messages_container                                                      , 'Messages container exists' )
        assert.ok(messages_container.querySelector('slot')                                , 'Has slot element'         )
    })

    test('handles message operations', async assert => {
        assert.equal(chat_messages.messages_size()              , 0                       , 'Starts with no messages'  )
        chat_messages.show_sent_messages = true
        const test_message = 'Test message'
        const sent_message = chat_messages.add_message_sent({ user_prompt: test_message })

        assert.equal(chat_messages.messages_size()              , 1                       , 'Message added'            )
        assert.equal(sent_message.type, 'sent')

        chat_messages.messages_clear()
        assert.equal(chat_messages.messages_size()              , 0                       , 'Messages cleared'         )
    })

    test('handles stream events', async assert => {
        const platform = 'test-platform'
        const provider = 'test-provider'
        const model    = 'test-model'
        const channel  = 'test-channel'

        chat_messages.channel = channel

        // Test stream start
        chat_messages.handle_stream_start({ channel, platform, provider, model})

        assert.ok(chat_messages.current_message                                           , 'Creates current message'  )
        assert.equal(chat_messages.current_message.platform     , platform                , 'Sets platform'            )
        assert.equal(chat_messages.current_message.provider     , provider                , 'Sets provider'            )
        assert.equal(chat_messages.current_message.model        , model                   , 'Sets model'               )

        // Test stream data
        const test_chunk = 'Test chunk'
        chat_messages.handle_stream_data({
            channel, data: test_chunk
        })

        const message_content = chat_messages.current_message.message()
        assert.ok(message_content.includes(test_chunk)                                    , 'Appends chunk to message' )
    })

    test('handles message types correctly', async assert => {
        // Test system message
        chat_messages.add_message_system('System message')
        assert.ok(chat_messages.querySelector('webc-system-prompt')                       , 'Creates system prompt'    )

        // Test initial message
        const initial = chat_messages.add_message_initial('Initial message')

        assert.equal(initial.type, 'initial'                                   , 'Creates initial message'  )

        // Test received message
        const received = chat_messages.add_message_received('Received message')
        assert.equal(received.type, 'received'                                 , 'Creates received message' )

        chat_messages.messages_clear()
    })

    test('handles auto-scroll behavior', assert => {
        const messages_div = chat_messages.messages_div()

        assert.ok(chat_messages.auto_scroll                                               , 'Auto-scroll starts true'  )

        // Simulate wheel event
        messages_div.dispatchEvent(new WheelEvent('wheel'))
        assert.notOk(chat_messages.auto_scroll                                            , 'Disables on manual scroll')
    })

    test('handles channel filtering', assert => {
        const correct_channel = 'test-channel'
        const wrong_channel   = 'wrong-channel'

        chat_messages.channel = correct_channel

        assert.ok(chat_messages.is_message_to_current_channel({ channel: correct_channel }), 'Accepts correct channel')
        assert.notOk(chat_messages.is_message_to_current_channel({ channel: wrong_channel }), 'Rejects wrong channel' )
    })

    test('handles show_sent_messages attribute', assert => {
        chat_messages.show_sent_messages = false
        const sent_message = chat_messages.add_message_sent({ user_prompt: 'Test' })
        assert.notOk(sent_message                                                         , 'No message when disabled' )

        chat_messages.show_sent_messages = true
        const visible_message = chat_messages.add_message_sent({ user_prompt: 'Test' })
        assert.ok(visible_message                                                         , 'Shows message when enabled')
    })

    test('spinner behavior in messages', async assert => {
        chat_messages.show_sent_messages = true
        const message = chat_messages.add_message_sent({ user_prompt: 'Test' })

        assert.ok(chat_messages.dom_spinner                                               , 'Creates spinner'          )

        assert.ok(message.query_selector('.spinner')                                       , 'Spinner in message'       )

        chat_messages.handle_stream_data({ channel: chat_messages.channel, data: 'test' })
        assert.notOk(chat_messages.dom_spinner                                            , 'Removes spinner on data'  )
    })

    test('load_attributes - channel load', assert => {
        const channel = 'test-channel-abc-123'
        const chat_messages_1 = WebC__Chat_Messages.create({ channel: channel })
        assert.equal    (chat_messages_1.channel, null)
        assert.deepEqual(chat_messages_1.channels, ["Web_Component"])
        chat_messages_1.load_attributes()
        assert.equal(chat_messages_1.channel, channel)
        assert.deepEqual(chat_messages_1.channels, ["Web_Component", channel, 'WebC__Chat_Messages'])
    })

    test('add-message event', assert => {
        const event_data = { message  : 'another test message',
                             type     : 'sent'                ,
                             images   : null                  ,
                             platform : 'xyz-test-platform'   ,
                             provider : 'xyz-test-provider'   ,
                             model    : 'xyz-test-model'      }
        chat_messages.messages_clear()
        chat_messages.raise_event_global('add-message', event_data)
        assert.equal(chat_messages.messages()[0].message() , 'another test message')
        assert.equal(chat_messages.messages()[0].platform  , 'xyz-test-platform')
        assert.equal(chat_messages.messages()[0].provider  , 'xyz-test-provider')
        assert.equal(chat_messages.messages()[0].model     , 'xyz-test-model'   )
    })

    test('streamStart event', assert => {
        chat_messages.raise_event_global('streamStart', {})
        assert.ok(1)
    })

})