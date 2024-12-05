import WebC__Target_Div      from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component         from '../../../js/core/Web_Component.mjs'
import WebC__Document__Diff  from '../../../js/cbr/document-assistant/WebC__Document__Diff.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test , only} = QUnit

const MOCK_FILE_ID = 'test-file-123'
const MOCK_CHANGES = {
    document: {
        new_version: '# Updated Content',
        changes: [
            {
                type: 'addition',
                original: '',
                updated: 'New section content',
                reason: 'Added new section'
            },
            {
                type: 'modification',
                original: 'Old content',
                updated: 'Modified content',
                reason: 'Improved clarity'
            }
        ]
    }
}

module('WebC__Document__Diff', hooks => {
    let target_div
    let diff_view

    hooks.before(async (assert) => {
        assert.timeout(10)
        setup_mock_responses()
        target_div = WebC__Target_Div.add_to_body()
        diff_view = await target_div.append_child(WebC__Document__Diff, { 'file-id': MOCK_FILE_ID })
        await diff_view.wait_for__component_ready()
    })

    hooks.after(() => {
        diff_view.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(diff_view.tagName.toLowerCase()        , 'webc-document-diff'      , 'Has correct tag name')
        assert.equal(diff_view.constructor.element_name     , 'webc-document-diff'      , 'Has correct element name')
        assert.equal(diff_view.constructor.name             , 'WebC__Document__Diff'    , 'Has correct class name')
        assert.equal(diff_view.file_id                      , MOCK_FILE_ID              , 'Sets file ID')
        assert.equal(diff_view.view_mode                    , 'split'                   , 'Default view mode')

        assert.ok(diff_view.shadowRoot                                                  , 'Has shadow root')
        assert.ok(diff_view.api_invoke                                                  , 'Has API__Invoke')
        assert.ok(diff_view instanceof Web_Component                                    , 'Extends Web_Component')
        assert.ok(diff_view instanceof HTMLElement                                      , 'Is HTML Element')
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = diff_view.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                                    , 'Has CSS rules')
        assert.ok(css_rules['.diff-container']                                         , 'Has container styles')
        assert.ok(css_rules['.diff-header']                                            , 'Has header styles')
        assert.ok(css_rules['.diff-content']                                           , 'Has content styles')
        assert.ok(css_rules['.diff-line']                                              , 'Has line styles')
    })

    test('renders initial state correctly', assert => {
        const container = diff_view.query_selector('.diff-container')
        assert.ok(container                                                            , 'Container exists')

        const header = diff_view.query_selector('.diff-header')
        assert.ok(header                                                               , 'Header exists')
        assert.ok(header.textContent.includes('Proposed Changes')                      , 'Shows title')

        const content = diff_view.query_selector('.diff-content')
        assert.ok(content                                                              , 'Content exists')
        assert.ok(content.textContent.includes('No changes')                           , 'Shows placeholder')
    })

    test('updates diff view with changes', async assert => {
        diff_view.update_diff(MOCK_CHANGES)

        const changes = diff_view.query_selector_all('.change-block')
        assert.equal(changes.length                      , 2                           , 'Shows all changes')

        const first_change = changes[0]
        assert.ok(first_change.textContent.includes('ADDITION')                        , 'Shows change type')
        assert.ok(first_change.textContent.includes('Added new section')               , 'Shows change reason')
        assert.ok(first_change.querySelector('.content-original')                      , 'Shows original content')
        assert.ok(first_change.querySelector('.content-updated')                       , 'Shows updated content')
    })

    test('toggles view mode', assert => {
        diff_view.update_diff(MOCK_CHANGES)

        assert.equal(diff_view.view_mode               , 'split'                       , 'Initial split view')

        diff_view.toggle_view_mode()
        assert.equal(diff_view.view_mode               , 'unified'                     , 'Toggles to unified')
        assert.ok(diff_view.query_selector('.content-unified')                         , 'Shows unified view')

        diff_view.toggle_view_mode()
        assert.equal(diff_view.view_mode               , 'split'                       , 'Toggles back to split')
        assert.ok(diff_view.query_selector('.content-original')                        , 'Shows split view')
    })

    test('handles change acceptance', async assert => {
        assert.expect(2)

        window.addEventListener('changes:accept', event => {
            assert.equal(event.detail.new_version     , MOCK_CHANGES.document.new_version, 'Correct version')
            assert.deepEqual(event.detail.changes     , MOCK_CHANGES.document.changes    , 'Correct changes')
        }, { once: true })

        await diff_view.update_diff(MOCK_CHANGES)
        const accept_btn = diff_view.query_selector('.btn-success')
        accept_btn.click()

    })

    test('handles change rejection', assert => {
        assert.expect(1)
        const done = assert.async()

        window.addEventListener('changes:reject', () => {
            assert.ok(true                                                             , 'Rejects changes')
            done()
        }, { once: true })

        const reject_btn = diff_view.query_selector('.btn-danger')
        reject_btn.click()
    })

    test('handles diff hiding', assert => {
        assert.expect(1)
        const done = assert.async()

        window.addEventListener('diff:hide', () => {
            assert.ok(true                                                             , 'Hides diff view')
            done()
        }, { once: true })

        const close_btn = diff_view.query_selector('.btn-secondary:last-child')
        close_btn.click()
    })

    test('highlights diff lines correctly', assert => {
        const added = diff_view.highlight_diff_lines('test line', 'added')
        assert.ok(added.includes('diff-added')                                         , 'Adds added class')
        assert.ok(added.includes('+ test line')                                        , 'Adds plus marker')

        const removed = diff_view.highlight_diff_lines('test line', 'removed')
        assert.ok(removed.includes('diff-removed')                                     , 'Adds removed class')
        assert.ok(removed.includes('- test line')                                      , 'Adds minus marker')
    })

    test('creates unified diff correctly', assert => {
        const unified = diff_view.create_unified_diff('old\ntext', 'new\ntext')
        assert.ok(unified.includes('diff-removed')                                     , 'Shows removed lines')
        assert.ok(unified.includes('diff-added')                                       , 'Shows added lines')
        assert.ok(unified.includes('- old')                                           , 'Shows old content')
        assert.ok(unified.includes('+ new')                                           , 'Shows new content')
    })

    test('handle__on_update_diff_view only updates when file_id matches', async assert => {
        assert.expect(2)                                                                   // Test two scenarios

        // Setup tracking
        let update_called = false
        const original_update_diff = diff_view.update_diff
        diff_view.update_diff = () => { update_called = true }

        // Test with non-matching file_id
        diff_view.handle__on_update_diff_view({ detail: { file_id: 'different-id',  changes: MOCK_CHANGES }})
        assert.notOk(update_called                                 , 'Ignores non-matching file_id')

        // Test with matching file_id
        diff_view.handle__on_update_diff_view({detail: { file_id: MOCK_FILE_ID,  changes: MOCK_CHANGES }})
        assert.ok(update_called                                    , 'Updates on matching file_id')
        diff_view.update_diff = original_update_diff
    })

    test('update_diff handles null/undefined result', async assert => {
        assert.expect(4)
        diff_view.changes     = null
        diff_view.new_version = null

        // Test with undefined
        await diff_view.update_diff(undefined)
        assert.equal(diff_view.changes     , null                  , 'No changes set for undefined')
        assert.equal(diff_view.new_version , null                  , 'No version set for undefined')

        // Test with null
        await diff_view.update_diff(null)
        assert.equal(diff_view.changes     , null                  , 'No changes set for null')
        assert.equal(diff_view.new_version , null                  , 'No version set for null')
    })

    test('update_diff handles missing document property', async assert => {
        assert.expect(2)

        await diff_view.update_diff({ some: 'data' })             // Object without document property

        assert.equal(diff_view.changes     , null                  , 'No changes set for invalid data')
        assert.equal(diff_view.new_version , null                  , 'No version set for invalid data')
    })

    test('handle__on_update_diff_view integration', async assert => {
        assert.expect(3)

        const event = new CustomEvent('update-diff-view', {
            detail: {
                file_id: MOCK_FILE_ID,
                changes: MOCK_CHANGES
            }
        })

        await diff_view.handle__on_update_diff_view(event)

        assert.ok(diff_view.changes                               , 'Changes were updated')
        assert.equal(diff_view.changes.length , 2                  , 'Correct number of changes')
        assert.equal(diff_view.view_mode      , 'split'            , 'View mode preserved')
    })

    test('accept_changes handles no changes state', async assert => {
        assert.expect(2)                                                                   // Test both empty state and event

        const events_raised = []                                                          // Track raised events
        diff_view.raise_event_global = (event_name) => events_raised.push(event_name)

        diff_view.changes = null                                                          // Ensure no changes exist
        await diff_view.accept_changes()                                                  // Call accept with no changes

        assert.equal(events_raised.length     , 0                                         , 'No events raised when no changes')

        diff_view.update_diff(MOCK_CHANGES)                                               // Add changes and try again
        await diff_view.accept_changes()
        assert.deepEqual(events_raised        , ['changes:accept', 'diff:hide']           , 'Both events raised with changes')
    })
})