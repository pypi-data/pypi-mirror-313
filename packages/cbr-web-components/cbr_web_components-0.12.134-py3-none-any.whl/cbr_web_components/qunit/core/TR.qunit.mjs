import TR from "../../js/core/TR.mjs";
import Tag from "../../js/core/Tag.mjs";

const { module, test, only } = QUnit

module('TR', hooks => {
    test('constructor creates tr element', assert => {
        const tr = new TR({})
        assert.equal(tr.tag                      , 'tr'            , 'Sets correct tag name')
        assert.ok   (tr instanceof Tag                             , 'Inherits from Tag'    )

        const complex = new TR({
            id        : 'test-id'                ,
            class     : 'test-class'             ,
            value     : 'Test Content'
        })
        assert.equal(complex.id                   , 'test-id'      , 'Sets ID'             )
        assert.equal(complex.class                , 'test-class'   , 'Sets class'          )
        assert.equal(complex.value                , 'Test Content' , 'Sets content'        )
    })

    test('generates correct HTML', assert => {
        const tr = new TR({
            id    : 'test-tr'                    ,
            class : 'test-class'                 ,
            value : 'Test Content'
        })
        const expected = '<tr id="test-tr" class="test-class">Test Content</tr>\n'
        assert.equal(tr.html()                   , expected         , 'Generates valid HTML' )
    })
})