import Web_Component    from '../../core/Web_Component.mjs'
import CSS__Icons       from '../../css/icons/CSS__Icons.mjs'
import CSS__Forms       from '../../css/CSS__Forms.mjs'
import Icon             from '../../css/icons/Icon.mjs'
import API__Invoke      from '../../data/API__Invoke.mjs'
import Div              from '../../core/Div.mjs'

export default class WebC__User_Files__Tree_View extends Web_Component {

    constructor() {
        super()
        this.api_invoke = new API__Invoke()
        this.data      = null
    }
    async apply_css() {
        new CSS__Icons    (this).apply_framework()
        new CSS__Forms    (this).apply_framework()
        this.add_css_rules (this.css_rules()                )
    }

    add_event_listeners() {
        this.add_window_event_listener('file-selected'  , this.handle__event__on_selection)                                  // Selection events from document
        this.add_window_event_listener('folder-selected', this.handle__event__on_selection)
    }

    add_event_handlers() {
        // Chevron clicks
        this.query_selector_all('.tree-item').forEach(item => {
            const chevron = item.querySelector('.tree-item-icon')
            if (chevron && !chevron.classList.contains('hidden')) {
                this.add_event__to_element__on('click', chevron, this.handle__on_click__chevron, { item, chevron })}
        })

        // Folder clicks
        this.query_selector_all('.tree-item[data-type="folder"]').forEach(item => {
            this.add_event__to_element__on('click', item, this.handle__on_click__folder, { item })})

        // File clicks
        this.query_selector_all('.tree-item[data-type="file"]').forEach(item => {
            this.add_event__to_element__on('click', item,this.handle__on_click__file, { item })
        })

    }

    async load_data() {
        try {
            this.data = await this.api_invoke.invoke_api('/api/user-data/files/json-view')
        } catch (error) {
            //console.error('Error loading file structure:', error)
            this.data = { node_type: 'folder', children: [], files: [] }
        }
    }

    async add_folder(parentId, folderName) {
        try {
            await this.api_invoke.invoke_api('/api/user-data/files/add-folder', 'POST', {
                folder_name      : folderName,
                parent_folder_id : parentId
            })
            await this.refresh()
        } catch (error) {
            //console.error('Error adding folder:', error)
        }
    }

    async refresh() {
        await this.load_data()
        this.render()
    }


    create_tree_item(node, level = 0) {
        if (node === null) { return new Div() }

        const item_div = new Div({ class: 'tree-item', attributes: {
            'data-id': node.node_id,
            'data-type': node.node_type,
            'data-level': level
        }})
        const content  = new Div({ class: `tree-item-content level-${level}` })  // Add level class

        let is_root  = node.parent_id === null
        let expand = is_root || true                                            // expand by default

        if (node.node_type === 'folder') {

            const chevron  = new Icon({ icon: 'chevron-right', class: `tree-item-icon ${node.children?.length ? '' : 'hidden'} ${is_root ? 'tree-item-expanded' : ''}`})
            const folder   = new Icon({ icon: 'folder'       , class: 'tree-item-icon folder-icon'})
            content.add_elements(chevron, folder)

            //const children = new Div({class: `tree-children ${expand ? '' : 'tree-folder-closed'}`, id: `folder-${node.node_id}`})
            const children = new Div({class: `tree-children`, id: `folder-${node.node_id}`})

            node.children?.forEach(child => children.add_element(this.create_tree_item(child, level + 1)))
            node.files   ?.forEach(file  => children.add_element(this.create_tree_item(file, level + 1)))

            item_div.add_elements(content, children)
        } else {
            const file_icon = new Icon({ icon: 'file', class: 'tree-item-icon file-icon' })
            content.add_element(file_icon)
            item_div.add_element(content)
        }

        const text    = new Div({ class: 'tree-item-text', value: node.name })
        const actions = new Div({ class: 'tree-item-actions' })

        content.add_elements(text, actions)
        return item_div
    }

    handle__event__on_selection = (event) => {
        this.handle_selection(event.detail.node_id)
    }

    handle__on_click__chevron({item, chevron, event}) {
        event.stopPropagation();
        const children = item.querySelector('.tree-children');
        children.classList.toggle('tree-folder-closed');
        chevron.classList.toggle('tree-item-expanded');
    }

    handle__on_click__file({item, event}) {
        event.stopPropagation();
        const custom_event = new CustomEvent('file-selected', { detail: { node_id: item.dataset.id,
                                                                          name: item.querySelector('.tree-item-text').textContent },
                                                                          bubbles: true    ,
                                                                          composed: true   })
        this.dispatchEvent(custom_event)
    }

    handle__on_click__folder = ({item, event}) =>{
        event.stopPropagation()

        this.shadowRoot.querySelectorAll('.tree-item-content.selected').forEach(i => {          // Remove previous selections
            i.classList.remove('selected')
        })

        item.querySelector('.tree-item-content').classList.add('selected')

        // Dispatch selection event
        const custom_event = new CustomEvent('folder-selected', {detail  : {node_id : item.dataset.id,
                                                                            name    : item.querySelector('.tree-item-text').textContent },
                                                                            bubbles : true,
                                                                            composed: true })
        this.dispatchEvent(custom_event)
    }

