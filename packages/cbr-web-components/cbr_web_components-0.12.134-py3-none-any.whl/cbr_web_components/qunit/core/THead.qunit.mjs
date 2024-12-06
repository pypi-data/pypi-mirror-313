import THead from '../../js/core/THead.mjs'
import Tag   from '../../js/core/Tag.mjs'

const { module, test, only } = QUnit

module('THead', hooks => {
    test('constructor creates thead element', assert => {
        const thead = new THead({})
        assert.equal(thead.tag                    , 'thead'         , 'Sets correct tag name')
        assert.ok   (thead instanceof Tag                           , 'Inherits from Tag'    )

        const complex = new THead({
            id        : 'test-id'                ,
            class     : 'test-class'             ,
            value     : 'Test Content'
        })
        assert.equal(complex.id                   , 'test-id'      , 'Sets ID'             )
        assert.equal(complex.class                , 'test-class'   , 'Sets class'          )
        assert.equal(complex.value                , 'Test Content' , 'Sets content'        )
    })

    test('generates correct HTML', assert => {
        const thead = new THead({
            id    : 'test-thead'                 ,
            class : 'test-class'                 ,
            value : 'Test Content'
        })
        const expected = '<thead id="test-thead" class="test-class">Test Content</thead>\n'
        assert.equal(thead.html()                , expected         , 'Generates valid HTML' )
    })
})

