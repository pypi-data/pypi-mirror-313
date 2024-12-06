import Figure from '../../js/core/Figure.mjs'
import Tag    from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Figure', hooks => {
    test('constructor creates figure element', assert => {
        // Basic instantiation
        const figure = new Figure({})
        assert.equal(figure.tag                 , 'figure'          , 'Sets correct tag name')
        assert.ok   (figure instanceof Tag                          , 'Inherits from Tag')

        // With content
        const with_content = new Figure({ value: 'Figure Content' })
        assert.equal(with_content.value        , 'Figure Content'   , 'Sets figure content')

        // With multiple attributes
        const complex = new Figure({
            value : 'Test Figure'               ,
            class : 'custom-figure'             ,
            id    : 'figure-1'
        })
        assert.equal(complex.value              , 'Test Figure'     , 'Sets content')
        assert.equal(complex.class              , 'custom-figure'   , 'Sets class')
        assert.equal(complex.id                 , 'figure-1'        , 'Sets id')
    })

    test('generates correct HTML', assert => {
        const figure = new Figure({
            value : 'Test Figure'               ,
            class : 'test-figure'
        })
        const expected = '<figure class="test-figure">Test Figure</figure>\n'
        assert.equal(figure.html()              , expected          , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const figure = new Figure()

        assert.equal(figure.tag                 , 'figure'                , 'Sets correct tag name')
        assert.ok   (figure instanceof Tag                                , 'Inherits from Tag')
        assert.deepEqual(figure.attributes      , {}                      , 'Has empty attributes')
        assert.equal(figure.html()              , '<figure>\n</figure>\n' , 'Generates minimal HTML')
    })
})