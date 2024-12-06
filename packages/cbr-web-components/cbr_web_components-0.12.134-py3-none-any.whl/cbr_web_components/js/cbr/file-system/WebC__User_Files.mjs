import Web_Component        from '../../core/Web_Component.mjs'
import Div                  from '../../core/Div.mjs'
import API__Invoke          from "../../data/API__Invoke.mjs";
import WebC__Resize_Button  from "../../elements/ui/WebC__Resize_Button.mjs";
import WebC__User_Files__Tree_View from "./WebC__User_Files__Tree_View.mjs";
import WebC__User_Files__Actions from "./WebC__User_Files__Actions.mjs";
import WebC__User_Files__Upload from "./WebC__User_Files__Upload.mjs";
import WebC__User_Files__File_Viewer from "./WebC__User_Files__File_Viewer.mjs";
import WebC__User_Files__Folder_Viewer from "./WebC__User_Files__Folder_Viewer.mjs";

export default class WebC__User_Files extends Web_Component {

    constructor() {
        super();
        this.api_invoke = new API__Invoke()
    }

    async apply_css() {
        this.add_css_rules(this.css_rules())
    }


    add_event_listeners() {
        this.addEventListener('resize-user-files-left-panel', (event) => this.on_left_panel_resize(event))

        this.shadowRoot.addEventListener('files-refresh', () => {                                               // Tree refresh handler
            const tree_view = this.shadowRoot.querySelector('webc-user-files-tree-view')
            if (tree_view) { tree_view.refresh() }
        })


        document.addEventListener('active_session_changed', () => this.reload_all_components())                 // Session change handler - reload all components

        document.addEventListener('file-selected', async (e) => {
            const file_viewer   = this.shadowRoot.querySelector('webc-user-files-file-viewer')
            const folder_viewer = this.shadowRoot.querySelector('webc-user-files-folder-viewer')
            //const chatbot       = this.shadowRoot.querySelector('chatbot-openai')

            if (file_viewer  ) { file_viewer.style.display = 'block' }
            if (folder_viewer) { folder_viewer.style.display = 'none' }

        })

        // Folder selection handler
        document.addEventListener('folder-selected', async (e) => {
            const file_viewer   = this.shadowRoot.querySelector('webc-user-files-file-viewer')
            const folder_viewer = this.shadowRoot.querySelector('webc-user-files-folder-viewer')

            if (file_viewer  ) { file_viewer.style.display = 'none' }
            if (folder_viewer) { folder_viewer.style.display = 'block' }

        })
    }

    get div__left_panel() {
        return this.query_selector('.left-panel')
    }

    on_left_panel_resize (event) {
        const minimized = event.detail.minimized
        if (minimized) {
            this.div__left_panel.add_class   ('left-panel-minimized')
        } else {
            this.div__left_panel.remove_class('left-panel-minimized')
        }
    }

    reload_all_components() {
        const tree_view = this.shadowRoot.querySelector('webc-user-files-tree-view')                    // Refresh tree view
        if (tree_view) {
            tree_view.refresh()
        }

        const file_viewer = this.shadowRoot.querySelector('webc-user-files-file-viewer')                // Refresh file viewer
        if (file_viewer) {
            file_viewer.clear_viewer?.()                                                                // Use optional chaining in case method doesn't exist
        }

        this.shadowRoot.querySelectorAll('.selected').forEach(element => {                      // Clear any active selections or states
            element.classList.remove('selected')
        })
    }

    add_web_components() {
        let params = { resize_event_name : 'resize-user-files-left-panel' }
        this.add_web_component(WebC__Resize_Button, params )

        this.add_web_component_to('.left-panel'     , WebC__User_Files__Tree_View    )
        this.add_web_component_to('.left-panel'     , WebC__User_Files__Actions      )
        this.add_web_component_to('.left-panel'     , WebC__User_Files__Upload       )
        this.add_web_component_to('.preview-section', WebC__User_Files__File_Viewer  )
        this.add_web_component_to('.preview-section', WebC__User_Files__Folder_Viewer)
    }


