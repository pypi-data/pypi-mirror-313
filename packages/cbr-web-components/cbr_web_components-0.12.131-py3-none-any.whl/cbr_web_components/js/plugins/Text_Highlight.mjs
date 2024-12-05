//import aaa from "/assets/plugins/highlight/lib/core.js"
//import hljs from 'https://unpkg.com/@highlightjs/cdn-assets@11.10.0/es/highlight.min.js';

export default class Text_Highlight {

    constructor(target_webc) {
        this.css_loaded  = false
        this.js_loaded   = false
        this.target_webc = target_webc
        this.css_code    = ''
    }

    ///assets/plugins/highlight/highlight.min.js
    async fetch_css_code() {
        try {
            const path        = '/assets/plugins/highlight/default.min.css'
            const cssResponse = await fetch(path);
            this.css_code     = await cssResponse.text();
        } catch (error) {
            console.error('[Text_Highlight] Error in fetch_css_code:', error);
            return ''
        }
    }

    async load_highlight_js() {
        try {
            if (typeof(hljs) !== 'undefined') {
                this.js_loaded = true                           // since hljs has already been loaded by another instance (or test)
                return
            }
            const path           = '/assets/plugins/highlight/highlight.min.js';
            const scriptElement  = document.createElement('script');
            scriptElement.src    = path;
            scriptElement.async  = true; // Load asynchronously

            document.head.appendChild(scriptElement);

            await new Promise((resolve, reject) => {
                scriptElement.onload = resolve;
                scriptElement.onerror = () => reject(new Error('[Text_Highlight] Error loading JS script'));
            });
            this.js_loaded =  true
        } catch (error) {
            console.error('[Text_Highlight] Error in fetch_js_code:', error);
        }
    }

    async load_css() {
        await this.fetch_css_code()
        if (this.css_code) {
            const sheet       = new CSSStyleSheet();
            sheet.replaceSync(this.css_code);
            this.target_webc.add_adopted_stylesheet(sheet);
            this.css_loaded = true
            this.target_webc.raise_event('css-loaded')              // todo: see if we still need this
            //this.target_webc.dispatchEvent(new CustomEvent('css-loaded', { bubbles: false }));
        }
    }

    format_text(text, language) {
        return hljs.highlight(text, { language: language }).value
    }
}