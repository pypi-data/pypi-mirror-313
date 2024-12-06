import LLM__Handler                                 from '../../../js/cbr/llms/LLM__Handler.mjs'
import { Mock_Fetch }                               from '../../../js/testing/Mock_Fetch.mjs'
import { setup_mock_responses, set_mock_response }  from '../../../js/testing/Mock_API__Data.mjs'

const { module, test , only, skip} = QUnit

const MOCK_USER_PROMPT     = 'test prompt'
const MOCK_SYSTEM_PROMPTS  = ['system prompt 1', 'system prompt 2']

module('LLM__Handler', hooks => {
    let handler
    let original_fetch_url
    let mock_fetch
    let original_console_error

    hooks.before(() => {
        setup_mock_responses()
        original_console_error = console.error
        console.error = () => {}

        handler = new LLM__Handler()
        mock_fetch = Mock_Fetch.apply_mock(LLM__Handler)
    })

    hooks.after(() => {
        Mock_Fetch.restore_original(LLM__Handler, original_fetch_url)
        console.error = original_console_error
    })

    test('fetch_url sends correct request', async assert => {
        const test_path = '/test/path'
        const test_payload = { key: 'value' }

        mock_fetch.set_response(test_path, test_payload)
        const response = await handler.fetch_url(test_path, test_payload)

        assert.ok(response.ok                                                      , 'Response is successful')
        assert.equal(response.status                    , 200                      , 'Status is 200')
        assert.deepEqual(await response.json()          , test_payload             , 'Returns correct data')
    })

    test('fetch_url handles errors', async assert => {
        const test_path = '/error/path'
        mock_fetch.set_response(test_path, {}, 500)

        const response = await handler.fetch_url(test_path, {})
        assert.notOk(response.ok                                                   , 'Response shows error')
        assert.equal(response.status                    , 500                      , 'Status is 500')
    })

    // Previous constructor, payload and uuid tests remain unchanged
    test('stream_response handles successful stream', async assert => {
        const chunks = ['Hello', ' World', '!'];

        mock_fetch.set_stream_response(handler.api_path, chunks);

        const received_chunks = [];

        const result = await handler.stream_response(
            MOCK_USER_PROMPT,
            MOCK_SYSTEM_PROMPTS,
            { onChunk: chunk => received_chunks.push(chunk) });

        assert.equal(result, 'Hello World!');
        assert.deepEqual(received_chunks, ['Hello', 'Hello World', 'Hello World!']);
    });

    test('stream_response handles errors', async assert => {
        const fetch_callback = () => {
            throw new Error('Network error')
        }
        mock_fetch.set_stream_response(handler.api_path, fetch_callback);

        const error_callback = (error) => {
            assert.equal(error.message, 'Network error'              , 'Error callback received')
        }

        try {
            await handler.stream_response(MOCK_USER_PROMPT, MOCK_SYSTEM_PROMPTS, { onError: error_callback })
            assert.notOk(true                                       , 'Should throw error')
        } catch (error) {
            assert.equal(error.message, 'Network error'              , 'Throws network error')
        }
    })

    test('create_payload with default system_prompts and config', assert => {
        const payload              = handler.create_payload(MOCK_USER_PROMPT)
        const chat_thread_id       = payload.chat_thread_id
        const user_data_session_id = payload.user_data.session_id
        const expected_payload = { chat_thread_id: chat_thread_id   ,
                                   temperature   : 0                ,
                                   user_prompt   : 'test prompt'    ,
                                   images        : []               ,
                                   system_prompts: []               ,
                                   histories     : []               ,
                                   user_data     : { session_id       : user_data_session_id     ,
                                                     selected_platform: 'Groq (Free)'            ,
                                                     selected_provider: '1. Meta'                ,
                                                     selected_model   : 'llama-3.1-70b-versatile'},
                                   stream         : true                                          }
        assert.deepEqual(payload, expected_payload)
    })

    test('stream_response with default system_prompts and config', async (assert) => {
        assert.expect(6)
        const chunks                = ['Hello', ' World', '!'];
        const messages_on_chunk     = []
        const messages_on_complete  = []
        mock_fetch.set_stream_response(handler.api_path, chunks);
        await handler.stream_response(MOCK_USER_PROMPT)

        const callbacks      = { onChunk    : (message) => { assert.ok(true); messages_on_chunk   .push(message) },
                                 onComplete : (message) => { assert.ok(true); messages_on_complete.push(message) }}
        const system_prompts = null
        mock_fetch.set_stream_response(handler.api_path, chunks);
        await handler.stream_response(MOCK_USER_PROMPT, system_prompts, callbacks)
        assert.deepEqual(messages_on_chunk   , ['Hello', 'Hello World', 'Hello World!'])
        assert.deepEqual(messages_on_complete, [                        'Hello World!'])
        
    })

})