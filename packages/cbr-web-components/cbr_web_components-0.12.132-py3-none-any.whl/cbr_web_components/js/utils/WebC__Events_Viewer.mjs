import Tag           from "../core/Tag.mjs"
import Table         from "../core/Table.mjs"
import Div           from "../core/Div.mjs"
import Web_Component from "../core/Web_Component.mjs"
import Button        from "../core/Button.mjs"
import Input         from "../core/Input.mjs"

export default class WebC__Events_Viewer extends Web_Component {    
    constructor() {
        super()
        this.channels.push('WebC__Events_Viewer')
        this.monitored_events = new Map()  // Map of event type to Set of targets
        this.events_data     = []
        this.index          = 0
        this.sort_column    = 0
        this.sort_direction = 'desc'
        this.filter_text    = ''
        this.refresh_timer  = null
        this.event_handler  = this.handle_event.bind(this)
        this.events_to_skip = ['mouseenter', 'resize', 'popstate', 'click', 'input']
    }

    connectedCallback() {
        super.connectedCallback()
        this.build()
        this.start_registry_monitoring()
    }

    disconnectedCallback() {
        super.disconnectedCallback()
        this.stop_monitoring_all()
        if (this.refresh_timer) {
            clearInterval(this.refresh_timer)
        }
    }

    start_registry_monitoring() {
        this.refresh_timer = setInterval(() => {
            this.update_monitored_events()
        }, 1000)
    }

    update_monitored_events() {
        for (const [target, events] of window._globalEventRegistry.entries()) {
            for (const event_type of Object.keys(events)) {
                if (!this.events_to_skip.includes(event_type)) {
                    if (!this.monitored_events.has(event_type)) {
                        this.monitored_events.set(event_type, new Set())
                    }
                    const targets = this.monitored_events.get(event_type)

                    if (!targets.has(target)) {
                        targets.add(target)
                        target.addEventListener(event_type, this.event_handler, true)
                    }
                }
            }
        }

        // Remove listeners for events no longer in registry
        for (const [event_type, targets] of this.monitored_events.entries()) {
            for (const target of targets) {
                if (!window._globalEventRegistry.has(target) ||
                    !window._globalEventRegistry.get(target)[event_type]) {
                    target.removeEventListener(event_type, this.event_handler, true)
                    targets.delete(target)
                }
            }
            if (targets.size === 0) {
                this.monitored_events.delete(event_type)
            }
        }

        this.update_events_list()
    }

    stop_monitoring_all() {
        for (const [event_type, targets] of this.monitored_events.entries()) {
            for (const target of targets) {
                target.removeEventListener(event_type, this.event_handler, true)
            }
        }
        this.monitored_events.clear()
    }

    handle_event(event) {
        // Don't capture own events
        if (event.target instanceof WebC__Events_Viewer) {
            return
        }

        const event_data = {
            index     : this.index++,
            type      : event.type,
            target    : this.get_target_info(event.target),
            data      : this.get_event_data(event),
            timestamp : new Date().getTime()
        }

        this.events_data.unshift(event_data)
        this.render_table_content()
    }

    get_event_data(event) {
        return JSON.stringify(event.detail)
        // try {
        //     const data = {
        //         detail         : event.detail,
        //         target        : this.get_target_info(event.target),
        //         current_target: event.currentTarget ? this.get_target_info(event.currentTarget) : null,
        //         bubbles       : event.bubbles,
        //         cancelable    : event.cancelable,
        //         timestamp     : event.timeStamp
        //     }
        //     return JSON.stringify(data)
        // } catch (error) {
        //     return 'Error serializing event data'
        // }
    }

    get_target_info(target) {
        if (!target) return 'unknown'

        let info = target.constructor?.name || 'unknown'
        if (target.tagName) {
            info += `:${target.tagName.toLowerCase()}`
        }
        if (target.id) {
            info += `#${target.id}`
        }
        if (target.className) {
            info += `.${target.className.split(' ').join('.')}`
        }
        return info
    }

