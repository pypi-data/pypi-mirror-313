import WebC__Target_Div                            from '../../../js/utils/WebC__Target_Div.mjs'
import Div                                         from '../../../js/core/Div.mjs'
import Web_Component                               from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__Tree_View                 from '../../../js/cbr/file-system/WebC__User_Files__Tree_View.mjs'
import { setup_mock_responses, set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test, only } = QUnit

const MOCK_TREE_DATA = {
    node_id     : 'root',
    node_type   : 'folder',
    name        : 'Root',
    parent_id   : null,
    children    : [
        {
            node_id   : 'folder-1',
            node_type : 'folder',
            name      : 'Folder 1',
            parent_id : 'root',
            children  : [],
            files    : [
                {
                    node_id   : 'file-1',
                    node_type : 'file',
                    name      : 'file1.txt',
                    parent_id : 'folder-1'
                }
            ]
        }
    ],
    files: [
        {
            node_id   : 'root-file',
            node_type : 'file',
            name      : 'root-file.txt',
            parent_id : 'root'
        }
    ]
}

module('WebC__User_Files__Tree_View', hooks => {
    let target_div
    let tree_view

    hooks.before(async (assert) => {
        assert.timeout(10)
        setup_mock_responses()
        set_mock_response('/api/user-data/files/json-view', 'GET', MOCK_TREE_DATA)
        set_mock_response('/api/user-data/files/add-folder', 'POST', { success: true })

        target_div = WebC__Target_Div.add_to_body()
        tree_view = await target_div.append_child(WebC__User_Files__Tree_View)
        await tree_view.wait_for__component_ready()
    })

    hooks.after(() => {
        tree_view.remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(tree_view.tagName.toLowerCase()         , 'webc-user-files-tree-view'    , 'Has correct tag name')
        assert.equal(tree_view.constructor.element_name      , 'webc-user-files-tree-view'    , 'Has correct element name')
        assert.equal(tree_view.constructor.name              , 'WebC__User_Files__Tree_View'  , 'Has correct class name')

        assert.ok(tree_view.shadowRoot                                                        , 'Has shadow root')
        assert.ok(tree_view.api_invoke                                                        , 'Has API__Invoke')
        assert.ok(tree_view instanceof Web_Component                                          , 'Extends Web_Component')
        assert.ok(tree_view instanceof HTMLElement                                            , 'Is HTML Element')
    })

    test('loads and renders tree structure', async assert => {
        const tree_container = tree_view.query_selector('.tree-view')
        const root_item      = tree_view.query_selector('.tree-item[data-id="root"]')
        const folder_1       = tree_view.query_selector('.tree-item[data-id="folder-1"]')
        const file_1         = tree_view.query_selector('.tree-item[data-id="file-1"]')

        assert.ok(tree_container , 'Tree container exists')
        assert.ok(root_item      , 'Root folder rendered')
        assert.ok(folder_1       , 'Subfolder rendered')
        assert.ok(file_1         , 'File rendered')

        const root_text = root_item.querySelector('.tree-item-text')
        assert.equal(root_text.textContent, 'Root' , 'Shows correct root name')
    })

    test ('handles folder click events', async assert => {
        assert.expect(3)
        const done = assert.async(1)

        const folder_1 = tree_view.query_selector('.tree-item[data-id="folder-1"]')
        const folder_content = folder_1.querySelector('.tree-item-content')

        tree_view.addEventListener('folder-selected', event => {
            assert.equal(event.detail.node_id        , 'folder-1'  , 'Event includes correct ID'  )
            assert.equal(event.detail.name           , 'Folder 1'  , 'Event includes correct name')
            assert.ok(folder_content.classList.contains('selected'), 'Folder is selected'         )
            done()
        }, {once: true})

        folder_1.click()
    })

    test('handles file click events', async assert => {
        assert.expect(2)
        const done = assert.async()

        const file_1 = tree_view.query_selector('.tree-item[data-id="file-1"]')

        tree_view.addEventListener('file-selected', event => {
            assert.equal(event.detail.node_id, 'file-1'    , 'Event includes correct ID'  )
            assert.equal(event.detail.name   , 'file1.txt' , 'Event includes correct name')
            done()
        })

        file_1.click()
    })

    test('file click raises folder-selected', async assert => {
        assert.expect(1)
        const file_1 = tree_view.query_selector('.tree-item[data-id="folder-1"]')
        const on_folder_selected = (event) => {
            assert.deepEqual(event.detail, { node_id: 'folder-1', name: 'Folder 1' } )
        }
        tree_view.addEventListener('folder-selected', on_folder_selected, {once: true})
        file_1.click()
    })


    test('handles add folder operation', async assert => {
        set_mock_response('/api/user-data/files/json-view', 'GET', {            // Setup mock API response for refresh
            ...MOCK_TREE_DATA, children: [...MOCK_TREE_DATA.children, { node_id   : 'new-folder',
                                                                        node_type : 'folder'    ,
                                                                        name      : 'New Folder',
                                                                        parent_id : 'root'      ,
                                                                        children  : []          ,
                                                                        files     : []          }]})

        await tree_view.add_folder('root', 'New Folder')
        const new_folder = tree_view.query_selector('.tree-item[data-id="new-folder"]')
        assert.ok(new_folder, 'New folder is rendered')
    })

    test('handles data loading failure gracefully', async assert => {
        set_mock_response('/api/user-data/files/json-view', 'GET', null, 500)

        await tree_view.load_data()

        assert.deepEqual(tree_view.data, {
            node_type: 'folder',
            children: [],
            files: []
        }, 'Uses empty structure on error')
    })

    // todo: fix this test
    test('handles chevron click for folder expansion', async assert => {
        const folder_1 = tree_view.query_selector('.tree-item[data-id="folder-1"]')
        const chevron = folder_1.querySelector('.tree-item-icon')
        const children = folder_1.querySelector('.tree-children')
        const event    = new CustomEvent('click')
        const item     = folder_1

        assert.notOk(children.classList.contains('tree-folder-closed'))                 // before click
        assert.notOk(chevron.classList.contains('tree-item-expanded' ))

        tree_view.handle__on_click__chevron({item, chevron, event})                     // this is the event called byclick

        assert.ok(children.classList.contains('tree-folder-closed'   ))                 // after first click
        assert.ok(chevron.classList.contains('tree-item-expanded'    ))

        tree_view.handle__on_click__chevron({item, chevron, event    })                 // this is the event called byclick

        assert.notOk(children.classList.contains('tree-folder-closed'))                 //after 2nd click
        assert.notOk(chevron.classList.contains('tree-item-expanded' ))
    })

    test('create_tree_item handles null', (assert)=>{
        assert.deepEqual(tree_view.create_tree_item(null), new Div())
        assert.ok(1)
    })
})