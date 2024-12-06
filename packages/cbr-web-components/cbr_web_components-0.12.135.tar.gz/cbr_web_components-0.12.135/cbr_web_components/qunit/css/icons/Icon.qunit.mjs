import Icon           from '../../../js/css/icons/Icon.mjs'
import Span           from '../../../js/core/Span.mjs'

const { module, test } = QUnit

module('Icon', hooks => {
    test('constructor creates basic icon', assert => {
        const icon = new Icon({})
        assert.ok   (icon instanceof Span                                        , 'Inherits from Span'     )
        assert.ok   (icon.class.includes('icon')                                , 'Has icon class'         )
    })

    test('handles icon parameter', assert => {
        // Test with valid icon
        const arrow = new Icon({ icon: 'arrow-left' })
        assert.equal(arrow.value                            , '←'                , 'Sets correct symbol'    )
        assert.equal(arrow.attributes.icon                  , 'arrow-left'       , 'Stores icon name'      )

        // Test with invalid icon
        const invalid = new Icon({ icon: 'nonexistent' })
        assert.equal(invalid.value                         , 'nonexistent'       , 'Falls back to name'     )
        assert.equal(invalid.attributes.icon               , 'nonexistent'       , 'Stores invalid name'    )
    })

    test('applies size classes', assert => {
        const sizes = ['xs', 'sm', 'md', 'lg', 'xl']

        sizes.forEach(size => {
            const icon = new Icon({ size: size })
            assert.ok(icon.class.includes(`icon-${size}`)                       , `Applies ${size} class`  )
        })
    })

    test('applies color classes', assert => {
        const colors = ['primary', 'secondary', 'success', 'error', 'warning', 'info']

        colors.forEach(color => {
            const icon = new Icon({ color: color })
            assert.ok(icon.class.includes(`icon-${color}`)                      , `Applies ${color} class` )
        })
    })

    test('handles rotation', assert => {
        const rotations = [90, 180, 270]

        rotations.forEach(deg => {
            const icon = new Icon({ rotate: deg })
            assert.ok(icon.class.includes(`icon-rotate-${deg}`)                 , `Rotates ${deg} degrees` )
        })
    })

    test('handles animation flags', assert => {
        // Test spin
        const spinning = new Icon({ spin: true })
        assert.ok(spinning.class.includes('icon-spin')                          , 'Applies spin class'     )

        // Test pulse
        const pulsing = new Icon({ pulse: true })
        assert.ok(pulsing.class.includes('icon-pulse')                         , 'Applies pulse class'    )

        // Test both
        const animated = new Icon({ spin: true, pulse: true })
        assert.ok(animated.class.includes('icon-spin')                         , 'Has spin class'         )
        assert.ok(animated.class.includes('icon-pulse')                        , 'Has pulse class'        )
    })

    test('handles spacing', assert => {
        const spaces = ['left', 'right']

        spaces.forEach(space => {
            const icon = new Icon({ spacing: space })
            assert.ok(icon.class.includes(`icon-spacing-${space}`)             , `Applies ${space} spacing`)
        })
    })

    test('combines multiple properties', assert => {
        const icon = new Icon({
            icon   : 'arrow-left'           ,
            size   : 'lg'                   ,
            color  : 'primary'              ,
            rotate : 90                     ,
            spin   : true                   ,
            spacing: 'right'
        })

        assert.ok   (icon.class.includes('icon')                               , 'Has base class'         )
        assert.ok   (icon.class.includes('icon-lg')                           , 'Has size class'         )
        assert.ok   (icon.class.includes('icon-primary')                      , 'Has color class'        )
        assert.ok   (icon.class.includes('icon-rotate-90')                    , 'Has rotation class'     )
        assert.ok   (icon.class.includes('icon-spin')                         , 'Has spin class'         )
        assert.ok   (icon.class.includes('icon-spacing-right')                , 'Has spacing class'      )
        assert.equal(icon.value             , '←'                             , 'Has correct symbol'     )
    })

    test('preserves custom classes', assert => {
        const icon = new Icon({
            icon : 'star'                   ,
            class: 'custom-class'
        })

        assert.ok(icon.class.includes('icon')                                  , 'Keeps icon class'       )
        assert.ok(icon.class.includes('custom-class')                         , 'Adds custom class'      )
    })

    test('handles empty/undefined values', assert => {
        const icon = new Icon({
            size   : undefined              ,
            color  : null                   ,
            rotate : undefined              ,
            spin   : undefined              ,
            pulse  : undefined              ,
            spacing: null
        })

        assert.ok   (icon.class.includes('icon')                              , 'Has only base class'    )
        assert.equal(icon.class.split(' ').length, 2                         , 'No extra classes'       ) // 2 because of empty string in default
    })
})