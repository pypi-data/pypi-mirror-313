import Tag from "./Tag.mjs";

export default class Img extends Tag {
    constructor({src = '', width='',height='', ...kwargs} = {}) {
        kwargs.attributes = { ...(kwargs.attributes || {}), src, width ,height};
        super({tag: 'img', ...kwargs})
    }
}