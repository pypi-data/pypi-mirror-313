import WebC__Target_Div from "../../js/utils/WebC__Target_Div.mjs";
import Web_Component    from '../../js/core/Web_Component.mjs'

QUnit.module('WebC__Target_Div', function(hooks) {

    let target_div
    let target_div_setup

    hooks.before(async (assert) => {
        target_div_setup = { right:"50px", top:"250px", width: "30%", height:"100px"}
        target_div       = WebC__Target_Div.add_to_body().build(target_div_setup)
    });


    QUnit.test('build', (assert) => {
        const expected_html = `\
<div class="target_div">
    <slot>
    </slot>
</div>
`
        assert.equal(target_div.html() , expected_html)
    })

    QUnit.test ('constructor', (assert) => {
        assert.ok(WebC__Target_Div.prototype instanceof Web_Component , 'WebC__Target_Div.prototype is an instance of Web_Component');
        assert.ok       (target_div instanceof Web_Component          , 'target_div is an instance of Web_Component')
        assert.deepEqual(target_div.channels, [ 'Web_Component', target_div.channel]     , 'target_div.channels == [ "Web_Component" ]')
    })


})