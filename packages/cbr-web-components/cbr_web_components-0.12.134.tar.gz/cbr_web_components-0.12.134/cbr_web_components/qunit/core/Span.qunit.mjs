// Span.qunit.mjs
import Span from '../../js/core/Span.mjs'
import Tag  from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Span', hooks => {
    test('constructor creates span element', assert => {
        // Basic instantiation
        const span = new Span({})
        assert.equal(span.tag                   , 'span'           , 'Sets correct tag name')
        assert.ok   (span instanceof Tag                           , 'Inherits from Tag')

        // With text content
        const with_text = new Span({ value: 'Span Text' })
        assert.equal(with_text.value            , 'Span Text'      , 'Sets span text')

        // With multiple attributes
        const complex = new Span({
            value : 'Complex Span'              ,
            class : 'custom-span'               ,
            id    : 'span-1'                    ,
            style : 'font-weight: bold;'
        })
        assert.equal(complex.value              , 'Complex Span'   , 'Sets text')
        assert.equal(complex.class              , 'custom-span'    , 'Sets class')
        assert.equal(complex.id                 , 'span-1'         , 'Sets id')
        assert.equal(complex.attributes.style   , 'font-weight: bold;', 'Sets style')
    })

    test('generates correct HTML', assert => {
        const span = new Span({
            value : 'Test Span'                 ,
            class : 'test-span'
        })
        const expected = '<span class="test-span">Test Span</span>\n'
        assert.equal(span.html()                , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const span = new Span()
        assert.equal(span.html()                , '<span>\n</span>\n', 'Generates minimal HTML')
    })
})