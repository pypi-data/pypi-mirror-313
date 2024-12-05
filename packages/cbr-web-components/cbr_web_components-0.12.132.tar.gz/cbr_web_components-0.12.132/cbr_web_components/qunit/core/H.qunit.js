import H   from '../../js/core/H.mjs';
import Tag from '../../js/core/Tag.mjs';

QUnit.module('H', function(hooks) {

    QUnit.test('.constructor',  function (assert) {
        assert.equal(new H().tag, 'h1')
        assert.equal(new H({level:1}).tag, 'h1')
        assert.equal(new H({level:2}).tag, 'h2')
        assert.equal(new H({level:3}).tag, 'h3')

        assert.equal(new H({level:'A'}).tag, 'hA')          // todo: this is a bug, only h1 .. h6 values should be accepted
    })


    QUnit.test('.add_element', function (assert) {
        assert.equal(new H().add_element('abc'), false)
    })

    QUnit.test('.inner_html', function (assert) {
        let h = new H()
        assert.deepEqual(h.inner_html(),'')

        h.value = 'abc'
        assert.deepEqual(h.inner_html(),'abc')
    })

    QUnit.test('.html', function (assert) {
        const h1 = new H();
        assert.equal(h1.html(), `<h1></h1>\n`)

        const h2 = new H({level:2, value:'abc'});
        assert.equal(h2.html(), `<h2>abc</h2>\n`)
    })

    QUnit.test('_should be an instance and inherit from Html_Tag', function(assert) {
        const h = new H();
        assert.ok(h instanceof Tag, 'Div is an instance of Html_Tag');
        assert.ok(H.prototype instanceof Tag, 'Div.prototype is an instance of Html_Tag');
        assert.equal(h.tag, 'h1');
  });
})
