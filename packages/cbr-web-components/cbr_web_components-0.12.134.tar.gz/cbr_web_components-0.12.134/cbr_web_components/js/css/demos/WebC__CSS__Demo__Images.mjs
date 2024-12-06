import Web_Component   from '../../core/Web_Component.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import HR              from '../../core/HR.mjs';
import Text            from '../../core/Text.mjs';
import Image           from '../../core/Image.mjs';
import Figure          from '../../core/Figure.mjs';
import Fig_Caption     from '../../core/Fig_Caption.mjs';
import CSS__Images     from '../CSS__Images.mjs';
import CSS__Typography from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__Images extends Web_Component {
    load_attributes() {
        this.css_images = new CSS__Images(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'images-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Images Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Responsive Images
        let h_responsive = new H({ level: 2, value: 'Responsive Images' })
        let responsive_demo = new Div({ class: 'demo-section' }).add_elements(
            new Image({ class: 'img img-fluid', src: '/assets/dev/img/800x400.png', alt: 'Responsive image' })
        )

        // Image Shapes
        let h_shapes = new H({ level: 2, value: 'Image Shapes' })
        let shapes_demo = new Div({ class: 'demo-section' }).add_elements(
            new Image({ class: 'img img-rounded img-spacing', src: '/assets/dev/img/200x200.png', alt: 'Rounded image' }),
            new Image({ class: 'img img-circle img-spacing', src: '/assets/dev/img/200x200.png', alt: 'Circular image' }),
            new Image({ class: 'img img-thumbnail img-spacing', src: '/assets/dev/img/200x200.png', alt: 'Thumbnail image' })
        )

        // Figure with Caption
        let h_figure = new H({ level: 2, value: 'Figure with Caption' })
        let figure_demo = new Figure({ class: 'figure' }).add_elements(
            new Image({ class: 'figure-img img-fluid', src: '/assets/dev/img/400x300.png', alt: 'Figure example' }),
            new Fig_Caption({ class: 'figure-caption figure-caption-center', value: 'A caption for the above image' })
        )

        // Image Alignment
        let h_alignment = new H({ level: 2, value: 'Image Alignment' })
        let alignment_demo = new Div({ class: 'demo-section clearfix' }).add_elements(
            new Image({ class: 'img img-thumbnail img-start img-spacing-start', src: '/assets/dev/img/200x200.png', alt: 'Left aligned image' }),
            new Image({ class: 'img img-thumbnail img-end img-spacing-end', src: '/assets/dev/img/200x200.png', alt: 'Right aligned image' }),
            new Text({ value: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris. Vivamus hendrerit arcu sed erat molestie vehicula. Sed auctor neque eu tellus rhoncus ut eleifend nibh porttitor. Ut in nulla enim. Phasellus molestie magna non est bibendum non venenatis nisl tempor. Suspendisse dictum feugiat nisl ut dapibus. Mauris iaculis porttitor posuere. Praesent id metus massa, ut blandit odio.' })
        )

        // Object Fit Examples
        let h_objectfit = new H({ level: 2, value: 'Object Fit Variants' })
        let objectfit_demo = new Div({ class: 'demo-section' }).add_elements(
            new Div({ style: 'width: 200px; height: 200px; display: inline-block; margin: 10px;' })
                .add_elements(new Image({ class: 'img-cover', src: '/assets/dev/img/400x300.png', alt: 'Cover fit' })),
            new Div({ style: 'width: 200px; height: 200px; display: inline-block; margin: 10px;' })
                .add_elements(new Image({ class: 'img-contain', src: '/assets/dev/img/400x300.png', alt: 'Contain fit' })),
            new Div({ style: 'width: 200px; height: 200px; display: inline-block; margin: 10px;' })
                .add_elements(new Image({ class: 'img-fill', src: '/assets/dev/img/400x300.png', alt: 'Fill fit' }))
        )

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_responsive, responsive_demo,
            h_shapes, shapes_demo,
            h_figure, figure_demo,
            h_alignment, alignment_demo,
            h_objectfit, objectfit_demo
        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_images.apply_framework()
            this.css_typography.apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Images.define()