    handle_selection(node_id) {
        this.shadowRoot.querySelectorAll('.tree-item-content.selected').forEach(item => {                       // Remove all current selections
            item.classList.remove('selected')
        })

        const selected_item = this.shadowRoot.querySelector(`.tree-item[data-id="${node_id}"] .tree-item-content`)      // Add selected class to the matching item
        if (selected_item) {
            selected_item.classList.add('selected')
        }
    }





    html() {
        const tree = new Div({ class: 'tree-view' })
        tree.add_element   (this.create_tree_item(this.data))
        return tree
    }

    css_rules() {
        return {
            // Base tree structure
            ".tree-view"                         : { display          : "flex"                                    ,
                                                    flexDirection    : "column"                                  ,
                                                    padding          : "1rem"                                    ,
                                                    margin           : "1rem"                                    ,
                                                    borderRadius     : "0.375rem"                                ,
                                                    boxShadow        : "2px 2px 4px rgba(0,0,0,0.2)"            ,
                                                    backgroundColor  : "#fff"                                    },

            // Tree items
            ".tree-item"                         : { alignItems       : "center"                                  ,
                                                    padding          : "0.25rem"                                 ,
                                                    cursor           : "pointer"                                 ,
                                                    position         : "relative"                                },

            ".tree-item:hover"                   : { backgroundColor  : "var(--table-hover-bg, rgba(0,0,0,0.04))" },

            // Item content structure
            ".tree-item-content"                 : { display          : "flex"                                    ,
                                                    alignItems       : "center"                                  ,
                                                    gap              : "0.5rem"                                  ,
                                                    padding          : "0.5rem"                                  ,
                                                    borderRadius     : "0.375rem"                                ,
                                                    transition       : "background-color 0.2s ease"              },

            // Level-based indentation
            ".tree-item-content.level-1"         : { paddingLeft      : "1.0rem"                                  },
            ".tree-item-content.level-2"         : { paddingLeft      : "2.0rem"                                  },
            ".tree-item-content.level-3"         : { paddingLeft      : "3.0rem"                                  },
            ".tree-item-content.level-4"         : { paddingLeft      : "4.0rem"                                  },
            ".tree-item-content.level-5"         : { paddingLeft      : "5.0rem"                                  },

            // Selection states
            ".tree-item-content.selected"        : { backgroundColor  : "var(--selected-bg, rgba(13, 110, 253, 0.1))",
                                                    color            : "var(--selected-color, #1a73e8)"           ,
                                                    fontWeight       : "500"                                      },

            ".tree-item-content.selected .tree-item-icon": {
                                                    color            : "var(--selected-color, #1a73e8)"           },

            // Icons
            ".tree-item-icon"                    : { width            : "1.5rem"                                  ,
                                                    height           : "1.5rem"                                  ,
                                                    display          : "flex"                                    ,
                                                    alignItems       : "center"                                  ,
                                                    color            : "var(--icon-color, #6c757d)"              ,
                                                    transition       : "transform 0.2s ease"                     },

            ".tree-item-expanded"                : { transform        : "rotate(90deg)"                           },

            ".file-icon"                         : { color            : "var(--file-color, #6c757d)"              },
            ".folder-icon"                       : { color            : "var(--folder-color, #ffd43b)"            },

            // Text content
            ".tree-item-text"                    : { fontSize         : "0.8rem"                                  ,
                                                    color            : "var(--text-color, #333)"                 ,
                                                    flexGrow         : "1"                                       ,
                                                    marginLeft       : "0.5rem"                                  ,
                                                    whiteSpace       : "nowrap"                                  ,
                                                    overflow         : "hidden"                                  ,
                                                    textOverflow     : "ellipsis"                                },

            // Children container
            ".tree-children"                     : { paddingLeft      : "1.5rem"                                  },
            ".tree-folder-closed"                : { display          : "none"                                    },

            // Action buttons
            ".tree-item-actions"                 : { marginLeft       : "auto"                                    },

            ".tree-item-button"                  : { padding          : "0.25rem"                                 ,
                                                    border           : "none"                                    ,
                                                    background       : "none"                                    ,
                                                    cursor           : "pointer"                                 ,
                                                    color            : "var(--action-color, #6c757d)"            },

            ".tree-item-button:hover"            : { color            : "var(--action-hover-color, #495057)"      },

            // Utility classes
            ".hidden"                            : { display          : "none"                                    },

            // Modal elements
            ".tree-view-modal"                   : { position         : "fixed"                                   ,
                                                    top              : "50%"                                     ,
                                                    left             : "50%"                                     ,
                                                    transform        : "translate(-50%, -50%)"                   ,
                                                    backgroundColor  : "#fff"                                    ,
                                                    padding          : "1rem"                                    ,
                                                    borderRadius     : "0.375rem"                                ,
                                                    boxShadow        : "0 4px 6px rgba(0,0,0,0.1)"              }
        }
    }
}

WebC__User_Files__Tree_View.define()