import Events__Utils    from "../../js/events/Events__Utils.mjs";
import Events__Dispatch from "../../js/events/Events__Dispatch.mjs";
import Events__Receive  from "../../js/events/Events__Receive.mjs";

QUnit.module('Events__Utils.qunit', function(hooks) {

    let events_utils
    let events_receive
    let events_dispatch
    let channel
    let event_name
    let event_data


    hooks.beforeEach((assert) => {
        events_utils    = new Events__Utils()
        events_receive  = events_utils.events_receive
        events_dispatch = events_utils.events_dispatch
        channel         = 'an_channel'
        event_name      = 'test_event'
        event_data      = { test_data: 'test_data'}
        assert.deepEqual(events_receive.channel_callbacks , {})
        assert.deepEqual(events_receive.document_callbacks, {})
    })

    hooks.afterEach(() => {
        events_receive.remove_all_event_listeners()
    })

    QUnit.test('.constructor()', (assert) => {
        assert.ok       (events_utils                 instanceof Events__Utils   )
        assert.ok       (events_utils.events_dispatch instanceof Events__Dispatch)
        assert.ok       (events_utils.events_receive  instanceof Events__Receive )
        assert.deepEqual(events_utils  .events_dispatch         , events_dispatch  )
        assert.deepEqual(events_utils  .events_receive          , events_receive   )
        assert.deepEqual(events_receive.logs_enabled            , false            )
        assert.deepEqual(events_receive.logs_events_received    , []               )
        assert.deepEqual(events_receive.logs_callbacks_invoked  , []               )
    })

    QUnit.test('.add_event_listener()',  (assert) => {

        let event_received_data = {}
        let event_received = (event) => {
            assert.equal(event.event_type  , event_name)
            assert.equal(event.event_data, event_data)
            event_received_data = { type: event.type, data: event.detail}
        }
        assert.deepEqual(events_receive.channel_callbacks , {})
        assert.deepEqual(events_receive.document_callbacks, {})
        assert.deepEqual(event_received_data              , {})

        events_receive .add_event_listener(event_name, channel, event_received)

        assert.deepEqual(events_receive.channel_callbacks , {[event_name]: {[channel]: [event_received]}})
        assert.deepEqual(events_receive.document_callbacks, {[event_name]: events_receive.on_event})

        events_utils.events_dispatch.send_event        (event_name, event_data)

        assert.deepEqual(events_receive.logs_enabled           , false     )
        assert.deepEqual(events_receive.logs_events_received   , []        )
        assert.deepEqual(events_receive.logs_callbacks_invoked , []        )
        assert.deepEqual(event_data                            , event_data)

    })

    QUnit.test('.logs_enabled == true', (assert) => {
        let expected_log_entry      = { callback: undefined, channel: channel,  event_type: event_name, event_data: event_data, webc_id: undefined}
        events_receive.logs_enabled = true
        let on_log_event = (event) =>{
            assert.deepEqual(event.event_type , event_name)
        }

        assert.deepEqual(events_receive.channel_callbacks, {})
        assert.deepEqual(events_receive.logs_events_received   , []   )
        assert.deepEqual(events_receive.logs_callbacks_invoked , []   )

        events_receive.add_event_listener(event_name, channel, on_log_event)
        assert.deepEqual(events_receive.channel_callbacks , {[event_name]: {[channel]: [on_log_event]}})
        assert.deepEqual(events_receive.document_callbacks, {[event_name]: events_receive.on_event})

        events_dispatch.send_to_channel(event_name, channel, event_data)

        assert.deepEqual(events_receive.logs_events_received   ,  [expected_log_entry])
        assert.deepEqual(events_receive.logs_callbacks_invoked ,  [expected_log_entry])

        events_dispatch.send_to_channel(event_name, channel, event_data)
        assert.deepEqual(events_receive.logs_events_received   ,  [expected_log_entry, expected_log_entry])
        assert.deepEqual(events_receive.logs_callbacks_invoked ,  [expected_log_entry, expected_log_entry])

        let expected_log_entry_2 = { callback  : undefined         ,
                                     channel   : 'another_channel' ,
                                     event_type: 'test_event'      ,
		                             event_data: event_data        ,
                                     webc_id   : undefined         }

        events_dispatch.send_to_channel(event_name, 'another_channel', event_data)
        assert.deepEqual(events_receive.logs_events_received   , [expected_log_entry, expected_log_entry, expected_log_entry_2])
        assert.deepEqual(events_receive.logs_callbacks_invoked ,  [expected_log_entry, expected_log_entry])

        events_receive.clear_logs()
        assert.deepEqual(events_receive.logs_events_received  , [])
        assert.deepEqual(events_receive.logs_callbacks_invoked, [])
        events_dispatch.send_to_channel(event_name, 'another_channel', event_data)
        assert.deepEqual(events_receive.logs_events_received   , [expected_log_entry_2])
        assert.deepEqual(events_receive.logs_callbacks_invoked ,  [])
    })


})