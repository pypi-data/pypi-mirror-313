export default class CSS__Navs_Tabs {
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
            // Base nav
            ".nav": {
                display: "flex",
                flexWrap: "wrap",
                padding: "0",
                margin: "0",
                listStyle: "none"
            },

            // Nav links
            ".nav-link": {
                display: "block",
                padding: "0.5rem 1rem",
                color: "#1a73e8",
                textDecoration: "none",
                transition: "color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out"
            },

            ".nav-link:hover": {
                color: "#1557b0"
            },

            ".nav-link.disabled": {
                color: "#6c757d",
                pointerEvents: "none",
                cursor: "default"
            },

            ".nav-link.active": {
                color: "#495057",
                cursor: "default"
            },

            // Basic tabs
            ".nav-tabs": {
                borderBottom: "1px solid #dee2e6"
            },

            ".nav-tabs .nav-link": {
                margin: "0",
                border: "1px solid transparent",
                borderTopLeftRadius: "0.25rem",
                borderTopRightRadius: "0.25rem",
                background: "none"
            },

            ".nav-tabs .nav-link:hover": {
                borderColor: "#e9ecef #e9ecef #dee2e6",
                isolation: "isolate"
            },

            ".nav-tabs .nav-link.active": {
                color: "#495057",
                backgroundColor: "#fff",
                borderColor: "#dee2e6 #dee2e6 #fff"
            },

            // Pills
            ".nav-pills .nav-link": {
                borderRadius: "0.25rem",
                background: "none"
            },

            ".nav-pills .nav-link.active": {
                color: "#fff",
                backgroundColor: "#1a73e8"
            },

            // Fill and justify variations
            ".nav-fill .nav-item": {
                flex: "1 1 auto",
                textAlign: "center"
            },

            ".nav-justified .nav-item": {
                flexBasis: "0",
                flexGrow: "1",
                textAlign: "center"
            },

            // Vertical variation
            ".nav-vertical": {
                flexDirection: "column"
            },

            ".nav-vertical .nav-link": {
                padding: "0.5rem 1rem",
                marginBottom: "0"
            },

            // Tab content
            ".tab-content": {
                padding: "1rem 0"
            },

            ".tab-pane": {
                display: "none"
            },

            ".tab-pane.active": {
                display: "block"
            },

            // Underline variation (material design style)
            ".nav-underline": {
                borderBottom: "2px solid #dee2e6"
            },

            ".nav-underline .nav-link": {
                padding: "0.5rem 0",
                marginRight: "1rem",
                borderBottom: "2px solid transparent",
                marginBottom: "-2px"
            },

            ".nav-underline .nav-link.active": {
                borderBottom: "2px solid #1a73e8",
                fontWeight: "500"
            },

            // Alignment variations
            ".nav-center": {
                justifyContent: "center"
            },

            ".nav-end": {
                justifyContent: "flex-end"
            },

            // Extra small nav variation
            ".nav-sm .nav-link": {
                padding: "0.25rem 0.5rem",
                fontSize: "0.875rem"
            }
        }
    }
}