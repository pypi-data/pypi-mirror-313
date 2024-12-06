export default class CSS__Breadcrumbs {
    constructor(target_element) {
        this.target_element = target_element
    }

    apply_framework() {
        if (this.target_element) {
            this.target_element.add_css_rules(this.css_rules__standard())
        }
    }

    css_rules__standard() {
        return {
            // Navigation container
            ".nav-breadcrumb": {
                display: "flex",
                alignItems: "center",
                padding: "0.75rem 0",
                margin: "0",
                listStyle: "none",
                backgroundColor: "transparent"
            },

            // List container
            ".nav-breadcrumb-list": {
                display: "flex",
                flexWrap: "wrap",
                padding: "0",
                margin: "0",
                listStyle: "none"
            },

            // Individual breadcrumb items
            ".nav-breadcrumb-item": {
                display: "flex",
                alignItems: "center",
                color: "#6c757d",
                fontSize: "0.875rem"
            },

            // Separator between items
            ".nav-breadcrumb-item:not(:last-child)::after": {
                display: "inline-block",
                padding: "0 0.5rem",
                color: "#6c757d",
                content: '"/"'
            },

            // Links within breadcrumb items
            ".nav-breadcrumb-link": {
                color: "#6c757d",
                textDecoration: "none",
                transition: "color 0.2s ease-in-out"
            },

            ".nav-breadcrumb-link:hover": {
                color: "#0d6efd",
                textDecoration: "underline"
            },

            // Current/active item
            ".nav-breadcrumb-item-current": {
                color: "#212529",
                fontWeight: "500"
            },

            // Optional icon support
            ".nav-breadcrumb-icon": {
                display: "inline-flex",
                alignItems: "center",
                marginRight: "0.25rem"
            }
        }
    }
}