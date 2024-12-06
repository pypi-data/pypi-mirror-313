export default class CSS__List_Groups {
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
            // Base list group
            ".list-group": {
                display: "flex",
                flexDirection: "column",
                paddingLeft: "0",
                marginBottom: "0",
                borderRadius: "0.375rem"
            },

            // List group items
            ".list-group-item": {
                position: "relative",
                display: "block",
                padding: "0.75rem 1.25rem",
                backgroundColor: "#fff",
                border: "1px solid rgba(0, 0, 0, 0.125)"
            },

            ".list-group-item:first-child": {
                borderTopLeftRadius: "inherit",
                borderTopRightRadius: "inherit"
            },

            ".list-group-item:last-child": {
                borderBottomLeftRadius: "inherit",
                borderBottomRightRadius: "inherit"
            },

            ".list-group-item + .list-group-item": {
                borderTop: "0"
            },

            // Active state
            ".list-group-item.active": {
                zIndex: "2",
                backgroundColor: "var(--primary-color, #1a73e8)",
                borderColor: "var(--primary-color, #1a73e8)",
                color: "#fff"
            },

            // Disabled state
            ".list-group-item.disabled": {
                pointerEvents: "none",
                backgroundColor: "#f8f9fa",
                color: "#6c757d"
            },

            // Interactive items
            ".list-group-item-action": {
                width: "100%",
                textAlign: "inherit",
                color: "#495057",
                textDecoration: "none",
                cursor: "pointer"
            },

            ".list-group-item-action:hover": {
                zIndex: "1",
                backgroundColor: "#f8f9fa",
                color: "#495057",
                textDecoration: "none"
            },

            // Contextual variants using our existing color system
            ".list-group-item-primary": {
                backgroundColor: "rgba(26, 115, 232, 0.1)",
                color: "#1a73e8"
            },

            ".list-group-item-secondary": {
                backgroundColor: "rgba(95, 99, 104, 0.1)",
                color: "#5f6368"
            },

            ".list-group-item-success": {
                backgroundColor: "rgba(24, 128, 56, 0.1)",
                color: "#188038"
            },

            ".list-group-item-error": {
                backgroundColor: "rgba(217, 48, 37, 0.1)",
                color: "#d93025"
            },

            ".list-group-item-warning": {
                backgroundColor: "rgba(249, 171, 0, 0.1)",
                color: "#f9ab00"
            },

            ".list-group-item-info": {
                backgroundColor: "rgba(25, 103, 210, 0.1)",
                color: "#1967d2"
            },

            // Horizontal variation
            ".list-group-horizontal": {
                flexDirection: "row"
            },

            ".list-group-horizontal .list-group-item": {
                borderRightWidth: "0",
                borderBottomWidth: "1px"
            },

            ".list-group-horizontal .list-group-item:first-child": {
                borderBottomLeftRadius: "0.375rem",
                borderTopRightRadius: "0"
            },

            ".list-group-horizontal .list-group-item:last-child": {
                borderRightWidth: "1px",
                borderBottomRightRadius: "0.375rem",
                borderTopRightRadius: "0"
            },

            // Flush variation (no borders)
            ".list-group-flush": {
                borderRadius: "0"
            },

            ".list-group-flush .list-group-item": {
                borderWidth: "0 0 1px",
                borderRadius: "0"
            },

            ".list-group-flush .list-group-item:last-child": {
                borderBottomWidth: "0"
            },

            // Numbered variation
            ".list-group-numbered": {
                listStyle: "none",
                counterReset: "section"
            },

            ".list-group-numbered .list-group-item": {
                counterIncrement: "section"
            },

            ".list-group-numbered .list-group-item::before": {
                content: "counter(section) \". \"",
                marginRight: "0.5rem"
            }
        }
    }
}