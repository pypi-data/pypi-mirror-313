import TH  from '../../js/core/TH.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test, only } = QUnit

module('TH', hooks => {
    test('constructor creates th element', assert => {
        const th = new TH({})
        assert.equal(th.tag                      , 'th'            , 'Sets correct tag name')
        assert.ok   (th instanceof Tag                             , 'Inherits from Tag'    )

        const complex = new TH({
            id        : 'test-id'                ,
            class     : 'test-class'             ,
            value     : 'Test Content'
        })
        assert.equal(complex.id                   , 'test-id'      , 'Sets ID'             )
        assert.equal(complex.class                , 'test-class'   , 'Sets class'          )
        assert.equal(complex.value                , 'Test Content' , 'Sets content'        )
    })

    test('generates correct HTML', assert => {
        const th = new TH({
            id    : 'test-th'                    ,
            class : 'test-class'                 ,
            value : 'Test Content'
        })
        const expected = '<th id="test-th" class="test-class">Test Content</th>\n'
        assert.equal(th.html()                   , expected         , 'Generates valid HTML' )
    })

    test('constructor handles no parameters', assert => {
        const th = new TH()

        assert.equal(th.tag                      , 'th'              , 'Sets correct tag name')
        assert.ok   (th instanceof Tag                               , 'Inherits from Tag'    )
        assert.deepEqual(th.attributes           , {}                , 'Has empty attributes' )
        assert.equal(th.html()                   , '<th>\n</th>\n'   , 'Generates minimal HTML')
    })

    test('handles complex attributes', assert => {
        const th = new TH({
            colspan   : '2'                      ,
            rowspan   : '3'                      ,
            scope     : 'col'                    ,
            headers   : 'header1 header2'
        })

        assert.equal(th.attributes.colspan       , '2'              , 'Sets colspan'        )
        assert.equal(th.attributes.rowspan       , '3'              , 'Sets rowspan'        )
        assert.equal(th.attributes.scope         , 'col'            , 'Sets scope'          )
        assert.equal(th.attributes.headers       , 'header1 header2', 'Sets headers'        )

        const html = th.html()
        assert.ok   (html.includes('colspan="2"')                   , 'Includes colspan'     )
        assert.ok   (html.includes('rowspan="3"')                   , 'Includes rowspan'     )
        assert.ok   (html.includes('scope="col"')                   , 'Includes scope'       )
        assert.ok   (html.includes('headers="header1 header2"')     , 'Includes headers'     )
    })
})