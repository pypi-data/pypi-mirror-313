// WebC__User_Files__Folder_Viewer.mjs
import Web_Component  from '../../core/Web_Component.mjs'
import CSS__Cards     from '../../css/CSS__Cards.mjs'
import CSS__Forms     from '../../css/CSS__Forms.mjs'
import CSS__Icons     from '../../css/icons/CSS__Icons.mjs'
import API__Invoke    from '../../data/API__Invoke.mjs'
import Icon           from '../../css/icons/Icon.mjs'
import Div            from '../../core/Div.mjs'
import Button         from '../../core/Button.mjs'
import Raw_Html       from "../../core/Raw_Html.mjs"
import CSS__Buttons   from "../../css/CSS__Buttons.mjs";

export default class WebC__User_Files__Folder_Viewer extends Web_Component {
    constructor() {
        super();
        this.api_invoke    = new API__Invoke()
        this.current_folder = null
    }

    async apply_css() {
        new CSS__Buttons  (this).apply_framework()
        new CSS__Cards    (this).apply_framework()
        new CSS__Forms    (this).apply_framework()
        new CSS__Icons    (this).apply_framework()
        this.add_css_rules(this.css_rules())
    }


    add_event_listeners() {
        document.addEventListener   ('folder-selected', this.handle__on_folder_selected)
    }

    remove_event_listeners() {
        document.removeEventListener('folder-selected', this.handle__on_folder_selected)
    }


    add_event_handlers() {
        this.query_selector('.create-summary-btn').addEventListener   ('click', this.create_folder_summary)
    }

    remove_event_handlers() {
        this.query_selector('.create-summary-btn').removeEventListener('click', this.create_folder_summary)
    }

    handle__on_folder_selected = async (e) => {
        this.current_folder = e.detail
        await this.load_folder_data()
        await this.refresh_ui()
    }

    async load_data() {
        await this.load_folder_data()
    }

    async load_folder_data() {

        if (!this.current_folder) {
            return
        }
        const path = `/api/user-data/files/folder?folder_id=${this.current_folder?.node_id}`
        const response = await this.api_invoke.invoke_api(path)
        this.folder_data = response.data
        await this.load_folder_summary()
        //this.show_error_message('Failed to load folder data')
    }

    async load_folder_summary() {

        const path = `/api/user-data/file-to-llms/folder-summary?folder_id=${this.current_folder.node_id}&re_create=false`
        const response = await this.api_invoke.invoke_api(path, 'POST')
        this.folder_summary = response.data
    }

    create_folder_summary = async () => {
        //button.innerHTML = '...creating folder summary'        // todo: refactor this into an event
        const path = `/api/user-data/file-to-llms/folder-summary?folder_id=${this.current_folder.node_id}&re_create=true`
        await this.api_invoke.invoke_api(path, 'POST')
        //  button.innerHTML = '...reloading'
        await this.load_folder_data()
        await this.refresh_ui()
        //button.innerHTML = 'Create Summary'
        //this.show_error_message('Failed to create folder summary')
    }

    format_date(timestamp) {
        const date = new Date(timestamp)
        return date.toLocaleString()
    }

    render_summary_section() {
        if (!this.folder_summary) {
            return new Div()
        }

        const summary_container = new Div     ({ class: 'summary-container'                                })
        const summary_header    = new Div     ({ class: 'summary-header'                                   })
        const summary_title     = new Div     ({ class: 'summary-title'    , value: 'Folder Summary'       })
        const summary_content   = new Raw_Html({ class: 'summary-content',  value: marked.marked(this.folder_summary)})

        summary_header.add_element(summary_title)
        summary_container.add_elements(summary_header, summary_content)

        return summary_container
    }

