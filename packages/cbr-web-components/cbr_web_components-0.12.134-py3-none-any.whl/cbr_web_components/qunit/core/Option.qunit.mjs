import Option from '../../js/core/Option.mjs'
import Tag    from '../../js/core/Tag.mjs'

const { module, test , only} = QUnit

module('Option', hooks => {
    test('constructor creates option element', assert => {
        // Basic instantiation
        const option = new Option({})
        assert.equal(option.tag                 , 'option'         , 'Sets correct tag name')
        assert.ok   (option instanceof Tag                         , 'Inherits from Tag')

        // With value and text
        const with_values = new Option({
            value : 'option_value'              ,
            text  : 'Option Text'
        })
        assert.equal(with_values.attributes.value, 'option_value'  , 'Sets value attribute')
        assert.equal(with_values.value          , 'Option Text'    , 'Sets display text')

        // With multiple attributes
        const complex = new Option({
            value    : 'complex_value'          ,
            text     : 'Complex Option'         ,
            class    : 'custom-option'          ,
            id       : 'option-1'               ,
            selected : true
        })
        assert.equal(complex.attributes.value   , 'complex_value'  , 'Sets value')
        assert.equal(complex.value              , 'Complex Option' , 'Sets text')
        assert.equal(complex.class              , 'custom-option'  , 'Sets class')
        assert.equal(complex.id                 , 'option-1'       , 'Sets id')
        assert.equal(complex.attributes.selected, true             , 'Sets selected')
    })

    test ('generates correct HTML', assert => {
        const option = new Option({
            value : 'test_value'                ,
            text  : 'Test Option'               ,
            class : 'test-option'
        })
        const expected = '<option class="test-option" value="test_value">Test Option</option>\n'
        assert.equal(option.html()              , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const option = new Option()
        assert.equal(option.html()              , '<option>\n</option>\n', 'Generates minimal HTML')
    })
})