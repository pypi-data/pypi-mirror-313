import Row from './Row.mjs'
import Div from '../../core/Div.mjs'

export default class Col extends Div {
    constructor({size, width, ...kwargs}={}) {
        // Support both size (1-12) and fixed widths
        let className = 'col'
        if (size) className   = `col-${size}`
        if (width) className += ` w-${width}px`

        kwargs.class = `${className} ${kwargs.class || ''}`
        super({...kwargs})
    }

    add_col({size, ...kwargs}={}) {
        const col = new Col({size, ...kwargs})
        this.add_element(col)
        return col
    }

    add_row({...kwargs}={}) {
        const row = new Row({...kwargs})
        this.add_element(row)
        return row
    }

    // Helper for nested content
    add_content({value, class: class_name}={}) {
        this.set_value(value)
        if (class_name) this.add_class(class_name)
        return this
    }
}