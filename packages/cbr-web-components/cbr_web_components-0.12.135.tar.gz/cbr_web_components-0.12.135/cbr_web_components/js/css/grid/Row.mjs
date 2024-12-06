import Div from '../../core/Div.mjs'
import Col from './Col.mjs'

export default class Row extends Div {
    constructor({...kwargs}={}) {
        kwargs.class = `row ${kwargs.class || ''}`
        super({...kwargs})
    }

    add_col({...kwargs}={}) {
        const col = new Col({...kwargs})
        this.add_element(col)
        return col
    }

    add_row({...kwargs}={}) {
        const row = new Row({...kwargs})
        this.add_element(row)
        return row
    }

    // Add multiple columns at once
    add_cols(colConfigs=[]) {
        colConfigs.forEach(config => this.add_col(config))
        return this
    }

    // Add a nested row within a column
    add_nested_row({col_config={}, row_config={}}={}) {
        const col = this.add_col(col_config)
        const row = new Row(row_config)
        col.add_element(row)
        return row
    }
}