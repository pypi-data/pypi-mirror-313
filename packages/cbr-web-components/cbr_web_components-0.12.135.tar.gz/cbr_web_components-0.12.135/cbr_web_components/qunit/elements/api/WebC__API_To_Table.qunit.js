import WebC__Target_Div     from "../../../js/utils/WebC__Target_Div.mjs";
import WebC__API_To_Table   from "../../../js/elements/api/WebC__API_To_Table.mjs";
import Web_Component        from "../../../js/core/Web_Component.mjs";
import API__Invoke          from "../../../js/data/API__Invoke.mjs";
import {MOCK_SERVER_REQUESTS_API_PATH,
        MOCK_SERVER_REQUESTS_DATA    ,
        setup_mock_responses         } from '../../../js/testing/Mock_API__Data.mjs'

QUnit.module('WebC__API_To_Json', function(hooks) {
    let target_div
    let webc_api_to_table
    let mock_responses
    let api_path
    let api_data

    hooks.beforeEach(async (assert) => {
        setup_mock_responses()
        api_data            = {'headers': ['requests_ids'], 'rows': [['a'], ['b'], ['c']], 'title':'an table'}
        target_div          = WebC__Target_Div.add_to_body().build()
        let attributes      = { api_path: MOCK_SERVER_REQUESTS_API_PATH}
        webc_api_to_table   = await target_div.append_child(WebC__API_To_Table, attributes)
        await webc_api_to_table.wait_for_event('build-complete')
    })

    hooks.afterEach(() => {
        webc_api_to_table.remove()
        target_div.remove()
    })

    QUnit.test('.constructor', (assert) => {
        assert.deepEqual(WebC__API_To_Table.name, 'WebC__API_To_Table')
        assert.ok(WebC__API_To_Table.prototype instanceof Web_Component)
        assert.ok(webc_api_to_table instanceof Web_Component)
        assert.ok(webc_api_to_table instanceof HTMLElement)
        assert.ok(webc_api_to_table.api_invoke instanceof API__Invoke)
        assert.deepEqual(webc_api_to_table.getAttributeNames(), ['api_path'])

        assert.deepEqual(webc_api_to_table.api_path, MOCK_SERVER_REQUESTS_API_PATH)
    })
})