    build() {
        this.set_inner_html(this.render_html())
        this.add_css_rules(this.css_rules())
        this.add_event_handlers()
        this.render_table_content()
    }

    add_event_handlers() {
        const filter_input = this.query_selector('#filter-input')
        const clear_btn = this.query_selector('#clear-events-btn')

        if (filter_input) {
            filter_input.addEventListener('input', (e) => {
                this.filter_text = e.target.value.toLowerCase()
                this.render_table_content()
            })
        }

        if (clear_btn) {
            clear_btn.addEventListener('click', () => {
                this.events_data = []
                this.index = 0
                this.render_table_content()
            })
        }

        const headers = this.query_selector_all('th')
        headers.forEach((header, index) => {
            header.addEventListener('click', () => this.sort_column_click(index))
        })
    }

    sort_column_click(column_index) {
        if (this.sort_column === column_index) {
            this.sort_direction = this.sort_direction === 'asc' ? 'desc' : 'asc'
        } else {
            this.sort_column = column_index
            this.sort_direction = 'asc'
        }
        this.render_table_content()
    }

    update_events_list() {
        const events_list = this.query_selector('#monitored-events')
        if (events_list) {
            const status = Array.from(this.monitored_events.entries())
                .sort(([typeA], [typeB]) => typeA.localeCompare(typeB))
                .map(([type, targets]) => `${type}`)
                .join(', ')
            events_list.textContent = status || 'No events monitored'
        }
    }

    render_html() {
        const container = new Div({ class: 'event_viewer' })

        // Header section
        const header = new Div({ class: 'viewer-header' })
        header.add_tag({ tag: 'h2', value: 'Event Activity Monitor' })

        // Controls section
        const controls = new Div({ class: 'viewer-controls' })
        controls.add_elements(
            new Button({
                id: 'clear-events-btn',
                class: 'control-btn',
                value: 'Clear Events'
            }),
            new Input({
                id: 'filter-input',
                class: 'event-input',
                attributes: { placeholder: 'Filter events...' }
            })
        )

        // Monitored events section
        const events_info = new Div({ class: 'events-info' })
        events_info.add_elements(
            new Div({ value: 'Monitored Events:' }),
            new Div({ id: 'monitored-events', class: 'events-list' })
        )

        // Table
        const table = new Table({ id: 'events-table', class: 'events-table' })
        table.headers = ['#', 'Event Type', 'Event Data']  // 'Target'

        // Table body for dynamic content
        const tbody = new Tag({ tag: 'tbody', id: 'events-tbody' })
        table.add_element(tbody)

        container.add_elements(header, controls, events_info, table)

        return container.html()
    }

    render_table_content() {
        const tbody = this.query_selector('#events-tbody')
        if (!tbody) return

        let filtered_data = this.events_data
        if (this.filter_text) {
            filtered_data = this.events_data.filter(event =>
                event.type.toLowerCase().includes(this.filter_text) ||
                event.target.toLowerCase().includes(this.filter_text) ||
                event.data.toLowerCase().includes(this.filter_text)
            )
        }

        // Apply sorting
        filtered_data.sort((a, b) => {
            let comparison = 0
            switch (this.sort_column) {
                case 0:
                    comparison = a.index - b.index;
                    break
                case 1:
                    comparison = a.type.localeCompare(b.type);
                    break
                case 2:
                    comparison = a.target.localeCompare(b.target);
                    break
                case 3:
                    comparison = a.data.localeCompare(b.data);
                    break
            }
            return this.sort_direction === 'asc' ? comparison : -comparison
        })

        // Update sort indicators
        const headers = this.query_selector_all('th')
        headers.forEach((header, index) => {
            header.classList.remove('sort-asc', 'sort-desc')
            if (index === this.sort_column) {
                header.classList.add(this.sort_direction === 'asc' ? 'sort-asc' : 'sort-desc')
            }
        })

        // Render table content
        tbody.innerHTML = filtered_data.map(event => `
            <tr>
                <td>${event.index}</td>
                <td>${event.type}</td>                
                <td>${event.data}</td>
            </tr>
        `).join('')
        // < td >${event.target} < /td>
    }

