export default class CSS__Tables {
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
                "--table-bg": "#ffffff",
                "--table-striped-bg": "rgba(0, 0, 0, 0.02)",
                "--table-hover-bg": "rgba(0, 0, 0, 0.04)",
                "--table-active-bg": "rgba(0, 0, 0, 0.1)",
                "--table-border-color": "#dee2e6",
                "--table-dark-border-color": "#373b3e",
                "--table-caption-color": "#6c757d",
                "--table-header-bg": "#f8f9fa",
                "--table-footer-bg": "#f8f9fa",

                // Contextual colors
                "--table-primary-bg": "rgba(13, 110, 253, 0.1)",
                "--table-primary-color": "#0d6efd",
                "--table-secondary-bg": "rgba(108, 117, 125, 0.1)",
                "--table-secondary-color": "#6c757d",
                "--table-success-bg": "rgba(25, 135, 84, 0.1)",
                "--table-success-color": "#198754",
                "--table-info-bg": "rgba(13, 202, 240, 0.1)",
                "--table-info-color": "#0dcaf0",
                "--table-warning-bg": "rgba(255, 193, 7, 0.1)",
                "--table-warning-color": "#ffc107",
                "--table-error-bg": "rgba(220, 53, 69, 0.1)",
                "--table-error-color": "#dc3545",
                "--table-light-bg": "#f8f9fa",
                "--table-light-color": "#000000",
                "--table-dark-bg": "#212529",
                "--table-dark-color": "#ffffff",

                // Spacing variables
                "--table-sm-padding-y": "0.25rem",
                "--table-sm-padding-x": "0.25rem",
                "--table-padding-y": "0.75rem",
                "--table-padding-x": "0.75rem",
                "--table-lg-padding-y": "1rem",
                "--table-lg-padding-x": "1rem"
            },

            // Base table styles
            ".table": {
                width: "100%",
                marginBottom: "1rem",
                verticalAlign: "top",
                borderCollapse: "collapse",
                "& caption": {
                    padding: "var(--table-padding-y) var(--table-padding-x)",
                    color: "var(--table-caption-color)",
                    textAlign: "start",
                    captionSide: "bottom"
                },
                "& th": {
                    fontWeight: "600",
                    backgroundColor: "var(--table-header-bg)",
                    verticalAlign: "bottom",
                    borderBottom: "2px solid var(--table-border-color)",
                    padding: "var(--table-padding-y) var(--table-padding-x)"
                },
                "& td": {
                    padding: "var(--table-padding-y) var(--table-padding-x)",
                    verticalAlign: "top",
                    borderTop: "1px solid var(--table-border-color)"
                },
                "& tfoot": {
                    backgroundColor: "var(--table-footer-bg)"
                },
                "& tbody tr:last-child td": {
                    borderBottom: "1px solid var(--table-border-color)"
                }
            },

            // Contextual classes
            ".table-primary, .table tr.table-primary, .table td.table-primary": {
                backgroundColor: "var(--table-primary-bg)",
                color: "var(--table-primary-color)",
                borderColor: "rgba(13, 110, 253, 0.2)"
            },

            ".table-secondary, .table tr.table-secondary, .table td.table-secondary": {
                backgroundColor: "var(--table-secondary-bg)",
                color: "var(--table-secondary-color)",
                borderColor: "rgba(108, 117, 125, 0.2)"
            },

            ".table-success, .table tr.table-success, .table td.table-success": {
                backgroundColor: "var(--table-success-bg)",
                color: "var(--table-success-color)",
                borderColor: "rgba(25, 135, 84, 0.2)"
            },

            ".table-info, .table tr.table-info, .table td.table-info": {
                backgroundColor: "var(--table-info-bg)",
                color: "var(--table-info-color)",
                borderColor: "rgba(13, 202, 240, 0.2)"
            },

            ".table-warning, .table tr.table-warning, .table td.table-warning": {
                backgroundColor: "var(--table-warning-bg)",
                color: "var(--table-warning-color)",
                borderColor: "rgba(255, 193, 7, 0.2)"
            },

            ".table-error, .table tr.table-error, .table td.table-error": {
                backgroundColor: "var(--table-error-bg)",
                color: "var(--table-error-color)",
                borderColor: "rgba(220, 53, 69, 0.2)"
            },

            ".table-light, .table tr.table-light, .table td.table-light": {
                backgroundColor: "var(--table-light-bg)",
                color: "var(--table-light-color)",
                borderColor: "rgba(248, 249, 250, 0.2)"
            },

            ".table-dark, .table tr.table-dark, .table td.table-dark": {
                backgroundColor: "var(--table-dark-bg)",
                color: "var(--table-dark-color)",
                borderColor: "rgba(33, 37, 41, 0.2)"
            },

            ".table-active, .table tr.table-active, .table td.table-active": {
                backgroundColor: "var(--table-active-bg)"
            },

            // Table variants
            ".table-striped tbody tr:nth-of-type(odd)": {
                backgroundColor: "var(--table-striped-bg)"
            },

            ".table-hover tbody tr:hover": {
                backgroundColor: "var(--table-hover-bg)",
                cursor: "pointer"
            },

            ".table-bordered": {
                "& th, & td": {
                    border: "1px solid var(--table-border-color)"
                }
            },

            ".table-borderless": {
                "& th, & td, & thead th, & tbody + tbody": {
                    border: "0"
                }
            },

            // Size variations
            ".table-sm": {
                "& th, & td": {
                    padding: "var(--table-sm-padding-y) var(--table-sm-padding-x)"
                }
            },

            ".table-lg": {
                "& th, & td": {
                    padding: "var(--table-lg-padding-y) var(--table-lg-padding-x)"
                }
            },

            // Responsive tables
            ".table-responsive": {
                overflowX: "auto",
                WebkitOverflowScrolling: "touch",
                "@media (max-width: 575.98px)": {
                    display: "block",
                    width: "100%",
                    overflowX: "auto",
                    "& .table": {
                        marginBottom: "0"
                    }
                }
            },

            // Table group divider
            ".table-group-divider": {
                borderTop: "2px solid var(--table-border-color)"
            },

            // Utilities
            ".cell-fit": {
                width: "1%",
                whiteSpace: "nowrap"
            },

            ".cell-nowrap": {
                whiteSpace: "nowrap"
            },

            ".cell-truncate": {
                maxWidth: "150px",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap"
            }
        }
    }
}