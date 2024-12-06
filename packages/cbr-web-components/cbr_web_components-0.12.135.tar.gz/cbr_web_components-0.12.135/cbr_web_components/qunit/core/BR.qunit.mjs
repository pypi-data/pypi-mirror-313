import BR  from '../../js/core/BR.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test, only } = QUnit

module('BR', hooks => {
    test('constructor creates break element', assert => {
        // Basic instantiation
        const br = new BR({})
        assert.equal(br.tag                   , 'br'             , 'Sets correct tag name')
        assert.ok   (br instanceof Tag                           , 'Inherits from Tag')

        // With class
        const styled = new BR({ class: 'custom-break' })
        assert.equal(styled.class            , 'custom-break'    , 'Sets class attribute')
    })

    test('generates correct HTML', assert => {
        const br = new BR({})
        assert.equal(br.html()               , '<br/>\n'            , 'Generates simple break')

        const styled = new BR({ class: 'test-break' })
        assert.equal(styled.html()           , '<br class="test-break"/>\n', 'Generates break with class')
    })

    test('constructor handles no parameters', assert => {
        // Call constructor with no parameters at all
        const br = new BR()

        assert.equal(br.tag                   , 'br'             , 'Sets correct tag name')
        assert.ok   (br instanceof Tag                           , 'Inherits from Tag')
        assert.deepEqual(br.attributes        , {}               , 'Has empty attributes')
        assert.equal(br.html()               , '<br/>\n'           , 'Generates minimal HTML')
    })
})
