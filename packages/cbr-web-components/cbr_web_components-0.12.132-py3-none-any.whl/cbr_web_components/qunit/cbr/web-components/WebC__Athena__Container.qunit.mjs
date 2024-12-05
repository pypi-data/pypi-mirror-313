import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__Athena__Container                     from '../../../js/cbr/web-components/WebC__Athena__Container.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test, only } = QUnit

const MOCK_USER_DATA = {
    name           : 'Test User',
    expertise_level: 'intermediate',
    interests      : ['security', 'ai'],
    preferences    : { theme: 'light', language: 'en' }
}

const MOCK_ATHENA_PROMPT = "You are Athena, an AI assistant focused on cybersecurity."

module('WebC__Athena__Container', hooks => {
    let target_div
    let container
    let original_local_storage_getItem
    let original_local_storage_setItem
    let storage_mock

    hooks.before(async () => {
        // Setup API mocks
        setup_mock_responses()
        set_mock_response('/api/user-data/user/user-profile', 'GET', MOCK_USER_DATA)
        set_mock_response(
            '/markdown/static_content/content-file?path=en/site/athena/athena-prompt.md',
            'GET',
            MOCK_ATHENA_PROMPT
        )

        // Setup localStorage mock
        storage_mock = {
            data: {},
            getItem: function(key) { return this.data[key] || null },
            setItem: function(key, value) { this.data[key] = value }
        }

        original_local_storage_getItem = window.localStorage.getItem
        original_local_storage_setItem = window.localStorage.setItem

        window.localStorage.getItem = (key) => storage_mock.getItem(key)
        window.localStorage.setItem = (key, value) => storage_mock.setItem(key, value)

        // Create component
        target_div = WebC__Target_Div.add_to_body()
        container = await target_div.append_child(WebC__Athena__Container)
        await container.wait_for__component_ready()
    })

    hooks.after(() => {
        // Restore localStorage
        window.localStorage.getItem = original_local_storage_getItem
        window.localStorage.setItem = original_local_storage_setItem

        container.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(container.tagName.toLowerCase()      , 'webc-athena-container' , 'Has correct tag name')
        assert.equal(container.constructor.element_name   , 'webc-athena-container' , 'Has correct element name')
        assert.equal(container.constructor.name          , 'WebC__Athena__Container', 'Has correct class name')

        assert.ok(container.shadowRoot                                             , 'Has shadow root')
        assert.ok(container.api_invoke                                             , 'Has API__Invoke')
        assert.ok(container.channel.startsWith('athena_')                         , 'Has generated channel')

        assert.ok(container instanceof Web_Component                               , 'Extends Web_Component')
        assert.ok(container instanceof HTMLElement                                 , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = container.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                               , 'Has CSS rules')
        assert.ok(css_rules['.h-100pc']                                          , 'Has height utility')
        assert.ok(css_rules['.d-flex']                                           , 'Has flex utility')
        assert.ok(css_rules['.flex-column']                                      , 'Has flex direction utility')
    })

    test('renders layout structure correctly', async assert => {
        const page = container.query_selector('#athena-page')
        assert.ok(page                                                            , 'Main container exists')
        assert.ok(page.classList.contains('h-100pc')                             , 'Has height class')
        assert.ok(page.classList.contains('d-flex')                              , 'Has flex class')

        // Banner row
        const banner_row = container.query_selector('#athena-row')
        assert.ok(banner_row                                                      , 'Banner row exists')
        assert.ok(banner_row.classList.contains('m-1')                           , 'Has margin class')

        // Content sections
        assert.ok(container.query_selector('#athena-banner')                     , 'Banner section exists')
        assert.ok(container.query_selector('#athena-welcome')                    , 'Welcome section exists')
        assert.ok(container.query_selector('#athena-chatbot')                    , 'Chat section exists')
        assert.ok(container.query_selector('#athena-examples')                   , 'Examples section exists')
        assert.ok(container.query_selector('#athena-config')                     , 'Config section exists')
    })

    test('loads configuration from localStorage', async assert => {
        // Test default values
        assert.equal(container.show_system_prompt, false                          , 'Default system prompt is false')
        assert.equal(container.edit_mode, false                                   , 'Default edit mode is false')

        // Set values in mock storage
        storage_mock.setItem('athena_show_system_prompt', 'true')
        storage_mock.setItem('athena_edit_mode', 'true')

        // Create new instance to test storage loading
        const new_container = WebC__Athena__Container.create()
        new_container.load_attributes()

        assert.equal(new_container.show_system_prompt, true                       , 'Loads system prompt from storage')
        assert.equal(new_container.edit_mode, true                                , 'Loads edit mode from storage')
    })

    test('builds system prompt correctly', async assert => {
        const system_prompt = await container.build_system_prompt()

        assert.ok(system_prompt.includes(MOCK_ATHENA_PROMPT)                     , 'Includes Athena prompt')
        assert.ok(system_prompt.includes('Test User')                            , 'Includes user data')
        assert.ok(system_prompt.includes('intermediate')                         , 'Includes expertise level')
    })

    test('handles config updates', async assert => {
        const event = new CustomEvent('config-update', {
            detail: {
                channel: container.channel,
                show_system_prompt: true,
                edit_mode: true
            }
        })

        window.dispatchEvent(event)

        assert.equal(container.show_system_prompt, true                           , 'Updates system prompt setting')
        assert.equal(container.edit_mode, true                                    , 'Updates edit mode setting')
    })

    test('handles missing user data gracefully', async assert => {
        set_mock_response('/api/user-data/user/user-profile', 'GET', null)

        const formatted_data = container.format_user_data(null)
        assert.equal(formatted_data, ''                                           , 'Returns empty string for null data')
    })

    test('formats user data correctly', assert => {
        const test_data = {
            name: 'Test User',
            role: 'Developer'
        }

        const formatted = container.format_user_data(test_data)

        assert.ok(formatted.includes('name')                                      , 'Includes field name')
        assert.ok(formatted.includes('Test User')                                 , 'Includes field value')
        assert.ok(formatted.includes('role')                                      , 'Includes second field name')
        assert.ok(formatted.includes('Developer')                                 , 'Includes second field value')
    })

    test('handles API errors gracefully', async assert => {
        set_mock_response('/api/user-data/user/user-profile', 'GET', null)
        set_mock_response(
            '/markdown/static_content/content-file?path=en/site/athena/athena-prompt.md',
            'GET',
            null
        )

        const user_data = await container.fetch_user_data()
        assert.equal(user_data, null                                              , 'Returns null on user data error')

        const athena_prompt = await container.fetch_athena_prompt()
        assert.equal(athena_prompt, ''                                            , 'Returns empty string on prompt error')
    })
})