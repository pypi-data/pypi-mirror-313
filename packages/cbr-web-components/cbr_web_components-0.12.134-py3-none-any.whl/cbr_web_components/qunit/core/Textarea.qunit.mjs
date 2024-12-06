import Textarea from '../../js/core/Textarea.mjs' ;
import Tag      from '../../js/core/Tag.mjs' ;

const { module, test , only} = QUnit

module('Textarea', hooks => {
    test('constructor creates textarea element', assert => {
        const textarea = new Textarea({})
        assert.equal(textarea.tag                , 'textarea'      , 'Sets correct tag name')
        assert.ok   (textarea instanceof Tag                       , 'Inherits from Tag'    )

        const complex = new Textarea({
            id        : 'test-id'                ,
            class     : 'test-class'             ,
            value     : 'Test Content'
        })
        assert.equal(complex.id                   , 'test-id'      , 'Sets ID'             )
        assert.equal(complex.class                , 'test-class'   , 'Sets class'          )
        assert.equal(complex.value                , 'Test Content' , 'Sets content'        )
    })

    test('generates correct HTML', assert => {
        const textarea = new Textarea({
            id    : 'test-textarea'              ,
            class : 'test-class'                 ,
            value : 'Test Content'
        })
        const expected = '<textarea id="test-textarea" class="test-class">Test Content</textarea>\n'
        assert.equal(textarea.html()              , expected        , 'Generates valid HTML' )
    })

    test('constructor handles no parameters', assert => {
        const textarea = new Textarea()
        assert.equal(textarea.html()  , '<textarea>\n</textarea>\n'        , 'Generates minimal HTML')
    })
})