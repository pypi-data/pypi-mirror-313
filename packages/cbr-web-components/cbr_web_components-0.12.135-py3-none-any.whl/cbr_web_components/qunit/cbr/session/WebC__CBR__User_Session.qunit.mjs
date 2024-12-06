import WebC__CBR__User_Session                     from '../../../js/cbr/session/WebC__CBR__User_Session.mjs'
import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import {
    setup_mock_responses,
    set_mock_response,
    MOCK_USER_ID,
    MOCK_USER_NAME,
    MOCK_USER_SESSION_ID,
    MOCK_USER_SESSION,
    MOCK_PERSONA_1_USER_ID,
    MOCK_PERSONA_1_USER_NAME,
    MOCK_PERSONA_1_SESSION_ID,
    MOCK_PERSONA_1_SESSION,
    MOCK_PERSONA_2_USER_ID,
    MOCK_PERSONA_2_USER_NAME,
    MOCK_PERSONA_2_SESSION_ID,
    MOCK_PERSONA_2_SESSION,
    MOCK_PERSONA_BAD_SESSION_ID
} from '../../../js/testing/Mock_API__Data.mjs'
import CBR_Events from "../../../js/cbr/CBR_Events.mjs";
import AAA__Element_Event from "../../../js/testing/AAA__Element_Event.mjs";

const { module, test , only, skip} = QUnit

