import CBR__Important_Alert from '../../../js/cbr/main-page/CBR__Important_Alert.mjs'

const { module, test } = QUnit

module('CBR__Important_Alert', hooks => {
    test('creates correct HTML structure', assert => {
        // Arrange
        const alert_id = 'test-alert'

        // Act
        const alert     = new CBR__Important_Alert({ id: alert_id })
        const dom       = alert.dom_create()

        // Assert - Element Structure
        assert.equal(dom.id                                     , alert_id          , 'Has correct ID'               )
        assert.ok   (dom.classList.contains('important-alert')                     , 'Has important-alert class'     )

        // Notice Element
        const notice = dom.querySelector('.alert-important-note')
        assert.ok   (notice                                                        , 'Notice element exists'         )
        assert.ok   (notice.classList.contains('alert')                           , 'Has alert class'               )
        assert.ok   (notice.classList.contains('alert-success')                   , 'Has alert-success class'       )

        // Content Elements
        const content = notice.querySelector('.alert-content')
        assert.ok   (content                                                       , 'Content element exists'        )

        const heading = content.querySelector('.alert-heading')
        assert.ok   (heading                                                       , 'Heading element exists'        )
        assert.equal(heading.textContent                       , 'Important Note'  , 'Has correct heading text'      )

        // Warning Text Content
        const warning_text = content.children[1].textContent
        assert.ok   (warning_text.includes("Don't use any private")               , 'Contains privacy warning'      )
        assert.ok   (warning_text.includes("no control over what happens")        , 'Contains control statement'    )
        assert.ok   (warning_text.includes("chat thread content is publicly")     , 'Contains visibility warning'   )
    })

    test('preserves additional classes', assert => {
        // Arrange & Act
        const custom_class = 'custom-class'
        const alert       = new CBR__Important_Alert({ class: custom_class })
        const html        = alert.html()

        // Assert
        assert.ok(html.includes(`class="important-alert ${custom_class}"`), 'Contains both important-alert and custom class')
    })

    test('static css_rules returns expected styles', assert => {
        // Act
        const css_rules = CBR__Important_Alert.css_rules()

        // Assert
        assert.deepEqual(css_rules['.important-alert'     ], { padding   : "1rem"  , fontWeight: 100      }, 'Important alert styles are correct')
        assert.deepEqual(css_rules['.alert-heading'       ], { fontWeight: 300                            }, 'Alert heading styles are correct')
        assert.deepEqual(css_rules['.alert-content > div' ], { lineHeight: "1.4" ,  fontSize : "0.875rem" }, 'Alert content styles are correct')
        assert.deepEqual(css_rules['.alert-important-note'], { backgroundColor: "rgba(38, 198, 218, 0.1)" }, 'Alert important note styles are correct')
    })

    test('elements structure is correct', assert => {
        // Arrange & Act
        const alert = new CBR__Important_Alert()

        // Assert
        assert.equal(alert.elements.length, 1                                   , 'Has one top-level element'        )

        const div_notice = alert.elements[0]
        assert.ok(div_notice.class.includes('alert-important-note')            , 'Notice has correct class'         )

        const div_content = div_notice.elements[0]
        assert.equal(div_content.class, 'alert-content'                        , 'Content has correct class'        )

        const [text_title, text_content] = div_content.elements
        assert.equal(text_title.class, 'alert-heading'                         , 'Title has correct class'          )
        assert.equal(text_title.value, 'Important Note'                        , 'Title has correct value'          )
        assert.ok(text_content.value.includes("Don't use any private")         , 'Content has correct warning text' )
    })
})