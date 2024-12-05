export default class CSS__Side_Menu {
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
            // Menu container
            ".side-menu": {
                width: "240px",
                padding: "8px 0",
                display: "flex",
                flexDirection: "column",
                backgroundColor: "#ffffff"
            },

            // Menu item
            ".side-menu-item": {
                display: "flex",
                alignItems: "center",
                padding: "12px 16px",
                margin: "2px 8px",
                borderRadius: "8px",
                cursor: "pointer",
                transition: "all 0.2s ease-in-out"
            },

            ".side-menu-item:hover": {
                backgroundColor: "rgba(38, 198, 218, 0.1)"
            },

            // Menu link
            ".side-menu-link": {
                display: "flex",
                alignItems: "center",
                textDecoration: "none",
                color: "#54667a",
                width: "100%",
                gap: "12px"
            },

            // Side menu icon specific styles
            ".side-menu-icon": {
                fontSize: "20px",
                color: "#96a5ac",
                minWidth: "24px",
                height: "24px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center"
            },

            // Menu text
            ".side-menu-text": {
                fontSize: "15px",
                fontWeight: "400",
                color: "inherit"
            },

            // Active states
            ".side-menu-item.active": {
                backgroundColor: "#26c6da"
            },

            ".side-menu-item.active .side-menu-link": {
                color: "#ffffff"
            },

            ".side-menu-item.active .icon": {
                color: "#ffffff"
            },

            // Hover states
            ".side-menu-item:hover .side-menu-link": {
                color: "#26c6da"
            },

            ".side-menu-item:hover .icon": {
                color: "#26c6da"
            },

            // Active items don't show hover color
            ".side-menu-item.active:hover .side-menu-link": {
                color: "#ffffff"
            },

            ".side-menu-item.active:hover .icon": {
                color: "#ffffff"
            }
        }
    }
}