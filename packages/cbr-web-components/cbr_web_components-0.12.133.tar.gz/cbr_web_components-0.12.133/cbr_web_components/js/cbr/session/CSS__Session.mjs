export default class CSS__Session {
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
            ".session-indicator": {
                display: "flex",
                alignItems: "center",
                gap: "8px",
                padding: "4px",
                backgroundColor: "rgba(0, 0, 0, 0.8)",
                borderRadius: "4px",
                minHeight: "40px"
            },

            ".session-item": {
                display: "flex",
                alignItems: "center",
                gap: "8px",
                padding: "4px 12px",
                borderRadius: "4px",
                cursor: "pointer",
                transition: "all 0.2s ease",
                backgroundColor: "rgba(255, 255, 255, 0.1)"
            },

            ".session-item:hover": {
                backgroundColor: "rgba(255, 255, 255, 0.15)"
            },

            ".session-item.active": {
                backgroundColor: "rgba(76, 175, 80, 0.2)",
                borderLeft: "3px solid #4caf50"
            },

            ".session-text": {
                color: "#ffffff",
                fontSize: "14px",
                fontWeight: "500"
            },

            ".session-icon": {
                width: "16px",
                height: "16px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#ffffff"
            }
        }
    }
}