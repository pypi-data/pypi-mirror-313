import WebC__Target_Div from '../../js/utils/WebC__Target_Div.mjs'
import Web_Component    from '../../js/core/Web_Component.mjs'
import WebC__System__Prompt from '../../js/chat-bot/WebC__System__Prompt.mjs'
import Icon__Mappings from "../../js/css/icons/Icon__Mappings.mjs"

const { module, test , only} = QUnit

module('WebC__System__Prompt', hooks => {
    let target_div
    let system_prompt

    hooks.beforeEach(async () => {
        target_div = WebC__Target_Div.add_to_body()
        system_prompt = await target_div.append_child(WebC__System__Prompt, { content: 'Test content' })
        await system_prompt.wait_for__component_ready()
    })

    hooks.afterEach(() => {
        system_prompt.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(system_prompt.tagName.toLowerCase()         , 'webc-system-prompt'    , 'Has correct tag name'     )
        assert.equal(system_prompt.constructor.element_name      , 'webc-system-prompt'    , 'Has correct element name' )
        assert.equal(system_prompt.constructor.name              , 'WebC__System__Prompt'  , 'Has correct class name'   )
        assert.equal(system_prompt.expanded                      , false                   , 'Initially not expanded'   )
        assert.equal(system_prompt.content                       , 'Test content'          , 'Sets content correctly'   )

        assert.ok(system_prompt.shadowRoot                                                 , 'Has shadow root'          )
        assert.ok(system_prompt instanceof Web_Component                                   , 'Extends Web_Component'    )
        assert.ok(system_prompt instanceof HTMLElement                                     , 'Is HTML Element'          )
    })

    test('applies CSS rules correctly', assert => {
        const css_rules = system_prompt.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                       , 'Has CSS rules'            )
        assert.ok(css_rules['.system-prompt-container']                                   , 'Has container styles'     )
        assert.ok(css_rules['.prompt-header']                                             , 'Has header styles'        )
        assert.ok(css_rules['.prompt-content']                                            , 'Has content styles'       )
    })

    test('renders initial structure correctly', assert => {
        const container = system_prompt.query_selector('.system-prompt-container')
        const header = system_prompt.query_selector('.prompt-header')
        const toggle = system_prompt.query_selector('.prompt-toggle')
        const content = system_prompt.query_selector('.prompt-content')

        assert.ok(container                                                               , 'Container exists'         )
        assert.ok(header                                                                  , 'Header exists'            )
        assert.ok(toggle                                                                  , 'Toggle exists'            )
        assert.ok(content                                                                 , 'Content exists'           )

        const summary = header.querySelector('.prompt-summary')
        assert.equal(summary.textContent,'System Prompt (12 chars)'                       , 'Shows content length'     )
        assert.equal(content.textContent                     , 'Test content'             , 'Shows correct content'    )
    })

    test('handles expansion toggle', assert => {
        const header = system_prompt.query_selector('.prompt-header')
        const content = system_prompt.query_selector('.prompt-content')
        const toggle = system_prompt.query_selector('.icon')

        assert.equal(content.style.display                   , ''                         , 'Initially hidden'         )
        assert.equal(toggle.textContent                      , Icon__Mappings.getIcon('triangle-right'),
                                                                                           'Initial toggle icon'       )

        header.click()
        assert.equal(content.style.display                   , 'block'                    , 'Shows content'           )
        assert.equal(toggle.textContent                      , Icon__Mappings.getIcon('triangle-down'),
                                                                                           'Updates toggle icon'      )

        header.click()
        assert.equal(content.style.display                   , 'none'                     , 'Hides content'          )
        assert.equal(toggle.textContent                      , Icon__Mappings.getIcon('triangle-right'),
                                                                                           'Restores toggle icon'    )
    })

    test('calculates content size correctly', assert => {
        const empty = system_prompt.calculate_size('')
        const short = system_prompt.calculate_size('test')
        const long  = system_prompt.calculate_size('test content')

        assert.equal(empty                                   , 0                          , 'Handles empty content'   )
        assert.equal(short                                   , 4                          , 'Counts short content'    )
        assert.equal(long                                    , 12                         , 'Counts long content'     )
    })

    test('handles content updates', async assert => {
        system_prompt.content = 'Updated content'
        await system_prompt.refresh_ui()

        const content = system_prompt.query_selector('.prompt-content')
        const summary = system_prompt.query_selector('.prompt-summary')

        assert.equal(content.textContent                     , 'Updated content'          , 'Updates content'         )
        assert.ok(summary.textContent.includes('15')                                      , 'Updates size display'    )
    })

    test('load_attributes', assert => {
        const prompt_1 = WebC__System__Prompt.create({content:'abc'})
        assert.equal(prompt_1.content, '')
        prompt_1.load_attributes()
        assert.equal(prompt_1.content, 'abc')

        const prompt_2 = WebC__System__Prompt.create()
        prompt_2.load_attributes()
        assert.equal(prompt_2.content, '')


    })
})