// WebC__Files__Actions.mjs
import Web_Component from '../../core/Web_Component.mjs'
import CSS__Forms    from '../../css/CSS__Forms.mjs'
import API__Invoke   from '../../data/API__Invoke.mjs'
import Div           from '../../core/Div.mjs'
import Text          from '../../core/Text.mjs'
import Button        from '../../core/Button.mjs'
import Input         from '../../core/Input.mjs'

export default class WebC__User_Files__Actions extends Web_Component {

    async apply_css() {
        this.add_css_rules(this.css_rules())
    }

    load_attributes() {
        new CSS__Forms(this).apply_framework()
        this.api_invoke  = new API__Invoke()
        this.current_folder = {
            node_id : null,
            name    : 'root'
        }
    }


    add_event_listeners() {
        document.addEventListener('folder-selected', this.handle__on_folder_selected)
    }

    add_event_handlers() {
        this.query_selector('.new-folder-btn'      ).addEventListener('click', this.handle__on_add_folder     );  // Add folder handler
        this.query_selector('.new-markdown-btn'    ).addEventListener('click', this.handle__on_create_markdown);  // Markdown creation handler
        this.query_selector('.action-button.rename').addEventListener('click', this.handle__on_rename_folder  );
        this.query_selector('.action-button.delete').addEventListener('click', this.handle__on_delete_folder  );
    }


    remove_event_listeners() {
        document.removeEventListener('folder-selected', this.handle__on_folder_selected);
    }
    remove_event_handlers() {
        this.query_selector('.new-folder-btn'      ).removeEventListener('click', this.handle__on_add_folder     );        // Remove folder handler
        this.query_selector('.new-markdown-btn'    ).removeEventListener('click', this.handle__on_create_markdown); // Remove markdown creation handler
        this.query_selector('.action-button.rename').removeEventListener('click', this.handle__on_rename_folder  );
        this.query_selector('.action-button.delete').removeEventListener('click', this.handle__on_delete_folder  );
    }

    async component_ready() {
        // todo add this logic here
        //this.show_rename_delete = this.current_folder.node_id &&  this.current_folder.name !== 'root'
    }


    // Build methods
    async add_folder(folder_name) {
        try {
            await this.api_invoke.invoke_api('/api/user-data/files/add-folder', 'POST', {
                folder_name      : folder_name,
                parent_folder_id : this.current_folder.node_id || ''
            })
            //this.input.value = ''
            this.raise_refresh_event()
        } catch (error) {
            //console.error('Error adding folder:', error)
        }
    }

    async create_markdown_file(filename) {
        if (!filename.endsWith('.md')) {
            filename = filename + '.md'
        }


        const file_content = '# New Document\n\nEnter your markdown content here...'
        await this.api_invoke.invoke_api('/api/user-data/files/add-file', 'POST', {
            file_name         : filename,
            file_bytes__base64: btoa(file_content),
            folder_id         : this.current_folder.node_id || ''
        })
        this.raise_refresh_event()
    }

    async delete_current_folder() {
        if (!this.current_folder.node_id) {
            alert('Cannot delete root folder')
            return
        }

        if (confirm(`Are you sure you want to delete folder "${this.current_folder.name}"?`)) {
            try {
                const path = `/api/user-data/files/delete-folder?folder_id=${this.current_folder.node_id}`
                await this.api_invoke.invoke_api(path, 'DELETE')
                this.raise_refresh_event()
            } catch (error) {
                console.error('Error deleting folder:', error)
            }
        }
    }

    async rename_current_folder(new_name) {
        if (!this.current_folder.node_id) {
            alert('Cannot rename root folder')
            return
        }

        try {
            await this.api_invoke.invoke_api('/api/user-data/files/folder-rename', 'POST', {
                folder_id       : this.current_folder.node_id,
                new_folder_name : new_name
            })
            this.raise_refresh_event()
        } catch (error) {
            console.error('Error renaming folder:', error)
        }
    }

    raise_refresh_event() {
        const event = new CustomEvent('files-refresh', {
            bubbles : true,
            composed: true
        })
        this.dispatchEvent(event)
    }

