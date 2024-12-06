import Web_Component       from '../../core/Web_Component.mjs';
import Button              from '../../core/Button.mjs';
import Div                 from '../../core/Div.mjs';
import Input               from '../../core/Input.mjs';
import Label               from '../../core/Label.mjs';
import Select              from '../../core/Select.mjs';
import Option              from '../../core/Option.mjs';
import Icon                from '../icons/Icon.mjs';
import CSS__Forms          from '../CSS__Forms.mjs';
import CSS__Typography     from '../CSS__Typography.mjs';
import CSS__Cards          from '../CSS__Cards.mjs';
import CSS__Buttons        from '../CSS__Buttons.mjs';
import CSS__Icons          from '../icons/CSS__Icons.mjs';
import CSS__Alerts         from '../CSS__Alerts.mjs';
import WebC__Events_Viewer from '../../utils/WebC__Events_Viewer.mjs';

export default class WebC__Component__Tester extends Web_Component {
    // server_check_interval = 1000                                            // Check every second
    // current_server_id    = null                                             // Track current server ID

    ws_connection        = null                                                    // Track WebSocket connection
    ws_retry_count      = 0                                                       // Track connection retry attempts
    ws_max_retries      = 5                                                       // Maximum number of retries
    ws_retry_delay      = 1000                                                    // Initial retry delay (1 second)

    add_events_viewer    = false
    base_path            = '/web_components/js/'
    presets              = [ { label: 'Markdown editor'    , path: 'cbr/markdown-editor/WebC__User_Files__Markdown.mjs'},
                             { label: 'Document Assistant' , path: 'cbr/document-assistant/WebC__Document__Assistant.mjs'      },
                             { label: 'User Files'         , path: 'cbr/file-system/WebC__User_Files.mjs'                   },
                             { label: 'User Session'       , path: 'cbr/session/WebC__CBR__User_Session.mjs'                   },
                             { label: 'Athena Examples'    , path: 'cbr/web-components/WebC__Athena__Examples.mjs'             },
                             { label: 'Athena Welcome'     , path: 'cbr/web-components/WebC__Athena__Welcome.mjs'              },
                             { label: 'Past Chats Welcome' , path: 'cbr/web-components/WebC__PastChats__Welcome.mjs'           }]

    apply_css() {
        this.add_css_rules(this.css_rules())
    }

