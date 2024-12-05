import Container__Two_Cols from "../../../js/core/layout/Container__Two_Cols.mjs";


QUnit.module('Table', function(hooks) {

    QUnit.test('constructor', (assert) => {
        let container_two_cols = new Container__Two_Cols({id: 'an_container', class: 'an_class'})
        let container_html = container_two_cols.html()
        assert.equal(container_html, expected_html__constructor)
    })

    let expected_html__constructor = `\
<div class="container">
    <div class="row">
        <div class="col">
        </div>
        <div class="col">
        </div>
    </div>
</div>
`
})