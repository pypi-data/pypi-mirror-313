import Web_Component        from "../../core/Web_Component.mjs";
import API__Invoke          from "../../data/API__Invoke.mjs";
import A                    from "../../core/A.mjs";
import B                    from "../../core/B.mjs";
import BR                   from "../../core/BR.mjs";
import Div                  from "../../core/Div.mjs";
import HR                   from "../../core/HR.mjs";
import Span                 from "../../core/Span.mjs";
import Table                from "../../core/Table.mjs";
import Container__Two_Cols  from "../../core/layout/Container__Two_Cols.mjs";
import WebC__API_To_Json    from "../api/WebC__API_To_Json.mjs";

// todo refactor into base class since 90% of this class is the same as WebC__S3_Browser__Server_Requests
export default class WebC__S3_Browser__Chat_Threads extends Web_Component {

    static url__api_list_file_contents   = "/api/server/s3-chat-threads/file-contents?file_path="
    static url__api_list_files_metadata  = "/api/server/s3-chat-threads/list-files-metadata?parent_folder="
    static url__api_list_folders         = "/api/server/s3-chat-threads/list-folders?parent_folder="


    constructor() {
        super();
    }

    async connectedCallback() {
        super.connectedCallback()
        this.setup()
        await this.build()
        this.raise_event('build-complete')
    }

    setup() {
        this.api_invoke  = new API__Invoke()
        this.api_invoke.mock_responses = JSON.parse(this.getAttribute('mock_responses'))
        this.current_paths = []
        this.current_folder = '/'
        this.current_path   = ''
        this.previous_path  = ''
        this.target_path   = ''

        // this.current_folder = 'list-folders'
        // this.current_path   = 'server-requests/cbr-website-dev-local/2024-09-16/21/api/server/s3-server-requests/list-folders/'
        // this.previous_path  = 'server-requests/cbr-website-dev-local/2024-09-16/21/api/server/s3-server-requests'
        // this.target_path    = 'server-requests/cbr-website-dev-local/2024-09-16/21/api/server/s3-server-requests/list-folders/'
    }


    // async api_get_file_contents(file_path) {
    //     const api_path = WebC__S3_Browser__Chat_Threads.url__api_list_file_contents + file_path
    //     const method = 'GET'
    //     const data = null
    //     return await this.api_invoke.invoke_api(api_path, method, data)
    // }

    // todo refactor all these api_get_* methods since the only thing that is really changing is the api_path
    async api_get_files_metadata(parent_folder) {
        const api_path = WebC__S3_Browser__Chat_Threads.url__api_list_files_metadata + (parent_folder || '')
        const method   = 'GET'
        const data     = null
        return await this.api_invoke.invoke_api(api_path, method, data)
    }

    async api_get_folders(parent_folder) {
        const api_path = WebC__S3_Browser__Chat_Threads.url__api_list_folders + (parent_folder || '')
        const method   = 'GET'
        const data     = null
        return await this.api_invoke.invoke_api(api_path, method, data)
    }

    async build() {
        let folders        = await this.api_get_folders(this.target_path)
        let files_metadata = await this.api_get_files_metadata  (this.target_path)
        let raw_html       = await this.html(folders, files_metadata)
        this.set_inner_html(raw_html)
        this.set_event_listeners()
    }

    set_event_listeners() {
        const file_links   = this.shadowRoot.querySelectorAll(".file-link"  );
        const folder_links = this.shadowRoot.querySelectorAll(".folder-link");
        const parent_link  = this.shadowRoot.querySelector   (".parent-link");
        const reload_link  = this.shadowRoot.querySelector   (".reload-link");

        parent_link.addEventListener('click', this.on_click__parent_link.bind(this));
        reload_link.addEventListener('click', this.on_click__reload_link.bind(this));

        file_links  .forEach(link => { link.addEventListener('click', this.on_click__file_link  .bind(this)); });
        folder_links.forEach(link => { link.addEventListener('click', this.on_click__folder_link.bind(this)); });

    }

    async add_folder(folder_name) {
        this.current_folder = folder_name
        if (this.previous_path === '')  {
            this.previous_path = '/'
        }
        else {
            this.previous_path = this.current_path
        }
        this.current_path  += folder_name + '/'
        this.current_paths.push({folder_name: folder_name, folder_path: this.current_path })
        this.target_path = this.current_path
        await this.build()
    }

    async on_click__folder_link(event) {
        event.preventDefault()
        const clicked_element = event.target;                           // Get the clicked element (the anchor tag)
        const target_folder = clicked_element.attributes.href.value
        await this.add_folder(target_folder)
    }

