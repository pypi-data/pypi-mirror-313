import Web_Component   from '../../core/Web_Component.mjs';
import A               from '../../core/A.mjs';
import Button          from '../../core/Button.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import Input           from '../../core/Input.mjs';
import HR              from '../../core/HR.mjs';
import Nav             from '../../core/Nav.mjs';
import Text            from '../../core/Text.mjs';
import CSS__Navbar     from '../CSS__Navbar.mjs';
import CSS__Buttons    from '../CSS__Buttons.mjs';
import CSS__Typography from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__Navbar extends Web_Component {
    load_attributes() {
        this.css_navbar     = new CSS__Navbar   (this)
        this.css_buttons    = new CSS__Buttons   (this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'navbar-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Navbar Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Basic Light Navbar
        let h_basic = new H({ level: 2, value: 'Basic Light Navbar' })
        let basic_navbar = new Nav({ class: 'navbar navbar-light' }).add_elements(
            new A({ class: 'navbar-brand', href: '#', value: 'Brand' }),
            new Button({ class: 'navbar-toggler', value: '☰' }),
            new Div({ class: 'navbar-collapse show' }).add_elements(
                new Div({ class: 'navbar-nav' }).add_elements(
                    new A({ class: 'navbar-nav-item active', href: '#', value: 'Home' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Features' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Pricing' }),
                    new A({ class: 'navbar-nav-item disabled', href: '#', value: 'Disabled' })
                )
            )
        )

        // Dark Navbar
        let h_dark = new H({ level: 2, value: 'Dark Navbar' })
        let dark_navbar = new Nav({ class: 'navbar navbar-dark' }).add_elements(
            new A({ class: 'navbar-brand', href: '#', value: 'Brand' }),
            new Button({ class: 'navbar-toggler', value: '☰' }),
            new Div({ class: 'navbar-collapse show' }).add_elements(
                new Div({ class: 'navbar-nav' }).add_elements(
                    new A({ class: 'navbar-nav-item active', href: '#', value: 'Home' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Features' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Pricing' })
                ),
                new Div({ class: 'navbar-text', value: 'Signed in as: Mark Otto' })
            )
        )

        // Navbar with Dropdown
        let h_dropdown = new H({ level: 2, value: 'Navbar with Dropdown' })
        let dropdown_navbar = new Nav({ class: 'navbar navbar-light' }).add_elements(
            new A({ class: 'navbar-brand', href: '#', value: 'Brand' }),
            new Button({ class: 'navbar-toggler', value: '☰' }),
            new Div({ class: 'navbar-collapse show' }).add_elements(
                new Div({ class: 'navbar-nav' }).add_elements(
                    new A({ class: 'navbar-nav-item active', href: '#', value: 'Home' }),
                    new Div({ class: 'navbar-dropdown' }).add_elements(
                        new A({ class: 'navbar-nav-item', href: '#', value: 'Dropdown' }),
                        new Div({ class: 'navbar-dropdown-menu' }).add_elements(
                            new A({ class: 'navbar-dropdown-item', href: '#', value: 'Action' }),
                            new A({ class: 'navbar-dropdown-item', href: '#', value: 'Another action' }),
                            new A({ class: 'navbar-dropdown-item', href: '#', value: 'Something else here' })
                        )
                    ),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Features' })
                )
            )
        )

        // Form in Navbar
        let h_form = new H({ level: 2, value: 'Navbar with Form' })
        let form_navbar = new Nav({ class: 'navbar navbar-light' }).add_elements(
            new A({ class: 'navbar-brand', href: '#', value: 'Brand' }),
            new Div({ class: 'navbar-collapse show' }).add_elements(
                new Div({ class: 'navbar-nav' }).add_elements(
                    new A({ class: 'navbar-nav-item active', href: '#', value: 'Home' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Features' })
                ),
                new Div({ class: 'navbar-text' }).add_elements(
                    new Button({ class: 'btn btn-outline-success', value: 'Search' })
                )
            )
        )

        let h_with_search= new H({ level: 2, value: 'Navbar with Form' })
        // Dark Theme Navbar
        let dark_navbar_with_search = new Nav({ class: 'navbar navbar-dark bg-dark' }).add_elements(
            new A({ class: 'navbar-brand', href: '#', value: 'Navbar' }),
            new Div({ class: 'navbar-collapse show' }).add_elements(
                new Div({ class: 'navbar-nav' }).add_elements(
                    new A({ class: 'navbar-nav-item active', href: '#', value: 'Home' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Features' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Pricing' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'About' })
                ),
                new Div({ class: 'navbar-search' }).add_elements(
                    new Input({ type: 'text', class: 'search-input', placeholder: 'Search' }),
                    new Button({ class: 'btn btn-outline-light', value: 'Search' })
                )
            )
        )

        // Primary Theme Navbar
        let primary_navbar_with_search = new Nav({ class: 'navbar navbar-dark bg-primary' }).add_elements(
            new A({ class: 'navbar-brand', href: '#', value: 'Navbar' }),
            new Div({ class: 'navbar-collapse show' }).add_elements(
                new Div({ class: 'navbar-nav' }).add_elements(
                    new A({ class: 'navbar-nav-item active', href: '#', value: 'Home' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Features' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Pricing' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'About' })
                ),
                new Div({ class: 'navbar-search' }).add_elements(
                    new Input({ type: 'text', class: 'search-input', placeholder: 'Search' }),
                    new Button({ class: 'btn btn-outline-light', value: 'Search' })
                )
            )
        )

        // Light Theme Navbar (with custom background)
        let light_navbar_with_search = new Nav({class: 'navbar navbar-light',  style: 'background-color: #e3f2fd;'
        }).add_elements(
            new A({ class: 'navbar-brand', href: '#', value: 'Navbar' }),
            new Div({ class: 'navbar-collapse show' }).add_elements(
                new Div({ class: 'navbar-nav' }).add_elements(
                    new A({ class: 'navbar-nav-item active', href: '#', value: 'Home' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Features' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'Pricing' }),
                    new A({ class: 'navbar-nav-item', href: '#', value: 'About' })
                ),
                new Div({ class: 'navbar-search' }).add_elements(
                    new Input({ type: 'text', class: 'search-input', placeholder: 'Search' }),
                    new Button({ class: 'btn btn-outline-primary', value: 'Search' })
                )
            )
        )
        let search_navbar = [dark_navbar_with_search, primary_navbar_with_search,light_navbar_with_search ]



        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_basic       , basic_navbar    ,
            h_dark        , dark_navbar     ,
            h_dropdown    , dropdown_navbar ,
            h_form        , form_navbar     ,
            h_with_search , ...search_navbar)

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_buttons   .apply_framework()
            this.css_navbar    .apply_framework()
            this.css_typography.apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Navbar.define()