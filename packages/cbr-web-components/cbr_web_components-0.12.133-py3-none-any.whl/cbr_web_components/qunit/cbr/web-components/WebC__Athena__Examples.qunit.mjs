import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__Athena__Examples                      from '../../../js/cbr/web-components/WebC__Athena__Examples.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test , only} = QUnit

const MOCK_EXAMPLES_DATA = {
    title: 'Test Examples',
    examples: [
        'Test example 1',
        'Test example 2',
        'Test example 3'
    ]
}

module('WebC__Athena__Examples', hooks => {
    let target_div
    let examples
    let original_console_error

    hooks.before(async () => {
        setup_mock_responses()
        set_mock_response('/markdown/static_content/data-file?path=en/site/athena/questions.toml', 'GET', MOCK_EXAMPLES_DATA)

        // Mock console.error
        // original_console_error = console.error
        // console.error = () => {}

        target_div = WebC__Target_Div.add_to_body()
        examples = await target_div.append_child(WebC__Athena__Examples, { channel: 'test-channel' })
        await examples.wait_for__component_ready()
    })

    hooks.after(() => {
        //console.error = original_console_error
        examples.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(examples.tagName.toLowerCase()         , 'webc-athena-examples'    , 'Has correct tag name')
        assert.equal(examples.constructor.element_name      , 'webc-athena-examples'    , 'Has correct element name')
        assert.equal(examples.constructor.name              , 'WebC__Athena__Examples'  , 'Has correct class name')
        assert.equal(examples.channel                       , 'test-channel'            , 'Sets channel from attributes')

        assert.ok(examples.shadowRoot                                                   , 'Has shadow root')
        assert.ok(examples.api_markdown                                                 , 'Has API__Markdown')
        assert.ok(examples instanceof Web_Component                                     , 'Extends Web_Component')
        assert.ok(examples instanceof HTMLElement                                       , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = examples.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                    , 'Has CSS rules')
        assert.ok(css_rules['.example-card']                                           , 'Has example card styles')
        assert.ok(css_rules['.text-center']                                            , 'Has utility styles')
    })

    test('renders examples correctly', async assert => {
        const title = examples.query_selector('h2')
        const cards = examples.query_selector_all('.example-card')

        assert.equal(title.textContent                      , MOCK_EXAMPLES_DATA.title , 'Shows correct title')
        assert.equal(cards.length                          , 3                        , 'Renders all examples')

        cards.forEach((card, index) => {
            assert.equal(card.querySelector('.card-body').textContent,
                        MOCK_EXAMPLES_DATA.examples[index]           , 'Shows correct example text')
        })
    })

    test('handles example clicks', assert => {
        assert.expect(4)  // Expecting 4 assertions

        function assert__new_input_message(event) {
            assert.equal(event.detail.channel                , 'test-channel'         , 'Event includes channel')
            assert.equal(event.detail.user_prompt           , 'Test example 1'        , 'Event includes example text')
            assert.deepEqual(event.detail.images            , []                      , 'Event includes empty images array')
            assert.ok(event.bubbles && event.composed                                 , 'Event is properly configured')

            window.removeEventListener('new_input_message',assert__new_input_message)
        }
        window.addEventListener('new_input_message',assert__new_input_message)

        const first_card = examples.query_selector('.example-card')
        first_card.click()
    })

    test('handles failed content loading', async assert => {
        set_mock_response('/markdown/static_content/data-file?path=en/site/athena/questions.toml', 'GET', null)

        examples = await target_div.append_child(WebC__Athena__Examples)
        await examples.wait_for__component_ready()

        const title = examples.query_selector('h2')
        const cards = examples.query_selector_all('.example-card')

        assert.equal(title.textContent                      , 'Prompt examples'        , 'Shows fallback title')
        assert.equal(cards.length                          , 5                        , 'Shows fallback examples')
    })

    test('css_rules() returns correct styles', assert => {
        const rules = examples.css_rules()

        assert.deepEqual(rules['.example-card'], {
            cursor         : "pointer"                     ,
            transition    : "all 0.2s ease-in-out"        ,
            backgroundColor: "#f8f9fa"
        }, 'Example card styles are correct')

        assert.deepEqual(rules['.example-card:hover'], {
            transform     : "translateY(-2px)"             ,
            boxShadow    : "0 4px 6px rgba(0,0,0,0.1)"
        }, 'Hover styles are correct')

        assert.deepEqual(rules['.text-center'], {
            textAlign: "center"
        }, 'Utility styles are correct')
    })
})