    async on_click__parent_link(event) {
        event.preventDefault()
        const clicked_element = event.target;                           // Get the clicked element (the anchor tag)
        const target_folder = clicked_element.attributes.href.value
        if (target_folder === '/') {
            this.current_path = ''
            this.previous_path = ''
            this.current_folder = ''
        }
        else {
            this.current_path   = this.remove_last_path_element(this.current_path)
            this.previous_path  = this.remove_last_path_element(this.previous_path)
            this.current_folder = this.get_last_path_element   (target_folder     )
        }
        this.target_path = target_folder
        await this.build()
    }

    async on_click__reload_link(event) {
        event.preventDefault()
        await this.build()
    }

    async on_click__file_link(event) {
        event.preventDefault()
        const clicked_element = event.target;                           // Get the clicked element (the anchor tag)
        const file_name     = clicked_element.attributes.href.value
        const file_path = `${this.current_path}${file_name}`
        const api_path = WebC__S3_Browser__Chat_Threads.url__api_list_file_contents + file_path

        let webc_api_to_json                        = new WebC__API_To_Json().setup()
        webc_api_to_json.api_path                   = api_path
        webc_api_to_json.use_api_path_as_title      = false
        webc_api_to_json.text_highlight.target_webc = this

        await webc_api_to_json.text_highlight.load_css()
        await webc_api_to_json.text_highlight.load_highlight_js()

        let file_html = await webc_api_to_json.html()

        let dom_file_contents = this.shadowRoot.querySelector('#file_contents')

        dom_file_contents.innerHTML = file_html
    }


    async html(folders, files_metadata) {
        let files_text          = `Files: ${files_metadata.file_count} in ${files_metadata.duration.seconds} secs`
        let div_root            = new Div({id:'api_to_table'    })
        let separator_pipe      = new Span({value:'|'})
        let hr_separator        = new HR()
        let div_file_contents   = new Div({id:'file_contents', class: 'file_contents', value: 'file contents will go here'})

        let container_two_cols = new Container__Two_Cols()


        let span_text_path      = new Span({ value: 'Path:'    })
        let span_text_folders   = new Span({ value: 'Folders:' })

        let a_reload            = new A({class:'reload-link',  value:'reload', attributes:{href: '#'}})
        let a_previous_path     = new A({class:'parent-link',  value:this.previous_path, attributes:{href:this.previous_path}})
        let b_current_folder    = new B({value: this.current_folder})

        div_root.add_elements(a_reload, hr_separator)
        div_root.add_elements(span_text_path, a_previous_path, b_current_folder)
        div_root.add_elements(hr_separator, span_text_folders)

        for (let folder of folders) {
            let a_folder_link = new A({class:'folder-link',  value:folder, attributes:{href:folder}})
            div_root.add_elements(a_folder_link, separator_pipe)
        }
        div_root.add_element(hr_separator)
        let table_rows    = []
        let table_headers = ['req id', 'request_id', 'request_type']

        for (let file_metadata of files_metadata.files_metadata) {
            const metadata      = file_metadata.metadata
            let file_name       = file_metadata.file_name
            //let file_name_short = file_name.substring(0,5)
            let a_file     = new A({class:'file-link',  value:file_name, attributes:{href:file_name}})
            const table_row = [a_file.html()         ,
                               metadata.request_id   ,
                               metadata.request_type ]
            table_rows.push(table_row)
        }

        let table_files    = new Table({headers:table_headers, rows: table_rows })
        container_two_cols.col_1.add_element(table_files)
        container_two_cols.col_2.add_element(div_file_contents)

        div_root.add_element(container_two_cols)
        this.add_css_rules(container_two_cols.css_rules())
        let html = div_root.html()

        this.add_css_rules(table_files.table_css__simple())
        return html
    }

    remove_last_path_element(path) {
        let pathElements = path.split('/').filter(element => element !== '');   // Split the path into elements and filter out empty strings
        pathElements.pop();                                                     // Remove the last element from the array
        return pathElements.join('/') + '/';                                    // Join the remaining elements back into a string with '/' and add a trailing '/'
    }
    get_last_path_element(path) {
        let pathElements = path.split('/').filter(element => element !== '');       // Split the path into elements and filter out empty strings
        return pathElements.pop() || ''; // Get the last element from the array or return an empty string if the array is empty
    }
}


WebC__S3_Browser__Chat_Threads.define()