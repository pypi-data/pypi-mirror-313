import WebC__Target_Div      from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component         from '../../../js/core/Web_Component.mjs'
import WebC__Document__Chat  from '../../../js/cbr/document-assistant/WebC__Document__Chat.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'
import CBR_Events from "../../../js/cbr/CBR_Events.mjs";

const { module, test , only} = QUnit

const MOCK_FILE_ID = 'test-file-123'
const MOCK_CONTENT = '# Test Document Content'
const MOCK_RESPONSE = {
    status: 'ok',
    data: {
        response_json: {
            document: {
                summary: 'Test summary',
                changes: [
                    {
                        type: 'addition',
                        reason: 'Added new section'
                    }
                ]
            }
        }
    }
}

module('WebC__Document__Chat', hooks => {
    let target_div
    let chat
    let original_marked

    hooks.before(async (assert) => {
        assert.timeout(10)
        setup_mock_responses()
        set_mock_response('https://osbot-llms.dev.aws.cyber-boardroom.com/json-prompt/improve-document', 'POST', MOCK_RESPONSE)

        original_marked = window.marked
        window.marked = { marked: (text) => text }

        target_div = WebC__Target_Div.add_to_body()
        chat = await target_div.append_child(WebC__Document__Chat, {
            'file-id': MOCK_FILE_ID,
            'content': MOCK_CONTENT
        })
        await chat.wait_for__component_ready()
    })

    hooks.beforeEach(async () => {
        //chat.query_selector('.chat-messages').innerHTML = ''
        chat.messages = []
        await chat.refresh_ui()
    })
    hooks.after(() => {
        window.marked = original_marked
        chat.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(chat.tagName.toLowerCase()        , 'webc-document-chat'     , 'Has correct tag name')
        assert.equal(chat.constructor.element_name     , 'webc-document-chat'     , 'Has correct element name')
        assert.equal(chat.constructor.name             , 'WebC__Document__Chat'   , 'Has correct class name')
        assert.equal(chat.file_id                     , MOCK_FILE_ID              , 'Sets file ID')
        assert.equal(chat.content                     , MOCK_CONTENT              , 'Sets content')

        assert.ok(chat.shadowRoot                                                 , 'Has shadow root')
        assert.ok(chat.api_invoke                                                 , 'Has API__Invoke')
        assert.ok(chat instanceof Web_Component                                   , 'Extends Web_Component')
        assert.ok(chat instanceof HTMLElement                                     , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = chat.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                              , 'Has CSS rules')
        assert.ok(css_rules['.chat-container']                                   , 'Has container styles')
        assert.ok(css_rules['.chat-messages']                                    , 'Has messages styles')
        assert.ok(css_rules['.message']                                          , 'Has message styles')
        assert.ok(css_rules['.chat-input']                                       , 'Has input styles')
    })

    test('renders initial UI correctly', assert => {
        const container = chat.query_selector('.chat-container')
        assert.ok(container                                                      , 'Container exists')

        const header = chat.query_selector('.chat-header')
        assert.ok(header                                                         , 'Header exists')
        assert.ok(header.textContent.includes('Document Assistant')              , 'Shows title')

        const messages = chat.query_selector('.chat-messages')
        assert.ok(messages                                                       , 'Messages container exists')

        const input = chat.query_selector('.chat-input')
        assert.ok(input                                                          , 'Input exists')
        assert.equal(input.tagName.toLowerCase()       , 'textarea'              , 'Input is textarea')

        const send_btn = chat.query_selector('.send-button')
        assert.ok(send_btn                                                       , 'Send button exists')
    })

    test('adds initial messages', assert => {
        const messages = chat.query_selector_all('.message-system')
        assert.ok(messages.length >= 2                                           , 'Shows initial messages')
        assert.ok(messages[0].textContent.includes('Hello!')                     , 'Shows welcome message')
        assert.ok(messages[1].textContent.includes('💡')                         , 'Shows suggestions')
    })

    test('handles message sending', async assert => {
        const input = chat.query_selector('.chat-input')
        const send_btn = chat.query_selector('.send-button')
        const test_message = 'Improve document structure'

        input.value = test_message
        send_btn.click()

        const user_msg = chat.query_selector('.message-user')
        assert.equal(user_msg.textContent             , test_message             , 'Shows user message')

        await chat.wait_for_event('diff:show')
        const assistant_msg = chat.query_selector('.message-assistant')
        assert.ok(assistant_msg.textContent.includes('Changes Summary')          , 'Shows response')
    })

    test('handles document updates', assert => {
        const new_content = '# Updated Content'
        window.dispatchEvent(new CustomEvent('document-updated', {
            detail: {
                file_id: MOCK_FILE_ID,
                content: new_content
            }
        }))

        assert.equal(chat.content                     , new_content              , 'Updates content')
        const update_msg = chat.query_selector('.message-system:last-child')
        assert.ok(update_msg.textContent.includes('Document updated')            , 'Shows update message')
    })
    //
    test('prevents concurrent streaming', async assert => {
        chat.streaming = true
        const input = chat.query_selector('.chat-input')
        const send_btn = chat.query_selector('.send-button')

        input.value = 'Test message'
        send_btn.click()

        const messages = chat.query_selector_all('.message')
        const initial_count = messages.length

        assert.equal(chat.query_selector_all('.message').length, initial_count   , 'No new messages during streaming')

        assert.deepEqual(await chat.send_message(), undefined )
        chat.streaming = false

    })

    test('handles API errors', async assert => {
        set_mock_response('https://osbot-llms.dev.aws.cyber-boardroom.com/json-prompt/improve-document', 'POST', null, 500)

        const input = chat.query_selector('.chat-input')
        const send_btn = chat.query_selector('.send-button')

        input.value = 'Test message'
        send_btn.click()

        await chat.wait_for_event(CBR_Events.CBR__LLM__REQUEST__ERROR)
        const error_msg = chat.query_selector('.message-assistant')
        assert.equal(error_msg.textContent, 'Error: Failed to get response' , 'Shows error message')
    })

    test('handles enter key', async assert => {
        const input = chat.query_selector('.chat-input')
        input.value = 'Test message'

        input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }))

        const message = chat.query_selector('.message-user')
        assert.ok(message                               , 'Sends on enter')
        assert.equal(message.textContent, 'Test message', 'Shows correct message')
    })

    test('handles empty content attribute', assert => {
        const chat_no_content = WebC__Document__Chat.create()
        chat_no_content.load_attributes()
        assert.equal(chat_no_content.content, '', 'Sets empty string as default content')
    })

    test('handles streaming state correctly', async assert => {
        assert.expect(4)

        const input = chat.query_selector('.chat-input')
        const send_btn = chat.query_selector('.send-button')
        input.value = 'Test message'

        // First message - should go through
        assert.notOk(chat.streaming, 'Initially not streaming')
        send_btn.click()
        assert.ok(chat.streaming, 'Sets streaming flag')

        // Second message - should be blocked
        input.value = 'Second message'
        send_btn.click()

        const messages = chat.query_selector_all('.message-user')
        assert.equal(messages.length, 1, 'Only first message sent')
        assert.equal(messages[0].textContent, 'Test message', 'Shows correct message')
    })

    test ('handles invalid API response format', async assert => {
        // Mock invalid response format
        set_mock_response('https://osbot-llms.dev.aws.cyber-boardroom.com/json-prompt/improve-document',
            'POST',
            { status: 'ok', data: { something_else: true } }
        )

        const input = chat.query_selector('.chat-input')
        const send_btn = chat.query_selector('.send-button')

        input.value = 'Test message'
        send_btn.click()

        await chat.wait_for_event(CBR_Events.CBR__LLM__REQUEST__ERROR)
        const error_msg = chat.query_selector('.message-assistant')
        assert.ok(error_msg.textContent.includes('Invalid response format'),
                 'Shows invalid format error')
    })

    // only('adds action buttons with correct event handlers', async assert => {
    //     //assert.expect(4)
    //     const received_events = []
    //     const test_result = {
    //         document: {
    //             changes: ['test change']
    //         }
    //     }
    //
    //     // Set up event handling methods
    //     const on_diff_show        = () => received_events.push('diff:show')
    //     const on_changes_accept   = (event) => {
    //         received_events.push('changes:accept')
    //         assert.deepEqual(event.detail.changes, test_result.document, 'Accept event includes changes')
    //     }
    //     const on_changes_reject   = () => received_events.push('changes:reject')
    //
    //     // Add event listeners
    //     window.addEventListener('diff:show'      , on_diff_show      )
    //     window.addEventListener('changes:accept' , on_changes_accept )
    //     window.addEventListener('changes:reject' , on_changes_reject )
    //
    //     // Set up test message
    //     chat.current_message = { id: 'test-123' }
    //     const msg_div = document.createElement('div')
    //     msg_div.id = `msg-${chat.current_message.id}`
    //     chat.shadowRoot.appendChild(msg_div)
    //
    //     // Add action buttons
    //     chat.add_action_buttons(test_result)
    //
    //     // Verify buttons were added
    //     const actions = chat.query_selector('.message-actions')
    //     assert.ok(actions, 'Action buttons container exists')
    //
    //     // Click each button and verify events
    //     const preview_btn = actions.querySelector('.preview-btn')
    //     const accept_btn  = actions.querySelector('.accept-btn')
    //     const reject_btn  = actions.querySelector('.reject-btn')
    //
    //     preview_btn.click()
    //     accept_btn.click()
    //     reject_btn.click()
    //
    //     console.log(received_events)
    //     // assert.deepEqual(received_events,
    //     //                 ['diff:show', 'changes:accept', 'changes:reject'],
    //     //                 'All button clicks trigger correct events')
    //     //
    //     // assert.ok(preview_btn.querySelector('.icon-sm'),
    //     //          'Buttons have icons with correct styling')
    //
    //     // Clean up event listeners
    //     window.removeEventListener('diff:show'      , on_diff_show      )
    //     window.removeEventListener('changes:accept' , on_changes_accept )
    //     window.removeEventListener('changes:reject' , on_changes_reject )
    //
    //     // Clean up DOM
    //     msg_div.remove()
    // })
})