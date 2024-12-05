// todo: rewrite this when we add a way to mock the css load calls or when we implement a better more WebC native way to show the JSON
//
// import Web_Component      from "../../../js/core/Web_Component.mjs";
// import WebC__API_To_Json  from "../../../js/elements/api/WebC__API_To_Json.mjs";
// import WebC__Target_Div   from "../../../js/utils/WebC__Target_Div.mjs";
// import API__Invoke        from "../../../js/data/API__Invoke.mjs";
// import Text_Highlight     from "../../../js/plugins/Text_Highlight.mjs";
//
//
// QUnit.module('WebC__API_To_Json', function(hooks) {
//     let target_div
//     let webc__api_to_json
//     let mock_responses
//     let api_path
//     let api_data
//     //let skip_tests;
//
//     hooks.beforeEach(async (assert) =>{
//         api_path            = '/an/path/to/load'
//         api_data            = { version: 'v0.6.8' };
//         mock_responses      = JSON.stringify({[api_path]: api_data})
//         target_div          = WebC__Target_Div.add_to_body().build()
//         let attributes      = {mock_responses: mock_responses, api_path: api_path}
//         webc__api_to_json   = await target_div.append_child(WebC__API_To_Json, attributes)
//         await webc__api_to_json.wait_for__component_ready()
//     })
//
//     hooks.afterEach(() => {
//         //if (skip_tests) { return }
//         webc__api_to_json.remove()
//         target_div.remove()
//     })
//
//     QUnit.only('.constructor', (assert) => {
//         assert.deepEqual(WebC__API_To_Json.name           , 'WebC__API_To_Json'     )
//         assert.ok       (WebC__API_To_Json.prototype      instanceof Web_Component  )
//         assert.ok       (webc__api_to_json                instanceof Web_Component  )
//         assert.ok       (webc__api_to_json                instanceof HTMLElement    )
//         assert.ok       (webc__api_to_json.api_invoke     instanceof API__Invoke    )
//         assert.ok       (webc__api_to_json.text_highlight instanceof Text_Highlight )
//         assert.ok       (webc__api_to_json.text_highlight.css_loaded     )
//         assert.ok       (webc__api_to_json.text_highlight.css_code !== '')
//         assert.deepEqual(webc__api_to_json.getAttributeNames(), ['mock_responses', 'api_path'])
//         assert.deepEqual(webc__api_to_json.api_invoke.mock_responses, JSON.parse(mock_responses))
//         assert.deepEqual(typeof(hljs), 'object')
//         assert.deepEqual(hljs.versionString, '11.9.0')
//         assert.deepEqual(webc__api_to_json.api_path    , api_path)
//     })
//
//     QUnit.test('.html', async (assert) => {
//         let api_response = await webc__api_to_json.invoke_api_path()
//         assert.deepEqual(api_response, api_data)
//     })
//
//     QUnit.test('.html', (assert) => {
//         let expected_html = '<h2>/an/path/to/load</h2><pre><span class="hljs-punctuation">{</span>\n    <span class="hljs-attr">"version"</span><span class="hljs-punctuation">:</span> <span class="hljs-string">"v0.6.8"</span>\n<span class="hljs-punctuation">}</span></pre>'
//         let html          = webc__api_to_json.inner_html()
//         assert.deepEqual(html, expected_html)
//
//     })
// })
//
// //Expected: '<h2>/an/path/to/load</h2><pre><span class="hljs-punctuation">{</span>\n <span class="hljs-attr">"version"</span><span class="hljs-punctuation">:</span> <span class="hljs-string">"v0.6.8"</span>\n<span class="hljs-punctuation">}</span></pre>'
// // 	Actual: '<h2>/an/path/to/load</h2><pre><span class="hljs-punctuation">{</span>\n    <span class="hljs-attr">"version"</span><span class="hljs-punctuation">:</span> <span class="hljs-string">"v0.6.8"</span>\n<span class="hljs-punctuation">}</span></pre>'