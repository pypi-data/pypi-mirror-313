import CBR__Session__State__Manager from '../../../js/cbr/session/CBR__Session__State__Manager.mjs'

const { module, test } = QUnit

const MOCK_USER_SESSION    = { user_name: 'test_user'     }
const MOCK_PERSONA_SESSION = { user_name: 'test_persona'  }

module('CBR__Session__State__Manager', hooks => {
    let manager

    hooks.beforeEach(() => {
        manager = new CBR__Session__State__Manager()
    })

    test('constructor initializes default state', assert => {
        assert.deepEqual(manager.state, {
            user_session    : null ,
            persona_session : null ,
            active_session  : null ,
            is_initialized  : false,
            error          : null
        }, 'Initial state is correct')
    })

    test('update_state preserves existing values', assert => {
        manager.update_state({ user_session: MOCK_USER_SESSION })
        assert.equal(manager.state.user_session      , MOCK_USER_SESSION , 'Updates user session'      )
        assert.equal(manager.state.persona_session   , null             , 'Preserves persona session'  )
        assert.equal(manager.state.is_initialized    , false            , 'Preserves initialization'   )
    })

    test('session setters and getters', assert => {
        manager.set_user_session(MOCK_USER_SESSION)
        assert.equal(manager.state.user_session      , MOCK_USER_SESSION , 'Sets user session'         )

        manager.set_persona_session(MOCK_PERSONA_SESSION)
        assert.equal(manager.state.persona_session   , MOCK_PERSONA_SESSION, 'Sets persona session'     )

        manager.set_active_session(MOCK_USER_SESSION)
        assert.equal(manager.state.active_session    , MOCK_USER_SESSION , 'Sets active session'       )

        manager.clear_persona_session()
        assert.equal(manager.state.persona_session   , null             , 'Clears persona session'    )
    })

    test('error handling', assert => {
        const error = new Error('Test error')
        manager.set_error(error)
        assert.equal(manager.state.error             , error            , 'Sets error state'          )
    })

    test('initialization state', assert => {
        assert.notOk(manager.is_initialized()                                      , 'Initially false'          )

        manager.set_initialized()
        assert.ok(manager.is_initialized()                                         , 'Sets to true'            )

        manager.set_initialized(false)
        assert.notOk(manager.is_initialized()                                      , 'Can set to false'        )
    })

    test('get_state returns copy of state', assert => {
        const state = manager.get_state()
        assert.deepEqual(state, manager.state                                      , 'Returns correct state'   )
        assert.notEqual(state, manager.state                                       , 'Returns new object'      )
    })

    test('has_active_persona detection', assert => {
        assert.notOk(manager.has_active_persona()                                  , 'Initially false'         )

        manager.set_persona_session(MOCK_PERSONA_SESSION)
        assert.ok(manager.has_active_persona()                                     , 'Detects active persona'  )

        manager.clear_persona_session()
        assert.notOk(manager.has_active_persona()                                  , 'False after clear'       )
    })

    test('active session comparison', assert => {
        manager.set_active_session(MOCK_USER_SESSION)

        assert.ok(manager.is_active_session(MOCK_USER_SESSION)                     , 'Matches active session'  )
        assert.notOk(manager.is_active_session(MOCK_PERSONA_SESSION)               , 'Non-match detected'      )
        assert.notOk(manager.is_active_session(null)                               , 'Handles null input'      )
    })

    test('get_active_session returns current session', assert => {
        assert.equal(manager.get_active_session()                  , null         , 'Initially null'          )

        manager.set_active_session(MOCK_USER_SESSION)
        assert.equal(manager.get_active_session()                  , MOCK_USER_SESSION, 'Returns active session' )
    })

    test('state updates maintain immutability', assert => {
        const initial_state = manager.get_state()
        manager.set_user_session(MOCK_USER_SESSION)

        const updated_state = manager.get_state()
        assert.notEqual(initial_state              , updated_state  , 'States are different objects')
        assert.notEqual(initial_state.user_session , MOCK_USER_SESSION, 'Original state unchanged'   )
    })
})