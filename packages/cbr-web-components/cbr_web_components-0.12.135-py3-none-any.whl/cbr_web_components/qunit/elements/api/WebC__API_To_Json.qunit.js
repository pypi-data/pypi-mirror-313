//todo: wire this test
// import WebC__API_To_Json       from '../../../js/elements/api/WebC__API_To_Json.mjs'
// import WebC__Target_Div        from '../../../js/utils/WebC__Target_Div.mjs'
// import Web_Component           from '../../../js/core/Web_Component.mjs'
// import { setup_mock_responses,
//          MOCK_SERVER_REQUESTS_API_PATH,
//          MOCK_SERVER_REQUESTS_DATA }   from '../../../js/testing/Mock_API__Data.mjs'
//
// const { module, test } = QUnit
//
// module.only('WebC__API_To_Json', hooks => {
//     let target_div
//     let api_to_json
//     let mock_highlight_loaded = false
//
//     hooks.before(async () => {
//         setup_mock_responses()
//
//         // Create mock Text_Highlight class
//         //api_to_json?.text_highlight?.mock_calls || []
//         class Mock_Text_Highlight {
//             constructor(component) {
//                 this.component = component
//                 this.mock_calls = []
//             }
//
//             async load_css()          { mock_highlight_loaded = true                }
//             async load_highlight_js() { mock_highlight_loaded = true                }
//             format_text(text)         { return `formatted:${text}`                  }
//         }
//
//         // Replace the actual Text_Highlight with our mock
//         WebC__API_To_Json.prototype.Text_Highlight = Mock_Text_Highlight
//
//         target_div = WebC__Target_Div.add_to_body()
//         api_to_json = await target_div.append_child(WebC__API_To_Json,
//             { api_path: MOCK_SERVER_REQUESTS_API_PATH })
//         await api_to_json.wait_for__component_ready()
//     })
//
//     hooks.after(() => {
//         api_to_json?.remove()
//         target_div?.remove()
//         mock_highlight_loaded = false
//     })
//
//     test('constructor and inheritance', assert => {
//         assert.equal(api_to_json.tagName.toLowerCase()    , 'webc-api-to-json'    , 'Has correct tag name'     )
//         assert.equal(api_to_json.constructor.element_name , 'webc-api-to-json'    , 'Has correct element name' )
//         assert.equal(api_to_json.constructor.name        , 'WebC__API_To_Json'   , 'Has correct class name'   )
//
//         assert.ok(api_to_json.shadowRoot                                          , 'Has shadow root'          )
//         assert.ok(api_to_json.api_invoke                                          , 'Has API invoke instance'  )
//         assert.ok(api_to_json.text_highlight                                      , 'Has text highlight'       )
//
//         assert.ok(api_to_json instanceof Web_Component                            , 'Extends Web_Component'    )
//         assert.ok(api_to_json instanceof HTMLElement                              , 'Is HTML Element'          )
//     })
//
//     test('loads API data correctly', async assert => {
//         assert.equal(api_to_json.api_path, MOCK_SERVER_REQUESTS_API_PATH          , 'Sets API path'           )
//         assert.deepEqual(api_to_json.api_data, MOCK_SERVER_REQUESTS_DATA          , 'Loads correct data'      )
//     })
//
//     test('applies syntax highlighting', async assert => {
//         assert.ok(mock_highlight_loaded                                           , 'Loads highlight.js'       )
//
//         const formatted = api_to_json.text_highlight.format_text('test')
//         assert.equal(formatted, 'formatted:test'                                  , 'Formats text correctly'   )
//     })
//
//     test('renders content with title', async assert => {
//         api_to_json.use_api_path_as_title = true
//         await api_to_json.refresh_ui()
//
//         const content = api_to_json.shadow_root().innerHTML
//         assert.ok(content.includes(`<h2>${MOCK_SERVER_REQUESTS_API_PATH}</h2>`)  , 'Shows API path as title' )
//         assert.ok(content.includes('<pre>')                                       , 'Includes pre element'    )
//         assert.ok(content.includes('formatted:')                                  , 'Content is formatted'    )
//     })
//
//     test('renders content without title', async assert => {
//         api_to_json.use_api_path_as_title = false
//         await api_to_json.refresh_ui()
//
//         const content = api_to_json.shadow_root().innerHTML
//         assert.notOk(content.includes('<h2>')                                     , 'No title shown'          )
//         assert.ok(content.includes('<pre>')                                       , 'Includes pre element'    )
//     })
//
//     test('handles API errors gracefully', async assert => {
//         // Setup error response
//         set_mock_response(MOCK_SERVER_REQUESTS_API_PATH, 'GET', null, 500)
//
//         try {
//             await api_to_json.invoke_api_path()
//             assert.notOk(true                                                     , 'Should throw error'      )
//         } catch (error) {
//             assert.ok(error instanceof Error                                      , 'Throws error'           )
//             assert.ok(error.message.includes('500')                               , 'Includes status code'    )
//         }
//     })
//
//     test('handles mock responses', async assert => {
//         const mock_data = { test: 'data' }
//         api_to_json.api_invoke.mock_responses = {
//             [MOCK_SERVER_REQUESTS_API_PATH]: mock_data
//         }
//
//         const result = await api_to_json.invoke_api_path()
//         assert.deepEqual(result, mock_data                                        , 'Uses mock response'      )
//     })
//
//     test('formats JSON correctly', async assert => {
//         const test_data = { test: 'value' }
//         api_to_json.api_data = test_data
//
//         const html = api_to_json.html()
//         const expected_json = JSON.stringify(test_data, null, '    ')
//
//         assert.ok(html.includes(`formatted:${expected_json}`)                     , 'JSON properly formatted' )
//     })
//
//     test('component lifecycle', async assert => {
//         assert.expect(2)
//         const new_api_to_json = document.createElement('webc-api-to-json')
//
//         new_api_to_json.addEventListener('webc::component-ready', () => {
//             assert.ok(true                                                        , 'Fires ready event'       )
//         })
//
//         document.body.appendChild(new_api_to_json)
//         assert.ok(new_api_to_json.shadowRoot                                      , 'Creates shadow root'     )
//
//         new_api_to_json.remove()
//     })
// })