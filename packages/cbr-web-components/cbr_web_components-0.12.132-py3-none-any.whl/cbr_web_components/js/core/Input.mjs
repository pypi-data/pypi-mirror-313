import Tag from "./Tag.mjs";

export default class Span extends Tag {
    constructor({value='', ...kwargs} = {}) {
        kwargs.attributes = { ...(kwargs.attributes || {}), value : value};
        super({tag: 'input', ...kwargs})
    }
}