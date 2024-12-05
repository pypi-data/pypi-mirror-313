export default class CSS__Grid {
    debug_mode = new URLSearchParams(window.location.search).has('debug__webc')

    constructor(target_element) {
        this.target_element = target_element
    }

    apply_framework({debug=false}={}) {
        if (this.target_element) {
            this.target_element.add_css_rules(this.css_rules__standard())
            if (this.debug_mode) {
                this.target_element.add_css_rules(this.css_rules_debug())
            }
        }
    }

    css_rules__standard() {
        return {
            // Breakpoint definitions as CSS custom properties for reuse
            ":host": {
                "--breakpoint-xs": "0",
                "--breakpoint-sm": "576px",
                "--breakpoint-md": "768px",
                "--breakpoint-lg": "992px",
                "--breakpoint-xl": "1200px",
                "--breakpoint-xxl": "1400px",
                "--grid-gutter": "0",
                "--grid-columns": "12"
            },

            // Container
            ".container": {
                width: "100%",
                marginLeft: "auto",
                marginRight: "auto",
                paddingLeft: "calc(var(--grid-gutter) / 2)",
                paddingRight: "calc(var(--grid-gutter) / 2)",
                boxSizing: "border-box",

                "@media (min-width: 576px)": {
                    maxWidth: "540px"
                },
                "@media (min-width: 768px)": {
                    maxWidth: "720px"
                },
                "@media (min-width: 992px)": {
                    maxWidth: "960px"
                },
                "@media (min-width: 1200px)": {
                    maxWidth: "1140px"
                },
                "@media (min-width: 1400px)": {
                    maxWidth: "1320px"
                }
            },

            ".container-fluid": {
                width: "100%",
                marginLeft: "auto",
                marginRight: "auto",
                paddingLeft: "calc(var(--grid-gutter) / 2)",
                paddingRight: "calc(var(--grid-gutter) / 2)",
                boxSizing: "border-box"
            },

            // Row
            ".row": {
                display: "flex",
                flexWrap: "wrap",
                boxSizing: "border-box",
                gap: "var(--grid-gutter)"  // Default gap, can be overridden by gap utilities
            } ,

            // Basic columns
            ".col": {
                boxSizing   : "border-box" ,
                position    : "relative"   ,
                flex        : "1 1 auto"   ,
                maxWidth    : "100%"       ,
                minWidth    : 0          ,
            },

            // Generate column widths
            ...[...Array(12)].reduce((acc, _, i) => ({
                ...acc,
                [`.col-${i + 1}`]: {
                    position: "relative",
                    paddingRight: "calc(var(--grid-gutter) / 2)",
                    paddingLeft: "calc(var(--grid-gutter) / 2)",
                    flex: "0 0 auto",
                    width: `${(i + 1) * 100 / 12}%`,
                    boxSizing: "border-box"
                }
            }), {}),

            // Responsive columns for each breakpoint
            ...[
                ['sm', '576px'],
                ['md', '768px'],
                ['lg', '992px'],
                ['xl', '1200px'],
                ['xxl', '1400px']
            ].reduce((acc, [breakpoint, width]) => ({
                ...acc,
                [`@media (min-width: ${width})`]: {
                    ...[...Array(12)].reduce((cols, _, i) => ({
                        ...cols,
                        [`.col-${breakpoint}-${i + 1}`]: {
                            flex: "0 0 auto",
                            width: `${(i + 1) * 100 / 12}%`
                        }
                    }), {})
                }
            }), {}),

            // Gap utilities
            ...[0, 1, 2, 3, 4, 5].reduce((acc, i) => ({
                ...acc,
                [`.gap-${i}`]: {
                    gap: `${i * 0.25}rem`
                },
                [`.gap-x-${i}`]: {
                    columnGap: `${i * 0.25}rem`
                },
                [`.gap-y-${i}`]: {
                    rowGap: `${i * 0.25}rem`
                }
            }), {}),

            // Alignment utilities
            ".justify-start": { justifyContent: "flex-start" },
            ".justify-center": { justifyContent: "center" },
            ".justify-end": { justifyContent: "flex-end" },
            ".justify-between": { justifyContent: "space-between" },
            ".justify-around": { justifyContent: "space-around" },

            ".align-start": { alignItems: "flex-start" },
            ".align-center": { alignItems: "center" },
            ".align-end": { alignItems: "flex-end" },
            ".align-stretch": { alignItems: "stretch" },

            // Order utilities
            ...[0, 1, 2, 3, 4, 5].reduce((acc, i) => ({
                ...acc,
                [`.order-${i}`]: {
                    order: i
                }
            }), {}),

            // Offset utilities
            ...[...Array(11)].reduce((acc, _, i) => ({
                ...acc,
                [`.offset-${i + 1}`]: {
                    marginLeft: `${(i + 1) * 100 / 12}%`
                }
            }), {}),

            // Margin utilities
            ...[0, 1, 2, 3, 4, 5].reduce((acc, i) => ({
                ...acc,
                [`.m-${i}`]: {
                    margin: `${i}rem` // Adjust units as needed
                }
            }), {}),

            // Height and Width (px) Utilities

            ...[25, 50, 75, 100, 150, 200, 250, 300, 350, 400, 450, 500].reduce((acc, size) => ({
                ...acc,
                [`.h-${size}px`]: {
                    maxHeight: `${size}px`,
                    minHeight: `${size}px`
                },
                [`.w-${size}px`]: {
                    maxWidth: `${size}px`,
                    minWidth: `${size}px`
                }
            }), {}),


            // Display utilities
            ".d-none": { display: "none" },
            ".d-flex": { display: "flex" },
            ".d-block": { display: "block" },

            // Responsive display utilities
            ...[
                ['sm', '576px'],
                ['md', '768px'],
                ['lg', '992px'],
                ['xl', '1200px'],
                ['xxl', '1400px']
            ].reduce((acc, [breakpoint, width]) => ({
                ...acc,
                [`@media (min-width: ${width})`]: {
                    [`.d-${breakpoint}-none`]: { display: "none" },
                    [`.d-${breakpoint}-flex`]: { display: "flex" },
                    [`.d-${breakpoint}-block`]: { display: "block" }
                }
            }), {}) ,

            // extra css rules (todo: see which ones can be extended with the same utilities patterns used above, and where they should be placed better)

            // Padding utilities
            ".p-0": { padding: "0"    },
            ".p-3": { padding: "1rem" },

            // Flex container behaviors
            ".flex-column": { flexDirection: "column" },
            ".flex-row"   : { flexDirection: "row"    },
            ".flex-wrap"  : { flexWrap     : "wrap"   },
            ".flex-nowrap": { flexWrap     : "nowrap" },

            // Flex child behaviors
            ".flex-grow-0": { flexGrow: "0" },
            ".flex-grow-1": { flexGrow: "1" },
            ".flex-shrink-0": { flexShrink: "0" },
            ".flex-shrink-1": { flexShrink: "1" },

            // Common flex shorthand combinations
            ".flex-fill": { flex: "1 1 auto" },
            ".flex-fixed": { flex: "0 0 auto" },

            // Height utilities for flex containers

            ".h-100vh"          : { height: "100vh" , boxSizing: "border-box"},          // Viewport height
            ".h-100pc"          : { height: "100%"  , boxSizing: "border-box"},          // Parent-relative height (auto add boxSizing since without it , 100% has weird side effects, i.e. it prevents "Prevents the element from growing beyond its parent when padding or borders are applied.")
            ".border-box"       : { boxSizing: "border-box" },
            // Flex alignment utilities (if not already present)
            ".align-items-start": { alignItems: "flex-start" },
            ".align-items-center": { alignItems: "center" },
            ".align-items-end": { alignItems: "flex-end" },
            ".align-items-stretch": { alignItems: "stretch" },

            ".justify-content-start": { justifyContent: "flex-start" },
            ".justify-content-center": { justifyContent: "center" },
            ".justify-content-end": { justifyContent: "flex-end" },
            ".justify-content-between": { justifyContent: "space-between" },
            ".justify-content-around": { justifyContent: "space-around" },

            //Layout
            ".layout": {
                display       : "flex"                      ,
                flexDirection : "column"
            },
            ".layout-vertical": {
                display: "flex",
                flexDirection: "column"
            },

            ".layout-horizontal": {
                display: "flex",
                flexDirection: "row"
            },

            ".layout-panel": {
                flex: "1 1 1px",
                minWidth: 0
            },

            ".layout-fixed": {
                flexShrink: 0
            }
        }
    }

    css_rules_debug() {
        return {
            ":host": {
                    // Debug colors
                    "--debug-layout-color": "#4A90E2",       // blue
                    "--debug-row-color"   : "#198754",       // green
                    "--debug-col-color"   : "#6200ee",       // purple

                    // Common debug styles
                    "--debug-label-padding"      : "4px 8px"    ,
                    "--debug-label-font-size"    : "8px"        ,
                    "--debug-label-border-radius": "4px"        ,
                    "--debug-element-padding"    : "15px 5px"   ,
                    "--debug-element-margin"     : "10px 5px"   ,
                    "--debug-border-width"       : "2px"        ,
                    "--debug-label-top"          : "-20px"      ,
                    "--debug-margin"             : "20px"
            },

            ".layout": {
                position: "relative",
                border  : "var(--debug-border-width) solid var(--debug-layout-color)",
                padding : "var(--debug-element-padding)"    ,
                margin  : "var(--debug-margin)"             ,
            },
            ".layout::before": {
                content     : "'Layout 'attr(id)",
                position    : "absolute",
                top         : "var(--debug-label-top)",
                left        : "0",
                background  : "var(--debug-layout-color)",
                color       : "white",
                padding     : "var(--debug-label-padding)",
                fontSize    : "var(--debug-label-font-size)",
                borderRadius: "var(--debug-label-border-radius)"
            },
            ".row": {
                position: "relative",
                border: "var(--debug-border-width) solid var(--debug-row-color)",
                padding: "var(--debug-element-padding)",
                margin: "var(--debug-element-margin)"
            },
            ".row::before": {
                content: "'Row 'attr(id)",
                position: "absolute",
                top: "var(--debug-label-top)",
                left: "0",
                background: "var(--debug-row-color)",
                color: "white",
                padding: "var(--debug-label-padding)",
                fontSize: "var(--debug-label-font-size)",
                borderRadius: "var(--debug-label-border-radius)"
            },

            ".col, [class*='col-']": {
                position: "relative",
                border: "var(--debug-border-width) solid var(--debug-col-color)",
                padding: "var(--debug-element-padding)",
                margin: "var(--debug-element-margin)"
            },
            ".col::before, [class*='col-']::before": {
                content: "'Column 'attr(id)",
                position: "absolute",
                top: "var(--debug-label-top)",
                left: "0",
                background: "var(--debug-col-color)",
                color: "white",
                padding: "var(--debug-label-padding)",
                fontSize: "var(--debug-label-font-size)",
                borderRadius: "var(--debug-label-border-radius)"
            }
        }
    }
}