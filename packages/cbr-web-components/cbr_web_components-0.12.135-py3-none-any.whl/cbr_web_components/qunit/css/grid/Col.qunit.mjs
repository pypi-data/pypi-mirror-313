import Col  from '../../../js/css/grid/Col.mjs'
import Row  from '../../../js/css/grid/Row.mjs'
import Div  from '../../../js/core/Div.mjs'

const { module, test, only } = QUnit

module('Col', hooks => {
    test('constructor creates column element', assert => {
        // Basic instantiation
        const col = new Col({})
        assert.equal(col.tag                  , 'div'                      , 'Sets correct tag name' )
        assert.ok   (col instanceof Div                                    , 'Inherits from Div'     )
        assert.ok   (col.class.includes('col')                            , 'Has col class'         )

        // With size
        const sized = new Col({ size: 6 })
        assert.ok   (sized.class.includes('col-6')                        , 'Sets size class'       )

        // With width
        const fixed = new Col({ width: 200 })
        assert.ok   (fixed.class.includes('w-200px')                      , 'Sets width class'      )

        // With custom class
        const styled = new Col({ class: 'custom-col' })
        assert.ok   (styled.class.includes('col')                         , 'Keeps col class'       )
        assert.ok   (styled.class.includes('custom-col')                  , 'Adds custom class'     )
    })

    test('add_col adds nested column', assert => {
        const col     = new Col({})
        const nested  = col.add_col({ size: 6 })

        assert.ok   (nested instanceof Col                                , 'Returns Col instance'  )
        assert.ok   (nested.class.includes('col-6')                      , 'Sets column size'      )
        assert.equal(col.elements.length       , 1                       , 'Adds to col elements'  )
    })

    test('add_row adds nested row', assert => {
        const col     = new Col({})
        const row     = col.add_row({ class: 'nested' })

        assert.ok   (row instanceof Row                                  , 'Returns Row instance'  )
        assert.ok   (row.class.includes('nested')                       , 'Sets custom class'     )
        assert.equal(col.elements.length       , 1                      , 'Adds to col elements'  )
    })

    test('handles multiple size configurations', assert => {
        // Test responsive sizes
        const responsive = new Col({
            size : 12                        ,
            class: 'col-md-6 col-lg-4'
        })
        assert.ok   (responsive.class.includes('col-12')                , 'Has base size'         )
        assert.ok   (responsive.class.includes('col-md-6')              , 'Has medium size'       )
        assert.ok   (responsive.class.includes('col-lg-4')              , 'Has large size'        )

        // Test auto-sizing
        const auto = new Col({})
        assert.ok   (auto.class.includes('col')                         , 'Has auto-size class'   )
    })

    test('handles no parameters', assert => {
        // Create column with no parameters
        const col = new Col()

        assert.ok   (col instanceof Div                                     , 'Inherits from Div'       )
        assert.equal(col.tag                  , 'div'                       , 'Has correct tag'         )
        assert.ok   (col.class.includes('col')                             , 'Has base col class'      )
        assert.notOk(col.class.includes('col-')                            , 'No size class added'     )
        assert.notOk(col.class.includes('w-')                              , 'No width class added'    )
        assert.equal(col.class.trim()         , 'col'                      , 'Only has col class'      )
    })

    test('handles empty size and width', assert => {
        // Test with empty object
        const col = new Col({})

        assert.ok   (col.class.includes('col')                             , 'Has base col class'      )
        assert.notOk(col.class.includes('col-')                            , 'No size class added'     )
        assert.notOk(col.class.includes('w-')                              , 'No width class added'    )
        assert.equal(col.class.trim()         , 'col'                      , 'Only has col class'      )

        // Test with undefined values
        const col2 = new Col({ size: undefined, width: undefined })
        assert.equal(col2.class.trim()        , 'col'                      , 'Only has col class'      )
    })

    test('handles no parameters', assert => {
        // Create column with no parameters
        const col = new Col()

        assert.ok   (col instanceof Div                                     , 'Inherits from Div'       )
        assert.equal(col.tag                  , 'div'                       , 'Has correct tag'         )
        assert.ok   (col.class.includes('col')                             , 'Has base col class'      )
        assert.notOk(col.class.includes('col-')                            , 'No size class added'     )
        assert.notOk(col.class.includes('w-')                              , 'No width class added'    )
        assert.equal(col.class.trim()         , 'col'                      , 'Only has col class'      )
    })

    test('handles empty size and width', assert => {
        // Test with empty object
        const col = new Col({})

        assert.ok   (col.class.includes('col')                             , 'Has base col class'      )
        assert.notOk(col.class.includes('col-')                            , 'No size class added'     )
        assert.notOk(col.class.includes('w-')                              , 'No width class added'    )
        assert.equal(col.class.trim()         , 'col'                      , 'Only has col class'      )

        // Test with undefined values
        const col2 = new Col({ size: undefined, width: undefined })
        assert.equal(col2.class.trim()        , 'col'                      , 'Only has col class'      )
    })
})