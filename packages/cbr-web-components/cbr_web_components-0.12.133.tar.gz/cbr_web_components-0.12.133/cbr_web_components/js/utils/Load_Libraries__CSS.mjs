export default  class Load_Libraries__CSS {

    static url__css__material_design_icons = 'https://static.dev.aws.cyber-boardroom.com/cbr-static/latest/assets/css/icons/material-design-iconic-font/css/materialdesignicons.min.css'

    constructor({target, mock_responses=null}) {
        this.target          = target
        this.mock_responses  = mock_responses
    }
    // core methods
    async fetch_data(url_path) {
        let text        = null
        let status_code = null
        let status_text = null
        let ok          = null
        if (this.mock_responses && this.mock_responses[url_path]) {
            text        =  this.mock_responses[url_path]
            status_code = 200
            status_text = 'OK'
            ok          = true
        }
        else {
            const response = await fetch(url_path);
            status_code = response.status
            status_text = response.statusText
            ok          = response.ok
            text        = await response.text()
        }
        return {status: ok, status_code: status_code, status_text: status_text, text: text}
    }
    // library specific methods
    async load_material_design() {
        const fetch_response = await this.fetch_data(Load_Libraries__CSS.url__css__material_design_icons);
        let   css_loaded     = false
        let   sheet          = new CSSStyleSheet();
        if (fetch_response.status) {
            const css_code    = fetch_response.text
            sheet.replaceSync(css_code);
            this.target.add_adopted_stylesheet(sheet);
            css_loaded       = true
        }

        const result = {css_loaded: css_loaded, sheet: sheet, fetch_response: fetch_response}
        return result
    }
}
