import TBody from '../../js/core/TBody.mjs'
import Tag   from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('TBody', hooks => {

    test('constructor creates tbody element', assert => {
        const tbody = new TBody({})
        assert.equal(tbody.tag                    , 'tbody'         , 'Sets correct tag name')
        assert.ok   (tbody instanceof Tag                           , 'Inherits from Tag'    )

        const complex = new TBody({
            id        : 'test-id'                ,
            class     : 'test-class'             ,
            value     : 'Test Content'
        })
        assert.equal(complex.id                   , 'test-id'       , 'Sets ID'             )
        assert.equal(complex.class                , 'test-class'    , 'Sets class'          )
        assert.equal(complex.value                , 'Test Content'  , 'Sets content'        )
    })

    test('generates correct HTML', assert => {
        const tbody = new TBody({
            id    : 'test-tbody'                 ,
            class : 'test-class'                 ,
            value : 'Test Content'
        })
        const expected = '<tbody id="test-tbody" class="test-class">Test Content</tbody>\n'
        assert.equal(tbody.html()                , expected         , 'Generates valid HTML' )
    })

    test('constructor handles no parameters', assert => {
        const tbody = new TBody()
        assert.equal(tbody.html()               , '<tbody>\n</tbody>\n', 'Generates minimal HTML')
    })
})

