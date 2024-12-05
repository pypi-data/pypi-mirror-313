import Web_Component   from '../../core/Web_Component.mjs';
import A               from '../../core/A.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import HR              from '../../core/HR.mjs';
import Text            from '../../core/Text.mjs';
import CSS__Pagination from '../CSS__Pagination.mjs';
import CSS__Typography from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__Pagination extends Web_Component {
    load_attributes() {
        this.css_pagination = new CSS__Pagination(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'pagination-demo' })

        // Header
        let header = [ new HR(),
                       new Text({ value: 'Pagination Demo' + (this.apply_css ? ' (with CSS)' : '') }),
                       new HR()]

        // Basic Pagination
        let h_basic = new H({ level: 2, value: 'Basic Pagination' })
        let basic_pagination = new Div({ class: 'pagination' }).add_elements(new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link disabled', href: '#', value: '«' })),
                                                                             new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link active'  , href: '#', value: '1' })),
                                                                             new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link'         , href: '#', value: '2' })),
                                                                             new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link'         , href: '#', value: '3' })),
                                                                             new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link'         , href: '#', value: '»' })))

        // Large Pagination
        let h_large = new H({ level: 2, value: 'Large Pagination' })
        let large_pagination = new Div({ class: 'pagination pagination-lg' }).add_elements(new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '«' })),
                                                                                          new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link active', href: '#', value: '1' })),
                                                                                          new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '2' })),
                                                                                          new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '3' })),
                                                                                          new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '»' })))

        // Small Pagination
        let h_small = new H({ level: 2, value: 'Small Pagination' })
        let small_pagination = new Div({ class: 'pagination pagination-sm' }).add_elements(new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '«' })),
                                                                                          new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link active', href: '#', value: '1' })),
                                                                                          new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '2' })),
                                                                                          new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '3' })),
                                                                                          new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '»' })))

        // Centered Pagination
        let h_centered = new H({ level: 2, value: 'Centered Pagination' })
        let centered_pagination = new Div({ class: 'pagination pagination-center' }).add_elements(new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: 'Previous' })),
                                                                                                 new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '1' })),
                                                                                                 new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link active', href: '#', value: '2' })),
                                                                                                 new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '3' })),
                                                                                                 new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: 'Next' })))

        // Working with items
        let h_working = new H({ level: 2, value: 'Working with Many Pages' })
        let working_pagination = new Div({ class: 'pagination' }).add_elements(new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: 'Previous' })),
                                                                               new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '1' })),
                                                                               new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '2' })),
                                                                               new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link active', href: '#', value: '3' })),
                                                                               new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '...' })),
                                                                               new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '8' })),
                                                                               new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '9' })),
                                                                               new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '10' })),
                                                                               new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: 'Next' })))

        // Rounded Pagination
        let h_rounded = new H({ level: 2, value: 'Rounded Pagination' })
        let rounded_pagination = new Div({ class: 'pagination pagination-rounded' }).add_elements(new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '«' })),
                                                                                                 new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '1' })),
                                                                                                 new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link active', href: '#', value: '2' })),
                                                                                                 new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '3' })),
                                                                                                 new Div({ class: 'pagination-item' }).add_elements(new A({ class: 'pagination-link', href: '#', value: '»' })))

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_basic, basic_pagination,
            h_large, large_pagination,
            h_small, small_pagination,
            h_centered, centered_pagination,
            h_working, working_pagination,
            h_rounded, rounded_pagination
        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_pagination.apply_framework()
            this.css_typography.apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Pagination.define()