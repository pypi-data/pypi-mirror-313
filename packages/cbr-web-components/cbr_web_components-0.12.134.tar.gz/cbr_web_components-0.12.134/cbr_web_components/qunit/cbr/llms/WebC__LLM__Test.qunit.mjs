import WebC__Target_Div        from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component           from '../../../js/core/Web_Component.mjs'
import WebC__LLM__Test         from '../../../js/cbr/llms/WebC__LLM__Test.mjs'
import { Mock_Fetch }          from '../../../js/testing/Mock_Fetch.mjs'
import LLM__Handler            from '../../../js/cbr/llms/LLM__Handler.mjs'
import CBR_Events              from "../../../js/cbr/CBR_Events.mjs";

const { module, test} = QUnit

module('WebC__LLM__Test', hooks => {
    let target_div
    let llm_test
    let mock_fetch

    hooks.before(async (assert) => {
        assert.timeout(10)
        mock_fetch = Mock_Fetch.apply_mock(LLM__Handler)
        mock_fetch.set_stream_response('/api/llms/chat/completion', ['Response chunk'])

        target_div = WebC__Target_Div.add_to_body()
        llm_test = await target_div.append_child(WebC__LLM__Test)
        await llm_test.wait_for__component_ready()
    })

    hooks.after(() => {
        Mock_Fetch.restore_original(LLM__Handler)
        llm_test.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(llm_test.tagName.toLowerCase()         , 'webc-llm-test'          , 'Has correct tag name'     )
        assert.equal(llm_test.constructor.element_name      , 'webc-llm-test'          , 'Has correct element name' )
        assert.equal(llm_test.constructor.name              , 'WebC__LLM__Test'        , 'Has correct class name'   )

        assert.ok(llm_test.shadowRoot                                                   , 'Has shadow root'          )
        assert.ok(llm_test.llm_handler                                                 , 'Has LLM handler'          )
        assert.ok(llm_test.response_handler                                            , 'Has response handler'     )
        assert.ok(llm_test instanceof Web_Component                                    , 'Extends Web_Component'    )
        assert.ok(llm_test instanceof HTMLElement                                      , 'Is HTML Element'          )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = llm_test.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                    , 'Has CSS rules'            )
        assert.ok(css_rules['.test-container']                                         , 'Has container styles'     )
        assert.ok(css_rules['.input-section']                                          , 'Has input styles'         )
        assert.ok(css_rules['.response-section']                                       , 'Has response styles'      )
    })

    test('renders initial state correctly', assert => {
        const system_prompt = llm_test.query_selector('#system-prompt')
        const user_prompt   = llm_test.query_selector('#user-prompt'  )
        const submit_btn    = llm_test.query_selector('#submit-prompt')
        const clear_btn     = llm_test.query_selector('#clear-form'   )
        const response_div  = llm_test.query_selector('#response-container')

        assert.ok(system_prompt                                                        , 'System prompt exists'     )
        assert.ok(user_prompt                                                          , 'User prompt exists'       )
        assert.ok(submit_btn                                                           , 'Submit button exists'     )
        assert.ok(clear_btn                                                            , 'Clear button exists'      )
        assert.ok(response_div                                                         , 'Response container exists')
    })

    test('handles form submission', async assert => {
        assert.expect(1)
        const done = assert.async()
        const system_prompt = llm_test.query_selector('#system-prompt')
        const user_prompt   = llm_test.query_selector('#user-prompt'  )
        const submit_btn    = llm_test.query_selector('#submit-prompt')

        system_prompt.value = 'System test'
        user_prompt.value   = 'User test'

        const on__llm_request_finished = (event) => {
            const response_div = llm_test.query_selector('#response-container')
            assert.ok(response_div.innerHTML.includes('Response chunk'))
            done()
        }

        await llm_test.add_window_event_listener(CBR_Events.CBR__LLM__REQUEST__FINISHED, on__llm_request_finished)
        submit_btn.click()
    })

    test('handles empty user prompt', async assert => {
        const user_prompt   = llm_test.query_selector('#user-prompt'  )
        const submit_btn    = llm_test.query_selector('#submit-prompt')
        const response_div  = llm_test.query_selector('#response-container')
        const initial_content = response_div.innerHTML
        user_prompt.value = ''
        submit_btn.click()
        assert.deepEqual(response_div.innerHTML, initial_content  , 'No change without prompt' )

    })

    test('handles clear operation', async assert => {
        const system_prompt = llm_test.query_selector('#system-prompt')
        const user_prompt   = llm_test.query_selector('#user-prompt'  )
        const clear_btn     = llm_test.query_selector('#clear-form'   )
        const response_div  = llm_test.query_selector('#response-container')

        system_prompt.value = 'Test system'
        user_prompt.value   = 'Test user'
        llm_test.current_response = 'Test response'
        llm_test.update_response()
        assert.ok(llm_test.current_response.includes('Test response')                  , 'Response is there' )
        clear_btn.click()
        assert.equal(system_prompt.value               , ''                            , 'Clears system prompt'    )
        assert.equal(user_prompt.value                 , ''                            , 'Clears user prompt'      )
        assert.notOk(llm_test.current_response.includes('Test response')               , 'Clears current response' )
        assert.equal(response_div.innerHTML, '<div class="llm-response response-content"></div>')           // todo: check if this is correct
    })

    test('handles stream error', async assert => {
        mock_fetch.set_response('/api/llms/chat/completion', null, 500)

        const user_prompt = llm_test.query_selector('#user-prompt')
        const submit_btn  = llm_test.query_selector('#submit-prompt')

        const on_llm_request_error = (event) => {
            assert.equal(event.detail.error.message, "Cannot read properties of undefined (reading \'getReader\')")
            const response_div = llm_test.query_selector('#response-container')
            assert.ok(response_div.innerHTML.includes('Error') , 'Shows error message'     )
        }
        user_prompt.value = 'Test prompt'
        submit_btn.click()

        await llm_test.add_window_event_listener(CBR_Events.CBR__LLM__REQUEST__ERROR, on_llm_request_error)
    })

    test('css_rules return correct styles', assert => {
        const rules = llm_test.css_rules()

        assert.deepEqual(rules['.test-container'], {
            padding         : "1rem"                      ,
            backgroundColor: "#fff"                       ,
            borderRadius   : "0.5rem"                     ,
            boxShadow      : "0 2px 4px rgba(0,0,0,0.1)"
        }, 'Container styles are correct')

        assert.deepEqual(rules['.response-content'], {
            fontFamily    : "system-ui, sans-serif"      ,
            lineHeight   : "1.6"
        }, 'Response content styles are correct')
    })
})