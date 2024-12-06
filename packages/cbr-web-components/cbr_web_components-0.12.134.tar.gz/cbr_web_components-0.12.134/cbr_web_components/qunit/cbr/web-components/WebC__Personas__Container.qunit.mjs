import WebC__Target_Div          from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component             from '../../../js/core/Web_Component.mjs'
import WebC__Personas__Container from '../../../js/cbr/web-components/WebC__Personas__Container.mjs'
import { setup_mock_responses,
         set_mock_response }     from '../../../js/testing/Mock_API__Data.mjs'
import CBR_Events from "../../../js/cbr/CBR_Events.mjs";

const { module, test , only} = QUnit

const MOCK_PERSONAS = {
    'guest-1': {
        user_data: {
            first_name              : 'John'                                ,
            last_name              : 'Doe'                                 ,
            role                   : 'CISO'                                ,
            organisation           : 'Test Corp'                           ,
            sector                : 'Technology'                          ,
            size_of_organisation   : '1000+ employees'                     ,
            country               : 'United Kingdom'                      ,
            additional_system_prompt: 'Prefer detailed technical responses'
        }
    },
    'guest-2': {
        user_data: {
            first_name              : 'Jane'                               ,
            last_name              : 'Smith'                              ,
            role                   : 'Security Analyst'                    ,
            organisation           : 'Tech Ltd'                           ,
            sector                : 'Finance'                            ,
            size_of_organisation   : '500-1000 employees'                 ,
            country               : 'United States'                      ,
            additional_system_prompt: 'Focus on practical examples'
        }
    }
}

