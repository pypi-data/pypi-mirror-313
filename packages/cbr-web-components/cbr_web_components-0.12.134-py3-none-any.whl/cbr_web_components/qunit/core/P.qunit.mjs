// P.qunit.mjs
import P   from '../../js/core/P.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('P', hooks => {
    test('constructor creates paragraph element', assert => {
        // Basic instantiation
        const p = new P({})
        assert.equal(p.tag                      , 'p'              , 'Sets correct tag name')
        assert.ok   (p instanceof Tag                              , 'Inherits from Tag')

        // With text content
        const with_text = new P({ value: 'Paragraph Text' })
        assert.equal(with_text.value            , 'Paragraph Text' , 'Sets paragraph text')

        // With multiple attributes
        const complex = new P({
            value : 'Complex Text'              ,
            class : 'custom-para'               ,
            id    : 'para-1'                    ,
            style : 'color: blue;'
        })
        assert.equal(complex.value              , 'Complex Text'   , 'Sets text')
        assert.equal(complex.class              , 'custom-para'    , 'Sets class')
        assert.equal(complex.id                 , 'para-1'         , 'Sets id')
        assert.equal(complex.attributes.style   , 'color: blue;'   , 'Sets style')
    })

    test('generates correct HTML', assert => {
        const p = new P({
            value : 'Test Paragraph'            ,
            class : 'test-para'
        })
        const expected = '<p class="test-para">Test Paragraph</p>\n'
        assert.equal(p.html()                   , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const p = new P()
        assert.equal(p.html()                   , '<p>\n</p>\n'    , 'Generates minimal HTML')
    })
})
