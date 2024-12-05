import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__Athena__Welcome                       from '../../../js/cbr/web-components/WebC__Athena__Welcome.mjs'
import { Mock_Fetch }                              from '../../../js/testing/Mock_Fetch.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'
import LLM__Handler                                from "../../../js/cbr/llms/LLM__Handler.mjs"

const { module, test, only } = QUnit

const MOCK_USER_DATA = {
    name           : 'Test User',
    expertise_level: 'intermediate',
    interests      : ['security', 'ai'],
    preferences    : { theme: 'light', language: 'en' }
}

const MOCK_WELCOME_MESSAGE = "Welcome Test User! Glad to see your interest in security and AI. I notice you have intermediate expertise - I'll tailor my responses accordingly."

module('WebC__Athena__Welcome', hooks => {
    let target_div
    let welcome
    let mock_fetch

    hooks.before(async () => {
        setup_mock_responses()
        set_mock_response('/api/user-data/user/user-profile', 'GET', MOCK_USER_DATA)

        mock_fetch = Mock_Fetch.apply_mock(LLM__Handler)
        mock_fetch.set_stream_response('/api/llms/chat/completion', [MOCK_WELCOME_MESSAGE])

        target_div = WebC__Target_Div.add_to_body()
        welcome = await target_div.append_child(WebC__Athena__Welcome)
        await welcome.wait_for__component_ready()
    })

    hooks.after(() => {
        welcome.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(welcome.tagName.toLowerCase()         , 'webc-athena-welcome'    , 'Has correct tag name')
        assert.equal(welcome.constructor.element_name      , 'webc-athena-welcome'    , 'Has correct element name')
        assert.equal(welcome.constructor.name              , 'WebC__Athena__Welcome'  , 'Has correct class name')
        assert.ok(welcome.shadowRoot                                                  , 'Has shadow root')
        assert.ok(welcome.api_invoke                                                  , 'Has API__Invoke')
        assert.ok(welcome.event_handler                                               , 'Has event handler')
        assert.ok(welcome instanceof Web_Component                                    , 'Extends Web_Component')
        assert.ok(welcome instanceof HTMLElement                                      , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = welcome.all_css_rules()
        assert.ok(Object.keys(css_rules).length > 0                                  , 'Has CSS rules')
        assert.ok(css_rules['.card']                                                 , 'Has card styles')
        assert.ok(css_rules['.card-body']                                            , 'Has card body styles')
        assert.ok(css_rules['.m-1']                                                  , 'Has margin utility styles')
    })

    test('renders welcome message correctly', async assert => {
        const card      = welcome.query_selector('.card')
        const card_body = welcome.query_selector('.card-body')
        const content   = welcome.query_selector('.card-text')

        assert.ok(card                                                               , 'Card container exists')
        assert.ok(card.classList.contains('h-100')                                   , 'Has full height class')
        assert.ok(card_body                                                          , 'Card body exists')
        assert.ok(content                                                            , 'Content exists')
        assert.ok(content.innerHTML.includes(MOCK_WELCOME_MESSAGE)                   , 'Shows welcome message')
    })

    test('handles failed user data fetch', async assert => {
        set_mock_response('/api/user-data/user/user-profile', 'GET', null)
        mock_fetch.set_stream_response('/api/llms/chat/completion', [''])

        const welcome_2 = await target_div.append_child(WebC__Athena__Welcome)
        await welcome_2.wait_for__component_ready()

        const content = welcome_2.query_selector('.card-text')
        assert.ok(welcome_2                                                            , 'Renders without user data')
        assert.deepEqual(welcome_2.welcome_message , '')
        assert.deepEqual(content.innerHTML.trim()  , '')

        set_mock_response('/api/user-data/user/user-profile', 'GET', MOCK_USER_DATA)
    })

    test('handles stream failure', async assert => {
        mock_fetch.set_response('/api/llms/chat/completion', null, 500)

        welcome = await target_div.append_child(WebC__Athena__Welcome)
        await welcome.wait_for__component_ready()

        const content = welcome.query_selector('.card-text')
        assert.ok(content                                                            , 'Renders despite stream error')
    })

    test('handles active session change', async assert => {
        const original_generate = welcome.generate_welcome
        const calls = []
        welcome.generate_welcome = async () => calls.push('generate_welcome')

        await welcome.handle__active_session_changed()
        assert.equal(calls.length, 1                                                 , 'Calls generate_welcome')

        welcome.generate_welcome = original_generate
    })

    test('show_message updates content', async assert => {
        const test_message = '**Test** _message_'
        welcome.show_message(test_message)

        const content = welcome.query_selector('.card-text')
        assert.equal(content.innerHTML.trim(), '**Test** _message_', 'Renders markdown correctly')
    })

    test('handles incremental stream updates', async assert => {
        const chunks = ['Hello', ' World', '!']
        mock_fetch.set_stream_response('/api/llms/chat/completion', chunks)

        welcome = await target_div.append_child(WebC__Athena__Welcome)
        await welcome.wait_for__component_ready()

        const content = welcome.query_selector('.card-text')
        assert.equal(content.innerHTML.trim(), 'Hello World!'                        , 'Shows complete message')
    })

    test('handles undefined marked library', async assert => {
       const original_marked = window.marked
       window.marked = undefined

       welcome.show_message('**Test** message')

       const content = welcome.query_selector('.card-text')
       assert.equal(content.innerHTML.trim(), '**Test** message', 'Shows raw markdown when marked undefined')

       window.marked = original_marked
    })

    test('handles marked library parsing', async assert => {
       const original_marked = window.marked
       window.marked = { marked: (text) => `<p><strong>Test</strong> message</p>` }

       welcome.show_message('**Test** message')

       const content = welcome.query_selector('.card-text')
       assert.equal(content.innerHTML.trim(), '<p><strong>Test</strong> message</p>', 'Parses markdown when marked available')

       window.marked = original_marked
    })
})