import CBR__Top_Banner from '../../../js/cbr/elements/CBR__Top_Banner.mjs'

const { module, test , only} = QUnit

module('CBR__Top_Banner', hooks => {
    test('creates correct HTML structure', assert => {
        // Arrange
        const banner_id = 'test-banner'

        // Act
        const banner    = new CBR__Top_Banner({ id: banner_id })
        const dom       = banner.dom_create()

        // Assert - Element Structure
        assert.equal(dom.id                                  , banner_id           , 'Has correct ID'               )
        assert.ok   (dom.classList.contains('top-banner')                         , 'Has top-banner class'         )

        // Menu Icon
        const menu_icon = dom.querySelector('.menu-icon')
        assert.ok   (menu_icon                                                    , 'Menu icon exists'             )
        assert.ok   (menu_icon.classList.contains('icon-lg')                      , 'Has icon-lg class'           )
        assert.ok   (menu_icon.classList.contains('menu-icon')                    , 'Has menu-icon class'         )
        assert.ok   (menu_icon.textContent.includes('☰')                         , 'Shows menu icon'              )

        // User Session Component
        const user_session = dom.querySelector('webc-cbr-user-session')
        assert.ok   (user_session                                                 , 'User session component exists')
    })

    test('preserves additional classes', assert => {
        // Arrange & Act
        const custom_class = 'custom-class'
        const banner      = new CBR__Top_Banner({ class: custom_class })
        const dom         = banner.dom_create()

        // Assert
        assert.ok(dom.classList.contains('top-banner')                            , 'Has top-banner class'         )
        assert.ok(dom.classList.contains(custom_class)                            , 'Has custom class'            )
    })

    test('static css_rules returns expected styles', assert => {
        // Act
        const css_rules = CBR__Top_Banner.css_rules()

        // Assert
        assert.deepEqual(css_rules['.top-banner'], {
            display         : "flex"               ,
            justifyContent : "space-between"       ,
            alignItems     : "center"              ,
            padding        : "0 1rem"              ,
            height         : "100%"                ,
            backgroundColor: "#1e88e5"             ,
            color          : "#ffffff"             ,
            position       : "relative"
        }, 'Top banner styles are correct')

        assert.deepEqual(css_rules['.menu-icon'], {
            color          : "#ffffff"             ,
            cursor        : "pointer"              ,
            fontSize      : "1.75rem"              ,
            padding       : "0.5rem"               ,
            marginLeft    : "-0.5rem"
        }, 'Menu icon styles are correct')

        assert.deepEqual(css_rules['.menu-icon:hover'], {
            backgroundColor: "rgba(255, 255, 255, 0.1)",
            borderRadius   : "4px"
        }, 'Menu icon hover styles are correct')
    })

    test('elements structure is correct', assert => {
        // Arrange & Act
        const banner = new CBR__Top_Banner()

        // Assert
        assert.equal(banner.elements.length   , 2                                 , 'Has two elements'             )

        const [menu_icon, user_session] = banner.elements

        // Menu Icon
        assert.ok   (menu_icon.class.includes('menu-icon')                       , 'Menu icon has correct class'  )
        assert.ok   (menu_icon.class.includes('icon-lg')                         , 'Menu icon has size class'     )
        assert.equal(menu_icon.attributes.icon, 'menu'                           , 'Menu icon has correct icon'   )

        // User Session
        assert.equal(user_session.tag         , 'webc-cbr-user-session'          , 'User session has correct tag' )
    })

    test('setup method adds required classes', assert => {
        // Arrange & Act
        const banner = new CBR__Top_Banner()

        // Assert
        assert.ok(banner.class.includes('top-banner')                            , 'Top banner class was added'   )
    })
})