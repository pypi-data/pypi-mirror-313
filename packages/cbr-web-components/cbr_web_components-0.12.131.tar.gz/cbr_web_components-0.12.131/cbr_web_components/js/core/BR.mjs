import Tag from "./Tag.mjs";

export default class BR extends Tag {
    constructor({...kwargs} = {}) {
        super({tag: 'br', ...kwargs})
    }
}