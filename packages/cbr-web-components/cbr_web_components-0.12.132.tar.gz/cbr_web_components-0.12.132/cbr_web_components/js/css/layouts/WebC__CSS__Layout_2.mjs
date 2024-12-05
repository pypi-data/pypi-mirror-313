import Web_Component   from '../../core/Web_Component.mjs'
import Layout          from '../../css/grid/Layout.mjs'
import CSS__Grid       from '../../css/grid/CSS__Grid.mjs'
import CSS__Typography from '../../css/CSS__Typography.mjs'

export default class WebC__CSS__Layout_2 extends Web_Component {
    load_attributes() {
        this.css_grid       = new CSS__Grid(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css      = this.hasAttribute('no-css') === false
    }

    render() {
        let layout, row_banner, row_content

        layout      = new Layout({ class: 'h-500px' })
        row_banner  = layout.add_row()
        row_content = layout.add_row({ class: 'flex-fill flex-nowrap'                               })

        row_banner .add_col({class: 'p-3 h-50px bg-blue'                    ,  value: 'Top Banner'  })
        row_content.add_col({width: 200, class: 'flex-column d-flex'                                })
                   .add_col({ class: 'p-3 flex-fill bg-light-green'         , value: 'Left Menu'    }).parent()
                   .add_col({ class: 'h-50px p-3 bg-light-black color-white', value: 'Fixed section'})
        row_content.add_col({ class: 'p-3 flex-fill bg-light-gray'          , value: 'Content area' })

        if (this.apply_css) {
            this.css_grid      .apply_framework()
            this.css_typography.apply_framework()
        }

        this.set_inner_html(layout.html())
    }
}

WebC__CSS__Layout_2.define()
