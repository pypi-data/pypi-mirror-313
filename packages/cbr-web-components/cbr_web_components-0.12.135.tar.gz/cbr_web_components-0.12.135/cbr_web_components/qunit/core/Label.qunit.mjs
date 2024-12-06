// Label.qunit.mjs
import Label from '../../js/core/Label.mjs'
import Tag   from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Label', hooks => {
    test('constructor creates label element', assert => {
        // Basic instantiation
        const label = new Label({})
        assert.equal(label.tag                  , 'label'          , 'Sets correct tag name')
        assert.ok   (label instanceof Tag                          , 'Inherits from Tag')

        // With value
        const with_text = new Label({ value: 'Label Text' })
        assert.equal(with_text.value            , 'Label Text'     , 'Sets label text')

        // With multiple attributes
        const complex = new Label({
            value  : 'Complex Label'            ,
            class  : 'custom-label'             ,
            id     : 'label-1'                  ,
            for    : 'input-1'
        })
        assert.equal(complex.value              , 'Complex Label'  , 'Sets text')
        assert.equal(complex.class              , 'custom-label'   , 'Sets class')
        assert.equal(complex.id                 , 'label-1'        , 'Sets id')
        assert.equal(complex.attributes.for     , 'input-1'        , 'Sets for attribute')
    })

    test('generates correct HTML', assert => {
        const label = new Label({
            value : 'Test Label'                ,
            class : 'test-label'                ,
            for   : 'test-input'
        })
        const expected = '<label class="test-label" for="test-input">Test Label</label>\n'
        assert.equal(label.html()               , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const label = new Label()
        assert.equal(label.html()               , '<label>\n</label>\n', 'Generates minimal HTML')
    })
})





