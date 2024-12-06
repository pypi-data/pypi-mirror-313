import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__PastChats__Container                 from '../../../js/cbr/web-components/WebC__PastChats__Container.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test , only} = QUnit

const MOCK_CHATS_DATA = {
    saved_chats: {
        'chat1': {
            chat_id         : 'chat1',
            chat_path       : 'chat1-path',
            date           : '2024-03-15',
            time           : '14:30',
            last_user_prompt: 'What is cybersecurity?',
            history_size    : 10,
            prompts_size    : 1024,
            responses_size  : 2048,
            timestamp      : 1647345600000
        },
        'chat2': {
            chat_id         : 'chat2',
            chat_path       : 'chat2-path',
            date           : '2024-03-16',
            time           : '15:45',
            last_user_prompt: 'Tell me about AI',
            history_size    : 5,
            prompts_size    : 512,
            responses_size  : 1536,
            timestamp      : 1647432000000
        }
    }
}

module('WebC__PastChats__Container', hooks => {
    let target_div
    let container

    hooks.before(async () => {
        setup_mock_responses()
        set_mock_response('/api/user-data/chats/chats', 'GET', MOCK_CHATS_DATA)

        target_div = WebC__Target_Div.add_to_body()
        container = await target_div.append_child(WebC__PastChats__Container)
        await container.wait_for__component_ready()
    })

    hooks.after(() => {
        container.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(container.tagName.toLowerCase()      , 'webc-pastchats-container'  , 'Has correct tag name')
        assert.equal(container.constructor.element_name   , 'webc-pastchats-container'  , 'Has correct element name')
        assert.equal(container.constructor.name          , 'WebC__PastChats__Container', 'Has correct class name')
        assert.ok(container.shadowRoot                                                  , 'Has shadow root')
        assert.ok(container.api_invoke                                                  , 'Has API__Invoke')
        assert.ok(container instanceof Web_Component                                    , 'Extends Web_Component')
        assert.ok(container instanceof HTMLElement                                      , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = container.all_css_rules()
        assert.ok(Object.keys(css_rules).length > 0                                    , 'Has CSS rules')
        assert.ok(css_rules['.container']                                              , 'Has container styles')
        assert.ok(css_rules['.table']                                                  , 'Has table styles')
        assert.ok(css_rules['.card']                                                   , 'Has card styles')
    })

    test('sorts chats by timestamp', async assert => {
        const rows = container.query_selector_all('tbody tr')
        const dates = Array.from(rows).map(row => row.cells[0].textContent)

        assert.deepEqual(dates, [
            '2024-03-16 15:45',
            '2024-03-15 14:30'
        ], 'Sorts in descending order')
    })

    test('renders intro card correctly', assert => {
        const card = container.query_selector('.card')
        const title = container.query_selector('.card-title')
        const description = container.query_selector('.card-text')

        assert.ok(card                                                                 , 'Card exists')
        assert.equal(title.textContent            , 'Past Chats'                       , 'Shows correct title')
        assert.ok(description.textContent.includes('View and manage')                  , 'Shows description')
    })

    test('renders chat table correctly', assert => {
        const table = container.query_selector('.table')
        const headers = container.query_selector_all('th')
        const rows = container.query_selector_all('tbody tr')

        assert.ok(table                                                                , 'Table exists')
        assert.equal(headers.length                , 6                                 , 'Has correct number of headers')
        assert.equal(rows.length                   , 2                                 , 'Shows all chats')

        // Check first row content
        const firstRow = rows[0]
        const cells = firstRow.querySelectorAll('td')
        assert.equal(cells[0].textContent         , '2024-03-16 15:45'                , 'Shows correct date/time')
        assert.equal(cells[1].textContent         , 'Tell me about AI'                , 'Shows correct prompt')
        assert.equal(cells[2].textContent         , '5'                               , 'Shows correct history size')
        assert.equal(cells[3].textContent         , '512'                             , 'Shows correct prompts size')
        assert.equal(cells[4].textContent         , '1536'                            , 'Shows correct responses size')

        // Check action links
        const actions = cells[5].querySelectorAll('a')
        assert.equal(actions.length               , 3                                  , 'Has all action links')
        assert.equal(actions[0].textContent       , 'view'                            , 'Has view link')
        assert.equal(actions[1].textContent       , 'pdf'                             , 'Has pdf link')
        assert.equal(actions[2].textContent       , 'image'                           , 'Has image link')
    })

    test('handles empty chat data', async assert => {
        set_mock_response('/api/user-data/chats/chats', 'GET', { saved_chats: {} })

        container = await target_div.append_child(WebC__PastChats__Container)
        await container.wait_for__component_ready()

        const rows = container.query_selector_all('tbody tr')
        const cell = container.query_selector('td[colspan="6"]')

        assert.equal(rows.length                  , 1                                 , 'Shows one row')
        assert.equal(cell.textContent            , 'No saved chats found'             , 'Shows empty message')
    })

    test('handles failed data fetch', async assert => {
        set_mock_response('/api/user-data/chats/chats', 'GET', null)

        container = await target_div.append_child(WebC__PastChats__Container)
        await container.wait_for__component_ready()

        const rows = container.query_selector_all('tbody tr')
        assert.equal(rows.length                  , 1                                  , 'Shows one row')
        assert.ok(container.chats                                                      , 'Initializes empty chats array')
    })

    test('formats date and time correctly', assert => {
        assert.equal(container.format_date_time('2024-03-15', '14:30'), '2024-03-15 14:30', 'Formats valid date/time')
        assert.equal(container.format_date_time(null, '14:30')        , '-'                , 'Handles missing date')
        assert.equal(container.format_date_time('2024-03-15', null)   , '-'                , 'Handles missing time')
        assert.equal(container.format_date_time(null, null)           , '-'                , 'Handles all missing')
    })

    test('creates correct action links', assert => {
        const chat = MOCK_CHATS_DATA.saved_chats.chat1
        const linkDiv = container.create_action_links(chat).dom_create()
        const links = linkDiv.querySelectorAll('a')

        assert.equal(links.length                 , 3                                  , 'Creates all links')
        assert.ok(links[0].href.endsWith('/web/chat/view/chat1-path')                , 'Correct view URL')
        assert.ok(links[1].href.endsWith('/web/chat/view/chat1-path/pdf')            , 'Correct PDF URL')
        assert.ok(links[2].href.endsWith('/web/chat/view/chat1-path/image')          , 'Correct image URL')

        assert.deepEqual(container.create_action_links({}).html(), "<div>\n</div>\n")
    })

    test('handles invalid saved_chats data', async assert => {
        // Test various invalid saved_chats scenarios
        const invalid_responses = [
            { saved_chats: null },              // null saved_chats
            { saved_chats: undefined },         // undefined saved_chats
            {},                                 // missing saved_chats property
            { saved_chats: 'invalid string' },  // wrong type
            { saved_chats: [] }                 // array instead of object
        ]

        for (const invalid_response of invalid_responses) {
            set_mock_response('/api/user-data/chats/chats', 'GET', invalid_response)

            container = await target_div.append_child(WebC__PastChats__Container)
            await container.wait_for__component_ready()

            assert.equal(container.chats.length, 0,
                `Handles invalid saved_chats: ${JSON.stringify(invalid_response)}`)

            const rows = container.query_selector_all('tbody tr')
            const cell = container.query_selector('td[colspan="6"]')

            assert.equal(rows.length, 1, 'Shows single row for empty state')
            assert.equal(cell.textContent, 'No saved chats found',
                'Shows empty message for invalid data')

            container.remove()
        }
    })
})