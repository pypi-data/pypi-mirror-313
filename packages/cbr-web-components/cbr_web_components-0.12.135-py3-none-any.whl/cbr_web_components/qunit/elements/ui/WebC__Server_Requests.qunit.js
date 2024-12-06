import WebC__Target_Div      from "../../../js/utils/WebC__Target_Div.mjs";
import WebC__Server_Requests from "../../../js/elements/ui/WebC__Server_Requests.mjs";
import Web_Component         from "../../../js/core/Web_Component.mjs";
import API__Invoke           from "../../../js/data/API__Invoke.mjs";
import WebC__API_To_Table    from "../../../js/elements/api/WebC__API_To_Table.mjs";
import Table                 from "../../../js/core/Table.mjs";
import {MOCK_SERVER_REQUESTS_API_PATH,
        MOCK_SERVER_REQUESTS_DATA    ,
        setup_mock_responses, set_mock_response  } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test } = QUnit

module('WebC__Server_Requests', function(hooks) {
    let target_div
    let webc_server_requests
    // let mock_responses
    // let api_path
    // let api_data

    hooks.beforeEach(async (assert) => {
        setup_mock_responses()
        target_div           = WebC__Target_Div.add_to_body().build()
        let attributes       = { api_path: MOCK_SERVER_REQUESTS_API_PATH}
        webc_server_requests = await target_div.append_child(WebC__Server_Requests, attributes)
        await webc_server_requests.wait_for_event('build-complete')
    })

    hooks.afterEach(() => {
        webc_server_requests.remove()
        target_div.remove()
    })

    QUnit.test ('.constructor', (assert) => {
        assert.deepEqual(WebC__Server_Requests.name, 'WebC__Server_Requests')
        assert.ok(WebC__Server_Requests.prototype instanceof WebC__API_To_Table)
        assert.ok(WebC__Server_Requests.prototype instanceof Web_Component)
        assert.ok(webc_server_requests instanceof Web_Component)
        assert.ok(webc_server_requests instanceof HTMLElement)
        assert.ok(webc_server_requests.api_invoke instanceof API__Invoke)
        assert.deepEqual(webc_server_requests.getAttributeNames(), ['api_path'])
        assert.deepEqual(webc_server_requests.api_path, MOCK_SERVER_REQUESTS_API_PATH)
    })

    QUnit.test ('.build', (assert) => {
        let table = new Table()
        table.headers = MOCK_SERVER_REQUESTS_DATA['headers']
        table.rows    = MOCK_SERVER_REQUESTS_DATA['rows']
        let expected_html = `\
<div id="api_to_table">
    <a id="data_reload" href="#reload">reload</a>
${table.html(1)}\
</div>
`;
        // let expected_html = "<div id=\"api_to_table\">\n"+
        //                     "    <a id=\"data_reload\" href=\"#reload\">reload</a>\n" +
        //                          table.html(1) +
        //                     "</div>\n"
        assert.deepEqual(webc_server_requests.inner_html(), expected_html)

    })

    test('processes API response correctly', async assert => {
        const response = await webc_server_requests.invoke_api_path()

        assert.ok(response                                                              , 'Returns response'         )
        assert.ok(response.rows                                                         , 'Has rows data'            )

        if (response.rows.length > 3) {
            const first_cell = response.rows[0][0]
            assert.ok(first_cell.includes('<a href="docs/dev/web-components/server-request?request_id='),
                                                                                         'Formats request ID link'   )
        }
    })

    test('handles empty response data', async assert => {
        setup_mock_responses()
        set_mock_response(MOCK_SERVER_REQUESTS_API_PATH, 'GET', { rows: [] })

        const response = await webc_server_requests.invoke_api_path()
        assert.deepEqual(response.rows             , []                                 , 'Handles empty rows'       )
    })

    test('preserves other response data', async assert => {
        const response = await webc_server_requests.invoke_api_path()

        assert.ok(response.headers                                                      , 'Preserves headers'        )
        assert.ok(response.title                                                        , 'Preserves title'          )
    })
})