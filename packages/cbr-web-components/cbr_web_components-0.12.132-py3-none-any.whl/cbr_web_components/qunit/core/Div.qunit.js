import Div from '../../js/core/Div.mjs';
import Tag from '../../js/core/Tag.mjs';

QUnit.module('Div', function(hooks) {

    QUnit.test('constructor', (assert) =>{
        let div_1  = new Div()
        let div_2  = new Div({id:'div_2'})
        let div_3  = new Div({class:'an_class'})
        let div_4  = new Div({id:'an_id', class:'another_class'})
        let html_1 = '<div>\n</div>\n'
        let html_2 = '<div id="div_2">\n</div>\n'
        let html_3 = '<div class="an_class">\n</div>\n'
        let html_4 = '<div id="an_id" class="another_class">\n</div>\n'
        assert.equal(div_1.html(), html_1)
        assert.equal(div_2.html(), html_2)
        assert.equal(div_3.html(), html_3)
        assert.equal(div_4.html(), html_4)
    })

    QUnit.test('add_div', (assert) =>{
        let div_parent = new Div({id:'parent'})
        let div_child  = div_parent.add_div({id:'child'})
        assert.equal(div_parent.html(), '<div id="parent">\n    <div id="child">\n    </div>\n</div>\n')
        assert.equal(div_child .html(), '<div id="child">\n</div>\n')
    })

    QUnit.test('add_tag', (assert) =>{
        let div_parent = new Div({id:'parent'})
        let tag_child  = div_parent.add_tag({tag:'title', id:'child'})
        assert.equal(div_parent.html(), '<div id="parent">\n    <title id="child">\n    </title>\n</div>\n')
        assert.equal(tag_child .html(), '<title id="child">\n</title>\n')
    })

    QUnit.test('add_text', (assert) =>{
        let text       = 'this is some text'
        let div_parent = new Div({id:'parent'})
        let text_child  = div_parent.add_text(text)
        assert.equal(div_parent.html(), `<div id="parent">\n    <text>${text}</text></div>\n`)
        assert.equal(text_child .html(), `<text>${text}</text>`)
    })

    QUnit.test('_should be an instance and inherit from Html_Tag', function(assert) {
        const divInstance = new Div()
        assert.ok(divInstance instanceof Tag, 'Div is an instance of Html_Tag');
        assert.ok(Div.prototype instanceof Tag, 'Div.prototype is an instance of Html_Tag');
    });

    QUnit.test('.dom , dom_add', function (assert) {
        const margin = 40
        const border = '10px solid blue'
        const div = new Div({id:'dom_add'})
        div.set_styles({'top'    : `${margin}px`   ,
                        'bottom' : `${margin}px`   ,
                        'right'  : `${margin}px`   ,
                        'left'   : `${margin}px`   ,
                        'border' : border          ,
                        'position': 'absolute'     })

        const expected_html = `<div id="dom_add" style="border: 10px solid blue; bottom: 40px; left: 40px; position: absolute; right: 40px; top: 40px;">\n</div>\n`
        const actual_html = div.html()
        assert.equal(actual_html, expected_html, "html matches expected")
        assert.equal(document.querySelectorAll('#'+div.id).length, 0, "there are no divs with div.id on the page")
        assert.equal(div.dom_add(), true , "adding once should work" )
        assert.equal(div.dom_add(), false, "adding again should fail")
        assert.equal(div.parent_id, null)
        assert.equal(div.parent_dom, document.body)
        assert.equal(document.querySelectorAll('#'+div.id).length, 1, "the div.id is now on the page")
        assert.equal(div.dom(), document.getElementById(div.id))
        assert.equal(div.dom_remove(), true)
        assert.equal(div.dom_remove(), false)
        assert.equal(document.querySelectorAll('#'+div.id).length, 0, "after remove the div.id is not on the page")
    })

})
