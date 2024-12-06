import Text_Highlight from "../../js/plugins/Text_Highlight.mjs";
import WebC__Target_Div from "../../js/utils/WebC__Target_Div.mjs";
import Web_Component from "../../js/core/Web_Component.mjs";


QUnit.module('Text_Highlight.qunit', function(hooks) {

    let text_highlight;
    let target_div

    hooks.beforeEach(() =>{
        target_div          = WebC__Target_Div.add_to_body().build()
        text_highlight      = new Text_Highlight(target_div)
    })

    QUnit.test('.constructor()', (assert)=> {
        assert.ok       (target_div     instanceof Web_Component )
        assert.ok       (text_highlight instanceof Text_Highlight)
        assert.deepEqual(text_highlight.css_loaded , false       )
        assert.deepEqual(text_highlight.js_loaded  , false       )
        assert.deepEqual(text_highlight.target_webc, target_div  )
    })

    QUnit.test('.load_css()', async (assert)=> {
        if (typeof window.__karma__ !== 'undefined') {
            assert.ok(true, 'Skipped in Karma environment');
            return;
        }
        let css_signature = 'Description: Original highlight.js style'

        assert.deepEqual(text_highlight.css_loaded, false)
        assert.deepEqual(text_highlight.css_code  , '')
        assert.deepEqual(text_highlight.css_code.indexOf(css_signature), -1)

        await text_highlight.load_css()

        assert.deepEqual(text_highlight.css_loaded, true)
        assert.notDeepEqual(text_highlight.css_code, '')
        assert.deepEqual(text_highlight.css_code.indexOf(css_signature), 23)
    })

    QUnit.test('.load_highlight_js()', async (assert)=> {
        if (typeof window.__karma__ !== 'undefined') {
            assert.ok(true, 'Skipped in Karma environment');
            return;
        }
        //assert.deepEqual(typeof(hljs), 'undefined')               // in Karma, hljs is already loaded by the time we reach here
        assert.ok(text_highlight.js_loaded === false)
        await text_highlight.load_highlight_js()
        assert.ok(text_highlight.js_loaded === true)
        assert.deepEqual(typeof(hljs), 'object')
        assert.deepEqual(hljs.versionString, '11.9.0')
    })

    QUnit.test('.format_text()',  async (assert)=> {
        if (typeof window.__karma__ !== 'undefined') {
            assert.ok(true, 'Skipped in Karma environment');
            return;
        }
        await text_highlight.load_highlight_js()
        let text = 'this is **bold** in markdown\n\nnew line'
        let expected_html = 'this is <span class="hljs-strong">**bold**</span> in markdown\n\nnew line'
        let formatted_html   = text_highlight.format_text(text, 'markdown')
        assert.deepEqual(formatted_html, expected_html)
    })
})