    css_rules() {
        return {
            "*"                : { fontFamily      : "Verdana"                    },    // Base styles

            ".event_viewer"    : { margin          : "0"                         ,     // Main container
                                 border          : "2px solid #e0e0e0"          ,
                                 padding         : "15px"                       ,
                                 backgroundColor : "#FCFCF0"                    },

            ".viewer-header"   : { marginBottom    : "15px"                      ,     // Header section
                                 borderBottom    : "1px solid #ddd"             ,
                                 padding         : "0 0 10px 0"                 },

            ".viewer-controls" : { display         : "flex"                      ,     // Controls area
                                 gap             : "10px"                       ,
                                 marginBottom    : "15px"                       ,
                                 flexWrap        : "wrap"                       },

            ".event-input"     : { padding         : "5px"                       ,     // Filter input
                                 width           : "200px"                      ,
                                 borderRadius    : "4px"                        ,
                                 border          : "1px solid #ccc"            },

            ".control-btn"     : { padding         : "5px 10px"                  ,     // Buttons
                                 borderRadius    : "4px"                        ,
                                 border          : "1px solid #666"            ,
                                 backgroundColor : "#fff"                       ,
                                 cursor          : "pointer"                    },

            ".control-btn:hover": { backgroundColor : "#f0f0f0"                  },    // Button hover

            ".events-info"     : { marginBottom    : "15px"                      ,     // Info section
                                 padding         : "10px"                       ,
                                 backgroundColor : "#fff"                       ,
                                 borderRadius    : "4px"                        ,
                                 boxShadow       : "0 1px 3px rgba(0,0,0,0.1)" },

            ".events-list"     : { marginTop       : "5px"                       ,     // Events list
                                 color           : "#666"                       ,
                                 fontSize        : "0.9em"                      ,
                                 wordWrap        : "break-word"                },

            ".events-table"    : { width           : "100%"                      ,     // Table styles
                                 borderCollapse  : "collapse"                   ,
                                 marginTop       : "10px"                       ,
                                 backgroundColor : "#fff"                       ,
                                 boxShadow       : "0 1px 3px rgba(0,0,0,0.1)" },

            ".events-table th" : { padding         : "8px"                       ,     // Table header
                                   backgroundColor : "#f8f9fa"                   ,
                                   cursor          : "pointer"                    ,
                                   textAlign       : "left"                       ,
                                   borderBottom    : "2px solid #ddd"            ,
                                   position        : "sticky"                     ,
                                   top             : "0"                         },

            ".events-table td" : { padding         : "8px"                       ,     // Table cells
                                   borderBottom    : "1px solid #ddd"            ,
                                   verticalAlign   : "top"                       },

            ".events-table td:nth-child(1)": { width           : "25px"                      ,     // # column
                                               textAlign       : "center"                     },

            ".events-table td:nth-child(2)": { width           : "100px"                     },    // Event Type column

            // ".events-table td:nth-child(3)": { width           : "250px"                     ,     // Target column
            //                                    wordBreak       : "break-all"                  },

            ".events-table td:nth-child(3)": { whiteSpace      : "pre-wrap"                  ,     // Event Data column
                                             wordBreak       : "break-all"                  },

            ".events-table tbody tr:hover": {                                           // Row hover
                                 backgroundColor : "#f5f5f5"                    },

            ".sort-asc::after" : { content         : '" ↑"'                      ,     // Sort indicators
                                 color           : "#666"                       },

            ".sort-desc::after": { content         : '" ↓"'                      ,
                                 color           : "#666"                       }
        }
    }
}

WebC__Events_Viewer.define()