    load_attributes() {
        new CSS__Forms     (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Buttons   (this).apply_framework()
        new CSS__Icons     (this).apply_framework()
        new CSS__Alerts    (this).apply_framework()
        this.script_path              = this.presets[0].path        // chose the first one
    }

    disconnectedCallback() {
        super.disconnectedCallback()
        this.stop_server_check()
    }

    add_web_components(){
        if (this.add_events_viewer){
          this.add_web_component_to(".events-viewer", WebC__Events_Viewer, {})
        }
    }

    async component_ready() {
        await this.refresh_component()
    }

    add_event_handlers() {
        const path_input    = this.shadowRoot.querySelector('.path-input'     )
        const preset_select = this.shadowRoot.querySelector('select'          )
        const refresh_btn   = this.shadowRoot.querySelector('.btn-primary'    )
        const container     = this.shadowRoot.querySelector('.tester-container')
        const auto_reload   = this.shadowRoot.querySelector('#auto-reload'    )
        const server_check  = this.shadowRoot.querySelector('#server-check'   )

        path_input.addEventListener('change', (e) => this.load_component(e.target.value))

        preset_select.addEventListener('change', (e) => {
            if (e.target.value) {
                path_input.value = e.target.value
                this.load_component(e.target.value)
            }
        })

        refresh_btn.addEventListener('click'     , () => this.refresh_component())
        container  .addEventListener('mouseenter', () => { if (auto_reload.checked) { this.refresh_component() }})

        server_check.addEventListener('change', (e) => {
            if (e.target.checked) {
                this.start_server_check()
            } else {
                this.stop_server_check()
            }
        })
    }

    async load_component(component_path) {
        const path = this.base_path + component_path
        const host = this.shadowRoot.querySelector('#component-host')
        const timestamp = Date.now()
        try {
            this.script_path        = component_path
            const module            = await import(path + '?t=' + timestamp)
            const original_name     = this.get_component_name(module.default.name)              // we need to do this to break the current cache of the defined web-component
            const versioned_name    = `${original_name}-${timestamp}`
            customElements.define(versioned_name, module.default)
            host.innerHTML      = `<${versioned_name}></${versioned_name}>`
            this.update_status('Component loaded successfully', 'success')
        } catch (error) {
            console.error('Failed to load component:', error)
            this.show_error(error.message)
        }
    }

    get_component_name(class_name) {
        return class_name.replace(/_/g, '-')                                        // Replace underscores with hyphens
                         .replace(/--/g, '-')                                       // Clean up double hyphens
                         .toLowerCase()                                             // Convert to lowercase
    }

    async refresh_component() {
        if (this.script_path) {
            await this.load_component(this.script_path)
        }
    }

    show_error(message) {
        const host = this.shadowRoot.querySelector('#component-host')
        const error_div = new Div({ class: 'alert alert-error' })
                            .add_element(new Div({
                                class: 'alert-content',
                                value: `Error: ${message}`
                            }))

        host.innerHTML = error_div.html()
        this.update_status('Failed to load component', 'error')
    }

    update_status(message, type = 'info') {
        const status_bar    = this.shadowRoot.querySelector('#status-bar')
        const status_text   = new Div({ class: `status-text color-${type}`,  value: message })
        const timestamp     = new Div({ class: 'status-text', value: new Date().toLocaleTimeString() })

        status_bar.innerHTML = ''
        status_bar.appendChild(status_text.dom_create())
        status_bar.appendChild(timestamp  .dom_create())
    }

    // async start_server_check() {
    //     if (this.current_stream) {
    //         this.stop_server_check()
    //     }
    //
    //     try {
    //         const wait_count = 200
    //         const wait_time  = 1
    //         const path       = `/api/user-data/notifications/live-stream?wait_count=${wait_count}&wait_time=${wait_time}`
    //         const response = await fetch(path)
    //         const reader = response.body.getReader()
    //         this.current_stream = reader
    //
    //         while (true) {
    //             const {value, done} = await reader.read()
    //
    //             if (done) {
    //                 console.log('Stream interrupted - server likely restarted')
    //                 this.update_status('Server restarted - reloading component', 'info')
    //                 await this.refresh_component()
    //                 await this.start_server_check()                                  // Restart stream
    //                 break
    //             }
    //
    //             // Continue receiving heartbeats
    //             const text = new TextDecoder().decode(value)
    //             console.log('Heartbeat received:', text)
    //         }
    //     } catch (error) {
    //         console.error('Stream error:', error)
    //         setTimeout(() => this.start_server_check(), 5000)                        // Retry after 5 seconds
    //     }
    // }
    //
    // stop_server_check() {
    //     if (this.current_stream) {
    //         this.current_stream.cancel()
    //         this.current_stream = null
    //     }
    // }


    start_server_check() {
        if (this.ws_connection) {
            this.stop_server_check()
        }

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host     = window.location.host;
        const path     = '/api/user-data/notifications/ws';
        this.ws_connection = new WebSocket(`${protocol}//${host}${path}`);

        this.ws_connection.onopen = () => {
            console.log('WebSocket connected')
            this.ws_retry_count = 0                                               // Reset retry count on successful connection
            this.update_status('Connected to server', 'success')
        }

        this.ws_connection.onmessage = async (event) => {
            const data = JSON.parse(event.data)
            //console.log('Heartbeat received:', data.data.timestamp)
        }

        this.ws_connection.onerror = (error) => {
            console.error('WebSocket error:', error)
            this.update_status('Connection error', 'error')
        }

        this.ws_connection.onclose = async () => {
            console.log('WebSocket connection closed')
            this.update_status('Server connection lost - reloading component', 'warning')

            // Attempt to reload the component
            await this.refresh_component()

            // Attempt to reconnect with exponential backoff
            if (this.ws_retry_count < this.ws_max_retries) {
                //const delay = this.ws_retry_delay * Math.pow(2, this.ws_retry_count)
                const delay = 0.1
                this.ws_retry_count++
                console.log(`Reconnecting in ${delay/1000} seconds...`, this.ws_retry_count, this.ws_max_retries)
                setTimeout(() => this.start_server_check(), delay)
            } else {
                console.log('Failed to reconnect to server', 'error')
            }
        }
    }

    stop_server_check() {
        if (this.ws_connection) {
            this.ws_connection.close()
            this.ws_connection = null
        }
        //this.ws_retry_count = 0                                                   // Reset retry count
    }


    html() {
        const container     = new Div   ({ class: 'tester-container'   })
        const card          = new Div   ({ class: 'card'               })
        const controls      = new Div   ({ class: 'controls'           })
        const events_viewer = new Div   ({ class: 'events-viewer'      })
        const input         = new Input ({class: 'input path-input',  value: this.script_path})
        const select        = new Select({ class: 'input'          })

        this.presets.forEach(preset => {
            select.add_element(new Option({ value: preset.path, text: preset.label }))
        })

        const refresh_btn   = new Button({ class: 'btn btn-primary',  title: 'Reload component'}).add_element(new Icon({icon: 'arrow-refresh', color: 'white', size: 'lg'}))
        const auto_reload   = new Div({ class: 'auto-reload' })
        const checkbox      = new Input({ type: 'checkbox',  id: 'auto-reload',  class: 'checkbox' })
        const label         = new Label({ for: 'auto-reload',  value: 'Reload on enter', class: 'checkbox-label'})
        const host          = new Div({ class: 'host-container',  id: 'component-host'})
        const status_bar    = new Div({ class: 'status-bar', id: 'status-bar'})
        const server_check  = new Div({ class: 'auto-reload' })
        const check_box     = new Input({ type: 'checkbox', id: 'server-check', class: 'checkbox' })
        const check_label   = new Label({ for: 'server-check', value: 'Auto reload on server change', class: 'checkbox-label'})

        server_check.add_elements(check_box, check_label)
        auto_reload .add_elements(checkbox, label)
        controls    .add_elements(select, refresh_btn, auto_reload, server_check, input)
        card        .add_elements(controls, host, status_bar)
        if (this.add_events_viewer) {
            container.add_elements(card, events_viewer)
        }
        container  .add_elements(card)

        return container
    }

    css_rules() {
        return {
            ".tester-container" : { display         : "flex"           ,        // Container for the whole component
                                    flexDirection   : "row"            ,
                                    gap             : "1rem"           ,

                                    backgroundColor: "red"},
            ".card"             : { flex            : 1                ,
                                    padding         : "1.5rem"         },       // Card wrapper
            ".controls"         : { display         : "grid"           ,        // Controls section
                                    gap            : "1rem"            ,
                                    gridTemplateColumns: "1fr 1fr auto",
                                    marginBottom   : "1rem"            },
            ".events-viewer"    : { flex           : 1                 },
            ".path-input"       : { gridColumn      : "1 / -1"         },       // Script path input spans full width
            ".host-container"   : { backgroundColor : "var(--table-striped-bg)",// Container for tested component
                                    borderRadius    : "0.375rem"       ,
                                    padding        : "1.5rem"         ,
                                    minHeight      : "200px"          },
            ".load-indicator"   : { display         : "flex"           ,        // Loading indicator
                                    justifyContent  : "center"         ,
                                    alignItems      : "center"         ,
                                    height         : "100%"           },
            ".status-bar"       : { display         : "flex"           ,        // Status information
                                    justifyContent  : "space-between"  ,
                                    alignItems      : "center"         ,
                                    marginTop      : "1rem"           },
            ".status-text"      : { fontSize        : "0.875rem"       ,        // Status text
                                    color          : "var(--color-muted)" },
            ".auto-reload"      : { display        : "flex"     ,
                                    alignItems     : "center"   ,
                                    gap            : "0.5rem"   }
        }
    }
}

WebC__Component__Tester.define()