import CBR_Events                                 from '../CBR_Events.mjs'
import Web_Component                              from '../../core/Web_Component.mjs'
import Div                                        from '../../core/Div.mjs'
import WebC__User_Files__Markdown__Versions_Panel from "./WebC__User_Files__Markdown__Versions_Panel.mjs";
import WebC__User_Files__Markdown__Toolbar        from "./WebC__User_Files__Markdown__Toolbar.mjs";
import WebC__User_Files__Markdown__Editor_View    from "./WebC__User_Files__Markdown__Editor_View.mjs";


export default class WebC__User_Files__Markdown extends Web_Component {

    apply_css() {
        this.add_css_rules(this.css_rules())
    }

    load_attributes() {
        this.file_id     = this.getAttribute('file_id')
    }

    component_ready() {
        //this.raise_event_global(CBR_Events.CBR__FILE__SHOW_HISTORY)                         // todo: see if this is the best place to raise this event
    }

    add_event_listeners() {
        this.add_window_event_listener(CBR_Events.CBR__FILE__SHOW_HISTORY, this.on_show_history)
        this.add_window_event_listener(CBR_Events.CBR__FILE__HIDE_HISTORY, this.on_hide_history)
        this.add_window_event_listener(CBR_Events.CBR__FILE__CANCEL      , this.on_file_cancel)
    }


    add_web_components() {
        const params_versions = { file_id: this.file_id }
        const params_editor   = { file_id: this.file_id }
        this.add_web_component_to('.versions-container', WebC__User_Files__Markdown__Versions_Panel , params_versions)
        this.add_web_component_to('.editor-toolbar'    , WebC__User_Files__Markdown__Toolbar        , {}             )
        this.add_web_component_to('.viewer-and-editor' , WebC__User_Files__Markdown__Editor_View    , params_editor  )
    }
    // event handlers

    on_file_cancel() {
        this.raise_event_global(CBR_Events.CBR__FILE__VIEW_MODE)
    }

    on_show_history() {
        this.query_selector('.versions-container').show()
    }

    on_hide_history(){
        this.query_selector('.versions-container').hide()
    }

    // API Calls

    // todo: implement and refactor to data file
    // async view_version(version_id) {
    //     try {
    //         const version_content = await this.api.get_version_content(this.file_id, version_id)
    //         this.temp_content = this.markdown_content  // Store current content
    //         this.markdown_content = version_content
    //         this.viewing_version = version_id
    //         this.render()
    //     } catch (error) {
    //         console.error('Error viewing version:', error)
    //         //this.show_error('Failed to load version')
    //     }
    // }
    //
    // async restore_version(version_id) {
    //     try {
    //         const version_content = await this.api.get_version_content(this.file_id, version_id)
    //         this.markdown_content = version_content
    //         await this.save_content()
    //         this.viewing_version = null
    //         this.render()
    //         //this.show_success('Version restored successfully')
    //     } catch (error) {
    //         console.error('Error restoring version:', error)
    //         //this.show_error('Failed to restore version')
    //     }
    // }

    // UI Methods

    html() {
        const container            = new Div({ class: 'markdown-container' })
        const editor_container     = new Div({ class: 'editor-container' })
        const editor_toolbar       = new Div({ class: 'editor-toolbar' })
        const preview_and_versions = new Div({ class: 'preview-and-versions' })
        const viewer_and_editor    = new Div({ class: 'viewer-and-editor' })
        const versions_container   = new Div({ class: 'versions-container' })

        preview_and_versions.add_elements(viewer_and_editor, versions_container)
        editor_container    .add_elements(preview_and_versions                 )
        container           .add_elements(editor_toolbar,  editor_container    )
        return container
    }

    final_ui_changes() {
        this.query_selector('.versions-container').hide()
    }

    css_rules() {
        return {
            ".markdown-container"   : { height          : "100%"                      ,         // Main container
                                        display         : "flex"                      ,
                                        flexDirection   : "column"                    ,
                                        backgroundColor : "#fff"                      ,
                                        borderRadius    : "0.375rem"                  ,
                                        boxShadow       : "0 2px 4px rgba(0,0,0,0.1)" },

            ".editor-container"     : { flex            : "1"                         ,         // Editor wrapper
                                        display         : "flex"                      ,
                                        flexDirection   : "column"                    ,
                                        padding         : "1rem"                      ,
                                        gap             : "1rem"                      },


            ".preview-and-versions" : { display         : "flex"                      ,         // Layout structure
                                        flexDirection   : "row"                       ,
                                        padding         : "10px"                      },

            ".versions-container"   : { flex            : "1"                         ,         // Versions panel
                                        overflow        : "auto"                      ,
                                        maxWidth        : "250px"                     ,
                                        padding         : "10px"                      },

            ".viewer-and-editor"    : { flex            : "1"                         ,         // Main content area
                                        padding         : "10px"                      },

        }
    }
}

WebC__User_Files__Markdown.define()