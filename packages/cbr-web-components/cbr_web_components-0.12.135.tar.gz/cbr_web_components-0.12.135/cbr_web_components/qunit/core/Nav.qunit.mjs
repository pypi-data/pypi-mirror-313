// Nav.qunit.mjs
import Nav from '../../js/core/Nav.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Nav', hooks => {
    test('constructor creates nav element', assert => {
        // Basic instantiation
        const nav = new Nav({})
        assert.equal(nav.tag                    , 'nav'            , 'Sets correct tag name')
        assert.ok   (nav instanceof Tag                            , 'Inherits from Tag')

        // With multiple attributes
        const complex = new Nav({
            class : 'custom-nav'                ,
            id    : 'nav-1'                     ,
            role  : 'navigation'                ,
            value : 'Navigation'
        })
        assert.equal(complex.value              , 'Navigation'     , 'Sets text')
        assert.equal(complex.class              , 'custom-nav'     , 'Sets class')
        assert.equal(complex.id                 , 'nav-1'          , 'Sets id')
        assert.equal(complex.attributes.role    , 'navigation'     , 'Sets role')
    })

    test('generates correct HTML', assert => {
        const nav = new Nav({
            class : 'test-nav'                  ,
            value : 'Test Nav'
        })
        const expected = '<nav class="test-nav">Test Nav</nav>\n'
        assert.equal(nav.html()                 , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const nav = new Nav()
        assert.equal(nav.html()                 , '<nav>\n</nav>\n', 'Generates minimal HTML')
    })
})