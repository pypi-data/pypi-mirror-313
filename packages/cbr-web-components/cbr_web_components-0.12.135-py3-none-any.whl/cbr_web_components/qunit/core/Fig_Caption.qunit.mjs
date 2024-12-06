// Fig_Caption.qunit.mjs
import Fig_Caption from '../../js/core/Fig_Caption.mjs'
import Tag        from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Fig_Caption', hooks => {
    test('constructor creates figcaption element', assert => {
        // Basic instantiation
        const fig_caption = new Fig_Caption({})
        assert.equal(fig_caption.tag              , 'figcaption'      , 'Sets correct tag name')
        assert.ok   (fig_caption instanceof Tag                       , 'Inherits from Tag')

        // With text content
        const with_text = new Fig_Caption({ value: 'Caption Text' })
        assert.equal(with_text.value            , 'Caption Text'     , 'Sets caption text')

        // With multiple attributes
        const complex = new Fig_Caption({
            value : 'Test Caption'              ,
            class : 'custom-caption'            ,
            id    : 'caption-1'
        })
        assert.equal(complex.value              , 'Test Caption'     , 'Sets text content')
        assert.equal(complex.class              , 'custom-caption'   , 'Sets class')
        assert.equal(complex.id                 , 'caption-1'        , 'Sets id')
    })

    test('generates correct HTML', assert => {
        const fig_caption = new Fig_Caption({
            value : 'Test Caption'              ,
            class : 'test-caption'
        })
        const expected = '<figcaption class="test-caption">Test Caption</figcaption>\n'
        assert.equal(fig_caption.html()         , expected           , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const fig_caption = new Fig_Caption()

        assert.equal(fig_caption.tag            , 'figcaption'              , 'Sets correct tag name')
        assert.ok   (fig_caption instanceof Tag                             , 'Inherits from Tag')
        assert.deepEqual(fig_caption.attributes , {}                        , 'Has empty attributes')
        assert.equal(fig_caption.html()         , '<figcaption>\n</figcaption>\n', 'Generates minimal HTML')
    })
})