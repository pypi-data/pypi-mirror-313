export default class CSS__Buttons {
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
            // Base button styling
            ".btn": {
                display: "inline-flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "0.625rem 1.25rem",
                fontSize: "0.875rem",
                fontWeight: "500",
                lineHeight: "1.25",
                textAlign: "center",
                textDecoration: "none",
                whiteSpace: "nowrap",
                verticalAlign: "middle",
                cursor: "pointer",
                userSelect: "none",
                border: "1px solid transparent",
                borderRadius: "0.375rem",
                transition: "all 0.2s ease-in-out",
                gap: "0.5rem",
                minWidth: "2.5rem",
                position: "relative"
            },

            // States
            ".btn:focus": {
                outline: "none",
                boxShadow: "0 0 0 2px rgba(13, 110, 253, 0.5)"
            },

            ".btn:disabled, .btn.disabled": {
                opacity: "0.65",
                pointerEvents: "none",
                cursor: "not-allowed"
            },

            // Regular Buttons
            ".btn-primary": {
                backgroundColor: "#0d6efd",
                color: "#ffffff",
                borderColor: "#0d6efd"
            },
            ".btn-primary:hover": {
                backgroundColor: "#0b5ed7",
                borderColor: "#0b5ed7"
            },
            ".btn-primary:active": {
                backgroundColor: "#0a58ca",
                borderColor: "#0a58ca"
            },

            ".btn-secondary": {
                backgroundColor: "#6c757d",
                color: "#ffffff",
                borderColor: "#6c757d"
            },
            ".btn-secondary:hover": {
                backgroundColor: "#5c636a",
                borderColor: "#5c636a"
            },
            ".btn-secondary:active": {
                backgroundColor: "#565e64",
                borderColor: "#565e64"
            },

            ".btn-success": {
                backgroundColor: "#198754",
                color: "#ffffff",
                borderColor: "#198754"
            },
            ".btn-success:hover": {
                backgroundColor: "#157347",
                borderColor: "#157347"
            },
            ".btn-success:active": {
                backgroundColor: "#146c43",
                borderColor: "#146c43"
            },

            ".btn-danger": {
                backgroundColor: "#dc3545",
                color: "#ffffff",
                borderColor: "#dc3545"
            },
            ".btn-danger:hover": {
                backgroundColor: "#bb2d3b",
                borderColor: "#bb2d3b"
            },
            ".btn-danger:active": {
                backgroundColor: "#b02a37",
                borderColor: "#b02a37"
            },

            ".btn-warning": {
                backgroundColor: "#ffc107",
                color: "#000000",
                borderColor: "#ffc107"
            },
            ".btn-warning:hover": {
                backgroundColor: "#ffca2c",
                borderColor: "#ffca2c"
            },
            ".btn-warning:active": {
                backgroundColor: "#ffcd39",
                borderColor: "#ffcd39"
            },

            ".btn-info": {
                backgroundColor: "#0dcaf0",
                color: "#000000",
                borderColor: "#0dcaf0"
            },
            ".btn-info:hover": {
                backgroundColor: "#31d2f2",
                borderColor: "#31d2f2"
            },
            ".btn-info:active": {
                backgroundColor: "#3dd5f3",
                borderColor: "#3dd5f3"
            },

            ".btn-light": {
                backgroundColor: "#f8f9fa",
                color: "#000000",
                borderColor: "#f8f9fa"
            },
            ".btn-light:hover": {
                backgroundColor: "#f9fafb",
                borderColor: "#f9fafb"
            },
            ".btn-light:active": {
                backgroundColor: "#f9fafb",
                borderColor: "#f9fafb"
            },

            ".btn-dark": {
                backgroundColor: "#212529",
                color: "#ffffff",
                borderColor: "#212529"
            },
            ".btn-dark:hover": {
                backgroundColor: "#1c1f23",
                borderColor: "#1c1f23"
            },
            ".btn-dark:active": {
                backgroundColor: "#1a1e21",
                borderColor: "#1a1e21"
            },

            // Outline Buttons
            ".btn-outline-primary": {
                backgroundColor: "transparent",
                color: "#0d6efd",
                borderColor: "#0d6efd"
            },
            ".btn-outline-primary:hover": {
                backgroundColor: "#0d6efd",
                color: "#ffffff"
            },

            ".btn-outline-secondary": {
                backgroundColor: "transparent",
                color: "#6c757d",
                borderColor: "#6c757d"
            },
            ".btn-outline-secondary:hover": {
                backgroundColor: "#6c757d",
                color: "#ffffff"
            },

            ".btn-outline-success": {
                backgroundColor: "transparent",
                color: "#198754",
                borderColor: "#198754"
            },
            ".btn-outline-success:hover": {
                backgroundColor: "#198754",
                color: "#ffffff"
            },

            ".btn-outline-danger": {
                backgroundColor: "transparent",
                color: "#dc3545",
                borderColor: "#dc3545"
            },
            ".btn-outline-danger:hover": {
                backgroundColor: "#dc3545",
                color: "#ffffff"
            },

            ".btn-outline-warning": {
                backgroundColor: "transparent",
                color: "#ffc107",
                borderColor: "#ffc107"
            },
            ".btn-outline-warning:hover": {
                backgroundColor: "#ffc107",
                color: "#000000"
            },

            ".btn-outline-info": {
                backgroundColor: "transparent",
                color: "#0dcaf0",
                borderColor: "#0dcaf0"
            },
            ".btn-outline-info:hover": {
                backgroundColor: "#0dcaf0",
                color: "#000000"
            },

            ".btn-outline-light": {
                backgroundColor: "transparent",
                color: "#f8f9fa",
                borderColor: "#f8f9fa"
            },
            ".btn-outline-light:hover": {
                backgroundColor: "#f8f9fa",
                color: "#000000"
            },

            ".btn-outline-dark": {
                backgroundColor: "transparent",
                color: "#212529",
                borderColor: "#212529"
            },
            ".btn-outline-dark:hover": {
                backgroundColor: "#212529",
                color: "#ffffff"
            },

            // Link Button
            ".btn-link": {
                fontWeight: "400",
                color: "#0d6efd",
                textDecoration: "underline",
                backgroundColor: "transparent",
                border: "0"
            },
            ".btn-link:hover": {
                color: "#0a58ca"
            },

            // Size variations
            ".btn-sm": {
                padding: "0.375rem 0.75rem",
                fontSize: "0.75rem",
                borderRadius: "0.25rem"
            },

            ".btn-lg": {
                padding: "0.75rem 1.5rem",
                fontSize: "1rem",
                borderRadius: "0.5rem"
            },

            // Layout variations
            ".btn-block": {
                display: "flex",
                width: "100%"
            },

            // Button groups
            ".btn-group": {
                display: "inline-flex",
                position: "relative",
                verticalAlign: "middle"
            },

            ".btn-group > .btn": {
                position: "relative",
                flex: "0 1 auto"
            },

            ".btn-group > .btn:not(:first-child)": {
                marginLeft: "-1px",
                borderTopLeftRadius: "0",
                borderBottomLeftRadius: "0"
            },

            ".btn-group > .btn:not(:last-child)": {
                borderTopRightRadius: "0",
                borderBottomRightRadius: "0"
            },

            // Button toolbar
            ".btn-toolbar": {
                display: "flex",
                flexWrap: "wrap",
                gap: "0.5rem"
            },

            // useful classes

            ".hidden"            : { display: "none" }
        }
    }
}