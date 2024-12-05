export default class CBR__Content__Loader {
    constructor(config = {}) {
        this.dev_mode = config.dev_mode !== undefined ?  config.dev_mode :
                                                         (window.location.protocol === 'http:');
        this.base_url     = config.base_url     || 'https://static.dev.aws.cyber-boardroom.com';
        this.version      = config.version      || 'latest';
        this.language     = config.language     || 'en';
        this.content_type = config.content_type || 'site';
    }

    async load_content(page) {
        const url = this.dev_mode ?
            this._build_dev_url(page) :
            this._build_prod_url(page);

        const response = await this.fetch_url(url)
        if (!response.ok) {
            throw new Error(`Failed to load content | ${response.status} | ${url}`);
        }

        return await response.json();
    }

    /* istanbul ignore next */
    async fetch_url(url) {
        return await fetch(url)
    }

    _build_prod_url(page) {
        return `${this.base_url}/cbr-content/${this.version}/${this.language}/${this.content_type}/${page}.md.json`;
    }

    _build_dev_url(page) {
        return `/markdown/render/markdown-file-to-html-and-metadata?path=${this.language}/${this.content_type}/${page}.md`;
    }

    set_language(language) {
        this.language = language;
    }

    set_version(version) {
        this.version = version;
    }
}