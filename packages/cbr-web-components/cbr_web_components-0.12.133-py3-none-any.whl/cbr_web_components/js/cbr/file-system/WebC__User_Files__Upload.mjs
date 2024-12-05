import Web_Component  from '../../core/Web_Component.mjs'
import CSS__Forms     from '../../css/CSS__Forms.mjs'
import CSS__Cards     from '../../css/CSS__Cards.mjs'
import CSS__Icons     from '../../css/icons/CSS__Icons.mjs'
import API__Invoke    from '../../data/API__Invoke.mjs'
import Icon           from '../../css/icons/Icon.mjs'
import Div            from '../../core/Div.mjs'
import Button         from '../../core/Button.mjs'
import Input          from '../../core/Input.mjs'
import CSS__Buttons  from "../../css/CSS__Buttons.mjs";
import CBR_Events from "../CBR_Events.mjs";

export default class WebC__User_Files__Upload extends Web_Component {

    constructor() {
        super();
        this.api_invoke = new API__Invoke()
    }

    async apply_css() {
        new CSS__Buttons (this).apply_framework()
        new CSS__Forms   (this).apply_framework()
        new CSS__Cards   (this).apply_framework()
        new CSS__Icons   (this).apply_framework()
        this.add_css_rules(this.css_rules())
    }

    load_attributes() {
        this.current_folder = { node_id: null,  name: 'root' }
    }




    add_event_listeners() {
        this.add_window_event_listener('folder-selected', this.handle__on__folder_selected)
    }

    add_event_handlers() {
        this.add_event__on('click'    , '#select-files-btn', this.handle__on__select_files_click)
        this.add_event__on('dragover' , '.drop-zone'       , this.handle__on__drag_over  )              // Drop zone events
        this.add_event__on('drop'     , '.drop-zone'       , this.handle__on__drop       )
        this.add_event__on('dragenter', '.drop-zone'       , this.handle__on__drag_enter )
        this.add_event__on('dragover' , '.drop-zone'       , this.handle__on__drag_over  )
        this.add_event__on('dragleave', '.drop-zone'       , this.handle__on__drag_leave )
        this.add_event__on('change'   , '#file-input'      , this.handle__on__file_change)             // File input events

        this.add_event__to_element__on('paste',this, this.handle__on__paste      )             // Component level events
    }

    // Event handler methods
    handle__on__select_files_click() {
        const input = this.query_selector('#file-input')
        input.click()
    }
    handle__on__folder_selected({detail}) {
        this.current_folder = detail
        this.update_folder_display()
    }

    handle__on__drag_over({event}) {
        event.preventDefault()
        event.stopPropagation()
        this.query_selector('.drop-zone').classList.add('drag-active')
    }

    async handle__on__drop({event}) {
        event.preventDefault()
        event.stopPropagation()

        const files = [...event.dataTransfer.files]
        for (const file of files) {
            await this.upload_file(file)
        }
    }

    handle__on__drag_enter() {
        this.query_selector('.drop-zone').classList.add('drag-active')
    }

    handle__on__drag_leave() {
        this.query_selector('.drop-zone').classList.remove('drag-active')
    }

    async handle__on__file_change({event}) {
        const files = [...event.target.files]
        for (const file of files) {
            await this.upload_file(file)
        }
    }

    async handle__on__paste({event}) {
        const items = [...event.clipboardData.items]
        for (const item of items) {
            if (item.kind === 'file') {
                const file = item.getAsFile()
                await this.upload_file(file)
            }
        }
    }

    // other methods

    async upload_file(file) {
        try {
            const base64_content = await this.get_file_as_base64(file)
            await this.upload_file_data(file.name, base64_content)

            this.show_success_message(`File ${file.name} uploaded successfully`)
            this.raise_refresh_event()
        } catch (error) {
            //console.error('Error uploading file:', error)
            this.show_error_message(`Failed to upload ${file.name}`)
        }
    }

    async get_file_as_base64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader()

