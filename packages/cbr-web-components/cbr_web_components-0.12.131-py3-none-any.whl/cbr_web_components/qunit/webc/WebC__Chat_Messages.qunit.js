import WebC__Chat_Messages  from '../../js/chat-bot/WebC__Chat_Messages.mjs'
import WebC__Target_Div     from '../../js/utils/WebC__Target_Div.mjs'
import Web_Component        from "../../js/core/Web_Component.mjs";


QUnit.module('WebC__Chat_Messages', function(hooks) {

    hooks.before((assert) => { });

    hooks.after((assert) => { });

    QUnit.test('constructor', (assert) => {
        assert.equal(WebC__Chat_Messages.element_name, 'webc-chat-messages'         , 'WebC__Chat_Message element name was correctly set'           )
        assert.ok   (WebC__Chat_Messages.prototype instanceof Web_Component      , 'WebC__Chat_Message.prototype is an instance of Web_Component');
    })

    QUnit.test('add_target_div', async (assert) =>  {
        assert.ok(true)

        const target_div       = WebC__Target_Div.add_to_body().build({width:"10%"})
        const chat_messages    = WebC__Chat_Messages.create({show_sent_messages: true})

        target_div.appendChild(chat_messages)
        await chat_messages.wait_for__component_ready()

        const sent_message     = 'a new SENT message'
        const received_message = 'message received'
        const exta_message     = '... added to message...'
        const message_sent     = chat_messages.add_message_sent    ({user_prompt: sent_message})
        const message_received = chat_messages.add_message_received(received_message)

        assert.equal(message_sent.message()     , sent_message)
        assert.equal(message_received.message(), received_message)
        message_sent.append(exta_message)
        assert.equal(message_sent.message()    , sent_message + exta_message, "message_sent has both messages now")
        assert.equal(message_received.message(), received_message           , "message_received wasn't impacted" )
        target_div.remove()
    })

    // QUnit.test('add_target_div', async (assert) =>  {
    //     const target_div       = WebC__Target_Div.add_to_body().build()
    //     const chat_messages    = target_div.append_child(WebC__Chat_Messages)
    //     const sent_message     = 'a new SENT message'
    //     const received_message = 'message received'
    //     const message_sent     = chat_messages.add_message_sent    ({user_prompt: sent_message})
    //
    //     window.message_sent = message_sent
    //
    //
    //     //await chat_messages.wait_for()
    //     //const message_received = chat_messages.add_message_received(received_message)
    //
    //     target_div.remove(WebC__Chat_Messages)
    //
    //     assert.ok(1)
    // })

})