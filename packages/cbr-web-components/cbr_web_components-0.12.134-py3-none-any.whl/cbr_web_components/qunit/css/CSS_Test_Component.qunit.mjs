import Web_Component    from '../../js/core/Web_Component.mjs'
import WebC__Target_Div from '../../js/utils/WebC__Target_Div.mjs'

// Import all CSS frameworks
import CSS__Alerts       from '../../js/css/CSS__Alerts.mjs'
import CSS__Badges      from '../../js/css/CSS__Badges.mjs'
import CSS__Breadcrumbs from '../../js/css/CSS__Breadcrumbs.mjs'
import CSS__Buttons     from '../../js/css/CSS__Buttons.mjs'
import CSS__Cards       from '../../js/css/CSS__Cards.mjs'
import CSS__Forms       from '../../js/css/CSS__Forms.mjs'
import CSS__Images      from '../../js/css/CSS__Images.mjs'
import CSS__List_Groups from '../../js/css/CSS__List_Groups.mjs'
import CSS__Navbar      from '../../js/css/CSS__Navbar.mjs'
import CSS__Navs_Tabs   from '../../js/css/CSS__Navs_Tabs.mjs'
import CSS__Pagination  from '../../js/css/CSS__Pagination.mjs'
import CSS__Progress    from '../../js/css/CSS__Progress.mjs'
import CSS__Spinners    from '../../js/css/CSS__Spinners.mjs'
import CSS__Tables      from '../../js/css/CSS__Tables.mjs'
import CSS__Typography  from '../../js/css/CSS__Typography.mjs'

const { module, test, only } = QUnit

// Create a test component that will load all CSS frameworks
class CSS_Test_Component extends Web_Component {
    async apply_css() {
        new CSS__Alerts     (this).apply_framework()
        new CSS__Badges     (this).apply_framework()
        new CSS__Breadcrumbs(this).apply_framework()
        new CSS__Buttons    (this).apply_framework()
        new CSS__Cards      (this).apply_framework()
        new CSS__Forms      (this).apply_framework()
        new CSS__Images     (this).apply_framework()
        new CSS__List_Groups(this).apply_framework()
        new CSS__Navbar     (this).apply_framework()
        new CSS__Navs_Tabs  (this).apply_framework()
        new CSS__Pagination (this).apply_framework()
        new CSS__Progress   (this).apply_framework()
        new CSS__Spinners   (this).apply_framework()
        new CSS__Tables     (this).apply_framework()
        new CSS__Typography (this).apply_framework()
    }
}

CSS_Test_Component.define()

module('CSS Frameworks Integration', hooks => {
    let target_div
    let component

    hooks.beforeEach(async () => {
        target_div = WebC__Target_Div.add_to_body()
        component = await target_div.append_child(CSS_Test_Component)
        await component.wait_for__component_ready()
    })

    hooks.afterEach(() => {
        component.remove()
        target_div.remove()
    })

    test('all CSS frameworks load successfully', async assert => {
        const css_rules = component.all_css_rules()

        // Alert styles
        assert.ok(css_rules['.alert']                              , 'Alert styles loaded'         )
        assert.ok(css_rules['.alert-primary']                      , 'Alert variants loaded'       )

        // Badge styles
        assert.ok(css_rules['.badge']                              , 'Badge styles loaded'         )
        assert.ok(css_rules['.badge-pill']                         , 'Badge variants loaded'       )

        // Breadcrumb styles
        assert.ok(css_rules['.nav-breadcrumb']                     , 'Breadcrumb styles loaded'    )
        assert.ok(css_rules['.nav-breadcrumb-item']                , 'Breadcrumb items loaded'     )

        // Button styles
        assert.ok(css_rules['.btn']                                , 'Button styles loaded'        )
        assert.ok(css_rules['.btn-primary']                        , 'Button variants loaded'      )

        // Card styles
        assert.ok(css_rules['.card']                               , 'Card styles loaded'          )
        assert.ok(css_rules['.card-body']                          , 'Card components loaded'      )

        // Form styles
        assert.ok(css_rules['.inline-form']                        , 'Form styles loaded'          )
        assert.ok(css_rules['.input'      ]                         , 'Form components loaded'      )

        // Image styles
        assert.ok(css_rules['.img-fluid']                          , 'Image styles loaded'         )
        assert.ok(css_rules['.img-thumbnail']                      , 'Image variants loaded'       )

        // List Group styles
        assert.ok(css_rules['.list-group']                         , 'List Group styles loaded'    )
        assert.ok(css_rules['.list-group-item']                    , 'List items loaded'           )

        // Navbar styles
        assert.ok(css_rules['.navbar']                             , 'Navbar styles loaded'        )
        assert.ok(css_rules['.navbar-nav']                         , 'Navbar components loaded'    )

        // Nav/Tab styles
        assert.ok(css_rules['.nav']                                , 'Nav styles loaded'           )
        assert.ok(css_rules['.nav-tabs']                           , 'Tab styles loaded'           )

        // Pagination styles
        assert.ok(css_rules['.pagination'     ]                    , 'Pagination styles loaded'    )
        assert.ok(css_rules['.pagination-item']                    , 'Page items loaded'           )

        // Progress styles
        assert.ok(css_rules['.progress']                           , 'Progress styles loaded'      )
        assert.ok(css_rules['.progress-bar']                       , 'Progress bar loaded'         )

        // Spinner styles
        assert.ok(css_rules['.spinner'     ]                       , 'Spinner styles loaded'       )
        assert.ok(css_rules['.spinner-grow']                       , 'Spinner variants loaded'     )

        // Table styles
        assert.ok(css_rules['.table']                              , 'Table styles loaded'         )
        assert.ok(css_rules['.table-bordered']                     , 'Table variants loaded'       )

        // Typography styles
        assert.ok(css_rules['.type-mega']                          , 'Typography styles loaded'    )
        assert.ok(css_rules['.weight-thin']                        , 'Text utilities loaded'       )

        // Verify total number of rules (minimum expected)
        const rule_count = Object.keys(css_rules).length
        assert.ok(rule_count > 100                                 , 'Loaded substantial ruleset'  )
    })
})