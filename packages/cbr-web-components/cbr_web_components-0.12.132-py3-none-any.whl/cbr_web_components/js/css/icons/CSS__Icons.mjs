export default class CSS__Icons {

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
            // CSS Custom Properties for theming
            ":host": {
                "--icon-size-xs": "0.75rem",
                "--icon-size-sm": "1rem",
                "--icon-size-md": "1.5rem",
                "--icon-size-lg": "2rem",
                "--icon-size-xl": "3rem",
                "--icon-color": "currentColor",
                "--icon-spacing": "0.25rem"
            },

            // Base icon class
            ".icon": {
                display: "inline-flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "var(--icon-size-md)",
                width: "1em",
                height: "1em",
                verticalAlign: "middle",
                color: "var(--icon-color)",
                userSelect: "none"
            },

            // Size variations
            ".icon-xs": {
                fontSize: "var(--icon-size-xs)"
            },

            ".icon-sm": {
                fontSize: "var(--icon-size-sm)"
            },

            ".icon-md": {
                fontSize: "var(--icon-size-md)"
            },

            ".icon-lg": {
                fontSize: "var(--icon-size-lg)"
            },

            ".icon-xl": {
                fontSize: "var(--icon-size-xl)"
            },

            // Color variations
            ".icon-primary": {
                color: "var(--color-primary)"
            },

            ".icon-secondary": {
                color: "var(--color-secondary)"
            },

            ".icon-success": {
                color: "var(--color-success)"
            },

            ".icon-error": {
                color: "var(--color-error)"
            },

            ".icon-warning": {
                color: "var(--color-warning)"
            },

            ".icon-info": {
                color: "var(--color-info)"
            },

            ".icon-muted": {
                color: "var(--color-muted)"
            },

            // Rotation classes
            ".icon-rotate-90": {
                transform: "rotate(90deg)"
            },

            ".icon-rotate-180": {
                transform: "rotate(180deg)"
            },

            ".icon-rotate-270": {
                transform: "rotate(270deg)"
            },

            ".icon-flip-horizontal": {
                transform: "scaleX(-1)"
            },

            ".icon-flip-vertical": {
                transform: "scaleY(-1)"
            },

            // Animation classes
            ".icon-spin": {
                animation: "icon-spin 2s infinite linear"
            },

            ".icon-pulse": {
                animation: "icon-spin 1s infinite steps(8)"
            },

            "@keyframes icon-spin": {
                "0%": {
                    transform: "rotate(0deg)"
                },
                "100%": {
                    transform: "rotate(359deg)"
                }
            },

            // Spacing utilities
            ".icon-spacing-right": {
                marginRight: "var(--icon-spacing)"
            },

            ".icon-spacing-left": {
                marginLeft: "var(--icon-spacing)"
            }
        }
    }
}