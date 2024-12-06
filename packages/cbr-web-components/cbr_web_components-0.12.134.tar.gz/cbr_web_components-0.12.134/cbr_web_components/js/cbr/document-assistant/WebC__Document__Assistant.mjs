import Web_Component          from '../../core/Web_Component.mjs'
import CSS__Grid              from '../../css/grid/CSS__Grid.mjs'
import CSS__Typography        from '../../css/CSS__Typography.mjs'
import CSS__Cards             from '../../css/CSS__Cards.mjs'
import CSS__Forms             from '../../css/CSS__Forms.mjs'
import Div                    from '../../core/Div.mjs'
import API__Invoke            from '../../data/API__Invoke.mjs'
import WebC__Document__Editor from "./WebC__Document__Editor.mjs";

export default class WebC__Document__Assistant extends Web_Component {

    constructor() {
        super()
        this.api_invoke = new API__Invoke()
        this.state      = {document: {  content : '',
                                        version : 1,
                                        changes : [],
                                        history : []},
                            diff   : {  visible   : false,
                                        changes   : [],
                                        selected  : [] }
        }
    }
    async apply_css() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Forms     (this).apply_framework()
        this.add_css_rules(this.css_rules())
    }

    load_attributes() {
        this.file_id    = this.getAttribute('file-id')
    }
    async load_data() {
        await this.load_document_data()
    }


    add_web_components() {
        const params = { 'file-id': this.file_id,
                         'content': this.state.document.content }
        this.add_web_component_to('.document-panel', WebC__Document__Editor, params)
    }

    async load_document_data() {
        try {
            const response = await this.api_invoke.invoke_api(
                `/api/user-data/files/file-contents?file_id=${this.file_id}`
            )

            const decoded_content = atob(response.data.file_bytes__base64)
            this.state.document.content = new TextDecoder().decode(
                new Uint8Array([...decoded_content].map(c => c.charCodeAt(0)))
            )
            this.file_data = response.data.file_data
        } catch (error) {
            console.error('Error loading document:', error)
            this.show_error(error.message)
        }
    }

    add_event_listeners() {
        this.add_window_event_listener('document:change', this.handle__document_change )
        this.add_window_event_listener('diff:show'      , this.handle__diff_show       )
        this.add_window_event_listener('diff:hide'      , this.handle__diff_hide       )
        this.add_window_event_listener('changes:accept' , this.handle__changes_accept  )
        this.add_window_event_listener('changes:reject' , this.handle__changes_reject  )
        this.add_window_event_listener('version:commit' , this.handle__version_commit  )
        this.add_window_event_listener('version:reset'  , this.handle__version_reset   )
    }

    handle__document_change = (event) => {                                  // Separate handler methods with consistent naming
        this.handle_document_change(event.detail)
    }

    handle__diff_show = () => {
        this.state.diff.visible = true
        this.update_diff_visibility()
    }

    handle__diff_hide = () => {
        this.state.diff.visible = false
        this.update_diff_visibility()
    }

    handle__changes_accept = (event) => {
        this.accept_changes(event.detail.changes)
    }

    handle__changes_reject = () => {
        this.reject_changes()
    }

    handle__version_commit = () => {
        this.commit_version()
    }

    handle__version_reset = (event) => {
        this.reset_to_version(event.detail.version)
    }

    handle_document_change(detail) {
        this.state.document.content = detail.content
        this.state.document.version++

        // Notify child components
        this.raise_event_global('document-updated', {
            file_id : this.file_id,
            content : detail.content,
            version : this.state.document.version
        })
    }

    update_diff_visibility() {
        const diff_overlay = this.query_selector('.diff-overlay')
        if (diff_overlay) {
            if (this.state.diff.visible) {
                diff_overlay.classList.add('visible')
            } else {
                diff_overlay.classList.remove('visible')
            }
        }
    }

    accept_changes(changes) {
        // Update document content with accepted changes
        this.state.document.content = changes.new_version
        this.state.document.version++
        this.state.diff.visible = false

        // Clear current changes
        this.state.diff.changes = []
        this.state.diff.selected = []

        this.refresh_ui()
    }

    reject_changes() {
        // Clear current changes
        this.state.diff.changes = []
        this.state.diff.selected = []
        this.state.diff.visible = false

        this.refresh_ui()
    }

    commit_version() {
        // Add current state to history
        this.state.document.history.push({
            version: this.state.document.version,
            content: this.state.document.content,
            timestamp: new Date().toISOString()
        })
    }

    async reset_to_version(version) {
        const target_version = this.state.document.history.find(v => v.version === version)
        if (target_version) {
            this.state.document.content = target_version.content
            this.state.document.version = target_version.version
            await this.refresh_ui()
        }
    }

    show_error(message) {
        console.error(message)
        // TODO: Implement error notification system
    }

    html() {
        const container = new Div({ class: 'document-assistant' })

        // Chat panel (left)
        const chat_panel = new Div({ class: 'chat-panel' })
        chat_panel.add_tag({
            tag: 'webc-document-chat',
            attributes: {
                'file-id': this.file_id,
                'content': this.state.document.content
            }
        })

        // Document panel (right)
        const document_panel = new Div({ class: 'document-panel' })

        // Diff overlay // todo: implement diff overlay
        //const diff_overlay = new Div({ class: `diff-overlay ${this.state.diff.visible ? 'visible' : ''}` })
        const diff_overlay = new Div({ class: `diff-overlay` })
        //
        diff_overlay.add_tag({
            tag: 'webc-document-diff',
            attributes: {
                'file-id': this.file_id
            }
        })
        document_panel.add_element(diff_overlay)

        container.add_elements(chat_panel, document_panel)

        return container

    }

    css_rules() {
        return {
            ".document-assistant" : { display         : "grid"                      ,      // Main container
                                     gridTemplateColumns: "30% 70%"                 ,
                                     height          : "100%"                      ,
                                     minHeight       : "0"                         ,      // Allow content to scroll
                                     backgroundColor : "#fff"                      },

            ".chat-panel"        : { display         : "flex"                      ,      // Left panel
                                     flexDirection    : "column"                    ,
                                     borderRight     : "1px solid #dee2e6"         ,
                                     height          : "100%"                      ,
                                     minHeight       : "0"                         },      // Allow content to scroll

            ".document-panel"    : { flex            : 1                           ,
                                     position        : "relative"                   ,      // For diff overlay
                                     minHeight       : "0"                         },      // Allow content to scroll

            ".diff-overlay"      : { position        : "absolute"                  ,      // Diff overlay
                                     top             : "0"                         ,
                                     right           : "0"                         ,
                                     width           : "100%"                      ,
                                     height          : "100%"                      ,
                                     backgroundColor : "rgba(255,255,255,0.95)"    ,
                                     transform       : "translateX(100%)"          ,      // Hide by default
                                     transition      : "transform 0.3s ease"       ,
                                     zIndex          : "100"                       },      // Ensure overlay is on top

            ".diff-overlay.visible": { transform     : "translateX(0)"             } ,     // Show overlay
        }
    }


