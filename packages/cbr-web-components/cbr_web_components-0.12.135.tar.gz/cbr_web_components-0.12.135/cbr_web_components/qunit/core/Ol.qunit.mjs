// Ol.qunit.mjs
import Ol  from '../../js/core/Ol.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Ol', hooks => {
    test('constructor creates ol element', assert => {
        // Basic instantiation
        const ol = new Ol({})
        assert.equal(ol.tag                     , 'ol'             , 'Sets correct tag name')
        assert.ok   (ol instanceof Tag                             , 'Inherits from Tag')

        // With multiple attributes
        const complex = new Ol({
            class : 'custom-list'               ,
            id    : 'list-1'                    ,
            type  : 'A'                         ,
            start : '3'
        })
        assert.equal(complex.class              , 'custom-list'    , 'Sets class')
        assert.equal(complex.id                 , 'list-1'         , 'Sets id')
        assert.equal(complex.attributes.type    , 'A'              , 'Sets type')
        assert.equal(complex.attributes.start   , '3'              , 'Sets start')
    })

    test('generates correct HTML', assert => {
        const ol = new Ol({
            class : 'test-list'                 ,
            type  : '1'
        })
        const expected = '<ol class="test-list" type="1">\n</ol>\n'
        assert.equal(ol.html()                  , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const ol = new Ol()
        assert.equal(ol.html()                  , '<ol>\n</ol>\n'  , 'Generates minimal HTML')
    })
})