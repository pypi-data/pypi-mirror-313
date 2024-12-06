// Li.qunit.mjs
import Li  from '../../js/core/Li.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Li', hooks => {
    test('constructor creates li element', assert => {
        // Basic instantiation
        const li = new Li({})
        assert.equal(li.tag                     , 'li'             , 'Sets correct tag name')
        assert.ok   (li instanceof Tag                             , 'Inherits from Tag')

        // With value
        const with_text = new Li({ value: 'List Item' })
        assert.equal(with_text.value            , 'List Item'      , 'Sets list item text')

        // With multiple attributes
        const complex = new Li({
            value : 'Complex Item'              ,
            class : 'custom-item'               ,
            id    : 'item-1'
        })
        assert.equal(complex.value              , 'Complex Item'   , 'Sets text')
        assert.equal(complex.class              , 'custom-item'    , 'Sets class')
        assert.equal(complex.id                 , 'item-1'         , 'Sets id')
    })

    test('generates correct HTML', assert => {
        const li = new Li({
            value : 'Test Item'                 ,
            class : 'test-item'
        })
        const expected = '<li class="test-item">Test Item</li>\n'
        assert.equal(li.html()                  , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const li = new Li()
        assert.equal(li.html()                  , '<li>\n</li>\n'  , 'Generates minimal HTML')
    })
})