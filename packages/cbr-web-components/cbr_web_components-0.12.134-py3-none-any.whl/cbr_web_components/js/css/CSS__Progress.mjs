export default class CSS__Progress {
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
            // Base progress container
            ".progress": {
                display: "flex",
                height: "1rem",
                overflow: "hidden",
                fontSize: ".75rem",
                backgroundColor: "#e9ecef",
                borderRadius: "0.25rem"
            },

            // Progress bar
            ".progress-bar": {
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                overflow: "hidden",
                color: "#fff",
                textAlign: "center",
                whiteSpace: "nowrap",
                backgroundColor: "#1a73e8",
                transition: "width .6s ease"
            },

            // Striped variation
            ".progress-bar-striped": {
                backgroundImage: "linear-gradient(45deg, rgba(255,255,255,.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,.15) 50%, rgba(255,255,255,.15) 75%, transparent 75%, transparent)",
                backgroundSize: "1rem 1rem"
            },

            // Animated stripes
            ".progress-bar-animated": {
                animation: "progress-bar-stripes 1s linear infinite"
            },

            // Different heights
            ".progress-sm": {
                height: "0.5rem"
            },

            ".progress-lg": {
                height: "1.5rem"
            },

            // Color variations using our color system
            ".progress-bar-success": {
                backgroundColor: "#188038"
            },

            ".progress-bar-info": {
                backgroundColor: "#1967d2"
            },

            ".progress-bar-warning": {
                backgroundColor: "#f9ab00"
            },

            ".progress-bar-error": {
                backgroundColor: "#d93025"
            },
        }
    }
}