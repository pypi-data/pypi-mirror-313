import Button from '../../js/core/Button.mjs'
import Tag    from '../../js/core/Tag.mjs'

const { module, test, only } = QUnit

module('Button', hooks => {
    test('constructor creates button element', assert => {
        // Basic instantiation
        const button = new Button({})
        assert.equal(button.tag               , 'button'         , 'Sets correct tag name')
        assert.ok   (button instanceof Tag                       , 'Inherits from Tag')

        // With text
        const text_btn = new Button({ value: 'Click Me' })
        assert.equal(text_btn.value          , 'Click Me'       , 'Sets button text')

        // With multiple attributes
        const complex = new Button({
            type     : 'submit'              ,
            class    : 'btn-primary'         ,
            value    : 'Submit'              ,
            disabled : true
        })
        assert.equal(complex.attributes.type  , 'submit'         , 'Sets type')
        assert.equal(complex.class           , 'btn-primary'     , 'Sets class')
        assert.equal(complex.value           , 'Submit'          , 'Sets text')
        assert.equal(complex.attributes.disabled, true           , 'Sets disabled')
    })

    test('generates correct HTML', assert => {
        const button = new Button({
            type  : 'button'                 ,
            class : 'test-btn'               ,
            value : 'Test Button'
        })
        const expected = '<button class="test-btn" type="button">Test Button</button>\n'
        assert.equal(button.html()           , expected          , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        // Call constructor with no parameters at all
        const button = new Button()

        assert.equal(button.tag               , 'button'             , 'Sets correct tag name')
        assert.ok   (button instanceof Tag                            , 'Inherits from Tag')
        assert.deepEqual(button.attributes    , {}                    , 'Has empty attributes')
        assert.equal(button.html()           , '<button>\n</button>\n', 'Generates minimal HTML')
    })
})
