import Icon__Mappings from '../../../js/css/icons/Icon__Mappings.mjs'

const { module, test, only } = QUnit

module('Icon__Mappings', hooks => {
    test('static categories contain expected icons', assert => {
        // Test ARROWS category
        assert.equal(Icon__Mappings.ARROWS['arrow-left']     , '←'                , 'Has left arrow'         )
        assert.equal(Icon__Mappings.ARROWS['arrow-right']    , '→'                , 'Has right arrow'        )

        // Test UI_ELEMENTS category
        assert.equal(Icon__Mappings.UI_ELEMENTS['close']     , '×'                , 'Has close symbol'       )
        assert.equal(Icon__Mappings.UI_ELEMENTS['menu']      , '☰'                , 'Has menu symbol'        )

        // Test SHAPES category
        assert.equal(Icon__Mappings.SHAPES['star']           , '★'                , 'Has star symbol'        )
        assert.equal(Icon__Mappings.SHAPES['heart']          , '♥'                , 'Has heart symbol'       )

        // Test STATUS category
        assert.equal(Icon__Mappings.STATUS['warning']        , '⚠'                , 'Has warning symbol'     )
        assert.equal(Icon__Mappings.STATUS['success']        , '✔'                , 'Has success symbol'     )
    })

    test('ALL combines all categories', assert => {
        const all = Icon__Mappings.ALL

        // Test presence of icons from different categories
        assert.equal(all['arrow-left']                       , '←'                , 'Has arrows'             )
        assert.equal(all['close']                            , '×'                , 'Has UI elements'        )
        assert.equal(all['star']                             , '★'                , 'Has shapes'             )
        assert.equal(all['warning']                          , '⚠'                , 'Has status icons'       )
        assert.equal(all['play']                             , '▶'                , 'Has media controls'     )
        assert.equal(all['sun']                              , '☀'                , 'Has weather icons'      )
        assert.equal(all['mail']                             , '✉'                , 'Has communication icons')
        assert.equal(all['folder']                           , '📁'                , 'Has file icons'         )
        assert.equal(all['clock']                            , '🕐'                , 'Has time icons'         )
        assert.equal(all['link']                             , '🔗'                , 'Has misc icons'         )
    })

    test('getIcon returns correct icons', assert => {
        // Test existing icons
        assert.equal(Icon__Mappings.getIcon('arrow-left')    , '←'                , 'Gets existing icon'     )
        assert.equal(Icon__Mappings.getIcon('close')         , '×'                , 'Gets UI element'        )

        // Test fallback behavior
        assert.equal(Icon__Mappings.getIcon('nonexistent')   , 'nonexistent'      , 'Falls back to name'     )
        assert.equal(Icon__Mappings.getIcon('')              , ''                 , 'Handles empty string'   )
    })

    test('getCategory returns correct category', assert => {
        // Test existing categories
        const arrows = Icon__Mappings.getCategory('ARROWS')
        assert.equal(arrows['arrow-left']                    , '←'                , 'Gets arrows category'   )

        const shapes = Icon__Mappings.getCategory('SHAPES')
        assert.equal(shapes['star']                          , '★'                , 'Gets shapes category'   )

        // Test nonexistent category
        const invalid = Icon__Mappings.getCategory('INVALID')
        assert.deepEqual(invalid                             , {}                 , 'Returns empty object'   )
    })

    test('getCategories returns all categories', assert => {
        const categories = Icon__Mappings.getCategories()

        assert.ok   (categories.includes('ARROWS')                                , 'Has ARROWS category'    )
        assert.ok   (categories.includes('UI_ELEMENTS')                           , 'Has UI_ELEMENTS'        )
        assert.ok   (categories.includes('SHAPES')                                , 'Has SHAPES'             )
        assert.ok   (categories.includes('STATUS')                                , 'Has STATUS'             )
        assert.ok   (categories.includes('MEDIA')                                 , 'Has MEDIA'              )
        assert.ok   (categories.includes('WEATHER')                               , 'Has WEATHER'            )
        assert.ok   (categories.includes('COMMUNICATION')                         , 'Has COMMUNICATION'      )
        assert.ok   (categories.includes('FILES')                                 , 'Has FILES'              )
        assert.ok   (categories.includes('TIME')                                  , 'Has TIME'               )
        assert.ok   (categories.includes('MISC')                                  , 'Has MISC'               )
        assert.equal(categories.length                       , 10                 , 'Has correct count'      )
    })
})