import Web_Component   from '../../core/Web_Component.mjs';
import Button          from '../../core/Button.mjs'       ;
import Div             from '../../core/Div.mjs'          ;
import Input           from '../../core/Input.mjs'        ;
import Form            from '../../core/Form.mjs'         ;
import H               from '../../core/H.mjs'            ;
import HR              from '../../core/HR.mjs'           ;
import Label           from '../../core/Label.mjs'        ;
import Option          from '../../core/Option.mjs'       ;
import Select          from '../../core/Select.mjs'       ;
import Text            from '../../core/Text.mjs'         ;
import Textarea        from '../../core/Textarea.mjs'     ;
import CSS__Forms      from  '../CSS__Forms.mjs'          ;
import CSS__Typography from "../CSS__Typography.mjs";


export default class WebC__CSS__Demo__Forms extends Web_Component {

    load_attributes() {
        this.css_forms      = new CSS__Forms(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css      = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({id: 'forms-demo'})

        // Header elements
        let header_text = 'Forms Demo'
        if (this.apply_css) { header_text += ' (with CSS)' }
        let header = [
            new HR(),
            new Text({value: header_text}),
            new HR()
        ]

        // Basic Form Controls
        let h_basic = new H({level: 2, value: 'Form Controls'})
        let basics = [
            new Div({class: 'field-group'}).add_elements(
                new Label({class: 'label', value: 'Email address'}),
                new Input({type: 'email',  class: 'input',  placeholder: 'name@example.com' }),
                new Text({class: 'help', value: 'Enter your email address'})
            ),
            new Div({class: 'field-group'}).add_elements(
                new Label({class: 'label', value: 'Message'}),
                new Textarea({ class: 'input',  attributes: {rows: '3'} ,value:''})
            ),
            new Div({class: 'field-group'}).add_elements(
                new Label({class: 'label', value: 'Disabled input'}),
                new Input({ type: 'text',  class: 'input',  placeholder: 'Disabled input',  attributes: {disabled: true}
                })
            ),
            new Div({class: 'field-group'}).add_elements(
                new Label({class: 'label', value: 'Readonly input'}),
                new Input({
                    type: 'text',
                    class: 'input',
                    value: 'Readonly input',
                    attributes: {readonly: true}
                })
            )
        ]

        // Input Sizes
        let h_sizes = new H({level: 2, value: 'Input Sizes'})
        let sizes = [
            new Div({class: 'field-group'}).add_elements(
                new Input({class: 'input input-large', type: 'text', placeholder: 'Large input'})
            ),
            new Div({class: 'field-group'}).add_elements(
                new Input({class: 'input', type: 'text', placeholder: 'Default input'})
            ),
            new Div({class: 'field-group'}).add_elements(
                new Input({class: 'input input-small', type: 'text', placeholder: 'Small input'})
            )
        ]

        // Select Controls
        let h_select = new H({level: 2, value: 'Select Controls'})
        let selects = [
            new Div({class: 'field-group'}).add_elements(
                new Label({class: 'label', value: 'Default select'}),
                new Select({class: 'input'}).add_elements(
                    new Option({value: '', selected: true, text: 'Open this select menu'}),
                    new Option({value: '1', text: 'One'}),
                    new Option({value: '2', text: 'Two'}),
                    new Option({value: '3', text: 'Three'})
                )
            ),
            new Div({class: 'field-group'}).add_elements(
                new Label({class: 'label', value: 'Multiple select'}),
                new Select({class: 'input', attributes: {multiple: true}}).add_elements(
                    new Option({value: '1', text: 'One'}),
                    new Option({value: '2', text: 'Two'}),
                    new Option({value: '3', text: 'Three'}),
                    new Option({value: '4', text: 'Four'})
                )
            )
        ]

        // Validation States
        let h_validation = new H({level: 2, value: 'Validation States'})
        let validations = [
            new Div({class: 'field-group'}).add_elements(
                new Label({class: 'label', value: 'Valid input'}),
                new Input({type: 'text', class: 'input valid', value: 'Valid value'}),
                new Text({class: 'help valid', value: 'Looks good!'})
            ),
            new Div({class: 'field-group'}).add_elements(
                new Label({class: 'label', value: 'Invalid input'}),
                new Input({type: 'text', class: 'input invalid', value: 'Invalid value'}),
                new Text({class: 'help invalid', value: 'Please provide a valid value.'})
            )
        ]

        // Checkboxes and Radios
        let h_checks = new H({level: 2, value: 'Checkboxes and Radios'})
        let checks = [
            new Div({class: 'field-group'}).add_elements(
                new Div({class: 'checkbox-group'}).add_elements(
                    new Input({class: 'checkbox', type: 'checkbox', id: 'check1'}),
                    new Label({class: 'checkbox-label', for: 'check1', value: 'Default checkbox'})
                ),
                new Div({class: 'checkbox-group'}).add_elements(
                    new Input({class: 'checkbox', type: 'checkbox', id: 'check2', attributes: {checked: true}}),
                    new Label({class: 'checkbox-label', for: 'check2', value: 'Checked checkbox'})
                ),
                new Div({class: 'radio-group'}).add_elements(
                    new Input({class: 'radio', type: 'radio', name: 'radioGroup', id: 'radio1'}),
                    new Label({class: 'radio-label', for: 'radio1', value: 'Default radio'})
                ),
                new Div({class: 'radio-group'}).add_elements(
                    new Input({class: 'radio', type: 'radio', name: 'radioGroup', id: 'radio2', attributes: {checked: true}}),
                    new Label({class: 'radio-label', for: 'radio2', value: 'Selected radio'})
                )
            )
        ]

        // Input Groups
        let h_groups = new H({level: 2, value: 'Input Groups'})
        let groups = [
            new Div({class: 'field-group'}).add_elements(
                new Div({class: 'input-group'}).add_elements(
                    new Text({class: 'input-addon', value: '@'}),
                    new Input({class: 'input', type: 'text', placeholder: 'Username'})
                )
            ),
            new Div({class: 'field-group'}).add_elements(
                new Div({class: 'input-group'}).add_elements(
                    new Input({class: 'input', type: 'text', placeholder: 'Amount'}),
                    new Text({class: 'input-addon', value: '.00'})
                )
            ),
            new Div({class: 'field-group'}).add_elements(
                new Div({class: 'input-group'}).add_elements(
                    new Text({class: 'input-addon', value: '$'}),
                    new Input({class: 'input', type: 'text', placeholder: 'Amount'}),
                    new Text({class: 'input-addon', value: '.00'})
                )
            )
        ]

        // Plaintext Readonly Section
        let h_plaintext = new H({level: 2, value: 'Readonly Plain Text'})
        let plaintext = [
            new Div({class: 'field-group'}).add_elements(
                new Label({class: 'label', value: 'Email'}),
                new Input({
                    type: 'text',
                    class: 'input input-plain',
                    value: 'email@example.com',
                    attributes: {readonly: true}
                })
            ),
            new Div({class: 'field-group'}).add_elements(
                new Label({class: 'label', value: 'Password'}),
                new Input({
                    type: 'password',
                    class: 'input',
                    attributes: {readonly: true}
                })
            )
        ]

        // Inline Form Section
        let h_inline = new H({level: 2, value: 'Inline Form'})
        let inline = [
            new Form({class: 'inline-form'}).add_elements(
                new Div({class: 'field-group'}).add_elements(
                    new Label({ class: 'label visually-hidden', value: 'Email'}),
                    new Input({ type: 'text', class: 'input input-plain',
                                value: 'email@example.com', attributes: {readonly: true}
                    })
                ),
                new Div({class: 'field-group'}).add_elements(
                    new Label({ class: 'label visually-hidden', value: 'Password'}),
                    new Input({ type: 'password',
                                class: 'input',
                                value: 'secure password',
                                placeholder: 'Password'
                    })
                ),
                new Button({
                    class: 'button button-primary',
                    value: 'Confirm identity'
                })
            )
        ]

        // File Inputs Section
        let h_files = new H({level: 2, value: 'File Inputs'})
        let files   = [ new Div({class: 'field-group'}).add_elements(new Label({ class: 'label', value: 'Default file input'                       }),
                                                                     new Input({ type : 'file' ,  class: 'input-file'                              })),

                        new Div({class: 'field-group'}).add_elements(new Label({ class: 'label', value: 'Multiple files input'                     }),
                                                                     new Input({ type : 'file' , class: 'input-file', attributes: {multiple: true} })),

                        new Div({class: 'field-group'}).add_elements(new Label({ class: 'label', value: 'Disabled file input'                      }),
                                                                     new Input({ type : 'file' , class: 'input-file', attributes: {disabled: true} }) ),

                        new Div({class: 'field-group'}).add_elements(new Label({ class: 'label', value: 'Small file input'                         }),
                                                                     new Input({ type : 'file' , class: 'input-file input-small'                   })),

                        new Div({class: 'field-group'}).add_elements(new Label({ class: 'label', value: 'Large file input'                         }),
                                                                     new Input({ type : 'file' , class: 'input-file input-large'                   }) )]

        div_root.add_elements(...header,
                              h_basic     , ...basics     ,
                              h_sizes     , ...sizes      ,
                              h_select    , ...selects    ,
                              h_validation, ...validations,
                              h_checks    , ...checks     ,
                              h_groups    , ...groups     ,
                              h_plaintext, ...plaintext   ,
                              h_inline    , ...inline     ,
                              h_files     , ...files      )

        // Apply CSS and render
        if (this.apply_css) {
            this.css_forms     .apply_framework()
            this.css_typography.apply_framework()
        }
        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Forms.define()