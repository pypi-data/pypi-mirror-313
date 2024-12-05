// todo: see if we still need this functionality (if so this test needs to be updated to the new Mock_API__Invoke testing architecture)
// import WebC__S3_Browser__Server_Requests from "../../../js/elements/ui/WebC__S3_Browser__Server_Requests.mjs";
// import WebC__Target_Div                  from "../../../js/utils/WebC__Target_Div.mjs";
// import Web_Component                     from "../../../js/core/Web_Component.mjs";
// import API__Invoke                       from "../../../js/data/API__Invoke.mjs";
//
//
// QUnit.module('WebC__S3_Browser__Server_Requests', function(hooks) {
//     let target_div
//     let webc_s3_browser_server_requests
//     let mock_responses
//     let api_path
//     let api_data
//
//     hooks.beforeEach(async (assert) => {
//         api_path            = '/an/path/to/load'
//         mock_responses      = JSON.stringify(api_mock_data())
//         //console.log(mock_responses)
//         target_div          = WebC__Target_Div.add_to_body().build()
//         let attributes      = { mock_responses: mock_responses, api_path: api_path}
//         webc_s3_browser_server_requests   = await target_div.append_child(WebC__S3_Browser__Server_Requests, attributes)
//         await webc_s3_browser_server_requests.wait_for_event('build-complete')
//     })
//
//     function api_mock_data() {
//         let api__file_contents       = WebC__S3_Browser__Server_Requests.url__api_file_contents
//         let api__list_folders        = WebC__S3_Browser__Server_Requests.url__api_list_folders
//         let api__list_files_metadata = WebC__S3_Browser__Server_Requests.url__api_list_files_metadata
//         return {
//                  [api__list_folders                    ]: ["server-requests"               ],
//                  [api__list_folders + "server-requests"]: ["qunit-server", 'another-server'],
//                  [api__file_contents                   ]: ['file-a.json.gz'                ],
//                  [api__list_files_metadata             ]: {"file_count"    : 0              ,
//                                                            "duration"      : {"seconds": 1 },
//                                                            "files_metadata": []}
//                 }
//     }
//
//     hooks.afterEach(() => {
//         webc_s3_browser_server_requests.remove()
//         target_div.remove()
//     })
//
//     QUnit.test ('.constructor', (assert) => {
//         assert.deepEqual(WebC__S3_Browser__Server_Requests.name, 'WebC__S3_Browser__Server_Requests')
//         assert.ok(WebC__S3_Browser__Server_Requests.prototype instanceof Web_Component)
//         assert.ok(webc_s3_browser_server_requests instanceof Web_Component)
//         assert.ok(webc_s3_browser_server_requests instanceof HTMLElement)
//         assert.ok(webc_s3_browser_server_requests.api_invoke instanceof API__Invoke)
//         assert.deepEqual(webc_s3_browser_server_requests.getAttributeNames(), ['mock_responses', 'api_path'])
//
//         assert.deepEqual(webc_s3_browser_server_requests.api_invoke.mock_responses, JSON.parse(mock_responses))
//     })
//
//     QUnit.test ('.api_get_folders', async (assert) => {
//         let result = await webc_s3_browser_server_requests.api_get_folders()
//         assert.deepEqual(result, ['server-requests'])
//     })
//
//     QUnit.test ('.html', async (assert) => {
//         const element_html = webc_s3_browser_server_requests.inner_html()
//         //console.log(element_html)
//         assert.deepEqual(element_html, expected_html)
//     })
//
// })
//
// // todo: find a better way to test the html output
// const expected_html = '<div id="api_to_table">\n' +
// 		  '    <a class="reload-link" href="#">reload</a>\n' +
// 		  '    <hr>\n' +
// 		  '    \n' +
// 		  '    <span>Path:</span>\n' +
// 		  '    <a class="parent-link" href=""></a>\n' +
// 		  '    <b>/</b>\n' +
// 		  '    <hr>\n' +
// 		  '    \n' +
// 		  '    <span>Folders:</span>\n' +
// 		  '    <a class="folder-link" href="server-requests">server-requests</a>\n' +
// 		  '    <span>|</span>\n' +
// 		  '    <hr>\n' +
// 		  '    \n' +
// 		  '<div class="container">\n' +
// 		  '    <div class="row">\n' +
// 		  '        <div class="col">\n' +
// 		  '            <table>\n' +
// 		  '                <thead>\n' +
// 		  '                    <tr>\n' +
// 		  '                        <td>req id</td>\n' +
// 		  '                        <td>method</td>\n' +
// 		  '                        <td>path</td>\n' +
// 		  '                        <td>duration</td>\n' +
// 		  '                        <td>status_code</td>\n' +
// 		  '                        <td>time</td>\n' +
// 		  '                    </tr>\n' +
// 		  '                </thead>\n' +
// 		  '                <tbody>\n' +
// 		  '                </tbody>\n' +
// 		  '            </table>\n' +
// 		  '        </div>\n' +
// 		  '        <div class="col">\n' +
// 		  '            <div id="file_contents" class="file_contents">file contents will go here</div>\n' +
// 		  '        </div>\n' +
// 		  '    </div>\n' +
// 		  '</div>\n' +
// 		  '</div>\n' +
// 		  ''