    css_rules() {
        return {
            ".actions-container"    : { padding           : "1rem"                      ,
                                      backgroundColor   : "#fff"                      ,
                                      borderRadius      : "0.375rem"                  ,
                                      boxShadow         : "2px 2px 4px rgba(0,0,0,0.2)",
                                      display          : "flex"                      ,
                                      flexDirection    : "column"                    ,
                                      gap              : "1rem"                      },

            ".folder-info"          : { paddingBottom     : "0.5rem"                   ,
                                      display           : "flex"                      ,
                                      alignItems        : "center"                    ,
                                      gap               : "0.5rem"                    ,
                                      borderBottom      : "1px solid #dee2e6"         },

            ".current-folder"       : { fontSize          : "0.875rem"                 ,
                                      color             : "#6c757d"                   },

            ".folder-name"          : { fontWeight        : "600"                      ,
                                      color             : "#212529"                   },

            ".actions-form"         : { display          : "flex"                      ,
                                      gap              : "0.5rem"                     },

            ".rename-form"          : { display          : "flex"                      ,
                                      gap              : "0.5rem"                     },

            ".folder-input"         : { flex             : "1"                         },

            ".rename-input"         : { flex             : "1"                         },

            ".action-button"        : { padding          : "0.375rem 0.75rem"         ,
                                      fontSize         : "0.875rem"                  ,
                                      fontWeight       : "500"                       ,
                                      color            : "#fff"                      ,
                                      backgroundColor  : "#0d6efd"                   ,
                                      border           : "none"                      ,
                                      borderRadius     : "0.375rem"                  ,
                                      cursor           : "pointer"                   },

            ".action-button:hover"  : { backgroundColor  : "#0b5ed7"                   },

            ".action-button.rename" : { backgroundColor  : "#198754"                   },

            ".action-button.rename:hover": { backgroundColor : "#146c43"               },

            ".action-button.delete" : { backgroundColor  : "#dc3545"                  ,
                                        marginTop        : "auto"                      },  // Push to bottom

            ".action-button.delete:hover"  : { backgroundColor : "#bb2d3b"             },
        }
    }


    html() {
        const container         = new Div({ class: 'actions-container' })
        const folder_info       = this.render_folder_info()
        const folder_form       = this.render_folder_form()
        const markdown_form     = this.render_markdown_form()

        //if (this.show_rename_delete) {                                // todo: add this logic to the UI  (when components that are not supposed to be visible should start hidden)
        const rename_form = this.render_rename_delete_form()
        const delete_btn  = this.render_delete_button()
        container.add_elements(folder_info, folder_form, markdown_form, rename_form, delete_btn)

        return container
    }

    // Render helper methods
    render_folder_info() {
        const folder_info          = new Div({ class: 'folder-info' })
        const text__current_folder = new Text({ class: 'current-folder', value: 'Current Folder: ' })
        const text__folder_name    = new Text({ class: 'folder-name', value: this.current_folder.name })
        folder_info.add_elements(text__current_folder, text__folder_name)
        return folder_info
    }

    render_folder_form() {
        const form__new_folder = new Div  ({ class: 'actions-form' })
        const input            = new Input({ class: 'input folder-input new-folder-input', value: 'new-folder'})
        const add_button      = new Button({ class: 'action-button new-folder-btn'       , value: 'Add'       })
        form__new_folder.add_elements(input, add_button)
        return form__new_folder
    }

    render_markdown_form() {
        const form__new_markdown = new Div   ({ class: 'actions-form' })
        const markdown_input     = new Input ({ class: 'input folder-input new-markdown-input', value: 'new-document.md' })
        const markdown_button    = new Button({ class: 'action-button new-markdown-btn'       , value: 'Create Markdown' })
        form__new_markdown.add_elements(markdown_input, markdown_button)
        return form__new_markdown
    }

    render_rename_delete_form() {
        const form__rename_folder = new Div   ({ class: 'rename-form' })
        const rename_input        = new Input ({ class: 'input rename-input'  , placeholder: 'New name', value: this.current_folder.name })
        const rename_button       = new Button({ class: 'action-button rename', value: 'Rename' })

        form__rename_folder.add_elements(rename_input, rename_button)
        return form__rename_folder
    }

    render_delete_button() {
        return new Button({
            class: 'action-button delete',
            value: 'Delete'
        })
    }

    handle__on_add_folder = async (e) =>{
        const input = this.query_selector('.new-folder-input');
        const name = input.value.trim();
        if (name) {
            await this.add_folder(name);
        }
    }

    handle__on_create_markdown = async (e) =>{
        const input = this.query_selector('.new-markdown-input');
        const filename = input.value.trim();
        if (filename) {
            await this.create_markdown_file(filename);
        }
    }

    handle__on_folder_selected = async (e) =>{
        this.current_folder    = e.detail
        await this.refresh_ui()
    }

    handle__on_rename_folder = async (e) =>{
        const input = this.query_selector('.rename-input');
        const new_name = input.value.trim();
        if (new_name && new_name !== this.current_folder.name) {
            await this.rename_current_folder(new_name);
        }
    }

    handle__on_delete_folder = async (e) =>{
        await this.delete_current_folder();
    }
}

WebC__User_Files__Actions.define()