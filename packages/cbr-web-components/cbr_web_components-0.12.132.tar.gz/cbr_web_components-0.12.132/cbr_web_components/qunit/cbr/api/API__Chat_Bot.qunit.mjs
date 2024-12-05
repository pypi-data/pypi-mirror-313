import API__Chat_Bot                                from '../../../js/cbr/api/API__Chat_Bot.mjs'
import { setup_mock_responses, set_mock_response }  from '../../../js/testing/Mock_API__Data.mjs'

const { module, test } = QUnit

const MOCK_CHAT_ID   = 'test-chat-123'
const MOCK_CHAT_PATH = '/chats/test-chat-123'
const MOCK_RESPONSE  = { chat_path: MOCK_CHAT_PATH }

module('API__Chat_Bot', hooks => {
    let api_chat_bot

    hooks.before(() => {
        setup_mock_responses()
        api_chat_bot = new API__Chat_Bot()
    })

    test('constructor initializes correctly', assert => {
        assert.ok(api_chat_bot.api_invoke                                                 , 'Has API invoke instance'   )
        assert.equal(api_chat_bot.url_current_user_add_chat_id, '/api/user-data/chats/chat-add?chat_path=',
                                                                                          'Has correct base URL'       )
    })

    test('add_chat_id handles successful response', async assert => {
        set_mock_response(`/api/user-data/chats/chat-add?chat_path=/${MOCK_CHAT_ID}`, 'POST', MOCK_RESPONSE)

        const result = await api_chat_bot.add_chat_id(MOCK_CHAT_ID)
        assert.deepEqual(result, MOCK_RESPONSE                                            , 'Returns correct response' )
    })

    test('add_chat_id handles API error', async assert => {
        set_mock_response(`/api/user-data/chats/chat-add?chat_path=/${MOCK_CHAT_ID}`, 'POST', null, 500)

        const result = await api_chat_bot.add_chat_id(MOCK_CHAT_ID)
        assert.deepEqual(result, { chat_path: null }                                     , 'Returns null path on error')
    })

    test('add_chat_id constructs correct URL', async assert => {
        const test_chat_id = 'custom-id-789'
        set_mock_response(`/api/user-data/chats/chat-add?chat_path=/${test_chat_id}`, 'POST',
                         { chat_path: `/chats/${test_chat_id}` })

        const result = await api_chat_bot.add_chat_id(test_chat_id)
        assert.equal(result.chat_path, `/chats/${test_chat_id}`                          , 'URL properly constructed' )
    })

    test('add_chat_id handles empty chat ID', async assert => {
        const result = await api_chat_bot.add_chat_id('')
        assert.deepEqual(result, { chat_path: null }                                     , 'Handles empty chat ID'    )
    })

    test('add_chat_id handles non-string inputs', async assert => {
        const inputs = [null, undefined, 123, {}, []]

        for (const input of inputs) {
            const result = await api_chat_bot.add_chat_id(input)
            assert.deepEqual(result, { chat_path: null }                                 , `Handles ${typeof input} input`)
        }
    })
})