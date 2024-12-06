import Layout  from '../../../js/css/grid/Layout.mjs'
import Row     from '../../../js/css/grid/Row.mjs'
import Div     from '../../../js/core/Div.mjs'

const { module, test, only } = QUnit

module('Layout', hooks => {
    test('constructor creates layout element', assert => {
        // Basic instantiation
        const layout = new Layout({})
        assert.equal(layout.tag               , 'div'                      , 'Sets correct tag name' )
        assert.ok   (layout instanceof Div                                 , 'Inherits from Div'     )
        assert.ok   (layout.class.includes('layout')                      , 'Has layout class'      )

        // With custom class
        const styled = new Layout({ class: 'custom-layout' })
        assert.ok   (styled.class.includes('layout')                      , 'Keeps layout class'    )
        assert.ok   (styled.class.includes('custom-layout')               , 'Adds custom class'     )
    })

    test('add_row adds row correctly', assert => {
        const layout = new Layout({})
        const row    = layout.add_row({ class: 'custom-row' })

        assert.ok   (row instanceof Row                                   , 'Returns Row instance'  )
        assert.ok   (row.class.includes('custom-row')                    , 'Sets custom class'     )
        assert.equal(layout.elements.length   , 1                        , 'Adds to layout elements')
    })

    test('add_rows adds multiple rows', assert => {
        const layout = new Layout({})
        const configs = [
            { class: 'header'   },
            { class: 'content'  },
            { class: 'footer'   }
        ]

        layout.add_rows(configs)

        assert.equal(layout.elements.length   , 3                        , 'Adds all rows'         )
        assert.ok   (layout.elements[0].class.includes('header')        , 'Sets header class'     )
        assert.ok   (layout.elements[1].class.includes('content')       , 'Sets content class'    )
        assert.ok   (layout.elements[2].class.includes('footer')        , 'Sets footer class'     )
    })

    test('generates correct HTML structure', assert => {
        const layout = new Layout({})
        const row1   = layout.add_row({ class: 'header' })
        const row2   = layout.add_row({ class: 'content' })

        row1.add_col({ size: 12, value: 'Header' })
        row2.add_col({ size: 6 , value: 'Left'   })
        row2.add_col({ size: 6 , value: 'Right'  })

        const html = layout.html()
        assert.ok   (html.includes('class="layout "')                     , 'Has layout class'      )
        assert.ok   (html.includes('class="row header"')                , 'Has header row'        )
        assert.ok   (html.includes('class="row content"')               , 'Has content row'       )
        assert.ok   (html.includes('class="col-12 "')                    , 'Has full-width column' )
        assert.ok   (html.includes('class="col-6 "')                     , 'Has half-width columns')
    })
})