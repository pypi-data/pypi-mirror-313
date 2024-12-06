import WebC__Container  from '../../js/core/WebC__Container.mjs'
import Web_Component    from '../../js/core/Web_Component.mjs'
import WebC__Target_Div from '../../js/utils/WebC__Target_Div.mjs'

const { module, test, only } = QUnit

module('WebC__Container', hooks => {
    let target_div
    let container

    hooks.beforeEach(async () => {
        target_div = WebC__Target_Div.add_to_body()
        container  = await target_div.append_child(WebC__Container)
        await container.wait_for__component_ready()
    })

    hooks.afterEach(() => {
        container.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(container.tagName.toLowerCase()     , 'webc-container'    , 'Has correct tag name'     )
        assert.equal(container.constructor.element_name  , 'webc-container'    , 'Has correct element name' )
        assert.equal(container.constructor.name         , 'WebC__Container'    , 'Has correct class name'   )

        assert.ok(container.shadowRoot                                         , 'Has shadow root'          )
        assert.ok(container instanceof Web_Component                           , 'Extends Web_Component'    )
        assert.ok(container instanceof HTMLElement                             , 'Is HTML Element'          )
    })

    test('applies correct styles', assert => {
        const styles = container.shadowRoot.querySelector('style')
        const style_text = styles.textContent

        assert.ok(style_text.includes('display: flex')                         , 'Sets flex display'      )
        assert.ok(style_text.includes('flex: auto')                           , 'Sets flex auto'         )
        assert.ok(style_text.includes('margin: 10px')                         , 'Sets margin'            )
        assert.ok(style_text.includes('padding: 0px')                         , 'Sets padding'           )
    })

    test('renders slot element', assert => {
        const slot = container.shadowRoot.querySelector('slot')
        assert.ok(slot                                                        , 'Creates slot element'    )
    })

    test('handles slotted content', async assert => {
        // Create and add test content
        const test_div = document.createElement('div')
        test_div.textContent = 'Test Content'
        container.appendChild(test_div)

        // Get computed styles
        const computed = window.getComputedStyle(test_div)

        assert.ok(computed.margin                                            , 'Applies margin to slotted content' )
        assert.equal(computed.display                , 'block'               , 'Displays slotted content'         )
        assert.equal(test_div.textContent           , 'Test Content'        , 'Preserves slotted content'        )
    })
})