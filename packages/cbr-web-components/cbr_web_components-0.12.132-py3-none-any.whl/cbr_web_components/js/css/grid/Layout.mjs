import Div from '../../core/Div.mjs'
import Row from './Row.mjs'

export default class Layout extends Div {
    constructor({...kwargs}={}) {
        kwargs.class = `layout ${kwargs.class || ''}`
        super({...kwargs})
    }

    add_row({...kwargs}={}) {
        const row = new Row({...kwargs})
        this.add_element(row)
        return row
    }

    // Helper for common layouts
    add_rows(row_configs=[]) {
        row_configs.forEach(config => this.add_row(config))
        return this
    }
}