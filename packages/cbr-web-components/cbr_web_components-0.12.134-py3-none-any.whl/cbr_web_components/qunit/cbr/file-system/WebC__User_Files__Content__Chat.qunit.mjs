import WebC__Target_Div                             from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                                from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__Content__Chat              from '../../../js/cbr/file-system/WebC__User_Files__Content__Chat.mjs'
import { setup_mock_responses, set_mock_response }  from '../../../js/testing/Mock_API__Data.mjs'

const { module, test, only , skip} = QUnit

const MOCK_FILE_ID = 'test-file-123'
const MOCK_CONTENT = 'Test file content'
const MOCK_SUMMARY = '"Test summary"'
const MOCK_FILE_DATA = {
    file_data: {
        name    : 'test.md',
        size    : 1024,
        type    : 'text/markdown'
    },
    file_bytes__base64: btoa(MOCK_CONTENT),
    file_summary: MOCK_SUMMARY
}

module('WebC__User_Files__Content__Chat', hooks => {
    let target_div
    let chat_component

    hooks.before(async () => {
        setup_mock_responses()
        set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`, 'GET', { data: MOCK_FILE_DATA } )

        target_div = WebC__Target_Div.add_to_body()
        chat_component = await target_div.append_child(WebC__User_Files__Content__Chat,
            { file_id: MOCK_FILE_ID })
        await chat_component.wait_for__component_ready()
    })

    hooks.after(() => {
        chat_component.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(chat_component.tagName.toLowerCase()    , 'webc-user-files-content-chat' , 'Has correct tag name'     )
        assert.equal(chat_component.constructor.element_name , 'webc-user-files-content-chat' , 'Has correct element name' )
        assert.equal(chat_component.constructor.name        , 'WebC__User_Files__Content__Chat', 'Has correct class name' )

        assert.ok(chat_component.shadowRoot                                                   , 'Has shadow root'          )
        assert.ok(chat_component.api_invoke                                                   , 'Has API__Invoke'         )
        assert.equal(chat_component.file_id                 , MOCK_FILE_ID                    , 'Sets file_id from attrs' )
        assert.equal(chat_component.chat_mode               , 'content'                       , 'Default chat mode set'   )

        assert.ok(chat_component instanceof Web_Component                                     , 'Extends Web_Component'    )
        assert.ok(chat_component instanceof HTMLElement                                       , 'Is HTML Element'          )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = chat_component.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                          , 'Has CSS rules'            )
        assert.ok(css_rules['.content-chat-container']                                       , 'Has container styles'     )
        assert.ok(css_rules['.chat-toolbar']                                                 , 'Has toolbar styles'       )
        assert.ok(css_rules['.chat-container']                                               , 'Has chat styles'          )
    })

    test('loads file data correctly', async assert => {
        assert.ok(chat_component.content                                                      , 'Content is loaded'        )
        assert.equal(chat_component.content                 , MOCK_CONTENT                    , 'Content matches mock'     )
        assert.ok(chat_component.file_summary                                                 , 'Summary is loaded'        )
        assert.deepEqual(chat_component.file_summary        , JSON.parse(MOCK_SUMMARY)        , 'Summary correctly parsed' )
    })

    test('renders initial state correctly', async assert => {
        const container = chat_component.query_selector('.content-chat-container')
        assert.ok(container                                                                   , 'Main container exists'    )

        const toolbar = chat_component.query_selector('.chat-toolbar')
        assert.ok(toolbar                                                                     , 'Toolbar exists'           )

        const mode_btn = toolbar.querySelector('.btn')
        assert.ok(mode_btn                                                                    , 'Mode toggle button exists')
        assert.ok(mode_btn.classList.contains('btn-primary')                                  , 'Button has primary style' )
        assert.equal(mode_btn.textContent                   , 'Chat with Summary'             , 'Correct button text'      )

        const chatbot = chat_component.query_selector('chatbot-openai')
        assert.ok(chatbot                                                                     , 'Chatbot component exists' )
        assert.ok(chatbot.getAttribute('system_prompt').includes(MOCK_CONTENT)                , 'Chatbot has content prompt')
    })

    test('toggles chat mode correctly', async assert => {
        assert.equal(chat_component.chat_mode               , 'content'                       , 'Initial mode is content'  )

        chat_component.toggle_chat_mode()
        const mode_btn_1 = chat_component.query_selector('.chat-toolbar .btn')
        const chatbot_1  = chat_component.query_selector('chatbot-openai')

        assert.ok   (mode_btn_1.classList.contains('btn-outline-primary')                     , 'Button style updated'     )
        assert.ok   (chatbot_1.getAttribute('system_prompt').includes('summary')              , 'Updates system prompt'    )
        assert.equal(chat_component.chat_mode               , 'summary'                       , 'Switches to summary mode' )
        assert.equal(mode_btn_1.textContent                 , 'Chat with Content'             , 'Button text updated'      )

        chat_component.toggle_chat_mode()
        const mode_btn_2 = chat_component.query_selector('.chat-toolbar .btn')
        const chatbot_2  = chat_component.query_selector('chatbot-openai')
        assert.equal(chat_component.chat_mode               , 'content'                       , 'Initial mode is content'  )
        assert.ok   (mode_btn_2.classList.contains('btn-primary')                       , 'Button style updated'     )
        assert.ok   (chatbot_2.getAttribute('system_prompt').includes('discussing a file')                , 'Updates system prompt'    )


    })

    test('generates correct system prompts', assert => {

        chat_component.chat_mode = 'content'
        let prompt = chat_component.get_system_prompt()                                              // Test 'content' mode prompt
        assert.ok(prompt.includes(MOCK_CONTENT)                     , 'Content included in prompt')
        assert.ok(prompt.includes('discussing a file\'s content')   , 'Correct context for content')


        chat_component.chat_mode = 'summary'                                                        // Test 'summary' mode prompt
        prompt                   = chat_component.get_system_prompt()

        assert.ok(prompt.includes(JSON.parse(MOCK_SUMMARY))       , 'Summary included in prompt')
        assert.ok(prompt.includes('discussing a file\'s summary') , 'Correct context for summary')
        chat_component.chat_mode = 'content'
    })

    test('adds event handlers correctly', async assert => {
        assert.expect(6)
        const mode_btn_1 = chat_component.query_selector('.mode-btn')                   // get a reference to the change mode-btn

        assert.deepEqual(chat_component.chat_mode, 'content')                           //  confirm we are in the 'content' mode
        assert.deepEqual(mode_btn_1.innerHTML, 'Chat with Summary')                     // confirm the button text is 'Chat with Summary'

        mode_btn_1.click()                                                              // click on that button
        await chat_component.wait_for__component_ready()                                // wait until the ui reloads
        const mode_btn_2 = chat_component.query_selector('.chat-toolbar .btn')          // get a reference to the new change mode-btn (recreated since the entire UI was rebuilt)
        assert.deepEqual(chat_component.chat_mode, 'summary')                           // confirm sure the mode has changed to 'summary'
        assert.deepEqual(mode_btn_2.innerHTML, 'Chat with Content')                     // confirm that mode_btn_2 has changed to 'Chat with Content'

        mode_btn_2.click()                                                              // click on the new button
        const mode_btn_3 = chat_component.query_selector('.chat-toolbar .btn')          // get another reference to the change mode-btn (recreated since the entire UI was rebuilt)
        await chat_component.wait_for__component_ready()                                // wait until the ui reloads
        assert.deepEqual(chat_component.chat_mode, 'content')                           // confirm sure the mode has changed back to 'content'
        assert.deepEqual(mode_btn_3.innerHTML, 'Chat with Summary')                     // confirm that mode_btn_3 has changed back to 'Chat with Summary'
    })
})