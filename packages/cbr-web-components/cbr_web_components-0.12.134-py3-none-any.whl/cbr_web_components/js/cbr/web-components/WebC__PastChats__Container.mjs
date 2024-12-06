import Web_Component    from '../../core/Web_Component.mjs';
import Layout          from '../../css/grid/Layout.mjs';
import CSS__Grid       from '../../css/grid/CSS__Grid.mjs';
import CSS__Typography from '../../css/CSS__Typography.mjs';
import CSS__Tables     from '../../css/CSS__Tables.mjs';
import CSS__Cards      from '../../css/CSS__Cards.mjs';
import API__Invoke     from '../../data/API__Invoke.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import Table           from '../../core/Table.mjs';
import THead           from '../../core/THead.mjs';
import TBody           from '../../core/TBody.mjs';
import TR              from '../../core/TR.mjs';
import TH              from '../../core/TH.mjs';
import TD              from '../../core/TD.mjs';
import A               from '../../core/A.mjs';
import Text            from '../../core/Text.mjs';

export default class WebC__PastChats__Container extends Web_Component {

    constructor() {
        super()
        this.api_invoke = new API__Invoke()
    }

    apply_css() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        new CSS__Tables    (this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        this.add_css_rules(this.css_rules())
    }

    async load_data() {
        await this.load_chats()
    }

    async load_chats() {
        try {
            const response = await this.api_invoke.invoke_api('/api/user-data/chats/chats', 'GET')
            const saved_chats = response?.saved_chats && typeof response.saved_chats === 'object' && !Array.isArray(response.saved_chats)
                                    ? response.saved_chats
                                    : {}
            this.chats = Object.entries(saved_chats).map(([id, chat]) => ({
                id,
                ...chat
            })).sort((a, b) => b.timestamp - a.timestamp)
            this.render()
        } catch (error) {
            //console.error('Error loading chats:', error)
            this.chats = []
        }
    }

    create_intro_card() {
        const card = new Div({ class: 'card mb-4' })
        const body = new Div({ class: 'card-body' })
        const title = new H({
            level: 2,
            class: 'card-title',
            value: 'Past Chats'
        })
        const description = new Div({
            class: 'card-text',
            value: 'View and manage your previous conversations with Athena. Each chat is saved and can be accessed in different formats - as a web page, PDF document, or image.'
        })

        body.add_elements(title, description)
        card.add_element(body)
        return card
    }

    format_date_time(date, time) {
        if (!date || !time) return '-'
        return `${date} ${time}`
    }

    format_size(bytes) {
        return bytes
        // if (!bytes) return '0.0 KB'
        // const kb = bytes / 1024
        // return `${kb.toFixed(1)} KB`
    }

    create_action_links(chat) {
        if (!chat?.chat_id) return new Div()

        const container  = new Div({ class: 'action-links' })
        const view_link  = new A  ({ value: 'view' ,  href: `/web/chat/view/${chat.chat_path}`      ,  target: '_blank' }) // View link
        const pdf_link   = new A  ({ value: 'pdf'  ,  href: `/web/chat/view/${chat.chat_path}/pdf`  ,  target: '_blank' }) // PDF link
        const image_link = new A  ({ value: 'image',  href: `/web/chat/view/${chat.chat_path}/image`,  target: '_blank' }) // Image link


        const separator1 = new Text({ value: ' | ' })               // Separators
        const separator2 = new Text({ value: ' | ' })

        container.add_elements(view_link, separator1, pdf_link, separator2, image_link)
        return container
    }

    html() {
        const layout = new Layout({ class: 'container' })

        layout.add_element(this.create_intro_card())                                // Add intro card
        const table = new Table({ class: 'table' })                                 // Create table

        const thead = new THead().add_element (new TR()                             // Table header
                                 .add_elements(new TH({ value: 'Date/Time'   }),
                                               new TH({ value: 'Last Prompt' }),
                                               new TH({ value: 'History'     }),
                                               new TH({ value: 'Prompts'     }),
                                               new TH({ value: 'Responses'   }),
                                               new TH({ value: 'Actions'     })))

        const tbody = new TBody()                                                   // Table body

        if (this.chats && this.chats.length > 0) {
            this.chats.forEach(chat => {
                const row = new TR().add_elements(new TD({ value: this.format_date_time(chat.date, chat.time) }),
                                                  new TD({ value: chat.last_user_prompt                       }),
                                                  new TD({ value: chat.history_size                           }),
                                                  new TD({ value: this.format_size(chat.prompts_size)         }),
                                                  new TD({ value: this.format_size(chat.responses_size)       }),
                                                  new TD().add_element(this.create_action_links(chat)         ))
                tbody.add_element(row)
            })
        } else {
            tbody.add_element(new TR().add_element(new TD({ value     : 'No saved chats found',
                                                            attributes: { colspan: '6'        },
                                                            class      : 'text-center'        })))
        }

        table.add_elements(thead, tbody)
        layout.add_element(table)

        return layout
    }

    css_rules() {
        return {
            ".container": {
                padding: "1rem"
            },
            ".card": {
                backgroundColor: "#ffffff",
                borderRadius: "8px",
                marginBottom: "2rem"
            },
            ".card-title": {
                fontSize: "1.5rem",
                fontWeight: "500",
                marginBottom: "1rem"
            },
            ".card-text": {
                color: "#666",
                lineHeight: "1.5"
            },
            ".table": {
                backgroundColor: "#ffffff",
                width: "100%",
                marginBottom: "1rem",
                borderCollapse: "collapse"
            },
            ".table th": {
                borderBottom: "2px solid #dee2e6",
                padding: "0.75rem",
                textAlign: "left",
                fontWeight: "500"
            },
            ".table td": {
                padding: "0.75rem",
                borderBottom: "1px solid #dee2e6"
            },
            "a": {
                color: "#4A90E2",
                textDecoration: "none"
            },
            "a:hover": {
                textDecoration: "underline"
            },
            ".action-links": {
                whiteSpace: "nowrap"
            }
        }
    }
}

WebC__PastChats__Container.define()