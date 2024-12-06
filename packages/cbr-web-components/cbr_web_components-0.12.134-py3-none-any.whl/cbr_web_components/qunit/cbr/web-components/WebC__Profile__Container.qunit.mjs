import WebC__Target_Div          from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component             from '../../../js/core/Web_Component.mjs'
import WebC__Profile__Container  from '../../../js/cbr/web-components/WebC__Profile__Container.mjs'
import { setup_mock_responses,
         set_mock_response }     from '../../../js/testing/Mock_API__Data.mjs'

const { module, test } = QUnit

const MOCK_PROFILE = {
    first_name              : 'John'                                ,
    last_name              : 'Doe'                                 ,
    role                   : 'Security Analyst'                    ,
    organisation           : 'Tech Corp'                           ,
    sector                : 'Technology'                          ,
    size_of_organisation   : '1000+ employees'                     ,
    country               : 'United Kingdom'                      ,
    linkedin              : 'https://linkedin.com/in/johndoe'     ,
    additional_system_prompt: 'Prefer technical details'
}

module('WebC__Profile__Container', hooks => {
    let target_div
    let container
 
    hooks.before(async () => {
        setup_mock_responses()
        set_mock_response('/api/user-data/user/user-profile', 'GET', MOCK_PROFILE)

        target_div = WebC__Target_Div.add_to_body()
        container  = await target_div.append_child(WebC__Profile__Container)
        await container.wait_for__component_ready()
    })

    hooks.after(() => {
        container .remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(container.tagName.toLowerCase()    , 'webc-profile-container', 'Has correct tag name'     )
        assert.equal(container.constructor.element_name , 'webc-profile-container', 'Has correct element name' )
        assert.equal(container.constructor.name        , 'WebC__Profile__Container', 'Has correct class name' )

        assert.ok(container.shadowRoot                                            , 'Has shadow root'          )
        assert.ok(container.api_invoke                                           , 'Has API__Invoke'          )
        assert.ok(container.channel.startsWith('profile_')                       , 'Has generated channel'    )

        assert.ok(container instanceof Web_Component                             , 'Extends Web_Component'     )
        assert.ok(container instanceof HTMLElement                               , 'Is HTML Element'          )
    })


    test('loads profile data correctly', async assert => {
        assert.deepEqual(container.current_profile, MOCK_PROFILE                 , 'Loads profile data'      )

        const first_name_input = container.query_selector('input[name="first_name"]')
        const last_name_input  = container.query_selector('input[name="last_name"]')
        const role_input      = container.query_selector('input[name="role"]')

        assert.equal(first_name_input.value         , MOCK_PROFILE.first_name   , 'Sets first name value'   )
        assert.equal(last_name_input.value          , MOCK_PROFILE.last_name    , 'Sets last name value'    )
        assert.equal(role_input.value               , MOCK_PROFILE.role         , 'Sets role value'         )
    })

    test('handles failed profile loading', async assert => {
        set_mock_response('/api/user-data/user/user-profile', 'GET', null, 500)

        const error_container = await target_div.append_child(WebC__Profile__Container)
        await error_container.wait_for__component_ready()

        assert.notOk(error_container.current_profile                            , 'No profile data on error' )
        const form = error_container.query_selector('form')
        assert.ok(form                                                          , 'Still renders form'       )
    })

    test('creates form structure correctly', assert => {
        const form = container.query_selector('form')
        assert.ok(form                                                          , 'Form exists'             )

        const title = form.querySelector('.card-title')
        assert.equal(title.textContent               , 'Update Profile'         , 'Shows correct title'     )

        const field_groups = form.querySelectorAll('.field-group')
        assert.equal(field_groups.length            , 9                        , 'Has all field groups'    )

        const submit_button = form.querySelector('button[type="submit"]')
        assert.ok(submit_button                                                 , 'Has submit button'       )
    })


    test('creates profile prompt correctly', assert => {
        const prompt = container.create_profile_prompt()

        assert.ok(prompt.includes(MOCK_PROFILE.first_name)                      , 'Includes first name'     )
        assert.ok(prompt.includes(MOCK_PROFILE.role)                            , 'Includes role'           )
        assert.ok(prompt.includes('personalized')                               , 'Includes instructions'   )
    })

    test('notifies about profile updates', assert => {
        assert.expect(3)  // Expecting 3 assertions

        let reload_called = false

        // Save original reload method
        const original_reload = container.reload_page

        // Define the event listener function
        const profileUpdateListener = (event) => {
            assert.equal(event.detail.channel      , container.channel          , 'Correct channel'         )
            assert.deepEqual(event.detail.profile  , container.current_profile  , 'Includes profile data'   )
        }

        // Setup event listener
        container.addEventListener('profile-update', profileUpdateListener)

        // Mock reload method
        container.reload_page = () => {
            reload_called = true
        }

        // Trigger the update
        container.notify_chatbot_profile_updated()

        assert.ok(reload_called                                                 , 'Reloads page'            )

        // Remove the event listener
        container.removeEventListener('profile-update', profileUpdateListener)
        // Restore original method
        container.reload_page = original_reload
    })

    test('renders chatbot component', assert => {
        const chatbot = container.query_selector('chatbot-openai')
        assert.ok(chatbot                                                       , 'Chatbot exists'          )
        assert.equal(chatbot.getAttribute('channel'), container.channel         , 'Has correct channel'     )
        assert.equal(chatbot.getAttribute('name')   , 'Profile Assistant'       , 'Has correct name'        )
        assert.ok(chatbot.getAttribute('system_prompt').length > 0              , 'Has system prompt'       )
    })

    test('handles form submission', async assert => {
        assert.expect(3)  // Updated to 3 assertions since we're now also checking reload

        let submit_called = false
        let reload_called = false

        // Save original methods
        const original_submit_form = container.api_web_forms.submit_form
        const original_reload     = container.reload_page

        // Mock submit_form
        container.api_web_forms.submit_form = async (form_data, endpoint) => {
            assert.equal(endpoint              , '/web/user/profile'            , 'Submits to correct endpoint')
            submit_called = true
            return { ok: true }
        }

        // Mock reload_page
        container.reload_page = () => {
            reload_called = true
        }

        const submit_event = {
            preventDefault: () => {},
            target       : container.query_selector('form')
        }
        await container.handle_form_submit(submit_event)
        assert.ok(submit_called                                                , 'Calls submit_form'        )
        assert.ok(reload_called                                               , 'Calls page reload'        )

        // Restore original methods
        container.api_web_forms.submit_form = original_submit_form
        container.reload_page              = original_reload
    })

    test('handles failed form submission', async assert => {
        assert.expect(2)  // Expecting 2 assertions

        let reload_called = false

        // Save original methods
        const original_submit_form = container.api_web_forms.submit_form
        const original_reload     = container.reload_page

        // Mock methods
        container.api_web_forms.submit_form = async () => {
            throw new Error('Submission failed')
        }

        container.reload_page = () => {
            reload_called = true
        }

        const submit_event = {
            preventDefault: () => {},
            target       : container.query_selector('form')
        }

        await container.handle_form_submit(submit_event)

        assert.notOk(reload_called                                            , 'Does not reload on error'  )
        assert.ok(true                                                       , 'Handles error gracefully'  )

        // Restore original methods
        container.api_web_forms.submit_form = original_submit_form
        container.reload_page              = original_reload
    })
})