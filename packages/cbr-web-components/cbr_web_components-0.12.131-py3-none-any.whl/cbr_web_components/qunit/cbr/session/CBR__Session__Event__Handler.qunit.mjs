import CBR__Session__Event__Handler from '../../../js/cbr/session/CBR__Session__Event__Handler.mjs'

const { module, test } = QUnit

const MOCK_EVENT_NAME = 'test_event'
const MOCK_DETAIL = { data: 'test_data' }

module('CBR__Session__Event__Handler', hooks => {
    let handler
    let original_add_event_listener
    let original_remove_event_listener
    let original_dispatch_event
    let added_events = []
    let removed_events = []
    let dispatched_events = []

    hooks.before((assert) => {
        assert.timeout(10)
        // Store original methods
        original_add_event_listener = document.addEventListener
        original_remove_event_listener = document.removeEventListener
        original_dispatch_event = document.dispatchEvent

        // Setup mock document event methods
        document.addEventListener = (event, callback) => {
            added_events.push({ event, callback })
        }
        document.removeEventListener = (event, callback) => {
            removed_events.push({ event, callback })
        }
        document.dispatchEvent = (event) => {
            dispatched_events.push(event)
            return true
        }
    })
    hooks.beforeEach(() => {
        handler = new CBR__Session__Event__Handler()
        // Clear tracking arrays
        added_events     .length = 0
        removed_events   .length = 0
        dispatched_events.length = 0
    })

    hooks.afterEach(() => {
        handler.unsubscribe_all()
    })

    hooks.after(() => {
        // Restore original methods
        document.addEventListener    = original_add_event_listener
        document.removeEventListener = original_remove_event_listener
        document.dispatchEvent       = original_dispatch_event
    })

    test('constructor initializes correctly', assert => {
        assert.ok(handler.callbacks                                , 'Has callbacks object')
        assert.ok(handler.events                                  , 'Has events object')
        assert.equal(Object.keys(handler.events).length, 8        , 'Has correct number of events')
        assert.equal(handler.events.USER_SESSION_CHANGED, 'user_session_changed'   , 'Has user session event')
        assert.equal(handler.events.SESSION_INITIALIZED, 'session_initialized'     , 'Has session init event')
    })

    test('dispatch creates and sends custom event', assert => {
        handler.dispatch(MOCK_EVENT_NAME, MOCK_DETAIL)

        const dispatched = dispatched_events[0]
        assert.equal(dispatched.type                              , MOCK_EVENT_NAME)
        assert.deepEqual(dispatched.detail                        , MOCK_DETAIL)
        assert.ok(dispatched.bubbles                              , 'Event bubbles')
        assert.ok(dispatched.composed                             , 'Event is composed')
    })

    test('dispatch with no detail ', assert => {
        handler.dispatch(MOCK_EVENT_NAME)

        const dispatched = dispatched_events[0]
        assert.equal(dispatched.type                              , MOCK_EVENT_NAME)
        assert.deepEqual(dispatched.detail                        , {})
        assert.ok(dispatched.bubbles                              , 'Event bubbles')
        assert.ok(dispatched.composed                             , 'Event is composed')
    })

    test('subscribe adds event listener', assert => {
        const callback = () => {}
        handler.subscribe(MOCK_EVENT_NAME, callback)

        assert.equal(added_events.length                          , 1)
        assert.equal(added_events[0].event                        , MOCK_EVENT_NAME)
        assert.equal(added_events[0].callback                     , callback)
        assert.equal(handler.callbacks[MOCK_EVENT_NAME].length    , 1)
        assert.equal(handler.callbacks[MOCK_EVENT_NAME][0]        , callback)
    })

    test('unsubscribe removes event listener', assert => {
        const callback = () => {}
        handler.subscribe(MOCK_EVENT_NAME, callback)
        handler.unsubscribe(MOCK_EVENT_NAME, callback)

        assert.equal(removed_events.length                        , 1)
        assert.equal(removed_events[0].event                      , MOCK_EVENT_NAME)
        assert.equal(removed_events[0].callback                   , callback)
        assert.equal(handler.callbacks[MOCK_EVENT_NAME].length    , 0)
    })

    test('unsubscribe handles non-existent events', assert => {
        handler.unsubscribe('non_existent_event', () => {})
        assert.equal(removed_events.length                        , 0)
    })

    test('unsubscribe_all clears all listeners', assert => {
        const callback_1 = () => {}
        const callback_2 = () => {}

        handler.subscribe('event1', callback_1)
        handler.subscribe('event2', callback_2)

        handler.unsubscribe_all()

        assert.equal(removed_events.length                        , 2)
        assert.deepEqual(handler.callbacks                        , {})
    })

    test('events property contains all expected events', assert => {
        const expected_events = [
            'USER_SESSION_CHANGED',
            //'PERSONA_SESSION_CHANGED',
            'ACTIVE_SESSION_CHANGED',
            'SESSION_ERROR',
            'LOGIN_AS_PERSONA',
            'LOGOUT_PERSONA',
            'SESSION_INITIALIZED',
            'SWITCH_SESSION',
            'RELOAD_PAGE'
        ]

        expected_events.forEach(event => {
            assert.ok(handler.events[event]                       , `Has ${event}`)
            assert.equal(typeof handler.events[event]             , 'string')
        })
    })

    test('multiple subscribers for same event', assert => {
        const callback_1 = () => {}
        const callback_2 = () => {}

        handler.subscribe(MOCK_EVENT_NAME, callback_1)
        handler.subscribe(MOCK_EVENT_NAME, callback_2)

        assert.equal(handler.callbacks[MOCK_EVENT_NAME].length    , 2)
        assert.equal(added_events.length                         , 2)
        assert.equal(added_events[0].callback                    , callback_1)
        assert.equal(added_events[1].callback                    , callback_2)
    })

    test('unsubscribe specific callback leaves others', assert => {
        const callback_1 = () => {}
        const callback_2 = () => {}

        handler.subscribe(MOCK_EVENT_NAME, callback_1)
        handler.subscribe(MOCK_EVENT_NAME, callback_2)
        handler.unsubscribe(MOCK_EVENT_NAME, callback_1)

        assert.equal(handler.callbacks[MOCK_EVENT_NAME].length    , 1)
        assert.equal(handler.callbacks[MOCK_EVENT_NAME][0]        , callback_2)
    })
})