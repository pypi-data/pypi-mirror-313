import B   from '../../js/core/B.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test, only } = QUnit

module('B', hooks => {
    test('constructor creates bold element', assert => {
        // Basic instantiation
        const b = new B({})
        assert.equal(b.tag                    , 'b'              , 'Sets correct tag name')
        assert.ok   (b instanceof Tag                            , 'Inherits from Tag')

        // With text content
        const bold = new B({ value: 'Bold Text' })
        assert.equal(bold.value              , 'Bold Text'       , 'Sets text content')

        // With class
        const styled = new B({
            value : 'Styled Bold'            ,
            class : 'custom-bold'
        })
        assert.equal(styled.value            , 'Styled Bold'     , 'Sets text')
        assert.equal(styled.class            , 'custom-bold'     , 'Sets class')
    })

    test('generates correct HTML', assert => {
        const bold = new B({
            value : 'Test Bold'              ,
            class : 'test-bold'
        })
        const expected = '<b class="test-bold">Test Bold</b>\n'
        assert.equal(bold.html()             , expected          , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        // Call constructor with no parameters at all
        const b = new B()

        assert.equal(b.tag                    , 'b'              , 'Sets correct tag name')
        assert.ok   (b instanceof Tag                            , 'Inherits from Tag')
        assert.deepEqual(b.attributes         , {}               , 'Has empty attributes')
        assert.equal(b.html()                , '<b>\n</b>\n'        , 'Generates minimal HTML')
    })
})