            reader.onload  = () => {
                const base64_content = reader.result.split(',')[1]
                resolve(base64_content)
            }
            reader.readAsDataURL(file)
        })
    }

    async upload_file_data(file_name, base64_content) {
        const post_data = {
            file_name         : file_name                      ,
            file_bytes__base64: base64_content                 ,
            folder_id         : this.current_folder.node_id || ''
        }

        await this.api_invoke.invoke_api('/api/user-data/files/add-file', 'POST', post_data)
    }

    raise_refresh_event() {
        const event = new CustomEvent('files-refresh', {
            bubbles : true,
            composed: true
        })
        this.dispatchEvent(event)
    }

    update_folder_display() {
        const folder_name = this.shadowRoot.querySelector('.current-folder')
        if (folder_name) {
            folder_name.textContent = `Current folder: ${this.current_folder.name}`
        }
    }

    show_success_message(message) {
        const status = this.shadowRoot.querySelector('.upload-status')
        status.textContent = message
        status.className = 'upload-status success'
        //setTimeout(() => { status.textContent = '' }, 3000)                   // find better way to clear message
    }

    show_error_message(message) {
        const status = this.shadowRoot.querySelector('.upload-status')
        status.textContent = message
        status.className = 'upload-status error'
        //setTimeout(() => { status.textContent = '' }, 3000)                   // find better way to clear message
        this.raise_event_global(CBR_Events.CBR__UI__NEW_ERROR_MESSAGE)
    }

    css_rules() {
        return {
            ".upload-container"    : { padding          : "1.5rem"                     ,
                                     backgroundColor   : "#fff"                        ,
                                     borderRadius      : "0.5rem"                      ,
                                     boxShadow         : "2px 2px 4px rgba(0,0,0,0.2)" },

            ".current-folder"      : { fontSize         : "0.875rem"                  ,
                                     color            : "#6c757d"                    ,
                                     marginBottom     : "1rem"                       },

            ".drop-zone"          : { border           : "2px dashed #dee2e6"        ,
                                     borderRadius      : "0.375rem"                   ,
                                     padding          : "2rem"                       ,
                                     textAlign        : "center"                     ,
                                     cursor           : "pointer"                    ,
                                     transition       : "all 0.2s ease-in-out"       },

            ".drag-active"        : { borderColor      : "#0d6efd"                   ,
                                     backgroundColor   : "rgba(13,110,253,0.05)"     },

            ".upload-icon"        : { fontSize         : "2rem"                      ,
                                     color            : "#6c757d"                    ,
                                     marginBottom     : "1rem"                       },

            ".upload-text"        : { color            : "#6c757d"                   ,
                                     marginBottom     : "1rem"                       },

            ".upload-methods"     : { display          : "flex"                      ,
                                     flexDirection    : "column"                     ,
                                     gap              : "0.5rem"                     ,
                                     alignItems       : "center"                     },

            ".upload-status"      : { marginTop        : "1rem"                      ,
                                     padding          : "0.5rem"                     ,
                                     borderRadius     : "0.25rem"                    ,
                                     textAlign        : "center"                     },

            ".success"            : { backgroundColor   : "#d1e7dd"                   ,
                                     color            : "#0f5132"                    },

            ".error"              : { backgroundColor   : "#f8d7da"                   ,
                                     color            : "#842029"                    },

            "#file-input"         : { display          : "none"                      }
        }
    }

    html() {
        const container = new Div({ class: 'upload-container' })
        const folder    = new Div({ class: 'current-folder', value: `Current folder: ${this.current_folder.name}` })
        const drop_zone = new Div({ class: 'drop-zone' })

        const upload_icon = new Icon({ icon: 'upload', class: 'upload-icon' })
        const text       = new Div({ class: 'upload-text', value: 'Drag and drop files here or:' })
        const methods    = new Div({ class: 'upload-methods' })

        // File input for selection dialog
        const file_input = new Input({
            id         : 'file-input',
            attributes : { type: 'file', multiple: true }
        })

        const select_button = new Button({
            class : 'btn btn-primary',
            value : 'Select Files',
            id    : 'select-files-btn'            // Added ID for querySelector
        })

        // Status display
        const status = new Div({ class: 'upload-status' })

        methods.add_elements(file_input, select_button)
        drop_zone.add_elements(upload_icon, text, methods)
        container.add_elements(folder, drop_zone, status)

        return container
    }
}

WebC__User_Files__Upload.define()