    css_rules() {
        return {
            ".viewer-container"    : { padding          : "1.5rem"                    ,            // Container padding
                                     backgroundColor   : "#fff"                      ,            // White background
                                     borderRadius      : "0.5rem"                    ,            // Rounded corners
                                     boxShadow         : "0 2px 4px rgba(0,0,0,0.1)" ,            // Subtle shadow
                                     minHeight         : "300px"                     },           // Minimum height

            // ".viewer-empty"        : { display          : "flex"                      ,            // Center content
            //                          alignItems        : "center"                    ,            // Vertically center
            //                          justifyContent    : "center"                    ,            // Horizontally center
            //                          height            : "300px"                     ,            // Fixed height
            //                          color             : "#6c757d"                   },           // Gray text

            ".folder-header"       : { display          : "flex"                      ,            // Flex container
                                     alignItems        : "center"                    ,            // Center items
                                     justifyContent    : "space-between"             ,            // Space between
                                     marginBottom      : "1rem"                      ,            // Bottom margin
                                     padding          : "0.5rem 0"                  ,            // Vertical padding
                                     borderBottom     : "1px solid #dee2e6"         },           // Bottom border

            ".folder-info"         : { display          : "flex"                      ,            // Flex container
                                     flexDirection     : "column"                    ,            // Stack vertically
                                     gap              : "0.25rem"                    },           // Gap between items

            ".folder-name"         : { fontSize         : "1.25rem"                   ,            // Larger text
                                     fontWeight        : "600"                       ,            // Semi-bold
                                     color             : "#212529"                   },           // Dark text

            ".folder-meta"         : { fontSize         : "0.875rem"                  ,            // Smaller text
                                     color             : "#6c757d"                   },           // Gray text

            ".summary-container"   : { marginTop        : "1rem"                      ,            // Top margin
                                     padding          : "1rem"                      ,            // Inner padding
                                     backgroundColor  : "#f8f9fa"                   ,            // Light background
                                     borderRadius     : "0.375rem"                  },           // Rounded corners

            ".summary-header"      : { display          : "flex"                      ,            // Flex container
                                     alignItems        : "center"                    ,            // Center items
                                     marginBottom     : "0.75rem"                   ,            // Bottom margin
                                     borderBottom     : "1px solid #dee2e6"         },           // Bottom border

            ".summary-title"       : { fontSize         : "1rem"                      ,            // Regular text
                                     fontWeight        : "600"                       ,            // Semi-bold
                                     color             : "#212529"                   },           // Dark text

            ".summary-content"     : { fontSize         : "0.875rem"                  ,            // Smaller text
                                     lineHeight        : "1.6"                       ,            // Line height
                                     color             : "#495057"                   }            // Gray text
        }
    }

    //todo: find a better way to show error messages
    // show_error_message(message) {
    //     const status = this.shadowRoot.querySelector('.viewer-status')
    //     if (status) {
    //         status.textContent = message
    //         status.className = 'viewer-status error'
    //         setTimeout(() => { status.textContent = '' }, 3000)
    //     }
    // }

    async clear_viewer() {
        this.current_folder = null
        this.folder_data = null
        this.folder_summary = null
        await this.refresh_ui()
    }

    html() {
        const container = new Div({ class: 'viewer-container' })

        //if (!this.current_folder || !this.folder_data) {
        //     container.add_element(
        //         new Div({
        //             class: 'viewer-empty',
        //             value: 'Select a folder to view its contents'
        //         })
        //     )
        //} else {

            const header = new Div({ class: 'folder-header' })
            const info = new Div({ class: 'folder-info' })

            info.add_elements(
                new Div({ class: 'folder-name', value: this.folder_data?.folder_name }),
                new Div({ class: 'folder-meta', value: `Created   : ${this.format_date(this.folder_data?.metadata.timestamp__created)}` }),
                new Div({ class: 'folder-meta', value: `Updated   : ${this.format_date(this.folder_data?.metadata.timestamp__updated)}` }),
                new Div({ class: 'folder-meta', value: `Files     : ${this.folder_data?.files.length}` }),
                new Div({ class: 'folder-meta', value: `Subfolders: ${this.folder_data?.folders.length}` })
            )

            const create_summary_btn = new Button({ class: 'btn btn-primary create-summary-btn', value: 'Create Summary' })
            header.add_elements(info, create_summary_btn)

            // Add summary section
            const summary_section = this.render_summary_section()
            container.add_elements(header, summary_section)

            const status = new Div({ class: 'viewer-status' })
            container.add_element(status)
        //}

        return container
    }

}

WebC__User_Files__Folder_Viewer.define()