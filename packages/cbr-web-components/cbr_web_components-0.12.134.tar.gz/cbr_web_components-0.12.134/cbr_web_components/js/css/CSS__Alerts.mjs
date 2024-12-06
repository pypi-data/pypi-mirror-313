export default class CSS__Alerts {
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
            // Base alert styling
            ".alert": {
                position: "relative",
                padding: "1rem",
                marginBottom: "1rem",
                border: "1px solid transparent",
                borderRadius: "0.375rem",
                display: "flex",
                alignItems: "center",
                gap: "0.5rem"
            },

            // Regular alerts
            ".alert-primary": {
                color: "#084298",
                backgroundColor: "#cfe2ff",
                borderColor: "#b6d4fe"
            },

            ".alert-secondary": {
                color: "#41464b",
                backgroundColor: "#e2e3e5",
                borderColor: "#d3d6d8"
            },

            ".alert-success": {
                color: "#0f5132",
                backgroundColor: "#d1e7dd",
                borderColor: "#badbcc"
            },

            ".alert-danger": {
                color: "#842029",
                backgroundColor: "#f8d7da",
                borderColor: "#f5c2c7"
            },

            ".alert-warning": {
                color: "#664d03",
                backgroundColor: "#fff3cd",
                borderColor: "#ffecb5"
            },

            ".alert-info": {
                color: "#055160",
                backgroundColor: "#cff4fc",
                borderColor: "#b6effb"
            },

            ".alert-light": {
                color: "#636464",
                backgroundColor: "#fefefe",
                borderColor: "#fdfdfe"
            },

            ".alert-dark": {
                color: "#141619",
                backgroundColor: "#d3d3d4",
                borderColor: "#bcbebf"
            },

            // Alert links - darker/bolder version of the alert color
            ".alert-primary a": {
                color: "#06357a",
                fontWeight: "700"
            },

            ".alert-secondary a": {
                color: "#34383c",
                fontWeight: "700"
            },

            ".alert-success a": {
                color: "#0c4128",
                fontWeight: "700"
            },

            ".alert-danger a": {
                color: "#6a1a21",
                fontWeight: "700"
            },

            ".alert-warning a": {
                color: "#523e02",
                fontWeight: "700"
            },

            ".alert-info a": {
                color: "#04414d",
                fontWeight: "700"
            },

            ".alert-light a": {
                color: "#4f5050",
                fontWeight: "700"
            },

            ".alert-dark a": {
                color: "#101214",
                fontWeight: "700"
            },

            // Alert heading
            ".alert-heading": {
                color: "inherit",
                marginTop: "0",
                marginBottom: "0.5rem",
                fontSize: "1.5rem",
                fontWeight: "500"
            },

            // Alert content
            ".alert-content": {
                margin: "0",
                flex: "1 1 auto"
            },

            // Additional content
            ".alert-content > p": {
                margin: "0"
            },

            ".alert-content > p + p": {
                marginTop: "0.5rem"
            },

            // Icon container
            ".alert-icon": {
                display: "flex",
                alignItems: "center",
                fontSize: "1.25em"
            }
        }
    }
}