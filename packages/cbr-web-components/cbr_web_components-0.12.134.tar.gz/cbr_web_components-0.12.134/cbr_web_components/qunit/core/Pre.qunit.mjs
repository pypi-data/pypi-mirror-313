// Pre.qunit.mjs
import Pre from '../../js/core/Pre.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Pre', hooks => {
    test('constructor creates pre element', assert => {
        // Basic instantiation
        const pre = new Pre({})
        assert.equal(pre.tag                    , 'pre'            , 'Sets correct tag name')
        assert.ok   (pre instanceof Tag                            , 'Inherits from Tag')

        // With text content
        const with_text = new Pre({ value: 'Preformatted Text' })
        assert.equal(with_text.value            , 'Preformatted Text', 'Sets preformatted text')

        // With multiple attributes
        const complex = new Pre({
            value : 'Complex Code'              ,
            class : 'custom-pre'                ,
            id    : 'pre-1'                     ,
            style : 'background: #eee;'
        })
        assert.equal(complex.value              , 'Complex Code'   , 'Sets text')
        assert.equal(complex.class              , 'custom-pre'     , 'Sets class')
        assert.equal(complex.id                 , 'pre-1'          , 'Sets id')
        assert.equal(complex.attributes.style   , 'background: #eee;', 'Sets style')
    })

    test('generates correct HTML', assert => {
        const pre = new Pre({
            value : 'Test Code'                 ,
            class : 'test-pre'
        })
        const expected = '<pre class="test-pre">Test Code</pre>\n'
        assert.equal(pre.html()                 , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const pre = new Pre()
        assert.equal(pre.html()                 , '<pre>\n</pre>\n', 'Generates minimal HTML')
    })
})