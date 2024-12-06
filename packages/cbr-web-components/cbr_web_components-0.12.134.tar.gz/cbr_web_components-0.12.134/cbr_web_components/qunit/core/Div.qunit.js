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

    QUnit.test('add_tag - no params', (assert) =>{
        let div_parent = new Div({id:'parent'})
        let tag_child  = div_parent.add_tag()
        assert.equal(div_parent.html(), '<div id="parent">\n    <tag>\n    </tag>\n</div>\n')
        assert.equal(tag_child .html(), '<tag>\n</tag>\n')
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

    QUnit.test('handles empty constructor parameters', (assert) => {
        const div = new Div()
        assert.equal(div.tag              , 'div'            , 'Sets correct tag name')
        assert.deepEqual(div.attributes   , {}               , 'Has empty attributes')
        assert.ok(div instanceof Tag                         , 'Inherits from Tag')
    })

    QUnit.test('nested divs maintain proper indentation', (assert) => {
        const parent = new Div()
        const child1 = parent.add_div()
        const child2 = child1.add_div()

        const expected = '<div>\n' +
                        '    <div>\n' +
                        '        <div>\n' +
                        '        </div>\n' +
                        '    </div>\n' +
                        '</div>\n'

        assert.equal(parent.html(), expected, 'Maintains proper nesting indentation')
    })

    QUnit.test('multiple child elements maintain order', (assert) => {
        const parent = new Div({ id: 'parent' })
        const div1   = parent.add_div ({ id: 'div1'   })
        const text1  = parent.add_text('text1')
        const div2   = parent.add_div ({ id: 'div2'   })

        const expected = '<div id="parent">\n' +
                        '    <div id="div1">\n' +
                        '    </div>\n' +
                        '    <text>text1</text>' +
                        '    <div id="div2">\n' +
                        '    </div>\n' +
                        '</div>\n'

        assert.equal(parent.html(), expected, 'Maintains child element order')
    })

    QUnit.test('add_div returns the created div instance', (assert) => {
        const parent = new Div()
        const child  = parent.add_div({ class: 'child' })

        assert.ok   (child instanceof Div            , 'Returns Div instance'     )
        assert.equal(child.class      , 'child'      , 'Sets provided attributes' )
    })

    QUnit.test('handles complex nested structures', (assert) => {
        const root = new Div({ id: 'root' })
        const div1 = root.add_div({ class: 'level-1' })
        div1.add_text('Text in level 1')
        const div2 = div1.add_div({ class: 'level-2' })
        div2.add_text('Text in level 2')

        const expected = '<div id="root">\n' +
                        '    <div class="level-1">\n' +
                        '        <text>Text in level 1</text>' +
                        '        <div class="level-2">\n' +
                        '            <text>Text in level 2</text>' +
                        '        </div>\n' +
                        '    </div>\n' +
                        '</div>\n'

        assert.equal(root.html(), expected, 'Correctly renders complex nested structure')
    })

    QUnit.test('add_tag with various HTML elements', (assert) => {
        const div = new Div()
        const span = div.add_tag({ tag: 'span', value: 'Span text' })
        const p    = div.add_tag({ tag: 'p'   , value: 'Paragraph' })

        const expected = '<div>\n' +
                        '    <span>Span text</span>\n' +
                        '    <p>Paragraph</p>\n' +
                        '</div>\n'

        assert.equal(div.html() , expected     , 'Renders mixed HTML elements')
        assert.equal(span.tag   , 'span'       , 'Sets correct tag for span' )
        assert.equal(p.tag      , 'p'          , 'Sets correct tag for p'    )
    })

    QUnit.test('add_text maintains text content integrity', (assert) => {
        const div = new Div()
        const text1 = div.add_text('Line 1\nLine 2')
        const text2 = div.add_text('Special chars: <>&"\'')

        assert.equal(text1.value, 'Line 1\nLine 2'          , 'Preserves line breaks'     )
        assert.equal(text2.value, 'Special chars: <>&"\''   , 'Preserves special chars'   )
    })
})
