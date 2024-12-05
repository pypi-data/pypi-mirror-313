import Raw_Html from '../../js/core/Raw_Html.mjs';
import Tag      from '../../js/core/Tag.mjs' ;

QUnit.module('Html', function(hooks) {

    QUnit.test('.constructor',  function (assert) {
        const html_1 = new Raw_Html();
        assert.equal(html_1.tag     , 'div')
        assert.equal(html_1.value   , null  )
        assert.equal(html_1.raw_html, ''    )
        assert.equal(html_1.class   , null  )
        assert.equal(html_1.id      , null  )
        assert.equal(html_1.html_config.include_tag, true)
        const html_2 = new Raw_Html({id:'an_id', 'class':'an_class'});
        assert.equal(html_2.tag     , 'div'    )
        assert.equal(html_2.value   , null      )
        assert.equal(html_2.raw_html, ''        )
        assert.equal(html_2.id      , 'an_id'   )
        assert.equal(html_2.class   , 'an_class')

    })

    QUnit.test('.config',  function (assert) {
        const html = new Raw_Html();
        const expected_html_config = {  include_id              : true ,
                                        include_end_tag         : true ,
                                        include_tag             : true,
                                        indent_before_last_tag  : true ,
                                        new_line_before_elements: true ,
		                                new_line_after_final_tag: true ,
                                        trim_final_html_code    : false }
        assert.propEqual(html.html_config, expected_html_config)
    })

    QUnit.test('.add_element',  function (assert) {
        const html = new Raw_Html();
        assert.equal(html.add_element(), false)
    })

    QUnit.test('.html',  function (assert) {
        const html_1 = new Raw_Html();                                          // .html() use case 1
        assert.equal(html_1.html_config.include_tag, true, 'html_config.include_tag should have the defaults of true')
        const expected_html_1 = '<div>\n</div>\n'
        assert.equal(html_1.html(), expected_html_1)

        const html_2  = new Raw_Html();                                         // .html() use case 2
        const value_1 = '<b>an<i>html</i> is here</b>'
        assert.equal(html_1.html_config.include_tag, true, 'html_config.include_tag should be the default true')
        html_2.raw_html = value_1
        const expected_html_2 = `<div>\n    ${value_1}\n</div>\n`
        assert.equal(html_2.html(), expected_html_2)

        const html_3 = new Raw_Html();                                          // .html() use case 3
        html_3.html_config.include_tag = true
        assert.equal(html_3.html_config.include_tag, true)
        const expected_html_3 = `<div>\n</div>\n`
        assert.equal(html_3.html(), expected_html_3)

        const html_4  = new Raw_Html();                                         // .html() use case 4
        const value_2 = '<b>an<i>html</i> is here</b>'
        html_4.html_config.include_tag = true
        html_4.raw_html = value_2
        assert.equal(html_4.html_config.include_tag, true)
        const expected_html_4 = `<div>\n    ${html_4.raw_html}\n</div>\n`
        assert.equal(html_4.html(), expected_html_4)
    })

    QUnit.test('.inner_html', function (assert) {
        let html = new Raw_Html()
        assert.deepEqual(html.inner_html(),'')

        html.raw_html = 'abc'
        assert.deepEqual(html.inner_html(),'abc\n')
    })

    QUnit.test('_should be an instance and inherit from Tag', function(assert) {
        const html = new Raw_Html();
        assert.ok(html instanceof Tag, 'Div is an instance of Tag');
        assert.ok(Raw_Html.prototype instanceof Tag, '.prototype is an instance of Tag');
        assert.equal(html.tag, 'div'               , 'raw_html tag name should be div');
    });
})