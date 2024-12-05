import CBR__Content__Placeholder from '../../../js/cbr/elements/CBR__Content__Placeholder.mjs'

const { module, test } = QUnit

module('CBR__Content__Placeholder', hooks => {
    test('creates correct HTML structure', assert => {
        // Arrange
        const placeholder_id = 'test-placeholder'

        // Act
        const placeholder = new CBR__Content__Placeholder({ id: placeholder_id })
        const dom         = placeholder.dom_create()

        // Assert - Element Structure
        assert.equal(dom.id                                        , placeholder_id       , 'Has correct ID'                )
        assert.ok   (dom.classList.contains('content-placeholder')                       , 'Has content-placeholder class' )

        // Container Element
        const container = dom.querySelector('#placeholder-container')
        assert.ok   (container                                                           , 'Container element exists'      )
        assert.ok   (container.classList.contains('placeholder-container')               , 'Has placeholder-container class')
    })

    test('preserves additional classes', assert => {
        // Arrange & Act
        const custom_class = 'custom-class'
        const placeholder = new CBR__Content__Placeholder({ class: custom_class })
        const dom         = placeholder.dom_create()

        // Assert
        assert.ok(dom.classList.contains('content-placeholder')                          , 'Has content-placeholder class' )
        assert.ok(dom.classList.contains(custom_class)                                   , 'Has custom class'             )
    })

    test('static css_rules returns expected styles', assert => {
        // Act
        const css_rules = CBR__Content__Placeholder.css_rules()

        // Assert
        assert.deepEqual(css_rules['.placeholder-container'], {
            height          : '100%'                                   ,
            width           : '100%'                                   ,
            backgroundColor : "#eef5f9"                               ,         // Light base color
            boxShadow       : "inset 10px 20px 30px rgba(0,0,0,0.07)"         // Soft shadow
        }, 'Placeholder container styles are correct')
    })

    test('elements structure is correct', assert => {
        // Arrange & Act
        const placeholder = new CBR__Content__Placeholder()

        // Assert
        assert.equal(placeholder.elements.length, 1                                      , 'Has one top-level element'    )

        const div_container = placeholder.elements[0]
        assert.equal(div_container.id           , 'placeholder-container'                , 'Container has correct ID'     )
        assert.equal(div_container.class        , 'placeholder-container'                , 'Container has correct class'  )
    })
})