export default class CSS__Navbar {
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
            // Base navbar
            ".navbar": {
                display: "flex",
                flexWrap: "wrap",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "0.5rem 1rem",
                position: "relative"
            },

            // Navbar brand/logo
            ".navbar-brand": {
                display: "inline-block",
                padding: "0.3125rem 0",
                marginRight: "1rem",
                fontSize: "1.25rem",
                lineHeight: "inherit",
                whiteSpace: "nowrap",
                textDecoration: "none",
                color: "inherit"
            },

            // Navbar toggler for mobile
            ".navbar-toggler": {
                padding: "0.25rem 0.75rem",
                fontSize: "1.25rem",
                lineHeight: "1",
                backgroundColor: "transparent",
                border: "1px solid rgba(0,0,0,.1)",
                borderRadius: "0.25rem",
                cursor: "pointer",
                display: "none"
            },

            // Container for navbar items
            ".navbar-collapse": {
                flexGrow: "1",
                alignItems: "center",
                display: "flex"
            },

            // Nav items container
            ".navbar-nav": {
                display: "flex",
                flexDirection: "row",
                padding: "0",
                margin: "0",
                listStyle: "none"
            },

            // Individual nav items
            ".navbar-nav-item": {
                padding: "0.5rem 1rem",
                color: "rgba(0,0,0,.55)",
                textDecoration: "none",
                whiteSpace: "nowrap"
            },

            ".navbar-nav-item:hover": {
                color: "rgba(0,0,0,.7)"
            },

            ".navbar-nav-item.active": {
                color: "rgba(0,0,0,.9)"
            },

            // Navbar text
            ".navbar-text": {
                padding: "0.5rem 1rem",
                color: "rgba(0,0,0,.55)"
            },


            // Dropdown
            ".navbar-dropdown": {
                paddingTop: "0.5rem",
                position: "relative"
            },

            ".navbar-dropdown-menu": {
                position: "absolute",
                top: "100%",
                left: "0",
                display: "none",
                minWidth: "10rem",
                padding: "0.5rem 0",
                margin: "0",
                backgroundColor: "#fff",
                borderRadius: "0.25rem",
                border: "1px solid rgba(0,0,0,.15)",
                boxShadow: "0 0.5rem 1rem rgba(0,0,0,.15)",
                zIndex: "1000"
            },

            ".navbar-dropdown:hover .navbar-dropdown-menu": {
                display: "block"
            },

            ".navbar-dropdown-item": {
                display: "block",
                padding: "0.25rem 1rem",
                color: "#212529",
                textDecoration: "none",
                whiteSpace: "nowrap"
            },

            ".navbar-dropdown-item:hover": {
                backgroundColor: "#f8f9fa",
                color: "#1e2125"
            },

            // Enhanced color schemes
            ".navbar-dark": {
                backgroundColor: "#212529",
                color: "rgba(255,255,255,.9)"
            },

            ".navbar-dark .navbar-brand": {
                color: "#fff"
            },

            ".navbar-dark .navbar-nav-item": {
                color: "rgba(255,255,255,.55)"
            },

            ".navbar-dark .navbar-nav-item:hover": {
                color: "rgba(255,255,255,.75)"
            },

            ".navbar-dark .navbar-nav-item.active": {
                color: "#fff"
            },

            ".navbar-dark .search-input": {
                backgroundColor: "#fff",
                border: "1px solid #ced4da",
                borderRadius: "0.25rem",
                padding: "0.375rem 0.75rem",
                marginRight: "0.5rem"
            },

            ".navbar-dark .navbar-toggler": {
                borderColor: "rgba(255,255,255,.1)"
            },

            // Light navbar styles
            ".navbar-light": {
                color: "rgba(0,0,0,.9)"
            },

            ".navbar-light .navbar-brand": {
                color: "rgba(0,0,0,.9)"
            },

            ".navbar-light .navbar-nav-item": {
                color: "rgba(0,0,0,.55)"
            },

            ".navbar-light .navbar-nav-item:hover": {
                color: "rgba(0,0,0,.7)"
            },

            ".navbar-light .navbar-nav-item.active": {
                color: "rgba(0,0,0,.9)"
            },

            // Search input styles
            ".navbar-search": {
                display: "flex",
                alignItems: "center",
                marginLeft: "auto"
            },

            ".search-input": {
                padding: "0.375rem 0.75rem",
                fontSize: "1rem",
                lineHeight: "1.5",
                backgroundColor: "#fff",
                border: "1px solid #ced4da",
                borderRadius: "0.25rem",
                marginRight: "0.5rem"
            }
        }
    }
}