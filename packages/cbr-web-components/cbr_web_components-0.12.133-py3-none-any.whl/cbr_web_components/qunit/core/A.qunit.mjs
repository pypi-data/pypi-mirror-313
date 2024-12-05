import A from  '../../js/core/A.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test, only } = QUnit

module('A', hooks => {
    test('constructor creates anchor element', assert => {
        // Basic instantiation
        const a = new A({})
        assert.equal(a.tag                    , 'a'              , 'Sets correct tag name')
        assert.ok   (a instanceof Tag                            , 'Inherits from Tag')

        // With href
        const link = new A({ href: 'test.html' })
        assert.equal(link.attributes.href     , 'test.html'      , 'Sets href attribute')

        // With text
        const text_link = new A({ value: 'Click me' })
        assert.equal(text_link.value         , 'Click me'        , 'Sets link text')

        // With multiple attributes
        const complex = new A({
            href     : 'page.html'           ,
            class    : 'link-primary'        ,
            value    : 'Visit'               ,
            target   : '_blank'
        })
        assert.equal(complex.attributes.href  , 'page.html'      , 'Sets href')
        assert.equal(complex.attributes.target, '_blank'         , 'Sets target')
        assert.equal(complex.class           , 'link-primary'    , 'Sets class')
        assert.equal(complex.value           , 'Visit'           , 'Sets text')
    })

    test('generates correct HTML', assert => {
        const link = new A({
            href  : 'test.html'              ,
            class : 'test-link'              ,
            value : 'Test Link'
        })
        const expected = '<a class="test-link" href="test.html">Test Link</a>\n'
        assert.equal(link.html()             , expected          , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        // Call constructor with no parameters at all
        const a = new A()

        assert.equal(a.tag                    , 'a'              , 'Sets correct tag name')
        assert.ok   (a instanceof Tag                            , 'Inherits from Tag')
        assert.deepEqual(a.attributes         , {}               , 'Has empty attributes')
        assert.equal(a.html()                , '<a>\n</a>\n'        , 'Generates minimal HTML')
    })
})