import Caption from '../../js/core/Caption.mjs'
import Tag     from '../../js/core/Tag.mjs'

const { module, test, only } = QUnit

module('Caption', hooks => {
    test('constructor creates caption element', assert => {
        // Basic instantiation
        const caption = new Caption({})
        assert.equal(caption.tag              , 'caption'        , 'Sets correct tag name')
        assert.ok   (caption instanceof Tag                      , 'Inherits from Tag')

        // With text
        const text_caption = new Caption({ value: 'Table Caption' })
        assert.equal(text_caption.value       , 'Table Caption'  , 'Sets caption text')

        // With styling
        const styled = new Caption({
            value : 'Styled Caption'         ,
            class : 'custom-caption'
        })
        assert.equal(styled.value            , 'Styled Caption'  , 'Sets text')
        assert.equal(styled.class            , 'custom-caption'  , 'Sets class')
    })

    test('generates correct HTML', assert => {
        const caption = new Caption({
            value : 'Test Caption'           ,
            class : 'test-caption'
        })
        const expected = '<caption class="test-caption">Test Caption</caption>\n'
        assert.equal(caption.html()          , expected          , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        // Call constructor with no parameters at all
        const caption = new Caption()

        assert.equal(caption.tag              , 'caption'               , 'Sets correct tag name')
        assert.ok   (caption instanceof Tag                             , 'Inherits from Tag')
        assert.deepEqual(caption.attributes   , {}                      , 'Has empty attributes')
        assert.equal(caption.html()          , '<caption>\n</caption>\n', 'Generates minimal HTML')
})
})