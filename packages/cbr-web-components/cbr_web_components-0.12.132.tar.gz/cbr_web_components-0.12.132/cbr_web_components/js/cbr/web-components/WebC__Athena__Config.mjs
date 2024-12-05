import Web_Component    from '../../core/Web_Component.mjs';
import CSS__Cards       from '../../css/CSS__Cards.mjs';
import CSS__Forms       from '../../css/CSS__Forms.mjs';
import CSS__Typography  from '../../css/CSS__Typography.mjs';
import Div              from '../../core/Div.mjs';
import H                from '../../core/H.mjs';
import CSS__Grid from "../../css/grid/CSS__Grid.mjs";

export default class WebC__Athena__Config extends Web_Component {

    load_attributes() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Forms     (this).apply_framework()
        new CSS__Typography(this).apply_framework()

        this.channel            = this.getAttribute('channel')
        this.show_system_prompt = localStorage.getItem('athena_show_system_prompt') === 'true'
        this.edit_mode          = localStorage.getItem('athena_edit_mode'         ) === 'true'
    }

    add_event_listeners() {
        this.add_event__on('change', '#system-prompt-toggle', this.handle_system_prompt_change)
        this.add_event__on('change', '#edit-mode-toggle'    , this.handle_edit_mode_change    )
    }

    handle_system_prompt_change({event}) {
        localStorage.setItem('athena_show_system_prompt', event.target.checked)
        this.dispatch_config_update()
    }

    handle_edit_mode_change({event}) {
        localStorage.setItem('athena_edit_mode', event.target.checked)
        this.dispatch_config_update()
    }

    dispatch_config_update() {
        this.raise_event_global('config-update', { channel           : this.channel                                                 ,
                                                   show_system_prompt: localStorage.getItem('athena_show_system_prompt') === 'true' ,
                                                   edit_mode         : localStorage.getItem('athena_edit_mode'         ) === 'true' })
    }

    html() {
        const card                 = new Div({ class: 'card m-1 bg-light-cyan' })
        const body                 = new Div({ class: 'card-body' })
        const title                = new H  ({ level: 3, class: 'card-title', value: 'Configuration' })
        const form                 = new Div({ class: 'form-group' })

        const system_prompt_toggle = this.create_form_switch({ id       : 'system-prompt-toggle'  ,
                                                               label    : 'Show System Prompt'    ,
                                                               checked  : this.show_system_prompt })

        const edit_mode_toggle     = this.create_form_switch({ id       : 'edit-mode-toggle'      ,
                                                               label    : 'Edit Mode'             ,
                                                               checked  : this.edit_mode          })

        form.add_elements(system_prompt_toggle, edit_mode_toggle)
        body.add_elements(title, form)
        card.add_element (body)

        return card
    }

    create_form_switch({ id, label, checked }) {
        const container           = new Div({ class   : 'mb-3'                   })
        const switch_container    = new Div({ class   : 'form-check form-switch' })
        const toggle_input        = new Div({ tag     : 'input'                  ,
                                              class   : 'form-check-input'       ,
                                              type    : 'checkbox'               ,
                                              id      : id                       })
        if (checked)
            toggle_input.attributes.checked = 'checked'
        const toggle_label        = new Div({ tag     : 'label'                  ,
                                              class   : 'form-check-label'       ,
                                              value   : label                    ,
                                              for     : id                       })

        switch_container.add_elements(toggle_input, toggle_label)
        container      .add_element (switch_container)
        return container
    }
}

WebC__Athena__Config.define()