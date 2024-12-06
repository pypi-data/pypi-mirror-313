import API_Invoke    from '../../js/data/API__Invoke.mjs';

import { MOCK_API_CHANNEL,
         MOCK_CONFIG_PATH,
         MOCK_CONFIG_DATA,
         setup_mock_responses } from '../../js/testing/Mock_API__Data.mjs'

QUnit.module('API_Invoke', function(hooks) {

    let api_invoke;
    let channel
    let api_path
    let api_data
    hooks.beforeEach(() =>{
        setup_mock_responses()
        channel         = 'api_invoke__qunit'
        api_invoke      = new API_Invoke(channel)
    })


    QUnit.test('.constructor()', (assert)=> {
        assert.ok       (api_invoke              instanceof API_Invoke)
        assert.deepEqual(api_invoke.channel , channel)
    })

    QUnit.test('.invoke_api()', async (assert)=> {
        // let event_name = 'api_invoke'
        // let event_data = { method:'GET', 'path':  '/config/version', 'data': null}
        //
        // let on_api_response = (data) =>{
        //     assert.deepEqual(data, mockResponse)
        // }
        // events_dispatch.send_to_channel(event_name, channel, event_data, null, on_api_response)
        let response = await api_invoke.invoke_api( MOCK_CONFIG_PATH, 'GET');
        assert.deepEqual(response, MOCK_CONFIG_DATA)
    })

})