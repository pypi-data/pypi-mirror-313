import TFoot from '../../js/core/TFoot.mjs' ;
import Tag   from '../../js/core/Tag.mjs' ;

const { module, test , only} = QUnit

module('TFoot', hooks => {
    test('constructor creates tfoot element', assert => {
        const tfoot = new TFoot({})
        assert.equal(tfoot.tag                   , 'tfoot'         , 'Sets correct tag name')
        assert.ok   (tfoot instanceof Tag                          , 'Inherits from Tag'    )

        const complex = new TFoot({
            id        : 'test-id'                ,
            class     : 'test-class'             ,
            value     : 'Test Content'
        })
        assert.equal(complex.id                   , 'test-id'      , 'Sets ID'             )
        assert.equal(complex.class                , 'test-class'   , 'Sets class'          )
        assert.equal(complex.value                , 'Test Content' , 'Sets content'        )
    })

    test('generates correct HTML', assert => {
        const tfoot = new TFoot({
            id    : 'test-tfoot'                 ,
            class : 'test-class'                 ,
            value : 'Test Content'
        })
        const expected = '<tfoot id="test-tfoot" class="test-class">Test Content</tfoot>\n'
        assert.equal(tfoot.html()                , expected         , 'Generates valid HTML' )
    })

    test('constructor handles no parameters', assert => {
        const tfoot = new TFoot()
        assert.equal(tfoot.html(), '<tfoot>\n</tfoot>\n'        , 'Generates minimal HTML')
    })
})