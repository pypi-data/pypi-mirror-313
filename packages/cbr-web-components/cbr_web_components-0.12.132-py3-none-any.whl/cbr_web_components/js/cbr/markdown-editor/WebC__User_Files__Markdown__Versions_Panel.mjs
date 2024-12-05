// WebC__Versions__Panel.mjs
import CBR_Events            from '../CBR_Events.mjs'
import Web_Component         from '../../core/Web_Component.mjs'
import CSS__Buttons          from '../../css/CSS__Buttons.mjs'
import CSS__Icons            from '../../css/icons/CSS__Icons.mjs'
import Div                   from '../../core/Div.mjs'
import Button                from '../../core/Button.mjs'
import Icon                  from '../../css/icons/Icon.mjs'
import CSS__Alerts           from "../../css/CSS__Alerts.mjs";
import CSS__Grid             from "../../css/grid/CSS__Grid.mjs";
import API__User_Data__Files from "../api/API__User_Data__Files.mjs";

export default class WebC__User_Files__Markdown__Versions_Panel extends Web_Component {

    constructor() {
        super();
        this.api     = new API__User_Data__Files()
        this.file_id = null
    }

    apply_css() {
        new CSS__Alerts (this).apply_framework()
        new CSS__Buttons(this).apply_framework()
        new CSS__Icons  (this).apply_framework()
        new CSS__Grid   (this).apply_framework()

        this.versions        = []
        this.current_version = null
        this.add_css_rules(this.css_rules())
    }

    add_event_listeners() {
        this.add_window_event_listener(CBR_Events.CBR__FILE__LOADED, this.on_file_loaded           )
        this.add_window_event_listener(CBR_Events.CBR__FILE__SAVED , this.on_file_loaded           )
        this.add_window_event_listener('versions-update'           , this.handle__versions_update  )
        this.add_window_event_listener('version-selected'          , this.handle__version_selected )
    }


    add_event_handlers() {
    this.query_selector_all('.view-btn').forEach(btn => {
        this.add_event__to_element__on('click', btn, this.handle__view_click, { version: btn.dataset.version })
    })

    this.query_selector_all('.restore-btn').forEach(btn => {
        this.add_event__to_element__on('click', btn, this.handle__restore_click, { version: btn.dataset.version })
    })
}

    // Event handlers

    handle__versions_update(event) {
        if (event.detail.file_id === this.file_id) {
            this.versions = event.detail.versions
            this.render()
        }
    }

    handle__version_selected(event) {
        if (event.detail.file_id === this.file_id) {
            this.current_version = event.detail.version_id
            this.render()
        }
    }

    handle__view_click({event, version}) {
        this.raise_version_event('version-view', version)
    }

    handle__restore_click({event, version}) {
        this.raise_version_event('version-restore', version)
    }

    // other methods

    async load_versions() {
        try {
            this.versions = await this.api.get_file_versions(this.file_id)
        } catch (error) {
            //console.error('Error loading versions:', error)
            this.versions = []
        }
    }

    async on_file_loaded(event) {
        this.file_id  = event.detail?.file_id
        await this.load_versions()
        await this.refresh_ui()
    }

    raise_version_event(event_name, version_id) {
        this.raise_event_global(event_name, { file_id    : this.file_id ,
                                              version_id : version_id   ,
                                              channel    : this.channel })
    }

    html() {
    //     const div_versions     = new Div({ class: 'versions-panel h-100pc'      })
    //     const primary_message  = new Div({ class: 'alert alert-primary h-100pc',  value:'versions will go here'})
    //     div_versions.add_element(primary_message)
    //     return div_versions
    // }
    //
    // html_versions() {
        const versions_list     = new Div({ class: 'versions-list'      })

        this.versions.forEach(version => {
            const version_item = new Div({ class: `version-item ${this.current_version === version.version_id ? 'current' : ''}` })


            const info           = new Div({ class: 'version-info'     })           // Version info section
            const version_header = new Div({ class: 'version-header'   })           // Version number and date/time
            const date_time      = new Div({ class: 'version-datetime' })           // Date and time
            const actions        = new Div({ class: 'version-actions'  })           // Version actions

            version_header.add_elements(new Div({ class: 'version-number', value: `Version ${version.version_number}`         }),
                                        new Div({ class: 'version-status', value: version.is_latest_version ? '(Latest)' : '' }))

            date_time     .add_elements(new Div({ class: 'version-date', value: version.created_date }),
                                        new Div({ class: 'version-time', value: version.created_time }))

            const size = new Div({class: 'version-size',  value: `${(version.file_size / 1024).toFixed(1)} KB` })       // File size

            info.add_elements(version_header, date_time, size)


            const view_btn = new Button({class     : 'btn btn-sm btn-outline-primary view-btn',
                                        value      : 'View',
                                        attributes : { 'data-version': version.version_id } })



            const restore_btn = new Button({class      : 'btn btn-sm btn-outline-success restore-btn',
                                            value      : 'Restore',
                                            attributes : { 'data-version': version.version_id } })

            view_btn    .add_element(new Icon({ icon: 'eye'    , size: 'sm', spacing: 'right' }))
            restore_btn .add_element(new Icon({ icon: 'history', size: 'sm', spacing: 'right' }))

            // Only add buttons if version_id is not null
            if (version.version_id !== 'null') { actions.add_elements(view_btn, restore_btn) }

            version_item .add_elements(info, actions)
            versions_list.add_element(version_item)
        })

        return versions_list
    }

    css_rules() {
        return {
            ".versions-panel" : { //height          : "100%"       ,
                                  boxSizing       : "border-box"
            },
            ".primary-message" : { height          : "100%"       ,
                                   boxSizing       : "border-box" } ,

            ".versions-list"     : { display          : "flex"                      ,         // List layout
                                    flexDirection    : "column"                    ,
                                    gap              : "0.75rem"                   },

            ".version-item"      : { padding          : "1rem"                      ,         // Version items
                                    backgroundColor  : "#f8f9fa"                   ,
                                    borderRadius     : "0.375rem"                  ,
                                    border           : "1px solid #dee2e6"         ,
                                    display          : "flex"                      ,
                                    justifyContent   : "space-between"             ,
                                    alignItems       : "center"                    },

            ".version-info"      : { fontSize         : "0.875rem"                  ,         // Version info
                                    color            : "#6c757d"                   },

            ".version-header"    : { display          : "flex"                      ,         // Version header
                                    alignItems       : "center"                    ,
                                    gap              : "0.5rem"                    ,
                                    marginBottom     : "0.25rem"                   },

            ".version-number"    : { fontWeight       : "600"                       ,         // Version number
                                    color            : "#212529"                   },

            ".version-status"    : { fontSize         : "0.75rem"                   ,         // Version status
                                    color            : "#198754"                   ,
                                    fontWeight       : "500"                       },

            ".version-datetime"  : { display          : "flex"                      ,         // DateTime
                                    gap              : "0.5rem"                    ,
                                    fontSize         : "0.875rem"                  ,
                                    color            : "#6c757d"                   ,
                                    marginBottom     : "0.25rem"                   },

            ".version-size"      : { fontSize         : "0.75rem"                   ,         // Size display
                                    color            : "#6c757d"                   },

            ".version-actions"   : { display          : "flex"                      ,         // Action buttons
                                    gap              : "0.5rem"                    ,
                                    alignItems       : "center"                    },

            ".version-item.current": { borderColor    : "#0d6efd"                   ,         // Current version
                                     borderWidth     : "2px"                       }
        }
    }
}

WebC__User_Files__Markdown__Versions_Panel.define()