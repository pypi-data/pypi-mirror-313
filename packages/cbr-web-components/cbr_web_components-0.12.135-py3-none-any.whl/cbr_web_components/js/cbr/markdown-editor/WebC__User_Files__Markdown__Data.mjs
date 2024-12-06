import Web_Component         from "../../core/Web_Component.mjs";
import Div                   from "../../core/Div.mjs";
import Text                  from "../../core/Text.mjs";
import CSS__Alerts           from "../../css/CSS__Alerts.mjs";
import CSS__Grid             from "../../css/grid/CSS__Grid.mjs";
import CBR_Events            from "../CBR_Events.mjs";
import API__User_Data__Files from "../api/API__User_Data__Files.mjs";

export default class WebC__User_Files__Markdown__Data extends Web_Component {

    constructor() {
        super();
        this.api     = new API__User_Data__Files()
        this.file_id = null
    }
    apply_css() {
        new CSS__Alerts (this).apply_framework()
        new CSS__Grid   (this).apply_framework()
        this.add_css_rules(this.css_rules())
    }

    add_event_listeners() {
        this.add_window_event_listener(CBR_Events.CBR__FILE__CANCEL    , this.on_file_load   )
        this.add_window_event_listener(CBR_Events.CBR__FILE__CHANGED   , this.on_file_changed)
        this.add_window_event_listener(CBR_Events.CBR__FILE__EDIT_MODE , this.on_edit_mode   )
        this.add_window_event_listener(CBR_Events.CBR__FILE__LOAD      , this.on_file_load   )
        this.add_window_event_listener(CBR_Events.CBR__FILE__SAVE      , this.on_file_save   )
    }

    component_ready() {
        this.show_message__info()
    }

    html() {
        const div_data_panel   = new Div({ class: 'data-panel'      })
        const primary_message  = new Text({ class: 'alert alert-primary data-message'})
        div_data_panel.add_element(primary_message)
        return div_data_panel
    }

    show_message(message='', alert_class='primary') {
        if (message) {
            this.text_data_message.show()
            this.text_data_message.innerText = message
            this.text_data_message.classList = `alert alert-${alert_class} data-message`        // reset the classes (since we need to remove the previous alert class)
        }
        else {
            this.text_data_message.hide()
        }
    }
    show_message__primary(message) { this.show_message(message, 'primary'  ) }
    show_message__success(message) { this.show_message(message, 'success'  ) }
    show_message__error  (message) { this.show_message(message, 'danger'   ) }
    show_message__warning(message) { this.show_message(message, 'warning'  ) }
    show_message__info   (message) { this.show_message(message, 'secondary') }

    get text_data_message() { return this.query_selector('.data-message')    }

    css_rules() {
        return { ".data-panel .alert" : { padding: "7 12 12 12"} }
    }

    // events/data methods

    on_edit_mode() {
        this.show_message()
    }
    on_file_changed() {
        this.show_message__warning('... unsaved changes... ')
    }

    async on_file_load(event) {
        this.file_id = event.detail?.file_id
        try {
            const { content, file_data } = await this.api.get_file_contents(this.file_id)
            this.markdown_content = content
            this.file_data        = file_data
            const event_params    = { content  : content      ,
                                      file_data: file_data    ,
                                      file_id  : this.file_id,}
            this.raise_event_global(CBR_Events.CBR__FILE__LOADED   , event_params)
            this.raise_event_global(CBR_Events.CBR__FILE__VIEW_MODE              )
            this.show_message('file data loaded ok')

        } catch (error) {
            this.raise_event_global(CBR_Events.CBR__FILE__LOAD_ERROR , {file_id: this.file_id, error:error})
            this.show_message__error(error.message)
        }
    }


    async on_file_save() {
        try {
            const event_response = this.raise_event_global(CBR_Events.CBR__FILE__GET_CONTENT, {file_id: this.file_id})
            const content        = event_response.detail.content
            this.show_message__primary('...saving file data')
            await this.api.update_file(this.file_id, content)
            this.show_message__success('Changes saved')
            this.raise_event_global(CBR_Events.CBR__FILE__SAVED    , {file_id: this.file_id})
            this.raise_event_global(CBR_Events.CBR__FILE__VIEW_MODE, {file_id: this.file_id})
        } catch (error) {
            this.show_message__error(error.message)
            this.raise_event_global(CBR_Events.CBR__FILE__SAVE_ERROR , {file_id: this.file_id, error:error})
        }

    }
}

WebC__User_Files__Markdown__Data.define()