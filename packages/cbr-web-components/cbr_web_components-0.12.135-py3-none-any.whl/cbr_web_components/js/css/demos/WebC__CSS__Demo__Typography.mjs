import Web_Component   from "../../core/Web_Component.mjs";
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import HR              from '../../core/HR.mjs';
import P               from '../../core/P.mjs';
import Text            from '../../core/Text.mjs';
import CSS__Typography from '../CSS__Typography.mjs'

export default class WebC__CSS__Demo__Typography extends Web_Component {


    load_attributes() {
        this.framework      = this.getAttribute('framework')
        this.css_typography = new CSS__Typography(this, this.framework)
    }



    render() {
        let div_root = new Div({id: 'typography-demo'})

        const hr_separator      = new HR()
        const text_demo_title   = new Text()
        text_demo_title.value = `Typography Demo (${this.framework || 'Default'})`

        div_root.add_elements(hr_separator, text_demo_title, hr_separator)

        // Headings Section
        let h_headings = new H({level: 2, value: 'Headings'})
        let headings = [
            new H({level: 1, value: 'Mega Heading',  class: 'type-mega'}),
            new H({level: 2, value: 'Hero Heading',  class: 'type-hero'}),
            new H({level: 3, value: 'Title Heading', class: 'type-title'}),
            new H({level: 4, value: 'XL Heading',    class: 'type-xl'}),
            new H({level: 5, value: 'LG Heading',    class: 'type-lg'}),
            new H({level: 6, value: 'MD Heading',    class: 'type-md'})
        ]

        // Text weights
        let h_weights = new H({level: 2, value: 'Text Weights'})
        let weights = [
            new P({value: 'Thin text',    class: 'weight-thin'}),
            new P({value: 'Light text',   class: 'weight-light'}),
            new P({value: 'Normal text',  class: 'weight-normal'}),
            new P({value: 'Medium text',  class: 'weight-medium'}),
            new P({value: 'Bold text',    class: 'weight-bold'}),
            new P({value: 'Heavy text',   class: 'weight-heavy'})
        ]

        // Text Alignments
        let h_alignments = new H({level: 2, value: 'Text Alignments'})
        let alignments = [
            new P({value: 'Start aligned text',  class: 'align-start'}),
            new P({value: 'Center aligned text', class: 'align-center'}),
            new P({value: 'End aligned text',    class: 'align-end'})
        ]

        // Text Styles
        let h_styles = new H({level: 2, value: 'Text Styles'})
        let styles = [
            new P({value: 'Normal style text', class: 'style-normal'}),
            new P({value: 'Italic style text', class: 'style-italic'})
        ]

        // Text Transforms
        let h_transforms = new H({level: 2, value: 'Text Transforms'})
        let transforms = [
            new P({value: 'LOWERCASE TEXT', class: 'transform-lower'}),
            new P({value: 'uppercase text', class: 'transform-upper'}),
            new P({value: 'capitalize text', class: 'transform-capital'})
        ]

        // Colors
        let h_colors = new H({level: 2, value: 'Text Colors'})
        let colors = [
            new P({value: 'Primary Color',   class: 'color-primary'}),
            new P({value: 'Secondary Color', class: 'color-secondary'}),
            new P({value: 'Accent Color',    class: 'color-accent'}),
            new P({value: 'Success Color',   class: 'color-success'}),
            new P({value: 'Warning Color',   class: 'color-warning'}),
            new P({value: 'Error Color',     class: 'color-error'}),
            new P({value: 'Info Color',      class: 'color-info'}),
            new P({value: 'Muted Color',     class: 'color-muted'})
        ]

        // Backgrounds
        let h_backgrounds = new H({level: 2, value: 'Background Colors'})
        let backgrounds = [
            new P({value: 'Primary Background',   class: 'bg-primary color-white'}),
            new P({value: 'Secondary Background', class: 'bg-secondary color-white'}),
            new P({value: 'Accent Background',    class: 'bg-accent color-white'}),
            new P({value: 'Success Background',   class: 'bg-success color-white'}),
            new P({value: 'Warning Background',   class: 'bg-warning color-white'}),
            new P({value: 'Error Background',     class: 'bg-error color-white'}),
            new P({value: 'Info Background',      class: 'bg-info color-white'}),
            new P({value: 'Muted Background',     class: 'bg-muted color-white'})
        ]

        // Special Text Types
        let h_special = new H({level: 2, value: 'Special Text Types'})
        let special = [
            new P({value: 'This is a lead paragraph with important opening text.',     class: 'type-lead'}),
            new P({value: 'This is a regular body text paragraph.',                    class: 'type-body'}),
            new P({value: 'This is a caption text, usually used for additional info.', class: 'type-caption'})
        ]

        // Add all elements to root
        div_root.add_elements(
            h_headings   , ...headings      ,
            h_weights    , ...weights       ,
            h_alignments , ...alignments    ,
            h_styles     , ...styles        ,
            h_transforms , ...transforms    ,
            h_colors     , ...colors        ,
            h_backgrounds, ...backgrounds   ,
            h_special    , ...special
        )

        this.css_typography.apply_framework()
        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Typography.define()