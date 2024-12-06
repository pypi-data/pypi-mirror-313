import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__PastChats__Welcome                    from '../../../js/cbr/web-components/WebC__PastChats__Welcome.mjs'
import { Mock_Fetch }                              from '../../../js/testing/Mock_Fetch.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'
import LLM__Handler                                from "../../../js/cbr/llms/LLM__Handler.mjs"

const { module, test, only , skip} = QUnit

const MOCK_USER_PROFILE = {
    first_name      : 'Test User',
    expertise_level : 'intermediate',
    interests      : ['security', 'ai']
}

const MOCK_CHAT_DATA = {
    saved_chats: {
        'chat1': {
            history_size    : 10,
            last_user_prompt: 'Security testing',
            prompts_size    : 500,
            responses_size  : 1000
        },
        'chat2': {
            history_size    : 5,
            last_user_prompt: 'AI integration',
            prompts_size    : 300,
            responses_size  : 800
        }
    }
}

const MOCK_WELCOME_MESSAGE = "Welcome back Test User! You've had 2 engaging conversations covering topics like security testing and AI integration. Your discussions have generated over 2.5KB of valuable insights."

module('WebC__PastChats__Welcome', hooks => {
    let target_div
    let welcome
    let mock_fetch

    hooks.before(async () => {
        setup_mock_responses()
        set_mock_response('/api/user-data/user/user-profile', 'GET', MOCK_USER_PROFILE)
        set_mock_response('/api/user-data/chats/chats'      , 'GET', MOCK_CHAT_DATA)

        mock_fetch = Mock_Fetch.apply_mock(LLM__Handler)
        mock_fetch.set_stream_response('/api/llms/chat/completion', [MOCK_WELCOME_MESSAGE])

        target_div = WebC__Target_Div.add_to_body()
        welcome = await target_div.append_child(WebC__PastChats__Welcome)
        await welcome.wait_for__component_ready()
    })

    hooks.after(() => {
        welcome.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(welcome.tagName.toLowerCase()        , 'webc-pastchats-welcome'  , 'Has correct tag name')
        assert.equal(welcome.constructor.element_name     , 'webc-pastchats-welcome'  , 'Has correct element name')
        assert.equal(welcome.constructor.name             , 'WebC__PastChats__Welcome', 'Has correct class name')
        assert.ok(welcome.shadowRoot                                                  , 'Has shadow root')
        assert.ok(welcome.api_invoke                                                  , 'Has API__Invoke')
        assert.ok(welcome instanceof Web_Component                                    , 'Extends Web_Component')
        assert.ok(welcome instanceof HTMLElement                                      , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = welcome.css_rules()
        assert.ok(Object.keys(css_rules).length > 0                                  , 'Has CSS rules')
        assert.ok(css_rules['.card']                                                 , 'Has card styles')
        assert.ok(css_rules['.welcome-message']                                      , 'Has welcome message styles')
    })

    test('analyzes chat history correctly', assert => {
        const analytics = welcome.analyze_chat_history(MOCK_CHAT_DATA.saved_chats)

        assert.equal    (analytics.total_chats         , 2      , 'Counts total chats'           )
        assert.equal    (analytics.total_messages      , 15     , 'Sums total messages'          )
        assert.equal    (analytics.topics.length       , 2      , 'Extracts unique topics'       )
        assert.equal    (analytics.total_prompts_size  , 800    , 'Calculates prompts size'      )
        assert.equal    (analytics.total_responses_size, 1800   , 'Calculates responses size'    )
        assert.deepEqual(analytics.topics              , [ 'Security testing', 'AI integration' ])
    })

    test('renders welcome message correctly', async assert => {
        const card    = welcome.query_selector('.card')
        const body    = welcome.query_selector('.card-body')
        const content = welcome.query_selector('.welcome-message')

        assert.ok(card                                                               , 'Card container exists')
        assert.ok(card.classList.contains('mb-4')                                    , 'Has margin class')
        assert.ok(body                                                               , 'Card body exists')
        assert.ok(content                                                            , 'Content exists')
        assert.ok(content.innerHTML.trim().includes(MOCK_WELCOME_MESSAGE)                   , 'Shows welcome message')
    })

    test('handles failed user data fetch', async assert => {
        set_mock_response('/api/user-data/user/user-profile', 'GET', null)
        set_mock_response('/api/user-data/chats/chats', 'GET', null)

        welcome = await target_div.append_child(WebC__PastChats__Welcome)
        await welcome.wait_for__component_ready()

        const content = welcome.query_selector('.welcome-message')
        assert.ok(welcome                                                            , 'Renders without user data')
        assert.equal(content.innerHTML.trim(), ''                                    , 'Shows empty message')
    })

    test('handles empty chat history', async assert => {
        set_mock_response('/api/user-data/chats/chats', 'GET', { saved_chats: {} })

        welcome = await target_div.append_child(WebC__PastChats__Welcome)
        await welcome.wait_for__component_ready()

        const analytics = welcome.analyze_chat_history({})
        assert.equal(analytics.total_chats, 0                                        , 'Handles empty chats')
        assert.equal(analytics.total_messages, 0                                     , 'Zero total messages')
        assert.equal(analytics.topics.length, 0                                      , 'No topics found')
    })

    test('handles stream failure', async assert => {
        mock_fetch.set_response('/api/llms/chat/completion', null, 500)

        welcome = await target_div.append_child(WebC__PastChats__Welcome)
        await welcome.wait_for__component_ready()

        const content = welcome.query_selector('.welcome-message')
        assert.ok(content                                                            , 'Renders despite stream error')
    })

    test('handles incremental stream updates', async assert => {
        set_mock_response('/api/user-data/user/user-profile', 'GET', MOCK_USER_PROFILE)
        const chunks = ['Welcome', ' back', ' Test User!']
        mock_fetch.set_stream_response('/api/llms/chat/completion', chunks)

        welcome = await target_div.append_child(WebC__PastChats__Welcome)
        await welcome.wait_for__component_ready()

        const content = welcome.query_selector('.welcome-message')
        assert.equal(content.innerHTML.trim(), 'Welcome back Test User!'      , 'Shows complete message')
    })

    test('handles missing message properties', async assert => {
        const incomplete_chats = {
            chat1: { history_size: 5 },                     // Missing other properties
            chat2: { last_user_prompt: 'test' }            // Different missing properties
        }

        const analytics = welcome.analyze_chat_history(incomplete_chats)
        assert.equal(analytics.total_chats     , 2                                   , 'Counts chats correctly')
        assert.equal(analytics.total_messages  , 5                                   , 'Handles missing sizes')
        assert.equal(analytics.topics.length   , 1                                   , 'Extracts available topics')
        assert.equal(analytics.total_prompts_size, 0                                 , 'Handles missing sizes')
    })

    test('handles marked library parsing', async assert => {
       const original_marked = window.marked
       window.marked = { marked: (text) => `<p><strong>Test</strong> message</p>` }

       welcome.show_message('**Test** message')

       const content = welcome.query_selector('.card-text')
       assert.equal(content.innerHTML.trim(), '<p><strong>Test</strong> message</p>', 'Parses markdown when marked available')

       window.marked = original_marked
    })

    test('generate_welcome - handles failed data fetch', async assert => {
        assert.notEqual(welcome.welcome_message, '')
        mock_fetch.set_stream_response('/api/llms/chat/completion', null)
        await welcome.generate_welcome()
        assert.equal(welcome.welcome_message, '')
    })
})