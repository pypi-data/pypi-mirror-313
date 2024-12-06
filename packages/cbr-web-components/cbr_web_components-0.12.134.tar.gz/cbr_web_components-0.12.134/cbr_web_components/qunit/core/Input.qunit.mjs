// Input.qunit.mjs
import Input from '../../js/core/Input.mjs'
import Tag   from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Input', hooks => {
    test('constructor creates input element', assert => {
        // Basic instantiation
        const input = new Input({})
        assert.equal(input.tag                  , 'input'          , 'Sets correct tag name')
        assert.ok   (input instanceof Tag                          , 'Inherits from Tag')
        assert.equal(input.attributes.value     , ''               , 'Empty default value')

        // With value
        const with_value = new Input({ value: 'test value' })
        assert.equal(with_value.attributes.value, 'test value'     , 'Sets value attribute')

        // With all attributes
        const complex = new Input({
            value  : 'test value'               ,
            type   : 'text'                     ,
            class  : 'custom-input'             ,
            id     : 'input-1'                  ,
            name   : 'test-input'               ,
            placeholder: 'Enter text'
        })
        assert.equal(complex.attributes.value   , 'test value'     , 'Sets value')
        assert.equal(complex.attributes.type    , 'text'           , 'Sets type')
        assert.equal(complex.class              , 'custom-input'   , 'Sets class')
        assert.equal(complex.id                 , 'input-1'        , 'Sets id')
        assert.equal(complex.attributes.name    , 'test-input'     , 'Sets name')
        assert.equal(complex.attributes.placeholder, 'Enter text'  , 'Sets placeholder')
    })

    test('generates correct HTML', assert => {
        const input = new Input({
            value  : 'test value'               ,
            type   : 'text'                     ,
            class  : 'test-input'
        })
        const expected = '<input class="test-input" value="test value" type="text"/>\n'
        assert.equal(input.html()               , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const input = new Input()
        assert.equal(input.html()               , '<input value=""/>\n', 'Generates minimal HTML')
    })
})