import Tag from "./Tag.mjs";

export default class Span extends Tag {
    constructor({value, text, ...kwargs} = {}) {
        kwargs.attributes = { ...(kwargs.attributes || {})};
        kwargs.attributes.value = value             // the value in attributes is the value of the input
        kwargs.value  = text                        // the value in the kwargs is the text of the input
        super({tag: 'option', ...kwargs})
    }
}