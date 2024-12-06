import CBR__Session__API__Handler from '../../../js/cbr/session/CBR__Session__API__Handler.mjs'
import {
    set_mock_response,
    setup_mock_responses,
    MOCK_PERSONA_1_SESSION_ID,
    MOCK_PERSONA_1_SESSION,
    MOCK_USER_SESSION_ID,
    MOCK_USER_SESSION,
    MOCK__API_RESPONSE__OK__LOGIN_AS_PERSONA, MOCK_PERSONA_2_SESSION_ID, MOCK_PERSONA_1_USER_ID
} from '../../../js/testing/Mock_API__Data.mjs'

const { module, test , only} = QUnit

module('CBR__Session__API__Handler', hooks => {
    let api_handler
    let original_cookie

    hooks.before((assert) => {
        assert.timeout(10)
        setup_mock_responses()
        original_cookie = document.cookie                             // Store original cookie
        api_handler = new CBR__Session__API__Handler()
    })

    hooks.after(() => {
        document.cookie = original_cookie                            // Restore original cookie
    })

    test('constructor initializes correctly', assert => {
        assert.ok(api_handler.api_invoke                            , 'Has API invoke instance'     )
        assert.equal(api_handler.base_path, '/api/user-session'     , 'Has correct base path'       )
    })

    test('get_current_session fetches session data', async assert => {
        const result = await api_handler.get_current_session()
        assert.deepEqual(result, MOCK_USER_SESSION                  , 'Returns correct session data')
    })

    test('get_session_details fetches details', async assert => {
        const result = await api_handler.get_session_details(MOCK_USER_SESSION_ID)
        assert.deepEqual(result, MOCK_USER_SESSION                      , 'Returns correct session details')
    })

    test('login_as_persona handles login', async assert => {
        const result = await api_handler.login_as_persona(MOCK_PERSONA_1_SESSION_ID)
        assert.deepEqual(result, MOCK__API_RESPONSE__OK__LOGIN_AS_PERSONA                  , 'Returns success response'     )
    })

    test('logout_persona handles logout', async assert => {
        const result = await api_handler.logout_persona()
        assert.deepEqual(result, { success: true }                  , 'Returns success response'     )
    })

    test('logout_all handles complete logout', async assert => {
        const result = await api_handler.logout_all()
        assert.deepEqual(result, { success: true }                  , 'Returns success response'     )
    })

    test('set_active_session sets cookie', async assert => {
        await api_handler.set_active_session(MOCK_USER_SESSION_ID)
        assert.ok(document.cookie.includes(`CBR__SESSION_ID__ACTIVE=${MOCK_USER_SESSION_ID}`), 'Sets correct cookie')
    })

    test('set_active_persona sets cookie', async assert => {
        await api_handler.set_active_persona(MOCK_PERSONA_2_SESSION_ID)
        assert.ok(document.cookie.includes(`CBR__SESSION_ID__PERSONA=${MOCK_PERSONA_2_SESSION_ID}`), 'Sets correct cookie')
    })

    test('get_cookie retrieves values', assert => {
        document.cookie = `test_cookie=test_value;path=/`
        assert.equal(api_handler.get_cookie('test_cookie'), 'test_value', 'Gets correct cookie value')
        assert.equal(api_handler.get_cookie('nonexistent'), null        , 'Returns null for missing cookie')
    })

    test('session ID getters return correct values', assert => {
        document.cookie = `CBR__SESSION_ID__USER=${MOCK_USER_SESSION_ID};path=/`
        assert.equal(api_handler.get_user_session_id(), MOCK_USER_SESSION_ID, 'Gets user session ID')

        document.cookie = `CBR__SESSION_ID__PERSONA=${MOCK_PERSONA_1_SESSION_ID};path=/`
        assert.equal(api_handler.get_persona_session_id(), MOCK_PERSONA_1_SESSION_ID, 'Gets persona session ID')

        document.cookie = `CBR__SESSION_ID__ACTIVE=${MOCK_PERSONA_2_SESSION_ID};path=/`
        assert.equal(api_handler.get_active_session_id(), MOCK_PERSONA_2_SESSION_ID, 'Gets active session ID')
    })

    test('switch_to_session changes session', async assert => {
        const result = await api_handler.switch_to_session(MOCK_PERSONA_1_SESSION_ID)
        assert.deepEqual(result, MOCK_PERSONA_1_SESSION                     , 'Returns session details')
        assert.ok(document.cookie.includes(`CBR__SESSION_ID__ACTIVE=${MOCK_PERSONA_1_SESSION_ID}`), 'Updates active session cookie')
    })

    test('handles API errors gracefully', async assert => {
        set_mock_response('/api/user-session/session/current-session', 'GET', null, 500)

        try {
            await api_handler.get_current_session()
            assert.notOk(true, 'Should throw error')
        } catch (error) {
            assert.ok(error instanceof Error, 'Throws error on API failure')
        }
    })


    test('handles get_session_details API error', async assert => {
        // Setup mock to return error
        set_mock_response(`/api/user-session/session/session-details?session_id=${MOCK_PERSONA_1_SESSION_ID}`, 'GET', null, 500)

        try {
            await api_handler.get_session_details(MOCK_PERSONA_1_SESSION_ID)
            assert.notOk(true, 'Should throw error')
        } catch (error) {
            assert.ok(error instanceof Error, 'Throws error on API failure')
            // assert.ok(console.error.calledWith('Error fetching session details:', error),
            //     'Logs error message correctly')
        }
    })

    test('handles login_as_persona API error', async assert => {
        // Setup mock to return error
        set_mock_response(`/api/user-session/guest/login-as-persona?persona_id=${MOCK_PERSONA_1_SESSION_ID}`, 'POST', null, 500)

        try {
            await api_handler.login_as_persona(MOCK_PERSONA_1_SESSION_ID)
            assert.notOk(true, 'Should throw error')
        } catch (error) {
            assert.ok(error instanceof Error, 'Throws error on API failure')
            // assert.ok(console.error.calledWith('Error logging in as persona:', error),
            //     'Logs error message correctly')
        }
    })

    test('handles logout_persona API error', async assert => {
        // Setup mock to return error
        set_mock_response('/api/user-session/guest/logout-persona', 'POST', null, 500)

        try {
            await api_handler.logout_persona()
            assert.notOk(true, 'Should throw error')
        } catch (error) {
            assert.ok(error instanceof Error, 'Throws error on API failure')
            // assert.ok(console.error.calledWith('Error logging out persona:', error),
            //     'Logs error message correctly')
        }
    })

    test('handles logout_all API error', async assert => {
        // Setup mock to return error
        set_mock_response('/api/user-session/guest/logout-all', 'POST', null, 500)

        try {
            await api_handler.logout_all()
            assert.notOk(true, 'Should throw error')
        } catch (error) {
            assert.ok(error instanceof Error, 'Throws error on API failure')
            // assert.ok(console.error.calledWith('Error logging out all sessions:', error),
            //     'Logs error message correctly')
        }
    })

    // Test for cookie edge cases
    test ('get_cookie handles malformed cookies', assert => {

        api_handler.delete_cookie('test');                                                      // Test with empty cookie
        assert.equal(api_handler.get_cookie('test'), null, 'Returns null for empty cookie')

        document.cookie = 'malformed;cookie;string'                                             // Test with malformed cookie string
        assert.equal(api_handler.get_cookie('test'), null, 'Returns null for malformed cookie')

        document.cookie = 'test=value;;;'                                                      // Test with cookie containing multiple semicolons
        assert.equal(api_handler.get_cookie('test'), 'value', 'Correctly parses cookie with multiple semicolons')
    })
})