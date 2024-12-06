// import API__Invoke from '../../js/data/API__Invoke.mjs'
//
// const { module, test } = QUnit
//
// const MOCK_API_PATH    = '/api/test'
// const MOCK_AUTH_HEADER = 'Bearer test-token'
// const MOCK_DATA        = { test: 'data' }
// const MOCK_RESPONSE    = { success: true }
//
// module('API__Invoke', hooks => {
//     let api_invoke
//     let original_fetch
//     let fetch_calls = []
//
//     hooks.beforeEach(() => {
//         api_invoke = new API__Invoke()
//         original_fetch = window.fetch
//
//         // Mock fetch to track calls and return mock response
//         window.fetch = async (url, options) => {
//             fetch_calls.push({ url, options })
//             return {
//                 ok: true,
//                 json: async () => MOCK_RESPONSE
//             }
//         }
//     })
//
//     hooks.afterEach(() => {
//         window.fetch = original_fetch
//         fetch_calls  = []
//     })
//
//     test('constructor initializes correctly', assert => {
//         assert.ok(api_invoke.channel.startsWith('api_invoke_')         , 'Generates default channel'     )
//         assert.equal(api_invoke.on_error_return_value, null           , 'Default error value is null'   )
//
//         const custom_channel = 'test-channel'
//         const custom_api    = new API__Invoke(custom_channel)
//         assert.equal(custom_api.channel, custom_channel               , 'Uses provided channel'         )
//     })
//
//     test('invoke_api sends GET request correctly', async assert => {
//         await api_invoke.invoke_api(MOCK_API_PATH)
//
//         const call = fetch_calls[0]
//         assert.equal(call.url                                , MOCK_API_PATH                   , 'Uses correct URL'            )
//         assert.equal(call.options.method                     , 'GET'                          , 'Uses GET method'             )
//         assert.equal(call.options.headers['Content-Type']    , 'application/json'             , 'Sets content type'           )
//         assert.equal(call.options.body                       , undefined                      , 'No body for GET'             )
//     })
//
//     test('invoke_api sends POST request with data', async assert => {
//         await api_invoke.invoke_api(MOCK_API_PATH, 'POST', MOCK_DATA)
//
//         const call = fetch_calls[0]
//         assert.equal(call.url                                , MOCK_API_PATH                   , 'Uses correct URL'            )
//         assert.equal(call.options.method                     , 'POST'                         , 'Uses POST method'            )
//         assert.equal(call.options.body                       , JSON.stringify(MOCK_DATA)      , 'Includes stringified data'   )
//     })
//
//     test('invoke_api sends PUT request with data', async assert => {
//         await api_invoke.invoke_api(MOCK_API_PATH, 'PUT', MOCK_DATA)
//
//         const call = fetch_calls[0]
//         assert.equal(call.url                                , MOCK_API_PATH                   , 'Uses correct URL'            )
//         assert.equal(call.options.method                     , 'PUT'                          , 'Uses PUT method'             )
//         assert.equal(call.options.body                       , JSON.stringify(MOCK_DATA)      , 'Includes stringified data'   )
//     })
//
//     test('invoke_api includes auth header when provided', async assert => {
//         await api_invoke.invoke_api(MOCK_API_PATH, 'GET', null, MOCK_AUTH_HEADER)
//
//         const call = fetch_calls[0]
//         assert.equal(call.options.headers['Authorization']   , MOCK_AUTH_HEADER               , 'Includes auth header'        )
//     })
//
//     test('invoke_api handles failed requests', async assert => {
//         window.fetch = async () => ({
//             ok: false,
//             status: 404
//         })
//
//         try {
//             await api_invoke.invoke_api(MOCK_API_PATH)
//             assert.notOk(true                                                                 , 'Should throw error'          )
//         } catch (error) {
//             assert.ok(error instanceof Error                                                  , 'Throws error'               )
//             assert.ok(error.message.includes('404')                                          , 'Includes status code'        )
//         }
//     })
//
//     test('invoke_api returns error value when set', async assert => {
//         window.fetch = async () => ({ ok: false })
//         api_invoke.on_error_return_value = MOCK_DATA
//
//         const result = await api_invoke.invoke_api(MOCK_API_PATH)
//         assert.deepEqual(result                               , MOCK_DATA                     , 'Returns error value'         )
//     })
//
//     test('invoke_api handles network errors', async assert => {
//         window.fetch = async () => { throw new Error('Network error') }
//
//         try {
//             await api_invoke.invoke_api(MOCK_API_PATH)
//             assert.notOk(true                                                                 , 'Should throw error'          )
//         } catch (error) {
//             assert.ok(error instanceof Error                                                  , 'Throws error'               )
//             assert.equal(error.message                        , 'Network error'               , 'Preserves error message'     )
//         }
//     })
//
//     test('random_id generates unique IDs', assert => {
//         const id1 = api_invoke.random_id()
//         const id2 = api_invoke.random_id()
//
//         assert.ok   (id1.startsWith('random_')                                               , 'Uses default prefix'         )
//         assert.ok   (id2.startsWith('random_')                                               , 'Consistent prefix'           )
//         assert.notEqual(id1                                   , id2                          , 'Generates unique IDs'        )
//
//         const custom_prefix = 'test'
//         const id3 = api_invoke.random_id(custom_prefix)
//         assert.ok(id3.startsWith(`${custom_prefix}_`)                                        , 'Uses custom prefix'          )
//     })
// })