    html() {
        const container = new Div({ class: 'files-container'           })

        const left_panel = new Div({ class: 'files-panel left-panel'   })                 // Left panel for tree view and actions
        // left_panel.add_tag({ tag: 'webc-user-files-tree-view'          })
        // left_panel.add_tag({ tag: 'webc-user-files-actions'            })
        // left_panel.add_tag({ tag: 'webc-user-files-upload'             })

        const right_panel = new Div({ class: 'files-panel right-panel' })               // Right panel for file preview and chat
        const preview_section = new Div({ class: 'preview-section'     })
        // preview_section.add_tag({ tag: 'webc-user-files-file-viewer'   })
        // preview_section.add_tag({ tag: 'webc-user-files-folder-viewer' })

        right_panel.add_elements(preview_section)
        container  .add_elements(left_panel, right_panel)

        return container
    }

    css_rules() {

        return {
            ":host"                : { display          : "block"                     ,            // Make component block level
                                     width             : "100%"                      ,            // Take full width
                                     height            : "100%"                      ,            // Take full height
                                     minHeight         : "0"                         },           // Allow content to shrink

            ".files-container"     : { display          : "flex"                      ,            // Main container as flex
                                     width             : "100%"                      ,            // Full width
                                     height            : "100%"                      ,            // Full height
                                     gap              : "1rem"                      ,            // Gap between panels
                                     padding          : "1rem"                      ,            // Padding around container
                                     backgroundColor  : "#f8f9fa"                   ,            // Light background
                                     position         : "absolute"                  ,            // Position absolute
                                     top              : "0"                         ,            // Align to top
                                     left             : "0"                         ,            // Align to left
                                     right            : "0"                         ,            // Stretch to right
                                     bottom           : "0"                         ,            // Stretch to bottom
                                     overflow         : "auto"                                  // Prevent overflow
                                    },

            ".files-panel"         : { //borderRadius     : "0.5rem"                   ,            // Rounded corners
                                       backgroundColor  : "#ffffff"                   ,            // White background
                                       //boxShadow        : "0 2px 4px rgba(0,0,0,0.1)" ,            // Subtle shadow
                                       overflow         : "hidden"                    ,            // Prevent overflow
                                       display          : "flex"                      ,            // Make panels flex containers
                                       flexDirection    : "column"                    },           // Stack children vertically

            ".left-panel"          : { width            : "350px"                     ,            // Fixed width for left panel
                                       minWidth         : "350px"                     ,            // Prevent shrinking below 350px
                                       display          : "flex"                      ,            // Flex for child elements
                                       flexDirection    : "column"                    ,            // Stack children vertically
                                       gap              : "1rem"                      ,            // Gap between components
                                       flexShrink       : "0"                         },           // Prevent shrinking

            ".left-panel-minimized": { width            : "0px"                      ,            // Minimized width
                                       minWidth         : "0px"                      ,            // Minimized width
                                       overflow         : "hidden"                    },           // Hide content

            ".right-panel"         : { flex             : "1 1 auto"                  ,            // Take remaining space
                                      minWidth         : "0"                         ,            // Allow shrinking
                                      display          : "flex"                      ,            // Make it flex container
                                      flexDirection    : "column"                    ,           // Stack children vertically
                                      overflow         : "auto"                      },

            // Component-specific styles
            "webc-user-files-tree-view": {  //flex             : "1"                         ,            // Take available space
                                            overflowY        : "auto"                      ,            // Scroll if needed
                                            minHeight        : "0"                         },           // Allow content to scroll

            "webc-user-files-actions" : { padding          : "1rem"                 },            // Padding around actions
            "webc-user-files-upload"  : { padding          : "1rem"                 } ,           // Padding around upload

            ".preview-section"     : { flex              : "1"                         ,            // Take available space
                                      minHeight         : "0"                         ,            // Allow content to scroll
                                      overflowY         : "auto"                      },           // Enable scrolling

                ".chat-section"        : { height            : "400px"                     ,            // Fixed height
                                          marginTop         : "1rem"                      ,            // Space above chat
                                          flexShrink        : "0"                         }            // Prevent shrinking

        }
    }
}

WebC__User_Files.define()