// Svg__Icons.qunit.mjs
import Svg__Icons  from '../../js/core/Svg__Icons.mjs'
import Raw_Html    from '../../js/core/Raw_Html.mjs'

const { module, test , only } = QUnit

module('Svg__Icons', hooks => {
    let icons

    hooks.beforeEach(() => {
        icons = new Svg__Icons()
    })

    test('picture_as_pdf creates correct icon', assert => {
        const result = icons.picture_as_pdf({ width: '32px' })
        assert.ok   (result instanceof Raw_Html                               , 'Returns Raw_Html instance')
        assert.equal(result.class               , 'icon-svg picture-as-pdf'   , 'Sets correct classes')
        assert.ok   (result.raw_html.includes('width="32px"')                , 'Applies attributes')
        assert.ok   (result.raw_html.includes('xmlns="http://www.w3.org/2000/svg"'), 'Includes SVG namespace')
    })

    test('screenshot_monitor creates correct icon', assert => {
        const result = icons.screenshot_monitor({ height: '48px' })
        assert.ok   (result instanceof Raw_Html                               , 'Returns Raw_Html instance')
        assert.equal(result.class               , 'icon-svg screenshot-monitor', 'Sets correct classes')
        assert.ok   (result.raw_html.includes('height="48px"')               , 'Applies attributes')
    })

    test('generic icon method handles valid icon name', assert => {
        const result = icons.icon('picture_as_pdf', { width: '32px' })
        assert.ok   (result instanceof Raw_Html                          , 'Returns Raw_Html instance')
        assert.equal(result.class            , 'icon-svg picture-as-pdf' , 'Sets correct classes')
        assert.ok   (result.raw_html.includes('width="32px"')            , 'Applies attributes')
    })

    test('generic icon method handles invalid icon name', assert => {
        const result = icons.icon('non_existent_icon')
        assert.equal(result                     , undefined                   , 'Returns undefined for invalid icon')
    })

    test('icon class names are correctly formatted', assert => {
        const result = icons.icon('user_profile')
        assert.equal(result.class               , 'icon-svg user-profile'     , 'Formats class name correctly')
    })

    test('applies multiple attributes to SVG', assert => {
        const attrs = {
            width  : '32px'                     ,
            height : '32px'                     ,
            fill   : 'red'
        }
        const result = icons.picture_as_pdf(attrs)
        assert.ok(result.raw_html.includes('width="32px"')                   , 'Sets width')
        assert.ok(result.raw_html.includes('height="32px"')                  , 'Sets height')
        assert.ok(result.raw_html.includes('fill="red"')                     , 'Sets fill')
    })
})