import CBR__Left_Logo    from '../../../js/cbr/main-page/CBR__Left_Logo.mjs'

const { module, test } = QUnit

module('CBR__Left_Logo', hooks => {
    test('creates correct HTML structure', assert => {
        // Arrange
        const logo_id = 'test-logo'

        // Act
        const logo     = new CBR__Left_Logo({ id: logo_id })
        const dom      = logo.dom_create()

        // Assert - Element Structure
        assert.equal(dom.id                             , logo_id              , 'Has correct ID'            )
        assert.ok   (dom.classList.contains('logo')                           , 'Has logo class'            )

        // Container Element
        const container = dom.querySelector('.logo-container')
        assert.ok   (container                                                , 'Container element exists'   )

        // Logo Wrapper
        const wrapper = container.querySelector('.logo-wrapper')
        assert.ok   (wrapper                                                  , 'Wrapper element exists'     )

        // Image Element
        const img = wrapper.querySelector('img.logo')
        assert.ok   (img                                                      , 'Image element exists'       )
        assert.equal(img.alt                            , 'Cyber Boardroom Logo', 'Has correct alt text'    )
        assert.equal(img.src                            , 'https://static.dev.aws.cyber-boardroom.com/cbr-static/latest/assets/cbr/cbr-logo-beta.png',
                                                                               'Has correct image source'   )
    })

    test('preserves additional classes', assert => {
        // Arrange & Act
        const custom_class = 'custom-class'
        const logo        = new CBR__Left_Logo({ class: custom_class })
        const dom         = logo.dom_create()

        // Assert
        assert.ok(dom.classList.contains('logo'        )                      , 'Has logo class'            )
        assert.ok(dom.classList.contains(custom_class  )                      , 'Has custom class'          )
    })

    test('static css_rules returns expected styles', assert => {
        // Act
        const css_rules = CBR__Left_Logo.css_rules()

        // Assert
        assert.deepEqual(css_rules['.logo-container'], {
            display         : "flex"          ,
            flexDirection  : "column"        ,
            padding        : "1rem"          ,
            backgroundColor: "#ffffff"        ,
            borderRadius   : "0.5rem"
        }, 'Logo container styles are correct')

        assert.deepEqual(css_rules['.logo-wrapper'], {
            marginBottom   : "1rem"
        }, 'Logo wrapper styles are correct')

        assert.deepEqual(css_rules['.logo'], {
            width          : "100%"          ,
            height         : "auto"
        }, 'Logo styles are correct')
    })

    test('elements structure is correct', assert => {
        // Arrange & Act
        const logo = new CBR__Left_Logo()

        // Assert
        assert.equal(logo.elements.length, 1                                  , 'Has one top-level element' )

        const div_container = logo.elements[0]
        assert.equal(div_container.class, 'logo-container'                    , 'Container has correct class')

        const div_logo = div_container.elements[0]
        assert.equal(div_logo.class, 'logo-wrapper'                          , 'Wrapper has correct class'  )

        const img_logo = div_logo.elements[0]
        assert.equal(img_logo.class, 'logo'                                  , 'Image has correct class'    )
        assert.equal(img_logo.attributes.alt, 'Cyber Boardroom Logo'         , 'Image has correct alt text' )
        assert.equal(img_logo.attributes.src, 'https://static.dev.aws.cyber-boardroom.com/cbr-static/latest/assets/cbr/cbr-logo-beta.png',
                                                                              'Image has correct source'    )
    })
})