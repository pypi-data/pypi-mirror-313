export default class CSS__Images {
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
                "--img-border-radius": "0.375rem",
                "--img-thumbnail-padding": "0.25rem",
                "--img-thumbnail-border-width": "1px",
                "--img-thumbnail-border-color": "#dee2e6",
                "--img-caption-color": "#6c757d",
                "--img-caption-font-size": "0.875rem"
            },

            // Base image styles
            ".img": {
                maxWidth: "100%",
                height: "auto",
                verticalAlign: "middle"
            },

            // Responsive behavior
            ".img-fluid": {
                maxWidth: "100%",
                height: "auto"
            },

            // Fixed size behavior
            ".img-fixed": {
                width: "100%",
                height: "100%",
                objectFit: "cover"
            },

            // Shape variants
            ".img-rounded": {
                borderRadius: "var(--img-border-radius)"
            },

            ".img-circle": {
                borderRadius: "50%"
            },

            ".img-thumbnail": {
                padding: "var(--img-thumbnail-padding)",
                backgroundColor: "#fff",
                border: "var(--img-thumbnail-border-width) solid var(--img-thumbnail-border-color)",
                borderRadius: "var(--img-border-radius)",
                maxWidth: "100%",
                height: "auto"
            },

            // Display control classes
            ".img-cover": {
                objectFit: "cover",
                width: "100%",
                height: "100%"
            },

            ".img-contain": {
                objectFit: "contain",
                width: "100%",
                height: "100%"
            },

            ".img-fill": {
                objectFit: "fill",
                width: "100%",
                height: "100%"
            },

            // Alignment classes
            ".img-center": {
                display: "block",
                marginLeft: "auto",
                marginRight: "auto"
            },

            ".img-start": {
                float: "inline-start"
            },

            ".img-end": {
                float: "inline-end"
            },

            // Figure components
            ".figure": {
                display: "inline-block",
                marginBottom: "0.5rem",
                maxWidth: "100%"
            },

            ".figure-img": {
                marginBottom: "0.5rem",
                lineHeight: "1"
            },

            ".figure-caption": {
                fontSize: "var(--img-caption-font-size)",
                color: "var(--img-caption-color)",
                marginTop: "0.5rem"
            },

            // Caption alignment
            ".figure-caption-start": {
                textAlign: "start"
            },

            ".figure-caption-center": {
                textAlign: "center"
            },

            ".figure-caption-end": {
                textAlign: "end"
            },

            // Spacing utilities for images in text
            ".img-spacing": {
                margin: "1rem"
            },

            ".img-spacing-start": {
                marginInlineEnd: "1rem"
            },

            ".img-spacing-end": {
                marginInlineStart: "1rem"
            },

            // Clear floats
            ".clearfix::after": {
                content: '""',
                display: "table",
                clear: "both"
            }
        }
    }
}