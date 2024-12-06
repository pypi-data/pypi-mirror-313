export default class CSS__CBR__Layout__Default {
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
            ".content-loader": { display: 'flex',
                                 justifyContent: 'center',
                                 alignItems: 'center',
                                 height: '100%',
                                 fontSize: '1.2em',
                                 color: '#666' },
            ".content-error": { display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                height: '100%',
                                color: '#ff0000',
                                fontSize: '1.2em' },
            ".route-content": { padding: '20px'   },

            ".nav-docs"     : { backgroundColor : "#fff"              ,         // White background
                                borderRadius    : "0.375rem"          ,         // Rounded corners
                                margin         : "10px"               ,         // Margin around content
                                padding        : "10px"               ,         // Inner padding
                                flex           : "1 1 auto"           ,         // Allow flex growing and shrinking
                                display        : "flex"               ,         // Make it a flex container
                                flexDirection  : "column"             ,         // Stack contents vertically
                                overflow       : "auto"               ,
                                position       : "absolute"           ,
                                top            : "0"                  ,
                                left           : "0"                  ,
                                bottom         : "0"                  ,
                                right          : "0"                  },

            ".nav-dev"      : { width           :"100%"                ,
                                boxSizing       : "border-box"         },

            // ".nav-docs > *" : { maxWidth        : "100%"              ,         // Ensure children don't overflow
            //                     overflow        : "auto"              ,         // Add scrollbars when needed
            //                     flex           : "1 1 auto"           }         // Allow children to grow/shrink
        }
    }
}