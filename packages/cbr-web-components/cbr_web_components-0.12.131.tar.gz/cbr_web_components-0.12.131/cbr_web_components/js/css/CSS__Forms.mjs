export default class CSS__Forms {
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
            // Base input styling
            ".input": {
                display: "block",
                width: "100%",
                padding: "0.5rem",
                fontSize: "1rem",
                lineHeight: "1.5",
                color: "#2c3e50",
                backgroundColor: "#fff",
                border: "1px solid #cbd5e1",
                borderRadius: "0.25rem",
                transition: "border-color 0.2s ease"
            },

            ".input:focus": {
                outline: "none",
                borderColor: "#3b82f6",
                boxShadow: "0 0 0 2px rgba(59, 130, 246, 0.1)"
            },

            ".input:disabled": {
                backgroundColor: "#f1f5f9",
                cursor: "not-allowed"
            },

            ".input[readonly]": {
                backgroundColor: "#f8fafc"
            },

            // Field group - container for input, label, help
            ".field-group": {
                marginBottom: "1.5rem"
            },

            // Label styling
            ".label": {
                display: "block",
                marginBottom: "0.5rem",
                fontSize: "0.875rem",
                fontWeight: "500",
                color: "#374151"
            },

            // Help text
            ".help": {
                display: "block",
                marginTop: "0.375rem",
                fontSize: "0.75rem",
                color: "#64748b"
            },

            // Validation states
            ".valid": {
                borderColor: "#10b981"
            },

            ".valid + .help": {
                color: "#10b981"
            },

            ".invalid": {
                borderColor: "#ef4444"
            },

            ".invalid + .help": {
                color: "#ef4444"
            },

            // Input sizes
            ".input-large": {
                fontSize: "1.125rem"
            },

            ".input-small": {
                padding: "0.25rem",
                fontSize: "0.875rem"
            },

            // Checkbox and Radio
            ".checkbox-group, .radio-group": {
                display: "flex",
                alignItems: "center",
                marginBottom: "0.5rem"
            },

            ".checkbox, .radio": {
                width: "1rem",
                height: "1rem",
                marginRight: "0.5rem",
                cursor: "pointer"
            },

            ".checkbox-label, .radio-label": {
                fontSize: "0.875rem",
                cursor: "pointer"
            },

            // Input Groups
            ".input-group": {
                display: "flex",
                alignItems: "stretch"
            },

            ".input-addon": {
                display: "flex",
                alignItems: "center",
                padding: "0.5rem 0.75rem",
                fontSize: "1rem",
                color: "#374151",
                backgroundColor: "#f1f5f9",
                border: "1px solid #cbd5e1",
                borderRadius: "0.25rem"
            },

            ".input-group .input": {
                borderRadius: "0"
            },

            ".input-group > :first-child": {
                borderTopRightRadius: "0",
                borderBottomRightRadius: "0"
            },

            ".input-group > :last-child": {
                borderTopLeftRadius: "0",
                borderBottomLeftRadius: "0"
            },

            // Select specific styling
            ".input[multiple]": {
                padding: "0.5rem"
            },

            // Plain text input styling
            ".input-plain": {
                backgroundColor: "transparent",
                border: "none",
                padding: "0.375rem 0"
            },

            ".input-plain:focus": {
                outline: "none",
                boxShadow: "none"
            },

            // Inline form styling
            ".inline-form": {
                display: "flex",
                alignItems: "baseline",
                gap: "1rem"
            },

            ".inline-form .field-group": {
                marginBottom: "0"
            },

            // Visually hidden (for accessibility)
            ".visually-hidden": {
                position: "absolute",
                width: "1px",
                height: "1px",
                padding: "0",
                margin: "-1px",
                overflow: "hidden",
                clip: "rect(0,0,0,0)",
                border: "0"
            },

            // Button styling
            ".button": {
                display: "inline-block",
                padding: "0.5rem 1rem",
                fontSize: "1rem",
                fontWeight: "500",
                lineHeight: "1.5",
                textAlign: "center",
                textDecoration: "none",
                borderRadius: "0.25rem",
                cursor: "pointer",
                border: "1px solid transparent",
                transition: "all 0.2s ease",
                margin: "10px"
            },

            ".button-primary": {
                backgroundColor: "#3b82f6",
                color: "#ffffff"
            },

            ".button-primary:hover": {
                backgroundColor: "#2563eb"
            },

            // File input styling
            ".input-file": {
                display: "block",
                width: "100%",
                fontSize: "1rem",
                lineHeight: "1.5",
                color: "#374151",
                backgroundColor: "#ffffff",
                border: "1px solid #cbd5e1",
                borderRadius: "0.25rem",
                cursor: "pointer"
            },

            ".input-file::-webkit-file-upload-button": {
                padding: "0.375rem 0.75rem",
                marginRight: "0.75rem",
                color: "#374151",
                backgroundColor: "#f3f4f6",
                border: "none",
                borderRadius: "0.25rem",
                cursor: "pointer"
            },

            ".input-file:disabled": {
                backgroundColor: "#f1f5f9",
                cursor: "not-allowed"
            },

            ".input-file:disabled::-webkit-file-upload-button": {
                backgroundColor: "#e5e7eb",
                cursor: "not-allowed"
            },

            ".input-file.input-small": {
                padding: "0.25rem",
                fontSize: "0.875rem"
            },

            ".input-file.input-small::-webkit-file-upload-button": {
                padding: "0.25rem 0.5rem",
                fontSize: "0.875rem"
            },

            ".input-file.input-large": {
                padding: "0.75rem",
                fontSize: "1.125rem"
            },

            ".input-file.input-large::-webkit-file-upload-button": {
                padding: "0.5rem 1rem",
                fontSize: "1.125rem"
            }
        }
    }
}