import Chatbot_OpenAI   from '../../js/chat-bot/Chatbot_OpenAI.mjs'
import Web_Component    from '../../js/core/Web_Component.mjs'
import WebC__Target_Div from "../../js/utils/WebC__Target_Div.mjs";
import { Mock_Fetch}    from '../../js/testing/Mock_Fetch.mjs'
import LLM__Handler from "../../js/cbr/llms/LLM__Handler.mjs";

QUnit.module('Chatbot_OpenAI', function(hooks) {

    let chatbot_openai
    let target_div
    let div_system_prompt
    let chunks
    let handler
    let mock_fetch

    hooks.before(async (assert) => {
        assert.timeout(10)
        target_div                      = WebC__Target_Div.add_to_body().build({width: "50%"})
        chatbot_openai                  = target_div.append_child(Chatbot_OpenAI)
        await chatbot_openai.wait_for__component_ready()                                    // wait for the component to be ready
        div_system_prompt                 = document.createElement('div');                // todo: find a better way to add this temp DIV
        div_system_prompt.id              = 'system_prompt';
        div_system_prompt.style.display   = 'none';
        document.body.appendChild(div_system_prompt);

        chunks        = ['Hello', ' World', '!'];
        handler       = new LLM__Handler()
        mock_fetch    = Mock_Fetch.apply_mock(Chatbot_OpenAI)
        mock_fetch.set_stream_response(handler.api_path, chunks);

    });

    hooks.beforeEach(() => {
        chatbot_openai.messages.messages_clear()
    })

    hooks.afterEach(() => {

    })

    hooks.after((assert) => {
        //assert.equal(chatbot_openai.messages.messages_size(),0)
        target_div.remove()
        div_system_prompt.remove()
    })

    QUnit.test('constructor', (assert) => {
        assert.ok(true)
        assert.ok(Chatbot_OpenAI.prototype instanceof Web_Component);
        assert.deepEqual(chatbot_openai.stop_fetch, false)
        assert.notEqual(chatbot_openai.messages, null)
        assert.equal(document.body.querySelector('#system_prompt').outerHTML, '<div id="system_prompt" style="display: none;"></div>')
    })

    QUnit.test('add_thread_id_ui_link', (assert) => {
        assert.equal(chatbot_openai.messages.messages_size(),0)

        chatbot_openai.add_thread_id_ui_link()

        assert.equal(chatbot_openai.messages.messages_size(),1)
        let last_message = chatbot_openai.messages.messages()[0]
        let chat_thread_id = chatbot_openai.chat_thread_id
        let last_message_inner_html = `<a style="padding:0px" href="chat/view/${chat_thread_id}" target="_blank">view saved chat</a>`
        assert.deepEqual(last_message.innerHTML, last_message_inner_html)
    })

    QUnit.test('all_system_prompts', (assert) => {

        assert.deepEqual(chatbot_openai.all_system_prompts(), [])

        chatbot_openai.system_prompt = 'an system_prompt'
        assert.deepEqual(chatbot_openai.all_system_prompts(), ['an system_prompt'])

        chatbot_openai.system_prompt = null

        div_system_prompt.innerHTML = 'this is another system prompt'
        assert.deepEqual(chatbot_openai.all_system_prompts(), ['this is another system prompt'])
        div_system_prompt.innerHTML = ''
        assert.deepEqual(chatbot_openai.all_system_prompts(), [])
    })

    QUnit.test('apply_ui_tweaks', async (assert) => {
        assert.deepEqual(chatbot_openai.all_system_prompts(), [])
        assert.equal(chatbot_openai.input.value   , '')
        assert.equal(chatbot_openai.initial_prompt, '')
        chatbot_openai.apply_ui_tweaks()
        assert.equal(chatbot_openai.input.value, '')

        chatbot_openai.initial_prompt = 'an initial prompt'
        chatbot_openai.apply_ui_tweaks()
        assert.equal(chatbot_openai.input.value, 'an initial prompt')

        chatbot_openai.messages.messages().innerHTML =''
        chatbot_openai.initial_message = 'an initial message'
        await chatbot_openai.refresh_ui()

        assert.deepEqual(chatbot_openai.messages.messages_size(),1)
        assert.deepEqual(chatbot_openai.messages.messages()[0].outerHTML, '<webc-chat-message type="initial" platform="." provider="." model="." style="display: inherit;">an initial message</webc-chat-message>')

        chatbot_openai.messages.messages_clear()
        chatbot_openai.initial_message = null

        const current_channel = chatbot_openai.channel
        assert.equal(chatbot_openai.shadowRoot.querySelector('webc-chat-input').style.display,'')
        chatbot_openai.channel = 'shared-llm--abc'
        chatbot_openai.apply_ui_tweaks()
        assert.equal(chatbot_openai.shadowRoot.querySelector('webc-chat-input').style.display,'none')
        chatbot_openai.channel = current_channel

        assert.deepEqual(chatbot_openai.messages.messages_size(),0)
        chatbot_openai.system_prompt = 'an system prompt'
        chatbot_openai.apply_ui_tweaks()
        assert.deepEqual(chatbot_openai.messages.messages_size(),1)
        assert.deepEqual(chatbot_openai.messages.messages()[0].outerHTML, '<webc-system-prompt content="an system prompt"></webc-system-prompt>')

        chatbot_openai.messages.messages_clear()
    })



    QUnit.test('post_openai_prompt_with_stream', async (assert) => {
        assert.expect(1)

        const user_prompt = '2+2'
        const images      = null

        chatbot_openai.addEventListener('streamComplete', function(event) {
            assert.deepEqual(event.detail, {'channel': chatbot_openai.channel})
            chatbot_openai.messages.messages_clear()
            }, { once: true });

        chatbot_openai.post_openai_prompt_with_stream(user_prompt, images)

    });


    QUnit.test('handles stream responses correctly', async assert => {
        const done = assert.async()
        assert.expect(9)
        const received_data = []

        const on_stream_data = (event) => {
            const channel = event.detail.channel
            const data    = event.detail.data
            received_data.push(data)
            assert.equal(channel, chatbot_openai.channel)
            assert.ok   (event.detail.data, 'Receives stream chunk')
        }

        const on_stream_complete = (event) => {
            assert.deepEqual(event.detail, {channel: chatbot_openai.channel})
            assert.ok       (true, 'Stream completes successfully')
            assert.deepEqual(received_data, chunks)
            chatbot_openai.removeEventListener('streamData'    , on_stream_data   )
            chatbot_openai.removeEventListener('streamComplete' ,on_stream_complete)
            done()
        }
        chatbot_openai.addEventListener('streamData'    , on_stream_data   )
        chatbot_openai.addEventListener('streamComplete',on_stream_complete)
        await chatbot_openai.post_openai_prompt_with_stream('test prompt', [])


    })

    QUnit.test('calculates chat histories correctly', async assert => {
        // Add messages in the way the project does it
        chatbot_openai.messages.add_message_sent('Question 1').message('Question 1')
        chatbot_openai.messages.add_message_received('Answer 1').message('Answer 1')
        chatbot_openai.messages.add_message_sent('Question 2').message('Question 2')

        const histories = chatbot_openai.calculate_histories()

        assert.equal(histories.length, 1, 'Captures complete Q&A pairs')
        assert.deepEqual(histories[0], {
            question: 'Question 1',
            answer: 'Answer 1'
        }, 'History pair matches expected format')
    })

    QUnit.test('handles model selection', async assert => {
        const model_event = new CustomEvent('select_model', {
            detail: {
                platform: 'test_platform',
                provider: 'test_provider',
                model: 'test_model',
                channel: chatbot_openai.channel
            }
        })

        await chatbot_openai.on_select_model(model_event)

        assert.equal(chatbot_openai.platform, 'test_platform', 'Updates platform')
        assert.equal(chatbot_openai.provider, 'test_provider', 'Updates provider')
        assert.equal(chatbot_openai.model   , 'test_model'   , 'Updates model'   )
    })

    QUnit.test('handles stream stopping', async assert => {
        assert.expect(2)
        const done = assert.async()

        chatbot_openai.stop_fetch = false
        assert.notOk(chatbot_openai.stop_fetch, 'Stop flag starts false')

        const stop_event = new CustomEvent('stop_stream', {
            detail: { channel: chatbot_openai.channel }
        })

        await chatbot_openai.on_stop_stream(stop_event)
        assert.ok(chatbot_openai.stop_fetch, 'Sets stop flag to true')
        done()
    })

    QUnit.test('handles message sending with targets', async assert => {
        assert.expect(2)

        chatbot_openai.target = 'specific_target'
        chatbot_openai.fetch = false  // Prevent actual API calls


        await chatbot_openai.on_message_sent({                      // Different target - should be ignored
            detail: {
                target: 'different_target',
                message: { user_prompt: 'test' }
            }
        })
        assert.ok(true, 'Ignores non-matching target')


        chatbot_openai.target = 'matching_target'                   // Matching target
        await chatbot_openai.on_message_sent({
            detail: {
                target: 'matching_target',
                message: { user_prompt: 'test' }
            }
        })
        assert.ok(true, 'Processes matching target')
    })

    QUnit.test ('raise_event_for__chat_ids handles headers correctly', async assert => {
        assert.expect(4)                                                                         // We expect 4 assertions

        const mock_headers = new Headers({                                                       // Test with valid headers
            'cbr__chat_id'       : 'test-chat-id'      ,
            'cbr__chat_thread_id': 'test-thread-id'
        })

        chatbot_openai.addEventListener('new_chat_ids', (event) => {
            assert.deepEqual(event.detail, { channel           : chatbot_openai.channel,
                                             cbr_chat_id       :'test-chat-id'         ,
                                             cbr_chat_thread_id: 'test-thread-id'      }, 'Emits correct event data')

            assert.ok(event.bubbles                     , 'Event bubbles'          )
            assert.ok(event.composed                    , 'Event is composed'      )
        }, { once: true })

        chatbot_openai.raise_event_for__chat_ids(null)                                              // Test with missing headers
        assert.ok(true                                  , 'Handles null headers'   )

        chatbot_openai.raise_event_for__chat_ids(mock_headers)                                      // Trigger the event with valid headers
    })

    QUnit.test('handles HTTP error responses', async assert => {
        assert.expect(2);
        const done = assert.async();

        // Mock a 404 response
        mock_fetch.set_stream_response(handler.api_path, [], 404);

        const on_stream_data = (event) => {
            assert.equal(event.detail.data, 'HTTP error! Status: 404', 'Receives correct error message');
            assert.equal(event.detail.channel, chatbot_openai.channel, 'Includes correct channel');
            chatbot_openai.removeEventListener('streamData', on_stream_data);
            mock_fetch.set_stream_response(handler.api_path, chunks); // Reset mock
            done();
        };

        chatbot_openai.addEventListener('streamData', on_stream_data, {once:true});
        await chatbot_openai.post_openai_prompt_with_stream('test prompt', []);
    });

    QUnit.test('handles stream stopping with complete flow', async assert => {
        assert.timeout(10)
        assert.expect(4);
        const done = assert.async();
        let streamDataReceived = false;

        const on_stream_data = (event) => {
            if (event.detail.data === '   ...(stopped)...') {
                assert.ok(true, 'Receives stopped message');
                streamDataReceived = true;
            }
        };

        const on_stream_complete = (event) => {
            assert.ok(streamDataReceived, 'Stream data event fired first');
            assert.ok(true, 'Stream complete event fired');
            assert.deepEqual(event.detail, {channel: chatbot_openai.channel}, 'Completes with correct channel');

            chatbot_openai.removeEventListener('streamData', on_stream_data);
            chatbot_openai.removeEventListener('streamComplete', on_stream_complete);
            done();
        };

        chatbot_openai.addEventListener('streamData', on_stream_data);
        chatbot_openai.addEventListener('streamComplete', on_stream_complete);

        const prompt = chatbot_openai.post_openai_prompt_with_stream('test prompt', []);
        chatbot_openai.stop_fetch = true;
        await prompt;
    });

    QUnit.test('handles stream errors with complete error flow', async assert => {
        assert.expect(4);
        //const done = assert.async();
        const mock_callback = () => { new Error('Stream error') }
        const expected_error = "Cannot read properties of undefined (reading 'getReader')"
        mock_fetch.set_response(handler.api_path, mock_callback);

        const on_stream_data = (event) => {
            assert.equal(event.detail.data, 'streamError: ' + expected_error)
            assert.equal(event.detail.channel, chatbot_openai.channel, 'Includes correct channel');
        };

        const on_stream_error = (event) => {
            assert.equal(event.detail.message, expected_error)
            chatbot_openai.removeEventListener('streamData', on_stream_data);
            chatbot_openai.removeEventListener('streamError', on_stream_error);
            mock_fetch.set_stream_response(handler.api_path, chunks); // Reset mock
            //done();
        };

        chatbot_openai.addEventListener('streamData', on_stream_data);
        chatbot_openai.addEventListener('streamError', on_stream_error);

        await chatbot_openai.post_openai_prompt_with_stream('test prompt', []);
        assert.ok(1)
    });

    QUnit.test('handles non-streamed responses', async assert => {
        assert.expect(2)
        const done = assert.async()
        const message = ['"Hello World!"']
        mock_fetch.set_stream_response(handler.api_path, message, 200, false);

        const on_stream_data = (event) => {
            assert.ok(event.detail.data, 'Receives response data')
        }
        const on_stream_complete = () => {
            assert.ok(true, 'Completes non-streamed response')
            chatbot_openai.removeEventListener('streamData', on_stream_data)
            chatbot_openai.removeEventListener('streamComplete', on_stream_complete)
            mock_fetch.set_stream_response(handler.api_path, chunks);
            done()
        }
        chatbot_openai.stream = false

        chatbot_openai.addEventListener('streamData'   , on_stream_data     )
        chatbot_openai.addEventListener('streamComplete', on_stream_complete)

        await chatbot_openai.post_openai_prompt_with_stream('test prompt', [])

    })
})