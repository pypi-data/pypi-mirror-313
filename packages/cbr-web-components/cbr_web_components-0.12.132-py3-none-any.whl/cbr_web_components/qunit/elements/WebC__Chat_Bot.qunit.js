import WebC__Chat_Bot   from '../../js/chat-bot/WebC__Chat_Bot.mjs';
import Web_Component    from '../../js/core/Web_Component.mjs';
import WebC__Target_Div from "../../js/utils/WebC__Target_Div.mjs";

QUnit.module('Chatbot_OpenAI', function(hooks) {

    let webc_chat_bot
    let target_div

    hooks.before(() => {
        target_div = WebC__Target_Div.add_to_body().build({width: "50%"})
        target_div.append_child(WebC__Chat_Bot)
        webc_chat_bot = $('webc-chat-bot')[0]
    });

    hooks.after(() => {
        target_div.remove()
    })


    QUnit.test('constructor', (assert) => {
        assert.ok(WebC__Chat_Bot.prototype instanceof Web_Component);
    })

    QUnit.test('chect_message_workflows', (assert)=>{
        assert.ok(true)
        assert.equal(webc_chat_bot.bot_name, 'ChatBot')
    })
})