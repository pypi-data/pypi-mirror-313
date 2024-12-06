import Tag from "./Tag.mjs";

export default class Span extends Tag {
    constructor({...kwargs} = {}) {
        super({tag: 'hr', ...kwargs})
        this.html_config.include_end_tag = false
    }
}