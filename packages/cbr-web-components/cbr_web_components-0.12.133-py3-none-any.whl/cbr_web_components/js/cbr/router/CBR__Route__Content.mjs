import CBR__Content__Loader from './CBR__Content__Loader.mjs';

export default class CBR__Route__Content {
    constructor(config = {}) {
        this.content_loader = new CBR__Content__Loader(config);
    }

    async fetch_content(route_path) {

        try {
            // Map routes to content sections
            const page    = this.map_route_to_page(route_path);
            const content = await this.content_loader.load_content(page);
            if (content && content.html) {
                return content.html
            } else {
                throw new Error('Invalid content format received');
            }
        } catch (error) {
            //console.error('Route content error:', error);
            return "... failed to load content ..."
        }
    }

    map_route_to_page(route_path) {     // in case we need to map routes to content sections
        return route_path;
    }

    set_language(language) {
        this.content_loader.set_language(language);
    }

    set_version(version) {
        this.content_loader.set_version(version);
    }
}