module('WebC__Personas__Container', hooks => {
    let target_div
    let container

    hooks.before(async (assert) => {
        assert.timeout(10)
        setup_mock_responses()
        set_mock_response('/api/user-session/guests/data', 'GET', MOCK_PERSONAS)

        target_div = WebC__Target_Div.add_to_body()
        container  = await target_div.append_child(WebC__Personas__Container)
        await container.wait_for__component_ready()
    })

    hooks.after(() => {
        container .remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(container.tagName.toLowerCase()    , 'webc-personas-container', 'Has correct tag name'     )
        assert.equal(container.constructor.element_name , 'webc-personas-container', 'Has correct element name' )
        assert.equal(container.constructor.name        , 'WebC__Personas__Container', 'Has correct class name' )

        assert.ok(container.shadowRoot                                            , 'Has shadow root'          )
        assert.ok(container.api_invoke                                           , 'Has API__Invoke'          )
        assert.ok(container.event_handler                                        , 'Has event handler'        )

        assert.ok(container instanceof Web_Component                             , 'Extends Web_Component'     )
        assert.ok(container instanceof HTMLElement                               , 'Is HTML Element'          )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = container.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                             , 'Has CSS rules'            )
        assert.ok(css_rules['.container']                                       , 'Has container styles'     )
        assert.ok(css_rules['.card']                                           , 'Has card styles'          )
        assert.ok(css_rules['.persona-name']                                   , 'Has persona name styles'  )
    })

    test('loads personas correctly', async assert => {
        assert.deepEqual(container.personas, MOCK_PERSONAS                      , 'Loaded personas data'     )

        const personas_container = container.query_selector('.personas-container')
        const cards = personas_container.querySelectorAll('.card')

        assert.equal(cards.length                     , 2                       , 'Renders correct number of cards')
    })

    test('creates persona card correctly', async assert => {
        const guest_id = 'guest-1'
        const persona  = MOCK_PERSONAS[guest_id]

        const card = container.create_persona_card(guest_id, persona)
        const dom  = card.dom_create()

        assert.ok(dom.classList.contains('card')                               , 'Has card class'           )
        assert.ok(dom.classList.contains('bg-white')                          , 'Has background class'     )

        const name = dom.querySelector('.persona-name')
        assert.equal(name.textContent                 ,
                    `${persona.user_data.first_name} ${persona.user_data.last_name}`,
                    'Shows correct name'              )

        const role = dom.querySelector('.persona-role')
        assert.equal(role.textContent                , persona.user_data.role  , 'Shows correct role'      )

        const details = dom.querySelector('.persona-details')
        assert.ok(details.textContent.includes(persona.user_data.organisation), 'Shows organisation'       )
        assert.ok(details.textContent.includes(persona.user_data.sector)      , 'Shows sector'            )
        assert.ok(details.textContent.includes(persona.user_data.country)     , 'Shows country'           )

        const login_button = dom.querySelector('.login-button')
        assert.ok(login_button                                                 , 'Has login button'        )
        assert.equal(login_button.dataset.guestId    , guest_id               , 'Button has correct ID'   )
    })

    test('handles persona login click', async (assert) => {
        assert.expect(1)

        const on_login_as_persona = (event) => {
            assert.deepEqual(event.detail, { persona_id: 'guest-1' } )
        }
        window.addEventListener('login_as_persona', on_login_as_persona, {once: true})
        const button = container.query_selector('.login-button')
        button.click()

    })

    test('updates persona buttons correctly', async assert => {
        const active_persona = 'John Doe'
        container.update_persona_buttons(active_persona)

        const buttons = container.query_selector_all('.login-button')

        const active_button   = buttons[0]
        const inactive_button = buttons[1]

        assert.equal(active_button.textContent       , 'Current Persona'      , 'Updates active button text')
        assert.ok(active_button.classList.contains('btn-success')            , 'Adds success class'       )
        assert.ok(active_button.disabled                                     , 'Disables active button'   )

        assert.equal(inactive_button.textContent     , 'Login as this persona', 'Keeps inactive button text')
        assert.ok(inactive_button.classList.contains('btn-outline-primary')  , 'Keeps outline class'      )
        assert.notOk(inactive_button.disabled                               , 'Keeps inactive button enabled')
    })

    test('handles persona session changes', assert => {
        const state = {
            persona_session: {
                user_name: 'John Doe'
            }
        }
        const active_button = container.query_selector('.login-button')

        container.event_handler.dispatch(CBR_Events.CBR__SESSION__PERSONA__CHANGED, { state })

        assert.equal(active_button.textContent       , 'Current Persona'      , 'Updates button on session change')
    })

    test('renders header section correctly', async assert => {
        const header = container.query_selector('.header')
        assert.ok(header                                                      , 'Header section exists'    )

        const title = header.querySelector('.main-title')
        assert.equal(title.textContent               , 'Personas'             , 'Shows correct title'      )

        const subtitle = header.querySelector('.subtitle')
        assert.ok(subtitle.textContent.includes('Select a persona')          , 'Shows correct subtitle'   )
    })


    test('handles failed personas loading', async assert => {
        // Setup API error response
        set_mock_response('/api/user-session/guests/data', 'GET', null, 500)

        const error_container = await target_div.append_child(WebC__Personas__Container)
        await error_container.wait_for__component_ready()

        assert.notOk(error_container.personas                                    , 'No personas data on error'  )
        const personas_container = error_container.query_selector('.personas-container')
        assert.ok(personas_container                                             , 'Still renders container'    )
        assert.equal(personas_container.children.length, 0                       , 'No persona cards rendered'  )
    })

    test('handles successful login click and navigation', async assert => {
        // Setup successful API response for login
        set_mock_response('/api/user-session/guest/login-as-persona?persona_id=guest-1', 'POST', { success: true })

        // Track navigation call
        let navigation_called = false
        container.navigate_to_personas_page = async () => {
            navigation_called = true
        }

        await container.handle_login_click({
            target: {
                matches: () => true,
                dataset: { guestId: 'guest-1' }
            }
        })

        assert.ok(navigation_called , 'Navigation method called'  )
    })

    test('handles failed login attempt', async assert => {
        // Setup failed API response
        set_mock_response('/api/user-session/guest/login-as-persona?persona_id=guest-1', 'POST', null, 500)

        // Track navigation call
        let navigation_called = false
        container.navigate_to_personas_page = async () => {
            navigation_called = true
        }

        try {
            await container.handle_login_click({
                target: {
                    matches: () => true,
                    dataset: { guestId: 'guest-1' }
                }
            })
            assert.notOk(true                                                    , 'Should throw error'       )
        } catch (error) {
            assert.ok(error                                                      , 'Throws error on API fail' )
            assert.notOk(navigation_called                                       , 'Navigation not called'    )
        }
    })
})