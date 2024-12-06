import Web_Component  from "../../core/Web_Component.mjs";
import API__Invoke    from "../../data/API__Invoke.mjs";
import Text_Highlight from "../../plugins/Text_Highlight.mjs";


export default class WebC__API_To_Json extends Web_Component {

    constructor() {
        super();
    }

    async apply_css() {
        await this.text_highlight.load_css()
        await this.text_highlight.load_highlight_js()
    }

    // async connectedCallback() {
    //     this.setup()
    //     //super.connectedCallback()
    //     this.load_attributes()
    //     await this.text_highlight.load_css()
    //     await this.text_highlight.load_highlight_js()
    //     await this.build()
    //     this.raise_event('build-complete')
    // }

    load_attributes() {
        this.api_path  = this.getAttribute('api_path')
    }

    disconnectedCallback() {
        super.disconnectedCallback()
    }

    async load_data() {
        this.api_invoke                = new API__Invoke()
        this.text_highlight            = new Text_Highlight(this)
        this.api_invoke.mock_responses = JSON.parse(this.getAttribute('mock_responses'))
        this.use_api_path_as_title     = true
        this.api_data                  = await this.invoke_api_path()
    }


    async invoke_api_path() {
        const api_path = this.api_path
        const method   = 'GET'
        const data     = null
        return await this.api_invoke.invoke_api(api_path, method, data)
    }

    html () {
        let data_str = `${JSON.stringify(this.api_data, null, '    ')}`
        let formatted_html = this.text_highlight.format_text(data_str, 'json')
        let html_code = ''
        if (this.use_api_path_as_title) {
            html_code = `<h2>${this.api_path}</h2>`
        }
        html_code += `<pre>${formatted_html}</pre>`
        return html_code
    }
}

WebC__API_To_Json.define()