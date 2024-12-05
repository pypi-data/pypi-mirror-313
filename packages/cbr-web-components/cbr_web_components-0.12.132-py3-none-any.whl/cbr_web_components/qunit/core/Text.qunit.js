import Text  from '../../js/core/Text.mjs' ;
import Tag  from '../../js/core/Tag.mjs' ;

QUnit.module('Text', function(hooks) {

    QUnit.test('.config',  function (assert) {
        const text = new Text();
        const expected_html_config = {  include_id              : true  ,
                                        include_tag             : true  ,
                                        include_end_tag         : true  ,
                                        indent_before_last_tag  : false ,
                                        new_line_before_elements: false ,
		                                new_line_after_final_tag: false ,
                                        trim_final_html_code    : false }
        assert.propEqual(text.html_config, expected_html_config)
    })

    QUnit.test('.add_element',  function (assert) {
        const text = new Text();
        assert.equal(text.add_element(), false)
    })

    QUnit.test('.html', function (assert) {
        const text = new Text();
        const expected_html_1 = `<text></text>`
        assert.equal(text.html(), expected_html_1)
        text.value = 'aaaa'
        const expected_html_2 = `<text>${text.value}</text>`
        assert.equal(text.html(), expected_html_2)
    })

    QUnit.test('.inner_html', function (assert) {
        let text = new Text()
        assert.deepEqual(text.inner_html(),'')

        text.value = 'abc'
        assert.deepEqual(text.inner_html(),'abc')
    })

    QUnit.test('.just_text', function (assert) {
        let text = new Text()
        assert.deepEqual(text.html_config.include_tag,true  )
        assert.deepEqual(text.just_text(), text             )
        assert.deepEqual(text.html_config.include_tag,false )
    })

    QUnit.test('_should be an instance and inherit from Html_Tag', function(assert) {
        const text = new Text();
        assert.ok(text instanceof Tag, 'Div is an instance of Html_Tag');
        assert.ok(Text.prototype instanceof Tag, '.prototype is an instance of Html_Tag');
        assert.equal(text.tag, 'text');
    });

    QUnit.test('_should escapte html payloads', function (assert) {
        let payload       = '<script>alert("hello")</script>'
        let expected_html = '&lt;script&gt;alert("hello")&lt;/script&gt;'
        const text = new Text({value:payload});
        assert.equal(text.inner_html(), expected_html)
    })
})