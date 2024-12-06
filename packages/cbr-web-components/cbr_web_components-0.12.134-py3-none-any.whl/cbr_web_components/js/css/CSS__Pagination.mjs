export default class CSS__Pagination {
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
            // Base pagination container
            ".pagination": {
                display: "flex",
                padding: "0",
                margin: "0",
                listStyle: "none",
                gap: "4px"
            },

            // Individual page items
            ".pagination-item": {
                display: "flex"
            },

            // Page links
            ".pagination-link": {
                position: "relative",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "0.375rem 0.75rem",
                minWidth: "2.5rem",
                fontSize: "1rem",
                border: "1px solid #dee2e6",
                backgroundColor: "#fff",
                color: "#1a73e8",
                textDecoration: "none",
                transition: "color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out",
                cursor: "pointer",
                borderRadius: "0.25rem"
            },

            ".pagination-link:hover": {
                backgroundColor: "#e9ecef",
                borderColor: "#dee2e6",
                color: "#0a58ca",
                zIndex: "2"
            },

            ".pagination-link.active": {
                zIndex: "3",
                color: "#fff",
                backgroundColor: "#1a73e8",
                borderColor: "#1a73e8",
                cursor: "default"
            },

            ".pagination-link.disabled": {
                color: "#6c757d",
                pointerEvents: "none",
                backgroundColor: "#fff",
                borderColor: "#dee2e6",
                cursor: "default"
            },

            // Sizing variations
            ".pagination-lg .pagination-link": {
                padding: "0.75rem 1.5rem",
                fontSize: "1.25rem",
                minWidth: "3rem"
            },

            ".pagination-sm .pagination-link": {
                padding: "0.25rem 0.5rem",
                fontSize: "0.875rem",
                minWidth: "2rem"
            },

            // Alignment variations
            ".pagination-center": {
                justifyContent: "center"
            },

            ".pagination-end": {
                justifyContent: "flex-end"
            },

            // Rounded variation
            ".pagination-rounded .pagination-link": {
                borderRadius: "50%",
                margin: "0 2px"
            }
        }
    }
}