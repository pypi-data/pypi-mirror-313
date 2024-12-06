import Web_Component                    from '../../core/Web_Component.mjs'
import CSS__Buttons                     from '../../css/CSS__Buttons.mjs'
import CSS__Icons                       from '../../css/icons/CSS__Icons.mjs'
import Div                              from '../../core/Div.mjs'
import Text                             from '../../core/Text.mjs'
import Button                           from '../../core/Button.mjs'
import Icon                             from '../../css/icons/Icon.mjs'
import CBR_Events                       from "../CBR_Events.mjs";
import WebC__User_Files__Markdown__Data from "./WebC__User_Files__Markdown__Data.mjs";

export default class WebC__User_Files__Markdown__Toolbar extends Web_Component {

    constructor() {
        super()
        this.file_id = null
    }

    apply_css() {
        new CSS__Buttons(this).apply_framework()
        new CSS__Icons  (this).apply_framework()
        this.add_css_rules(this.css_rules())
    }

    load_attributes() {
        this.file_id        = this.getAttribute('file-id')
        this.channel        = this.getAttribute('channel') || this.random_id('markdown_toolbar_')
        this.edit_mode      = this.getAttribute('edit-mode') === 'true'
        this.view_mode      = this.getAttribute('view-mode') || 'content'
    }

    add_event_listeners() {
        this.add_window_event_listener(CBR_Events.CBR__FILE__LOAD        , this.on_file_load      )
        this.add_window_event_listener(CBR_Events.CBR__FILE__VIEW_MODE   , this.on_file_view_mode )
        this.add_window_event_listener(CBR_Events.CBR__FILE__EDIT_MODE   , this.on_file_edit_mode )
        this.add_window_event_listener(CBR_Events.CBR__FILE__HIDE_HISTORY, this.on_hide_history   )
        this.add_window_event_listener(CBR_Events.CBR__FILE__SHOW_HISTORY, this.on_show_history   )
    }

    add_event_handlers() {
        this.add_event__on_click('.edit-btn'        , this.raise_toolbar_event, {event_name: CBR_Events.CBR__FILE__EDIT_MODE    })
        this.add_event__on_click('.cancel-btn'      , this.raise_toolbar_event, {event_name: CBR_Events.CBR__FILE__CANCEL       })
        this.add_event__on_click('.save-btn'        , this.raise_toolbar_event, {event_name: CBR_Events.CBR__FILE__SAVE         })
        this.add_event__on_click('.show-history-btn', this.raise_toolbar_event, {event_name: CBR_Events.CBR__FILE__SHOW_HISTORY })
        this.add_event__on_click('.hide-history-btn', this.raise_toolbar_event, {event_name: CBR_Events.CBR__FILE__HIDE_HISTORY })
    }

    add_web_components() {
        this.add_web_component_to('.markdown-data', WebC__User_Files__Markdown__Data)
    }

    on_file_load(event) {
        this.file_id = event.detail.file_id
    }

    on_file_view_mode() {
        this.btn_edit  .enable()
        this.btn_cancel.disable()
        this.btn_save  .disable()
    }

    on_file_edit_mode() {
        this.btn_edit  .disable()
        this.btn_cancel.enable()
        this.btn_save  .enable()
    }
    on_hide_history() {
        this.btn_show_history.show()
        this.btn_hide_history.hide()
    }

    on_show_history() {
        this.btn_show_history.hide()
        this.btn_hide_history.show()
    }
    raise_toolbar_event({event_name} ) {
        this.raise_event_global(event_name, { file_id  : this.file_id })
    }

    html() {
        const markdown_toolbar = new Div({ class: 'markdown-toolbar' })
        const left_group       = new Div({ class: 'left-group'       })
        const right_group      = new Div({ class: 'right-group'      })

        const save_btn          = new Button({ class: 'btn btn-success           save-btn'        })
        const cancel_btn        = new Button({ class: 'btn btn-secondary         cancel-btn'      })
        const edit_btn          = new Button({ class: 'btn btn-primary           edit-btn'        })
        const show_history_btn  = new Button({ class: 'btn btn-outline-secondary show-history-btn'})
        const hide_history_btn  = new Button({ class: 'btn btn-outline-secondary hide-history-btn'})
        const markdown_data     = new Div   ({ class: 'markdown-data'                             })
        save_btn        .add_elements(new Icon({ icon: 'save'   , size: 'sm', }), new Text({value: 'Save'        }))
        cancel_btn      .add_elements(new Icon({ icon: 'cross'  , size: 'sm', }), new Text({value: 'Cancel'      }))
        edit_btn        .add_elements(new Icon({ icon: 'edit'   , size: 'sm', }), new Text({value: 'Edit'        }))
        show_history_btn.add_elements(new Icon({ icon: 'history', size: 'sm', }), new Text({value: 'Show History'}))
        hide_history_btn.add_elements(new Icon({ icon: 'history', size: 'sm', }), new Text({value: 'Hide History'}))

        left_group      .add_elements(edit_btn, save_btn, cancel_btn, markdown_data)
        right_group     .add_elements(show_history_btn, hide_history_btn           )
        markdown_toolbar.add_elements(left_group, right_group                      )
        return markdown_toolbar
    }

    final_ui_changes() {
        this.btn_hide_history.hide()
    }

    // properties with dom elements
    get btn_edit()         { return this.query_selector('.edit-btn'        )}
    get btn_cancel()       { return this.query_selector('.cancel-btn'      )}
    get btn_save()         { return this.query_selector('.save-btn'        )}
    get btn_hide_history() { return this.query_selector('.hide-history-btn')}
    get btn_show_history() { return this.query_selector('.show-history-btn')}

    // css rules for this component
    css_rules() {
        return {
            ".markdown-toolbar"    : { display         : "flex"                      ,          // Main toolbar
                                       justifyContent  : "space-between"             , // Ensures the groups are at opposite ends
                                       padding         : "0.5rem 0"                  ,
                                       borderBottom    : "1px solid #dee2e6"         ,
            },
            ".markdown-data"          : { display: "inline-flex"                        },
        }
    }
}

WebC__User_Files__Markdown__Toolbar.define()