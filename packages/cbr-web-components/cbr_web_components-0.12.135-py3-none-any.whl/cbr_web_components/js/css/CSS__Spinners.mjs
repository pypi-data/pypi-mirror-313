export default class CSS__Spinners {
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
            // Base spinner styles
            ".spinner": {
                display: "inline-block",
                width: "2rem",
                height: "2rem",
                verticalAlign: "text-bottom",
                border: "0.25em solid currentColor",
                borderRightColor: "transparent",
                borderRadius: "50%",
                animation: "spinner-border .75s linear infinite"
            },

            // Border spinner animation
            "@keyframes spinner-border": {
                "100%": {
                    transform: "rotate(360deg)"
                }
            },

            // Growing spinner
            ".spinner-grow": {
                display: "inline-block",
                width: "2rem",
                height: "2rem",
                verticalAlign: "text-bottom",
                backgroundColor: "currentColor",
                borderRadius: "50%",
                opacity: "0",
                animation: "spinner-grow .75s linear infinite"
            },

            // Grow spinner animation
            "@keyframes spinner-grow": {
                "0%": {
                    transform: "scale(0)"
                },
                "50%": {
                    opacity: "1",
                    transform: "none"
                }
            },

            // Small size variation
            ".spinner-sm": {
                width: "1rem",
                height: "1rem",
                borderWidth: "0.2em"
            },

            ".spinner-grow-sm": {
                width: "1rem",
                height: "1rem"
            },

            // Color variations using our system
            ".spinner-primary": {
                color: "#1a73e8"
            },

            ".spinner-secondary": {
                color: "#5f6368"
            },

            ".spinner-success": {
                color: "#188038"
            },

            ".spinner-error": {
                color: "#d93025"
            },

            ".spinner-warning": {
                color: "#f9ab00"
            },

            ".spinner-info": {
                color: "#1967d2"
            },

            ".spinner-light": {
                color: "#f8f9fa"
            },

            ".spinner-dark": {
                color: "#212529"
            },

            // Flex utilities for centering
            ".spinner-flex": {
                display: "flex",
                alignItems: "center",
                justifyContent: "center"
            },

            // Text alignment with spinner
            ".spinner-text": {
                marginLeft: "0.5rem"
            },

            // Button spinner positioning
            ".btn .spinner": {
                verticalAlign: "middle",
                marginRight: "0.5rem"
            },

            ".btn .spinner-sm": {
                marginRight: "0.25rem"
            }
        }
    }
}