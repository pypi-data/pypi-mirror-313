import Web_Component from "../core/Web_Component.mjs";

export default class WebC__Browser_Params extends Web_Component {
    constructor() {
        super();
    }
    connectedCallback() {
        this.build()
    }

    build() {
        const pageParams = new URLSearchParams(window.location.search);
        const html = `<i>${pageParams.toString()}</i>`
        this.set_inner_html(html)
    }

}


WebC__Browser_Params.define()