export default class CSS__WebC__Chat_Bot {
    constructor(target_element) {
        this.target_element = target_element
    }

    apply_framework() {
        if (this.target_element) {
            this.target_element.add_css_rules(this.css_rules__standard())
        }
    }

    css_rules__standard() {
        return {    "*"                 : { "font-family": "Verdana"},
                    ".chatbot-ui"       : { display        : "flex"                   ,
                                            flex           : 1                        ,
                                            flexDirection  : "column"                 ,
                                            maxWidth       : "100%"                   ,
                                            minHeight      : "350px"                  ,
                                            height         : "100%"                   ,
                                            backgroundColor: "#fff"                   ,
                                            borderRadius   : "10px"                   ,
                                            boxShadow      : "0 0 5px rgba(0,0,0,0.4)",
                                            overflow       : "auto"                   ,
                                            position       : "relative"               },

                    ".chat-input-ui"    : { position: "absolute"      ,
                                            bottom  : 0               ,
                                            left    : 0               ,
                                            right   : 0               },
                    ".chat-messages"    : { flexGrow       : "1"       ,
                                            padding        : "10px"    ,
                                            overflowY      : "auto"    ,
                                            position       : "absolute",
                                            top            : "100px"   ,
                                            bottom         : "75px"    ,
                                            left           : "0"       ,
                                            right          : "0"       ,
                                            scrollBehavior : "smooth"  },
                    ".chat-ids"          : { backgroundColor: "black"  ,
                                             color          : "white"  ,
                                             padding        : "10px"   },
                    ".chat-ids a"        : { color          : "white"   },
                    ".chat-header"       : { backgroundColor : "#5a4ad1"           ,
                                             color           : "#fff"              ,
                                             padding         : "10px 20px"         ,   // Added horizontal padding
                                             display         : "flex"              ,
                                             alignItems      : "center"            ,
                                             justifyContent  : "space-between"     ,   // This spreads title and button
                                             fontSize        : "1.2em"             ,
                                             whiteSpace      : "nowrap"            ,
                                             overflow        : "hidden"            },
                    ".chat-header-title" : { overflow        : "hidden"            ,
                                             textOverflow    : "ellipsis"          ,
                                             flex            : "1"                 },   // Takes up available space
                    ".chat-input"        : { padding         : "10px",
                                             background      : "#fff",
                                             boxShadow       : "0 -2px 10px rgba(0,0,0,0.1)" },
                    ".chat-input input"  : {  width          : "90%"               ,
                                              padding        : "10px"            ,
                                              borderRadius   : "20px"    ,
                                              border         : "1px solid #ccc" } ,
                    ".save-chat:link"    : {  backgroundColor: '#007bff'  ,
                                              color          : '#fff'     ,
                                              padding        : '5px'      ,
                                              borderRadius   : "10px"     ,
                                              fontWeight     : '600'     },
                    ".header-content"     : { display         : "flex"               ,
                                              flex            : "1"                  ,
                                              justifyContent  : "space-between"      ,
                                              alignItems      : "center"             ,
                                              overflow        : "hidden"             },
                    ".maximize-button"    : { cursor          : "pointer"            ,
                                              fontSize        : "18px"               ,
                                              color           : "#fff"               ,
                                              display         : "flex"               ,
                                              alignItems      : "center"             ,
                                              justifyContent  : "center"             ,
                                              marginLeft      : "10px"               ,   // Space between title and button
                                              padding         : "5px"                ,   // Space for hover effect
                                              minWidth        : "24px"               },  // Maintain consistent size
                    ".maximize-button:hover": { background    : "rgba(255,255,255,0.1)",
                                               borderRadius   : "4px"                },
                    // Maximized state
                   ".chatbot-ui.maximized": { position         : "fixed"                  ,
                                              top              : "50px"                   ,
                                              left             : "50px"                   ,
                                              right            : "50px"                   ,
                                              height           : "unset"                  ,
                                              bottom           : "50px"                   ,
                                              zIndex           : "1000"                   ,
                                              borderRadius     : "10px"                   ,
                                              boxShadow      : "0 0px 50px rgba(0,0,0,1)" },
            }
        }
}


// todo: add this code to a separate class that provides a floating chat bot
        //   added to ".chat-header"  { cursor          : "move"              ,
        //                                              userSelect      : "none"}

                    //  ".chat-header:hover": { backgroundColor   : "#4a3ac1"          },
                    // // Resize handles - corners
                    // ".resize-handle" : { position        : "absolute"              ,
                    //                     width           : "10px"                   ,
                    //                     height          : "10px"                   ,
                    //                     background      : "transparent"            ,
                    //                     zIndex          : "1000"                   },
                    //
                    // ".resize-top-left"    : { top       : "0"                     ,
                    //                          left       : "0"                      ,
                    //                          cursor     : "nw-resize"              },
                    //
                    // ".resize-top-right"   : { top       : "0"                     ,
                    //                          right      : "0"                      ,
                    //                          cursor     : "ne-resize"              },
                    //
                    // ".resize-bottom-left" : { bottom    : "0"                     ,
                    //                          left       : "0"                      ,
                    //                          cursor     : "sw-resize"              },
                    //
                    // ".resize-bottom-right": { bottom    : "0"                     ,
                    //                          right      : "0"                      ,
                    //                          cursor     : "se-resize"              },
                    //
                    // // Resize handles - edges
                    // ".resize-top"    : { top            : "0"                     ,
                    //                     left           : "10px"                   ,
                    //                     right          : "10px"                   ,
                    //                     height         : "5px"                    ,
                    //                     cursor         : "n-resize"               },
                    //
                    // ".resize-bottom" : { bottom         : "0"                     ,
                    //                     left           : "10px"                   ,
                    //                     right          : "10px"                   ,
                    //                     height         : "5px"                    ,
                    //                     cursor         : "s-resize"               },
                    //
                    // ".resize-left"   : { left           : "0"                     ,
                    //                     top            : "10px"                   ,
                    //                     bottom         : "10px"                   ,
                    //                     width          : "5px"                    ,
                    //                     cursor         : "w-resize"               },
                    //
                    // ".resize-right"  : { right          : "0"                     ,
                    //                     top            : "10px"                   ,
                    //                     bottom         : "10px"                   ,
                    //                     width          : "5px"                    ,
                    //                     cursor         : "e-resize"               },
                    //
                    // // Show resize handles on hover when not maximized
                    // ".chatbot-ui:not(.maximized):hover .resize-handle": {
                    //     backgroundColor : "rgba(90, 74, 209, 0.2)"                 ,    // Light purple to match theme
                    //     transition     : "background-color 0.2s ease-in-out"
                    // },
                    //
                    // // Hide resize handles when maximized
                    // ".chatbot-ui.maximized .resize-handle": {
                    //     display        : "none"
                    // },
                    //
                    // // Disable transitions during resize
                    // ".chatbot-ui.resizing": {
                    //     transition     : "none"                                    ,
                    //     userSelect    : "none"
                    // }