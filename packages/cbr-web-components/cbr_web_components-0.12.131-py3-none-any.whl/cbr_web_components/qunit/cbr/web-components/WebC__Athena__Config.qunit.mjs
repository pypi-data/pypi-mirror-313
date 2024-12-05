import WebC__Target_Div     from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component        from '../../../js/core/Web_Component.mjs'
import WebC__Athena__Config from '../../../js/cbr/web-components/WebC__Athena__Config.mjs'

const { module, test , only} = QUnit

module('WebC__Athena__Config', hooks => {
    let target_div
    let config
    let original_get_item
    let original_set_item
    let storage_mock

    hooks.before(async () => {
        // Save original localStorage methods
        original_get_item = window.localStorage.getItem
        original_set_item = window.localStorage.setItem

        // Setup storage mock that doesn't affect real localStorage
        storage_mock = {
            data: {},
            getItem: function(key) { return this.data[key] || null },
            setItem: function(key, value) { this.data[key] = value }
        }

        // Patch only the specific localStorage methods we need
        window.localStorage.getItem = (key) => storage_mock.getItem(key)
        window.localStorage.setItem = (key, value) => storage_mock.setItem(key, value)

        target_div = WebC__Target_Div.add_to_body()
        config = await target_div.append_child(WebC__Athena__Config, { channel: 'test-channel' })
        await config.wait_for__component_ready()
    })

    hooks.after(() => {
        // Restore original localStorage methods
        window.localStorage.getItem = original_get_item
        window.localStorage.setItem = original_set_item

        config.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        // Test component registration and naming
        assert.equal(config.tagName.toLowerCase()        , 'webc-athena-config'    , 'Has correct tag name')
        assert.equal(config.constructor.element_name     , 'webc-athena-config'    , 'Has correct element name')
        assert.equal(config.constructor.name             , 'WebC__Athena__Config'  , 'Has correct class name')

        // Test shadow DOM
        assert.ok(config.shadowRoot                                                , 'Has shadow root')

        // Test inheritance
        assert.ok(config instanceof Web_Component                                  , 'Extends Web_Component')
        assert.ok(config instanceof HTMLElement                                    , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = config.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                               , 'Has CSS rules')
        assert.ok(css_rules['.card']                                              , 'Has card styles')
        assert.ok(css_rules['.card-body']                                         , 'Has card body styles')
    })

    test('renders configuration options correctly', assert => {
        // Test DOM structure
        const card = config.query_selector('.card')
        const body = config.query_selector('.card-body')
        const title = config.query_selector('.card-title')
        const form = config.query_selector('.form-group')

        assert.ok(card                                                            , 'Card exists')
        assert.ok(body                                                            , 'Card body exists')
        assert.ok(title                                                           , 'Title exists')
        assert.ok(form                                                            , 'Form exists')

        // Test toggle elements
        const systemPromptToggle = config.query_selector('#system-prompt-toggle')
        const editModeToggle     = config.query_selector('#edit-mode-toggle')

        assert.ok(systemPromptToggle                                              , 'System prompt toggle exists')
        assert.ok(editModeToggle                                                  , 'Edit mode toggle exists')
        assert.equal(title.textContent                  , 'Configuration'         , 'Shows correct title')
    })

    test('handles storage state correctly', assert => {
        // Test initial state
        assert.equal(config.show_system_prompt          , false                   , 'Default system prompt is false')
        assert.equal(config.edit_mode                   , false                   , 'Default edit mode is false')

        // Set values in mock storage
        storage_mock.setItem('athena_show_system_prompt', 'true')
        storage_mock.setItem('athena_edit_mode'         , 'true')

        // Create new instance to test storage loading
        const newConfig = WebC__Athena__Config.create()
        newConfig.load_attributes()

        assert.equal(newConfig.show_system_prompt       , true                    , 'Loads system prompt from storage')
        assert.equal(newConfig.edit_mode                , true                    , 'Loads edit mode from storage')

        assert.equal(config.show_system_prompt          , false                   , 'Default system prompt is still false')
        assert.equal(config.edit_mode                   , false                   , 'Default edit mode is still false')

        config.load_attributes()                                                 // now reload the attributes in config
        assert.equal(config.show_system_prompt          , true                   , 'Default system prompt is now true')
        assert.equal(config.edit_mode                   , true                   , 'Default edit mode is now true')

        // Set values in mock storage
        storage_mock.setItem('athena_show_system_prompt', 'false')              // now set to False
        storage_mock.setItem('athena_edit_mode'         , 'false')

        newConfig.load_attributes()                                              // reload the data
        config   .load_attributes()
        assert.equal(newConfig.show_system_prompt       , false                    , 'Loads system prompt from storage')
        assert.equal(newConfig.edit_mode                , false                    , 'Loads edit mode from storage')
        assert.equal(config.show_system_prompt          , false                    , 'Default system prompt is now true')
        assert.equal(config.edit_mode                   , false                    , 'Default edit mode is now true')
    })

    test('dispatches config update events', assert => {
        assert.expect(3)                                                                                                // Expecting 3 assertions

        function assert__config_update(event) {
            assert.equal(event.detail.channel                  , 'test-channel'   , 'Event includes channel'      )
            assert.equal(typeof event.detail.show_system_prompt, 'boolean'        , 'Event includes system prompt')
            assert.equal(typeof event.detail.edit_mode         , 'boolean'        , 'Event includes edit mode'    )

            config.removeEventListener('config-update', assert__config_update);
        }

        config.addEventListener('config-update',assert__config_update   )                                               // Setup event listener


        const systemPromptToggle   = config.query_selector('#system-prompt-toggle')                                     // Trigger config update
        systemPromptToggle.checked = true
        systemPromptToggle.dispatchEvent(new Event('change'))
    })

    test('handles toggle interactions', async assert => {                                // Test system prompt toggle
        storage_mock.setItem('athena_show_system_prompt', null)                 // reset values
        storage_mock.setItem('athena_edit_mode'         , null)
        assert.equal(storage_mock.getItem('athena_show_system_prompt'), null    , 'Before event, athena_show_system_prompt should be null')

        const systemPromptToggle = config.query_selector('#system-prompt-toggle')
        systemPromptToggle.checked = true
        systemPromptToggle.dispatchEvent(new Event('change'))

        assert.equal(storage_mock.getItem('athena_show_system_prompt'), true    , 'Updates system prompt in storage')

        assert.equal(storage_mock.getItem('athena_edit_mode'         ), null    )        // Test edit mode toggle

        const editModeToggle = config.query_selector('#edit-mode-toggle')
        editModeToggle.checked = true
        editModeToggle.dispatchEvent(new Event('change'))

        assert.equal(storage_mock.getItem('athena_edit_mode'), true             , 'Updates edit mode in storage')
    })

    test('preserves other localStorage values', assert => {
        const test_key   = 'test_preservation_key'                                                                                  // Set a test value in real localStorage
        const test_value = 'test_value'
        original_set_item.call(window.localStorage, test_key, test_value)

        const systemPromptToggle   = config.query_selector('#system-prompt-toggle')                                                 // Run through a normal test operation
        systemPromptToggle.checked = true
        systemPromptToggle.dispatchEvent(new Event('change'))

        assert.equal(original_get_item.call(window.localStorage, test_key), test_value, 'Preserves existing localStorage values')   // Verify the test value is still intact

        window.localStorage.removeItem(test_key)                                                                                    // Cleanup
    })

    test('html() creates correct DOM structure and elements', assert => {
        // Create component instance with controlled state
        const config = WebC__Athena__Config.create()
        config.show_system_prompt = true
        config.edit_mode = false

        // Get rendered element
        const card = config.html()
        const dom = card.dom_create()

        // Test card structure
        assert.equal(dom.tagName                    , 'DIV'                         , 'Root is a div element')
        assert.ok   (dom.classList.contains('card')                                 , 'Has card class')
        assert.ok   (dom.classList.contains('m-1')                                  , 'Has margin class')
        assert.ok   (dom.classList.contains('bg-light-cyan')                        , 'Has background class')

        // Test card body
        const body = dom.querySelector('.card-body')
        assert.ok   (body                                                           , 'Has card body')

        // Test title
        const title = body.querySelector('.card-title')
        assert.ok   (title                                                          , 'Has title element')
        assert.equal(title.tagName                  , 'H3'                          , 'Title is h3')
        assert.equal(title.textContent              , 'Configuration'               , 'Has correct title text')

        // Test form structure
        const form = body.querySelector('.form-group')
        assert.ok   (form                                                           , 'Has form group')

        // Test system prompt toggle
        const systemToggleContainer = form.querySelector('.mb-3')
        assert.ok   (systemToggleContainer                                          , 'Has toggle container')

        const systemToggleSwitch = systemToggleContainer.querySelector('.form-check.form-switch')
        assert.ok   (systemToggleSwitch                                            , 'Has switch element')

        const systemToggleInput = systemToggleSwitch.querySelector('input[type="checkbox"]')
        assert.ok   (systemToggleInput                                             , 'Has checkbox input')
        assert.equal(systemToggleInput.id           , 'system-prompt-toggle'        , 'Has correct input id')
        assert.ok   (systemToggleInput.checked                                     , 'Checkbox reflects true state')

        const systemToggleLabel = systemToggleSwitch.querySelector('label')
        assert.ok   (systemToggleLabel                                              , 'Has label element')
        assert.equal(systemToggleLabel.getAttribute('for'), 'system-prompt-toggle'  , 'Label is connected to input')
        assert.equal(systemToggleLabel.textContent.trim()   , 'Show System Prompt'  , 'Has correct label text')

        // Test edit mode toggle
        const editToggleContainer = form.querySelectorAll('.mb-3')[1]
        assert.ok   (editToggleContainer                                           , 'Has second toggle container')

        const editToggleSwitch = editToggleContainer.querySelector('.form-check.form-switch')
        assert.ok   (editToggleSwitch                                             , 'Has second switch element')

        const editToggleInput = editToggleSwitch.querySelector('input[type="checkbox"]')
        assert.ok   (editToggleInput                                              , 'Has second checkbox input')
        assert.equal(editToggleInput.id            , 'edit-mode-toggle'            , 'Has correct second input id')
        assert.notOk(editToggleInput.checked                                      , 'Checkbox reflects false state')

        const editToggleLabel = editToggleSwitch.querySelector('label')
        assert.ok   (editToggleLabel                                              , 'Has second label element')
        assert.equal(editToggleLabel.getAttribute('for'), 'edit-mode-toggle'       , 'Second label is connected to input')
        assert.equal(editToggleLabel.textContent.trim() , 'Edit Mode'                  , 'Has correct second label text')
    })

    test('html() handles state changes correctly', assert => {
        const config = WebC__Athena__Config.create()

        // Test initial state
        let card = config.html()
        let dom = card.dom_create()

        let systemToggle = dom.querySelector('#system-prompt-toggle')
        let editToggle   = dom.querySelector('#edit-mode-toggle')


        assert.notOk(systemToggle.checked                                          , 'System prompt initially unchecked')
        assert.notOk(editToggle.checked                                            , 'Edit mode initially unchecked')

        // Test with both toggles enabled
        config.show_system_prompt = true
        config.edit_mode          = true

        card = config.html()
        dom = card.dom_create()

        systemToggle = dom.querySelector('#system-prompt-toggle')
        editToggle = dom.querySelector('#edit-mode-toggle')

        assert.ok(systemToggle.checked                                            , 'System prompt becomes checked')
        assert.ok(editToggle.checked                                             , 'Edit mode becomes checked')

        // Test with mixed states
        config.show_system_prompt = false
        config.edit_mode = true

        card = config.html()
        dom = card.dom_create()

        systemToggle = dom.querySelector('#system-prompt-toggle')
        editToggle = dom.querySelector('#edit-mode-toggle')

        assert.notOk(systemToggle.checked                                        , 'System prompt becomes unchecked')
        assert.ok   (editToggle.checked                                         , 'Edit mode stays checked')
    })
})