module('WebC__CBR__User_Session', hooks => {
    let target_div
    let session_component
    let original_storage

    hooks.before(async (assert) => {
        assert.timeout(10)
        setup_mock_responses()

        // Save original storage
        original_storage = {
            getItem: window.localStorage.getItem,
            setItem: window.localStorage.setItem
        }

        // Mock storage
        const storage = {
            'cbr_user_session_id'    : MOCK_USER_SESSION.session_id,
            'cbr_active_session_id'  : MOCK_USER_SESSION.session_id
        }

        window.localStorage.getItem = (key) => storage[key]
        window.localStorage.setItem = (key, value) => storage[key] = value


        // Create component
        target_div = WebC__Target_Div.add_to_body()
        session_component = await target_div.append_child(WebC__CBR__User_Session)
        await session_component.wait_for__component_ready()
    })

    hooks.beforeEach(() => {
        session_component.api_handler.delete_cookie('CBR__SESSION_ID__USER'   )
        session_component.api_handler.delete_cookie('CBR__SESSION_ID__PERSONA')
        session_component.api_handler.delete_cookie('CBR__SESSION_ID__ACTIVE' )
        session_component.state_manager.reset_state()
    })

    hooks.after(() => {
        // Restore original storage
        window.localStorage.getItem = original_storage.getItem
        window.localStorage.setItem = original_storage.setItem

        session_component.remove()
        target_div.remove()
    })

    test('constructor and initialization', assert => {
        assert.ok(session_component instanceof WebC__CBR__User_Session           , 'Is correct component type'  )
        assert.ok(session_component instanceof Web_Component                     , 'Extends Web_Component'      )
        assert.ok(session_component.event_handler                                , 'Has event handler'          )
        assert.ok(session_component.api_handler                                  , 'Has API handler'            )
        assert.ok(session_component.state_manager                                , 'Has state manager'          )
        assert.ok(session_component.shadowRoot                                   , 'Has shadow root'            )
    })

    test('loads initial state correctly', async assert => {
        const state = session_component.state_manager.get_state()

        assert.deepEqual(state, { user_session   : null ,
                                  persona_session: null ,
                                  active_session : null ,
                                  is_initialized : false ,
                                  error          : null })
    })

    test('renders user session UI element correctly', async (assert) => {
        session_component.state_manager.set_user_session  (MOCK_USER_SESSION)       // login as user
        session_component.state_manager.set_active_session(MOCK_USER_SESSION)       // and set it as active session
        await session_component.refresh_ui()
        const user_element = session_component.query_selector('.session-item.user')

        const icon        = user_element.querySelector('.session-icon')
        const text        = user_element.querySelector('.session-text')
        const badge       = user_element.querySelector('.badge')

        assert.ok   (user_element                                               , 'User element exists'        )
        assert.ok   (user_element.classList.contains('active')                  , 'User session is active'     )
        assert.ok   (icon                                                      , 'Has icon element'           )
        assert.equal(text.textContent            , MOCK_USER_SESSION.user_name                  , 'Shows correct username'     )
        assert.ok   (badge.classList.contains('badge-success')                  , 'Has success badge'          )
    })

    test('handles persona login', async assert => {

        assert.deepEqual(session_component.state_manager.state.user_session   ,  null)                                  // confirm we have no user session data at the start
        assert.deepEqual(session_component.state_manager.state.persona_session,  null)                                  //   or persona session
        assert.deepEqual(session_component.state_manager.state.active_session ,  null)                                  //   or active session

        await session_component.handle__login_as_persona({ detail: { persona_id: MOCK_PERSONA_1_SESSION_ID } })         // login as persona 1
        assert.deepEqual(session_component.state_manager.state.persona_session,  MOCK_PERSONA_1_SESSION)                // confirm  we got persona 1 data
        assert.deepEqual(session_component.state_manager.state.user_session   ,  null)                                  //   and that the user_session
        assert.deepEqual(session_component.state_manager.state.active_session ,  null)                                  //   and active session did

        await session_component.handle__login_as_persona({ detail: { persona_id: MOCK_PERSONA_2_SESSION_ID } })         // login as persona 2
        assert.deepEqual(session_component.state_manager.state.persona_session,  MOCK_PERSONA_2_SESSION)                // confirm we got persona 2 data

        await session_component.handle__login_as_persona({ detail: { persona_id: MOCK_PERSONA_BAD_SESSION_ID } })       // login with an invalid persona id
        assert.deepEqual(session_component.state_manager.state.persona_session,  MOCK_PERSONA_2_SESSION)                // we should still have persona 2 data


    })

    //todo refactor with new AAA__Element_Event
    test('handles persona login - fires event CBR__SESSION__PERSONA__CHANGED', async assert => {
        assert.expect(2)

        let expected_persona_session = null

        const  on_persona_session_changed = () => {
            assert.deepEqual(session_component.state_manager.state.persona_session,  expected_persona_session)
        }
        session_component.addEventListener(CBR_Events.CBR__SESSION__PERSONA__CHANGED, on_persona_session_changed)

        expected_persona_session = MOCK_PERSONA_1_SESSION
        await session_component.handle__login_as_persona({ detail: { persona_id: MOCK_PERSONA_1_SESSION_ID } })

        expected_persona_session = MOCK_PERSONA_2_SESSION
        await session_component.handle__login_as_persona({ detail: { persona_id: MOCK_PERSONA_2_SESSION_ID } })

        session_component.removeEventListener(CBR_Events.CBR__SESSION__PERSONA__CHANGED, on_persona_session_changed)

    })

    test('handles persona login - fires event CBR__SESSION__PERSONA__CHANGED', async assert => {
        assert.expect(2)


        await AAA__Element_Event.test({                                 // Test first persona login
            element        : session_component                         ,
            event_name     : CBR_Events.CBR__SESSION__PERSONA__CHANGED ,
            raise_after_act: false                                     ,
            act            : async () => {
                await session_component.handle__login_as_persona({detail: { persona_id: MOCK_PERSONA_1_SESSION_ID }})
            },
            assert         : () => {
                assert.deepEqual(session_component.state_manager.state.persona_session, MOCK_PERSONA_1_SESSION,)
            }
        })


        await AAA__Element_Event.test({                                 // Test second persona login
            element        : session_component                         ,
            event_name     : CBR_Events.CBR__SESSION__PERSONA__CHANGED ,
            raise_after_act: false                                     ,
            act            : async () => {
                await session_component.handle__login_as_persona({detail: { persona_id: MOCK_PERSONA_2_SESSION_ID }})
            },
            assert         : () => {
                assert.deepEqual(session_component.state_manager.state.persona_session, MOCK_PERSONA_2_SESSION,)
            }
        })
    })

    test('handle__persona_session_changed - respond to event and refreshes UI', async assert => {
        await session_component.refresh_ui()
        const persona_element_1 = session_component.query_selector('.session-item.persona')
        assert.deepEqual(persona_element_1, null, 'No persona element exists')

        session_component.api_handler.set_cookie('CBR__SESSION_ID__PERSONA',MOCK_PERSONA_1_SESSION_ID)      // login persona via cookie
        await session_component.handle__persona_session_changed()                                           // trigger handle__persona_session_changed
        const persona_element_2 = session_component.query_selector('.session-item.persona')
        assert.equal(persona_element_2.querySelector('.session-text').textContent,  MOCK_PERSONA_1_SESSION.user_name)
        assert.ok   (persona_element_2                                           , 'Persona element exists'     )
        assert.ok   (persona_element_2.querySelector('.revert-icon')             , 'Has revert icon'           )

        session_component.api_handler.delete_cookie('CBR__SESSION_ID__PERSONA')                         // logout persona via cookie
        session_component.state_manager.set_persona_session  (MOCK_PERSONA_2_SESSION)                   // login persona vai state
        await session_component.handle__persona_session_changed()                                       // trigger handle__persona_session_changed
        const persona_element_3 = session_component.query_selector('.session-item.persona')
        assert.equal(persona_element_3.querySelector('.session-text').textContent,  MOCK_PERSONA_2_SESSION.user_name)

    })

    test('handles session switching', async assert => {
        assert.expect(6)

        await session_component.handle__login_as_persona({ detail: { persona_id: MOCK_PERSONA_1_SESSION_ID } })         // First login as persona 1
        assert.deepEqual(session_component.state_manager.state.persona_session, MOCK_PERSONA_1_SESSION)

        const on_active_session_changed = (event) => {
            assert.equal(event.detail.session_id             , MOCK_PERSONA_2_SESSION_ID, 'Correct session ID')
            assert.equal(event.detail.user_name              , MOCK_PERSONA_2_USER_NAME, 'Correct User Name')
            assert.equal(event.detail.state.user_session     , null                  )          // user_ession not set
            assert.equal(event.detail.state.persona_session  , MOCK_PERSONA_1_SESSION)          // persona_session did not change
            assert.equal(event.detail.state.active_session   , MOCK_PERSONA_2_SESSION)          // active session changed
        }
        session_component.addEventListener('active_session_changed', on_active_session_changed , {once: true})

        await session_component.handle__switch_session({detail: { session_id: MOCK_PERSONA_2_SESSION_ID }})         // then change session to persona 2

    })

    test('handles api errors gracefully', async assert => {
        assert.expect(4)
        const done = assert.async()

        set_mock_response('/api/user-session/guest/login-as-persona?persona_id=invalid-id', 'POST', null)           // Setup error response

        session_component.addEventListener('session_error', (event) => {
            const state = session_component.state_manager.get_state()
            assert.ok   (event.detail.error                                    , 'Error event dispatched' )
            assert.ok   (state.error                                           , 'Error state set'        )
            assert.equal(state.persona_session           , null                , 'No persona session set' )
            assert.equal(event.detail.error.message, 'Mock response is null for POST:/api/user-session/guest/login-as-persona?persona_id=invalid-id')
            done()
        }, {once:true})

        await session_component.handle__login_as_persona({detail: { persona_id: 'invalid-id' }})
    })

    test('dom event handlers work correctly', async (assert) => {
        assert.expect(2)
        document.cookie = `CBR__SESSION_ID__USER=${MOCK_USER_SESSION_ID};path=/`    // set the user session cookie
        session_component.state_manager.set_user_session  (MOCK_USER_SESSION)       // and simulate user login
        await session_component.refresh_ui()
        // Setup click event tracking
        let switch_clicked = false
        let logout_clicked = false

        session_component.addEventListener('switch_session', () => {switch_clicked = true}, {once: true})
        session_component.addEventListener('logout_persona', () => {logout_clicked = true}, {once: true})

        const user_element = session_component.query_selector('.session-item.user')
        await user_element.click()                                                      // Trigger user to trigger session switch

        assert.ok(switch_clicked            , 'Switch event triggered' )
        assert.ok(logout_clicked === false  , 'No logout triggered'    )

    })

    test('cleans up event listeners on disconnect', assert => {
        const original_remove = session_component.event_handler.unsubscribe_all
        let cleanup_called = false

        session_component.event_handler.unsubscribe_all = () => {
            cleanup_called = true
            original_remove.call(session_component.event_handler)
        }

        session_component.disconnectedCallback()
        assert.ok(cleanup_called                                               , 'Cleanup performed'      )

        session_component.event_handler.unsubscribe_all = original_remove
    })

    test('load_session_state', async(assert) => {
        const default_state = { user_session   : null ,
                                persona_session: null ,
                                active_session : null ,
                                is_initialized : false,
                                error          : null }
        assert.deepEqual(session_component.state_manager.state, default_state )

        await session_component.load_session_state()                                // call with no params will not change state
        assert.deepEqual(session_component.state_manager.state, default_state )

        await session_component.load_session_state({active_session_id:MOCK_USER_SESSION_ID})
        assert.deepEqual(session_component.state_manager.state.active_session , MOCK_USER_SESSION      )
        assert.deepEqual(session_component.state_manager.state.user_session   , null                   )
        assert.deepEqual(session_component.state_manager.state.persona_session, null                   )

        await session_component.load_session_state({user_session_id:MOCK_PERSONA_1_SESSION_ID})
        assert.deepEqual(session_component.state_manager.state.active_session , MOCK_USER_SESSION      )
        assert.deepEqual(session_component.state_manager.state.user_session   , MOCK_PERSONA_1_SESSION )
        assert.deepEqual(session_component.state_manager.state.persona_session, null                   )

        await session_component.load_session_state({persona_session_id:MOCK_PERSONA_2_SESSION_ID})
        assert.deepEqual(session_component.state_manager.state.active_session , MOCK_USER_SESSION      )
        assert.deepEqual(session_component.state_manager.state.user_session   , MOCK_PERSONA_1_SESSION )
        assert.deepEqual(session_component.state_manager.state.persona_session, MOCK_PERSONA_2_SESSION )
    })

    test('handle_revert_click', async(assert) => {
        assert.expect(1)
        const custom_event = new CustomEvent('an-event')
        const on_logout_persona = () => {
            assert.ok(1)
        }
        session_component.addEventListener(session_component.event_handler.events.LOGOUT_PERSONA, on_logout_persona, {once:true})
        session_component.handle_revert_click({event:custom_event})
    })
    test('load_session_state - handle errors', async(assert) => {
        const expected_error_message = `Mock response is null for GET:/api/user-session/session/session-details?session_id=${MOCK_USER_SESSION_ID}`
        assert.expect(5)
        const on_session_error = (error)=>{
            assert.ok   (error instanceof CustomEvent)
            assert.equal(error.type                , 'session_error'       )
            assert.equal(error.target              , session_component     )
            assert.equal(error.detail.error.message, expected_error_message)
        }
        session_component.addEventListener(session_component.event_handler.events.SESSION_ERROR, on_session_error, {once:true})
        set_mock_response(`/api/user-session/session/session-details?session_id=${MOCK_USER_SESSION_ID}`, 'GET' , null    )
        await session_component.load_session_state({active_session_id:MOCK_USER_SESSION_ID})
        assert.equal(session_component.state_manager.state.error, 'Error: ' + expected_error_message)
    })

    test('handle__switch_session - handles error', async (assert) => {
        assert.expect(6)
        const expected_error_message = `Mock response is null for GET:/api/user-session/session/session-details?session_id=${MOCK_USER_SESSION_ID}`
        const on_session_error = (error)=>{
            assert.ok   (error instanceof CustomEvent)
            assert.equal(error.type                , 'session_error'       )
            assert.equal(error.target              , session_component     )
            assert.equal(error.detail.error.message, expected_error_message)
        }
        session_component.addEventListener(session_component.event_handler.events.SESSION_ERROR, on_session_error, {once:true})
        set_mock_response(`/api/user-session/session/session-details?session_id=${MOCK_USER_SESSION_ID}`, 'GET' , null    )
        await session_component.handle__switch_session({detail: { session_id: MOCK_USER_SESSION_ID }})
        assert.equal(session_component.state_manager.state.error, 'Error: ' + expected_error_message)
        assert.ok(1)
    })

    test('handle__logout_persona', async (assert)=> {
        assert.expect(14)
        assert.deepEqual(session_component.state_manager.state.active_session , null)
        assert.deepEqual(session_component.state_manager.state.user_session   , null)
        assert.deepEqual(session_component.state_manager.state.persona_session, null)

        const on_session_persona_change = (event) => {
            assert.ok(event instanceof CustomEvent)
            assert.deepEqual(event.detail.state, session_component.state_manager.state)
            assert.deepEqual(event.detail.state.active_session , MOCK_PERSONA_2_SESSION)
            assert.deepEqual(event.detail.state.user_session   , null)
            assert.deepEqual(event.detail.state.persona_session, null)
        }
        session_component.addEventListener(CBR_Events.CBR__SESSION__PERSONA__CHANGED, on_session_persona_change, {once:true})
        document.cookie = `CBR__SESSION_ID__ACTIVE=${MOCK_PERSONA_1_SESSION_ID};path=/`                     // set active session id
        document.cookie = `CBR__SESSION_ID__USER  =${MOCK_PERSONA_2_SESSION_ID};path=/`                     // set user session id

        assert.equal(session_component.api_handler.get_active_session_id(), MOCK_PERSONA_1_SESSION_ID)      // before logout is Persona 1
        assert.equal(session_component.api_handler.get_user_session_id  (), MOCK_PERSONA_2_SESSION_ID)      // before logout is Persona 2

        session_component.state_manager.set_persona_session(MOCK_PERSONA_1_SESSION)                         // login as persona
        assert.deepEqual(session_component.state_manager.state.persona_session, MOCK_PERSONA_1_SESSION)     // confirm persona state is set

        await session_component.handle__logout_persona()                                                    // trigger handle__logout_persona

        assert.deepEqual(session_component.state_manager.state.persona_session, null)                       // confirm persona state has been cleared
        assert.equal(session_component.api_handler.get_active_session_id(), MOCK_PERSONA_2_SESSION_ID)      // after  logout is now Persona 2
        assert.equal(session_component.api_handler.get_user_session_id  (), MOCK_PERSONA_2_SESSION_ID)      // before logout is Persona 2
    })

    test('handle__logout_persona - handle error', async (assert)=> {
        assert.expect(5)
        set_mock_response('/api/user-session/session/session-details?session_id=null', 'GET', null)
        const expected_error_message = 'Mock response is null for GET:/api/user-session/session/session-details?session_id=null'

        const on_session_error = (error)=>{
            assert.ok   (error instanceof CustomEvent)
            assert.equal(error.type                , 'session_error'       )
            assert.equal(error.target              , session_component     )
            assert.equal(error.detail.error.message, expected_error_message)
        }
        session_component.addEventListener(session_component.event_handler.events.SESSION_ERROR, on_session_error, {once:true})

        await session_component.handle__logout_persona()
        assert.equal(session_component.state_manager.state.error.message, expected_error_message)
    });

    test('html - edge cases', async (assert)=>{
        session_component.state_manager.set_persona_session  (MOCK_USER_SESSION)       // login as user
        await session_component.refresh_ui()

        assert.equal(session_component.query_selector('.session-item').getAttribute('class'), 'session-item persona ')

        session_component.state_manager.set_active_session(MOCK_USER_SESSION)       // now set it as active session
        await session_component.refresh_ui()

        assert.equal(session_component.query_selector('.session-item').getAttribute('class'), 'session-item persona active')
    })
});