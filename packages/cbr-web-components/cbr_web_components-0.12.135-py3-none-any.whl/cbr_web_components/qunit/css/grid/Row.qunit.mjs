import Row  from '../../../js/css/grid/Row.mjs'
import Col  from '../../../js/css/grid/Col.mjs'
import Div  from '../../../js/core/Div.mjs'

const { module, test, only } = QUnit

module('Row', hooks => {
    test('constructor creates row element', assert => {
        // Basic instantiation
        const row = new Row({})
        assert.equal(row.tag                   , 'div'                       , 'Sets correct tag name' )
        assert.ok   (row instanceof Div                                      , 'Inherits from Div'     )
        assert.ok   (row.class.includes('row')                              , 'Has row class'         )

        // With custom class
        const styled = new Row({ class: 'custom-row' })
        assert.ok   (styled.class.includes('row')                           , 'Keeps row class'       )
        assert.ok   (styled.class.includes('custom-row')                    , 'Adds custom class'     )
    })

    test('add_col adds column correctly', assert => {
        const row = new Row({})
        const col = row.add_col({ size: 6 })

        assert.ok   (col instanceof Col                                     , 'Returns Col instance'  )
        assert.ok   (col.class.includes('col-6')                           , 'Sets column size'      )
        assert.equal(row.elements.length      , 1                          , 'Adds to row elements'  )
    })

    test('add_row adds nested row', assert => {
        const row    = new Row({})
        const nested = row.add_row({ class: 'nested' })

        assert.ok   (nested instanceof Row                                  , 'Returns Row instance'  )
        assert.ok   (nested.class.includes('nested')                       , 'Sets custom class'     )
        assert.equal(row.elements.length      , 1                          , 'Adds to row elements'  )
    })

    test('add_cols adds multiple columns', assert => {
        const row = new Row({})
        const configs = [
            { size: 4, class: 'first'  },
            { size: 4, class: 'second' },
            { size: 4, class: 'third'  }
        ]

        row.add_cols(configs)

        assert.equal(row.elements.length      , 3                          , 'Adds all columns'      )
        assert.ok   (row.elements[0].class.includes('first')              , 'Sets first class'      )
        assert.ok   (row.elements[1].class.includes('second')             , 'Sets second class'     )
        assert.ok   (row.elements[2].class.includes('third')              , 'Sets third class'      )
    })

    test('add_nested_row creates nested structure', assert => {
        const row = new Row({})
        const nested = row.add_nested_row({
            col_config: { size: 6               },
            row_config: { class: 'nested-row'   }
        })

        assert.ok   (nested instanceof Row                                 , 'Returns Row instance'  )
        assert.ok   (row.elements[0] instanceof Col                       , 'Creates parent column' )
        assert.ok   (nested.class.includes('nested-row')                  , 'Sets nested row class' )
        assert.equal(row.elements[0].elements[0], nested                  , 'Nests row in column'   )
    })

    test('generates correct HTML structure', assert => {
        const row = new Row({})
        row.add_col ({ size : 6, value: 'Left'  })
        row.add_col ({ size : 6, value: 'Right' })

        const html = row.html()
        assert.ok   (html.includes('class="row "')                         , 'Has row class'         )
        assert.ok   (html.includes('class="col-6 "')                      , 'Has column classes'    )
        assert.ok   (html.includes('>Left<')                             , 'Has first content'     )
        assert.ok   (html.includes('>Right<')                            , 'Has second content'    )
    })
})