//     simulate_diff_event() {
//         console.log("in simulate diff event")
//         const file_id = '970804a2-88d8-41d6-881e-e1c5910b80f8'
//         const result = {
//     "document": {
//         "new_version": "##  GDPR Compliance Guidelines\n\nThe GDPR outlines essential principles and requirements for processing personal data, emphasizing lawfulness, fairness, and transparency. Organizations must obtain explicit consent, maintain records, implement privacy measures, report breaches, conduct impact assessments, and appoint a DPO if necessary. Individuals have several rights, including access, rectification, erasure, and portability. Technical measures such as encryption, security testing, and access controls are mandatory. Documentation is required for various processes, and international data transfers must follow specific guidelines.\n\n###  Additional Considerations\n\n1. **Data Minimization**: Organizations should only collect personal data that is necessary for the specified purpose.\n2. **Accountability**: Organizations must demonstrate compliance with GDPR principles and be able to show how they are meeting their obligations.",
//         "changes": [
//             {
//                 "type": "addition",
//                 "original": "",
//                 "updated": "###  Additional Considerations\n\n1. **Data Minimization**: Organizations should only collect personal data that is necessary for the specified purpose.\n2. **Accountability**: Organizations must demonstrate compliance with GDPR principles and be able to show how they are meeting their obligations.",
//                 "reason": "To enhance the document by adding two important principles of GDPR compliance: Data Minimization and Accountability, which are crucial for organizations to understand their responsibilities."
//             }
//         ],
//         "summary": "Two additional principles of GDPR compliance, Data Minimization and Accountability, have been added to enhance the guidelines and provide a more comprehensive understanding of the requirements for organizations processing personal data under GDPR regulations."
//     },
//     "status": "success"
// }
//         // Raise event to show diff view
//         this.raise_event_global('diff:show')
//         this.raise_event_global('update-diff-view', {
//             file_id: this.file_id,
//             changes: result
//         })
//     }

}

WebC__Document__Assistant.define()