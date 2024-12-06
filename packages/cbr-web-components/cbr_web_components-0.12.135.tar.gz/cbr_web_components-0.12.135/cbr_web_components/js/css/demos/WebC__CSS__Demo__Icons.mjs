import Web_Component   from '../../core/Web_Component.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import HR              from '../../core/HR.mjs';
import P               from '../../core/P.mjs';
import Text            from '../../core/Text.mjs';
import Icon            from '../icons/Icon.mjs';
import Icon__Mappings  from '../icons/Icon__Mappings.mjs';
import CSS__Icons      from '../icons/CSS__Icons.mjs';
import CSS__Typography from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__Icons extends Web_Component {
    load_attributes() {
        this.css_icons = new CSS__Icons(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    // Helper method to create a category section
    create_category_section(categoryName, icons) {
        const formatted_name = categoryName.replace('_', ' ').toLowerCase()
        const title = formatted_name.charAt(0).toUpperCase() + formatted_name.slice(1)

        // Create the section container
        let section = new Div({ class: 'demo-section mb-4' }).add_elements(
            new H({ level: 2, value: title }),
            new P({ class: 'type-caption mb-2', value: `${Object.keys(icons).length} icons` })
        )

        // Create grid for icons
        let grid = new Div({ class: 'icon-grid' })

        // Add each icon with its name
        Object.entries(icons).forEach(([name, symbol]) => {
            grid.add_elements(
                new Div({ class: 'icon-item' }).add_elements(
                    new Icon({ icon: name, class: 'mb-2' ,spin: true}),
                    new Div({ class: 'icon-name type-sm', value: name })
                )
            )
        })

        section.add_elements(grid)
        return section
    }

    // Helper method to create style variations section
    create_style_variations() {
        return new Div({ class: 'demo-section mb-4' }).add_elements(
            new H({ level: 2, value: 'Style Variations' }),

            // Sizes
            new H({ level: 3, value: 'Sizes', class: 'mt-3 mb-2' }),
            new Div({ class: 'demo-row mb-3' }).add_elements(
                new Icon({ icon: 'star', size: 'xs', class: 'icon-spacing-right' }),
                new Icon({ icon: 'star', size: 'sm', class: 'icon-spacing-right' }),
                new Icon({ icon: 'star', size: 'md', class: 'icon-spacing-right' }),
                new Icon({ icon: 'star', size: 'lg', class: 'icon-spacing-right' }),
                new Icon({ icon: 'star', size: 'xl' })
            ),

            // Colors
            new H({ level: 3, value: 'Colors', class: 'mt-3 mb-2' }),
            new Div({ class: 'demo-row mb-3' }).add_elements(
                new Icon({ icon: 'heart', color: 'primary', class: 'icon-spacing-right' }),
                new Icon({ icon: 'heart', color: 'secondary', class: 'icon-spacing-right' }),
                new Icon({ icon: 'heart', color: 'success', class: 'icon-spacing-right' }),
                new Icon({ icon: 'heart', color: 'error', class: 'icon-spacing-right' }),
                new Icon({ icon: 'heart', color: 'warning', class: 'icon-spacing-right' }),
                new Icon({ icon: 'heart', color: 'info', class: 'icon-spacing-right' }),
                new Icon({ icon: 'heart', color: 'muted' })
            ),

            // Animations
            new H({ level: 3, value: 'Animations', class: 'mt-3 mb-2' }),
            new Div({ class: 'demo-row mb-3' }).add_elements(
                new Icon({ icon: 'arrow-refresh', spin: true, class: 'icon-spacing-right' }),
                new Icon({ icon: 'arrow-repeat', pulse: true, class: 'icon-spacing-right' })
            ),

            // Rotations
            new H({ level: 3, value: 'Rotations', class: 'mt-3 mb-2' }),
            new Div({ class: 'demo-row mb-3' }).add_elements(
                new Icon({ icon: 'arrow-right', class: 'icon-spacing-right' }),
                new Icon({ icon: 'arrow-right', rotate: '90', class: 'icon-spacing-right' }),
                new Icon({ icon: 'arrow-right', rotate: '180', class: 'icon-spacing-right' }),
                new Icon({ icon: 'arrow-right', rotate: '270' })
            )
        )
    }

    // Helper method to create usage examples section
    create_usage_examples() {
        return new Div({ class: 'demo-section mb-4' }).add_elements(
            new H({ level: 2, value: 'Common Usage Examples' }),

            // Button-like examples
            new Div({ class: 'demo-row mb-3' }).add_elements(
                new Div({ class: 'demo-button' }).add_elements(
                    new Icon({ icon: 'plus', class: 'icon-spacing-right' }),
                    new Text({ value: 'Add Item' })
                ),
                new Div({ class: 'demo-button' }).add_elements(
                    new Icon({ icon: 'search', class: 'icon-spacing-right' }),
                    new Text({ value: 'Search' })
                ),
                new Div({ class: 'demo-button demo-button-error' }).add_elements(
                    new Icon({ icon: 'trash', class: 'icon-spacing-right' }),
                    new Text({ value: 'Delete' })
                )
            ),

            // Status examples
            new Div({ class: 'demo-row mb-3' }).add_elements(
                new Div({ class: 'demo-status' }).add_elements(
                    new Icon({ icon: 'success', color: 'success', class: 'icon-spacing-right' }),
                    new Text({ value: 'Task completed' })
                ),
                new Div({ class: 'demo-status' }).add_elements(
                    new Icon({ icon: 'warning', color: 'warning', class: 'icon-spacing-right' }),
                    new Text({ value: 'Low disk space' })
                )
            ),

            // Navigation examples
            new Div({ class: 'demo-nav mb-3' }).add_elements(
                new Div({ class: 'demo-nav-item' }).add_elements(
                    new Icon({ icon: 'home', class: 'icon-spacing-right' }),
                    new Text({ value: 'Home' })
                ),
                new Div({ class: 'demo-nav-item' }).add_elements(
                    new Icon({ icon: 'mail', class: 'icon-spacing-right' }),
                    new Text({ value: 'Messages' })
                ),
                new Div({ class: 'demo-nav-item' }).add_elements(
                    new Icon({ icon: 'settings', class: 'icon-spacing-right' }),
                    new Text({ value: 'Settings' })
                )
            )
        )
    }

    render() {
        let div_root = new Div({ id: 'icons-demo' })

        // Header
        div_root.add_elements(
            new H({ level: 1, value: 'Icon System Demo' }),
            new P({ value: 'A comprehensive icon system using Unicode symbols' }),
            new HR()
        )

        // Add style variations
        div_root.add_elements(this.create_style_variations())

        // Add usage examples
        div_root.add_elements(this.create_usage_examples())

        // Add category sections
        Icon__Mappings.getCategories().forEach(category => {
            const categoryIcons = Icon__Mappings.getCategory(category)
            div_root.add_elements(this.create_category_section(category, categoryIcons))
        })

        // Add custom CSS for the demo
        if (this.apply_css) {
            this.css_icons.apply_framework()
            this.css_typography.apply_framework()
            this.add_css_rules({
                ":host": {"--color-bg-hover" : "#188038", "--color-primary": "#1a73e8", "--color-error": "red", "--color-text-muted": "gray"},
                ".icon-grid": {
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))",
                    gap: "1rem",
                    //padding: "1rem"
                },
                ".icon-item": {
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    //padding: "1rem",
                    border: "1px solid var(--color-border)",
                    borderRadius: "0.5rem",
                    transition: "all 0.2s ease",
                    "&:hover": {
                        backgroundColor: "var(--color-bg-hover)",
                        transform: "translateY(-2px)"
                    }
                },
                ".icon-name": {
                    textAlign: "center",
                    wordBreak: "break-word",
                    fontSize: "0.75rem",
                    color: "var(--color-text-muted)"
                },
                ".demo-button": {
                    display: "inline-flex",
                    alignItems: "center",
                    padding: "0.5rem 1rem",
                    borderRadius: "0.375rem",
                    backgroundColor: "var(--color-primary)",
                    color: "white",
                    marginRight: "1rem",
                    cursor: "pointer",
                    "&:hover": {
                        opacity: "0.9"
                    }
                },
                ".demo-button-error": {
                    backgroundColor: "var(--color-error)"
                },
                ".demo-status": {
                    display: "inline-flex",
                    alignItems: "center",
                    marginRight: "1rem"
                },
                ".demo-nav": {
                    display: "flex",
                    gap: "1rem"
                },
                ".demo-nav-item": {
                    display: "flex",
                    alignItems: "center",
                    padding: "0.5rem",
                    cursor: "pointer",
                    "&:hover": {
                        backgroundColor: "var(--color-bg-hover)"
                    }
                }
            })
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Icons.define()