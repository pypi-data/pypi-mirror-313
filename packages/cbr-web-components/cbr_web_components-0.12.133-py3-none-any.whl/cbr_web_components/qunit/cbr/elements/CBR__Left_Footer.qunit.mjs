import CBR__Left_Footer from '../../../js/cbr/elements/CBR__Left_Footer.mjs'

const { module, test , only} = QUnit

module('CBR__Left_Footer', hooks => {
        test('creates correct HTML structure', assert => {
        // Arrange
        const footer_id = 'test-footer'
        const version   = '1.2.3'

        // Act
        const footer    = new CBR__Left_Footer({ id: footer_id, version: version })
        const dom       = footer.dom_create()

        // Assert - Element Structure
        assert.equal(dom.id                                     , footer_id          , 'Has correct ID'              )
        assert.ok   (dom.classList.contains('left-footer')                          , 'Has left-footer class'       )

        // Container Elements
        const footer_container = dom.querySelector('.footer-container')
        assert.ok   (footer_container                                               , 'Footer container exists'      )

        const icons_container = footer_container.querySelector('.icons-container')
        assert.ok   (icons_container                                               , 'Icons container exists'       )

        const version_container = footer_container.querySelector('.version-container')
        assert.ok   (version_container                                             , 'Version container exists'     )

        // Links and Icons
        const links = icons_container.querySelectorAll('a.link-icon')
        assert.equal(links.length                              , 2                  , 'Has two icon links'          )

        const settings_link = links[0]
        assert.equal(settings_link.getAttribute('href')        , footer.href__settings, 'Settings link is correct'  )
        assert.ok   (settings_link.querySelector('.icon')                             , 'Settings icon exists'      )

        const logout_link = links[1]
        assert.equal(logout_link.getAttribute('href')          , footer.href__logout  , 'Logout link is correct'    )
        assert.ok   (logout_link.querySelector('.icon')                               , 'Logout icon exists'       )

        // Version Text
        const version_text = version_container.querySelector('.version-text')
        assert.ok   (version_text                                                  , 'Version text exists'         )
        assert.ok   (version_text.textContent.includes(version)                    , 'Shows correct version'       )
        assert.ok   (version_text.textContent.includes('© Cyber Boardroom')        , 'Shows copyright text'        )
    })

    test('preserves additional classes', assert => {
        // Arrange & Act
        const custom_class = 'custom-class'
        const footer      = new CBR__Left_Footer({ class: custom_class })
        const dom         = footer.dom_create()

        // Assert
        assert.ok(dom.classList.contains('left-footer')                            , 'Has left-footer class'       )
        assert.ok(dom.classList.contains(custom_class)                             , 'Has custom class'           )
    })

    test('static css_rules returns expected styles', assert => {
        // Act
        const css_rules = CBR__Left_Footer.css_rules()

        // Assert
        assert.deepEqual(css_rules['.left-footer'], {
            display    : "flex"           ,
            alignItems: "center"          ,
            padding   : "0 1rem"
        }, 'Left footer styles are correct')

        assert.deepEqual(css_rules['.footer-container'], {
            display       : "flex"        ,
            flexDirection: "column"       ,            // Stack containers vertically
            width        : "100%"
        }, 'Footer container styles are correct')

        assert.deepEqual(css_rules['.icons-container'], {
            display         : "flex"       ,
            alignItems     : "center"      ,
            justifyContent: "space-between",
            width          : "100%"        ,
            color          : "#6c757d"               // Medium gray for icons and text
        }, 'Icons container styles are correct')

        assert.deepEqual(css_rules['.version-container'], {
            display        : "flex"        ,
            alignItems    : "center"       ,
            justifyContent: "center"                 // Center the version text
        }, 'Version container styles are correct')

        assert.deepEqual(css_rules['.version-text'], {
            fontSize  : "0.875rem"        ,
            fontWeight: "300"             ,
            color     : "#495057"                   // Slightly darker for better readability
        }, 'Version text styles are correct')

        assert.deepEqual(css_rules['.footer-icon'], {
            fontSize: "1.5rem"            ,
            padding : "0.5rem"
        }, 'Footer icon styles are correct')

        assert.deepEqual(css_rules['.footer-icon:hover'], {
            color: "#495057"                             // Darker on hover
        }, 'Footer icon hover styles are correct')

        assert.deepEqual(css_rules['.link-icon'], {
            marginBottom   : "0.5rem"      ,
            textDecoration: "none"         ,      // Remove underline
            color         : "inherit"      ,      // Use parent's color
            display       : "flex"         ,      // Ensure icon alignment
            alignItems    : "center"
        }, 'Link icon styles are correct')
    })

    test('elements structure is correct', assert => {
        // Arrange & Act
        const version = '1.2.3'
        const footer = new CBR__Left_Footer({ version: version })

        // Assert
        assert.equal(footer.elements.length, 1                                     , 'Has one top-level element'    )

        const div_footer = footer.elements[0]
        assert.equal(div_footer.class, 'footer-container'                         , 'Footer has correct class'     )

        const [div_icons, div_version] = div_footer.elements
        assert.equal(div_icons  .class, 'icons-container'                         , 'Icons div has correct class'  )
        assert.equal(div_version.class, 'version-container'                       , 'Version div has correct class')

        const [a_settings, a_logout] = div_icons.elements
        assert.equal(a_settings.class     , 'link-icon'                          , 'Settings link has correct class')
        assert.equal(a_settings.attributes.href, '/web/user/profile'              , 'Settings has correct href'     )
        assert.equal(a_logout .class      , 'link-icon'                          , 'Logout link has correct class' )
        assert.equal(a_logout .attributes.href, '/web/sign-out'                   , 'Logout has correct href'      )

        const text_version = div_version.elements[0]
        assert.equal(text_version.class   , 'version-text'                       , 'Version has correct class'    )
        assert.ok   (text_version.value.includes(version)                        , 'Version shows correct value'  )
    })


    test('constructor handles default values', assert => {
        // Test with no parameters
        const left_footer__empty = new CBR__Left_Footer()
        assert.equal(left_footer__empty.version         , 'NA'                         , 'Sets default version when no params'     )
        assert.ok   (left_footer__empty.class.includes('left-footer')                 , 'Sets default class when no params'       )

        // Test with undefined values
        const left_footer__undefined = new CBR__Left_Footer({ version: undefined })
        assert.equal(left_footer__undefined.version     , 'NA'                         , 'Sets default version with undefined'     )
        assert.ok   (left_footer__undefined.class.includes('left-footer')             , 'Sets default class with undefined'       )
    })
})