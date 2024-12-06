import Div  from "../Div.mjs";
import Span from "../Span.mjs";

export default class Container__Two_Cols extends Div {

    constructor({...kwargs}={}) {
        super({...kwargs})
        this.setup()
    }

    setup() {
        this.div_root   = new Div({ class: 'container' });
        this.row_1  = new Div({ class: 'row'});
        this.col_1  = new Div({ class: 'col'});
        this.col_2  = new Div({ class: 'col'});
        this.div_root.add_element (this.row_1            )
        this.row_1   .add_elements(this.col_1, this.col_2)
    }

    html() {
        return this.div_root.html();
    }

    css_rules() {
        return {
            ".container": {
                "display": "flex",
                "flex-direction": "column",
                "width": "100%",
                "height": "100%",
                "border": "2px black solid",
                "box-sizing": "border-box"              // Ensures padding and border are included in the element's total width and height
            },
            ".row": {
                "display": "flex",
                "flex": "1",                            // Each row takes equal space within the container
                "width": "100%",
                "align-items": "top",                   // Vertically aligns the items in the row
                "justify-content": "center"             // Horizontally centers the items in the row
            },
            ".col": {
                "flex": "1",                            // Each column takes equal space within the row
                "display": "flex",
                "align-items": "top",                   // Aligns content vertically
                "justify-content": "center",            // Aligns content horizontally
                "height": "100%",                       // Ensures columns stretch to fill the row height
                "box-sizing": "border-box",
                "padding": "10px",
                "overflow-wrap": "break-word",
                "word-wrap": "break-word",              // Ensures long words wrap properly
                "white-space": "normal"                 // Allows the content to wrap naturally
            },
            ".col:nth-child(1)": {
                "flex": "1",                            // First column takes equal space
                "max-width": "50%",                     // Ensures an even 50% split for both columns
                "overflow": "hidden"                    // Prevents overflow issues for the first column
            },
            ".col:nth-child(2)": {
                "flex": "1",                            // Second column takes equal space
                "max-width": "50%",                     // Ensures an even 50% split for both columns
                "overflow": "auto",                     // Adds scroll when content exceeds available width
                "white-space": "normal",                // Allows wrapping of content in the second column
                "word-wrap": "break-word",              // Breaks long words if necessary
                "overflow-wrap": "break-word"           // Handles overflow with long content
            },
            "#file_contents": {
                "white-space": "pre-wrap",              // Ensures long content wraps within the column
                "word-wrap": "break-word",              // Breaks long words if necessary
                "overflow": "auto",                     // Scrolls content if it's too large
                "max-width": "100%",                    // Makes sure the content doesn't exceed its container's width
                "padding": "10px",
                "border": "1px solid #ccc"
            }
        };
    }


}