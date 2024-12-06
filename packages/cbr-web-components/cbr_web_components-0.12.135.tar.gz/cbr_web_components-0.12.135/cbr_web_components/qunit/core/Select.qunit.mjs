// Select.qunit.mjs
import Select from '../../js/core/Select.mjs'
import Tag    from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Select', hooks => {
    test('constructor creates select element', assert => {
        // Basic instantiation
        const select = new Select({})
        assert.equal(select.tag                 , 'select'         , 'Sets correct tag name')
        assert.ok   (select instanceof Tag                         , 'Inherits from Tag')

        // With multiple attributes
        const complex = new Select({
            class    : 'custom-select'          ,
            id       : 'select-1'               ,
            name     : 'test-select'            ,
            multiple : true                     ,
            required : true
        })
        assert.equal(complex.class               , 'custom-select'  , 'Sets class')
        assert.equal(complex.id                  , 'select-1'       , 'Sets id')
        assert.equal(complex.attributes.name     , 'test-select'    , 'Sets name')
        assert.equal(complex.attributes.multiple , true             , 'Sets multiple')
        assert.equal(complex.attributes.required , true             , 'Sets required')
    })

    test('generates correct HTML', assert => {
        const select = new Select({
            class : 'test-select'               ,
            name  : 'test-name'
        })
        const expected = '<select class="test-select" name="test-name">\n</select>\n'
        assert.equal(select.html()              , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const select = new Select()
        assert.equal(select.html()              , '<select>\n</select>\n', 'Generates minimal HTML')
    })
})