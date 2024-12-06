import TD  from '../../js/core/TD.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('TD', hooks => {
    test('constructor creates td element', assert => {
        const td = new TD({})
        assert.equal(td.tag                      , 'td'            , 'Sets correct tag name')
        assert.ok   (td instanceof Tag                             , 'Inherits from Tag'    )

        const complex = new TD({
            id        : 'test-id'                ,
            class     : 'test-class'             ,
            value     : 'Test Content'
        })
        assert.equal(complex.id                   , 'test-id'      , 'Sets ID'             )
        assert.equal(complex.class                , 'test-class'   , 'Sets class'          )
        assert.equal(complex.value                , 'Test Content' , 'Sets content'        )
    })

    test('generates correct HTML', assert => {
        const td = new TD({
            id    : 'test-td'                    ,
            class : 'test-class'                 ,
            value : 'Test Content'
        })
        const expected = '<td id="test-td" class="test-class">Test Content</td>\n'
        assert.equal(td.html()                   , expected         , 'Generates valid HTML' )
    })
})