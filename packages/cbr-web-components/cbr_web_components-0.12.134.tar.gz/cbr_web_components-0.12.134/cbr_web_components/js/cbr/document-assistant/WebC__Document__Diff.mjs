// WebC__Document__Diff.mjs

import Web_Component from '../../core/Web_Component.mjs'
import CSS__Grid     from '../../css/grid/CSS__Grid.mjs'
import CSS__Cards    from '../../css/CSS__Cards.mjs'
import CSS__Buttons  from '../../css/CSS__Buttons.mjs'
import CSS__Icons    from '../../css/icons/CSS__Icons.mjs'
import API__Invoke   from '../../data/API__Invoke.mjs'
import Icon          from '../../css/icons/Icon.mjs'
import Div           from '../../core/Div.mjs'
import Button        from '../../core/Button.mjs'
import Raw_Html      from '../../core/Raw_Html.mjs'

export default class WebC__Document__Diff extends Web_Component {

    constructor() {
        super()
        this.api_invoke = new API__Invoke()
        this.changes    = null
        this.view_mode  = 'split'                    // 'split' or 'unified'
        this.add_css_rules(this.css_rules())
    }

    apply_css() {
        new CSS__Grid    (this).apply_framework()
        new CSS__Cards   (this).apply_framework()
        new CSS__Buttons (this).apply_framework()
        new CSS__Icons   (this).apply_framework()
    }

    load_attributes() {
        this.file_id    = this.getAttribute('file-id')
    }


    add_event_listeners() {
        this.add_window_event_listener('update-diff-view', this.handle__on_update_diff_view)
    }


    add_event_handlers() {
        this.add_event__on_click('.btn-secondary:not(:last-child)', this.toggle_view_mode   )     // View mode toggle
        this.add_event__on_click('.btn-success'                   , this.accept_changes     )     // Accept all button
        this.add_event__on_click('.btn-danger'                    , this.reject_changes     )     // Reject all button
        this.add_event__on_click('.btn-secondary:last-child'      , this.handle_close       )     // Close button
    }

    handle_close() {                                                                                // New method to handle close event
        this.raise_event_global('diff:hide')
    }

    handle__on_update_diff_view(event) {
        if (event.detail.file_id === this.file_id) {
            this.update_diff(event.detail.changes)
        }
    }

    async update_diff(result) {
        if (!result?.document) return

        this.changes     = result.document.changes
        this.new_version = result.document.new_version
        await this.refresh_ui()
    }

    toggle_view_mode() {
        this.view_mode = this.view_mode === 'split' ? 'unified' : 'split'
        this.render()
    }

    accept_changes() {
        if (!this.changes) return

        this.raise_event_global('changes:accept', { new_version: this.new_version,  changes    : this.changes })
        this.raise_event_global('diff:hide')
    }

    reject_changes() {
        this.raise_event_global('changes:reject')
        this.raise_event_global('diff:hide')
    }

    render_change_block(change) {
        const block = new Div({ class: `change-block change-type-${change.type}` })

        // Header with type, line numbers, and reason
        const header = new Div({ class: 'change-header' })
        header.add_elements(
            new Div({ class: 'change-type' , value: change.type.toUpperCase() }),
            //new Div({ class: 'change-lines', value: `Lines ${change.location.start_line}-${change.location.end_line}` }),
            new Div({ class: 'change-reason', value: change.reason })
        )

        // Content area depends on view mode
        const content = new Div({ class: `change-content change-content-${this.view_mode}` })

        if (this.view_mode === 'split') {
            // Left side (original)
            const original = new Raw_Html({
                class: 'content-original',
                value: `<pre><code>${this.highlight_diff_lines(change.original, 'removed')}</code></pre>`
            })

            // Right side (updated)
            const updated = new Raw_Html({
                class: 'content-updated',
                value: `<pre><code>${this.highlight_diff_lines(change.updated, 'added')}</code></pre>`
            })

            content.add_elements(original, updated)
        } else {
            // Unified view
            const unified = new Raw_Html({
                class: 'content-unified',
                value: this.create_unified_diff(change.original, change.updated)
            })
            content.add_element(unified)
        }

        // Individual change controls
        const controls = new Div({ class: 'change-controls' })
        const accept_btn = new Button({
            class: 'btn btn-success btn-sm',
            value: 'Accept'
        })
        accept_btn.add_element(new Icon({ icon: 'check', size: 'sm', spacing: 'right' }))

        const reject_btn = new Button({
            class: 'btn btn-danger btn-sm',
            value: 'Reject'
        })
        reject_btn.add_element(new Icon({ icon: 'cross', size: 'sm', spacing: 'right' }))

        controls.add_elements(accept_btn, reject_btn)

        block.add_elements(header, content, controls)
        return block
    }

    highlight_diff_lines(text, type) {
        // Add syntax highlighting and diff markers
        return text.split('\n').map(line => {
            const marker = type === 'added' ? '+' : '-'
            return `<span class="diff-line diff-${type}">${marker} ${this.escape_html(line)}</span>`
        }).join('\n')
    }

    create_unified_diff(original, updated) {
        const lines = []
        const orig_lines = original.split('\n')
        const upd_lines = updated.split('\n')

        // Add removed lines first
        orig_lines.forEach(line => {
            lines.push(`<span class="diff-line diff-removed">- ${this.escape_html(line)}</span>`)
        })

        // Add added lines
        upd_lines.forEach(line => {
            lines.push(`<span class="diff-line diff-added">+ ${this.escape_html(line)}</span>`)
        })

        return `<pre><code>${lines.join('\n')}</code></pre>`
    }

    escape_html(text) {
        const div = document.createElement('div')
        div.textContent = text
        return div.innerHTML
    }

    html() {
        const container = new Div({ class: 'diff-container' })

        // Header with controls
        const header = new Div({ class: 'diff-header' })

        // Title and stats
        const title = new Div({ class: 'diff-title' })
        title.add_elements(
            new Icon({ icon: 'file', size: 'md', spacing: 'right' }),
            new Div({ value: 'Proposed Changes' })
        )

        if (this.changes) {
            title.add_element(
                new Div({
                    class: 'diff-stats',
                    value: `${this.changes.length} changes`
                })
            )
        }

        // Main controls
        const controls = new Div({ class: 'diff-controls' })

        // View mode toggle
        const view_toggle = new Button({
            class: 'btn btn-secondary btn-sm',
            value: this.view_mode === 'split' ? 'Unified View' : 'Split View'
        })
        view_toggle.add_element(new Icon({ icon: 'eye', size: 'sm', spacing: 'right' }))

        // Accept/Reject all
        const accept_btn = new Button({ class: 'btn btn-success btn-sm',  value: 'Accept All'})
        accept_btn.add_element(new Icon({ icon: 'check', size: 'sm', spacing: 'right' }))

        const reject_btn = new Button({ class: 'btn btn-danger btn-sm',  value: 'Reject All'})
        reject_btn.add_element(new Icon({ icon: 'cross', size: 'sm', spacing: 'right' }))

        // Close button
        const close_btn = new Button({ class: 'btn btn-secondary btn-sm',  value: 'Close'})
        close_btn.add_element(new Icon({ icon: 'close', size: 'sm', spacing: 'right' }))

        controls.add_elements(view_toggle, accept_btn, reject_btn, close_btn)
        header.add_elements(title, controls)

        // Changes content
        const content = new Div({ class: 'diff-content' })

        if (this.changes && this.changes.length > 0) {
            this.changes.forEach(change => {
                content.add_element(this.render_change_block(change))
            })
        } else {
            content.add_element(
                new Div({
                    class: 'diff-placeholder',
                    value: 'No changes to display'
                })
            )
        }

        container.add_elements(header, content)
        return container



    }


    css_rules() {
        return {
            ".diff-container"      : { display         : "flex"                      ,      // Main container
                                      flexDirection    : "column"                    ,
                                      height          : "100%"                      ,
                                      backgroundColor : "#fff"                      ,
                                      position        : "relative"                  },

            ".diff-header"         : { display         : "flex"                      ,      // Header area
                                      justifyContent  : "space-between"             ,
                                      alignItems      : "center"                    ,
                                      padding         : "0.75rem"                   ,
                                      borderBottom    : "1px solid #dee2e6"         ,
                                      backgroundColor : "#f8f9fa"                   },

            ".diff-title"          : { fontSize        : "1rem"                      ,      // Header title
                                      fontWeight      : "500"                       ,
                                      color           : "#212529"                   },

            ".diff-actions"        : { display         : "flex"                      ,      // Action buttons
                                      gap             : "0.5rem"                    },

            ".diff-content"        : { flex            : "1"                         ,      // Content area
                                      overflow        : "auto"                      ,
                                      padding         : "1rem"                      },

            ".diff-section"        : { marginBottom    : "1.5rem"                   ,      // Individual diff section
                                      border          : "1px solid #dee2e6"         ,
                                      borderRadius    : "0.375rem"                  ,
                                      overflow        : "hidden"                    },

            ".section-header"      : { display         : "flex"                      ,      // Section header
                                      justifyContent  : "space-between"             ,
                                      alignItems      : "center"                    ,
                                      padding         : "0.75rem"                   ,
                                      backgroundColor : "#f8f9fa"                   ,
                                      borderBottom    : "1px solid #dee2e6"         },

            ".section-title"       : { fontSize        : "0.875rem"                  ,      // Section title
                                      fontWeight      : "500"                       },

            ".section-actions"     : { display         : "flex"                      ,      // Section actions
                                      gap             : "0.5rem"                    },

            ".diff-block"          : { display         : "flex"                      ,      // Diff content block
                                      flexDirection   : "column"                    ,
                                      fontSize        : "0.875rem"                  ,
                                      fontFamily      : "Monaco, monospace"         ,
                                      lineHeight      : "1.5"                      },

            ".diff-line"          : { display         : "flex"                      ,      // Individual diff line
                                      padding         : "0.125rem 0.5rem"           ,
                                      whiteSpace     : "pre-wrap"                  },

            ".line-number"        : { width           : "3rem"                      ,      // Line numbers
                                      color           : "#6c757d"                   ,
                                      textAlign      : "right"                     ,
                                      paddingRight   : "1rem"                     ,
                                      userSelect     : "none"                     },

            ".line-content"       : { flex            : "1"                         ,      // Line content
                                      paddingLeft    : "0.5rem"                    },

            // Line types
            ".line-context"       : { backgroundColor : "#fff"                      },     // Unchanged line

            ".line-addition"      : { backgroundColor : "#e6ffed"                   ,      // Added line
                                      "& .line-number": { color: "#22863a"         },
                                      "& .line-content": { color: "#22863a"        }},

            ".line-deletion"      : { backgroundColor : "#ffeef0"                   ,      // Removed line
                                      "& .line-number": { color: "#cb2431"         },
                                      "& .line-content": { color: "#cb2431"        }},

            ".line-modification"  : { backgroundColor : "#fff5b1"                   ,      // Modified line
                                      "& .line-number": { color: "#735c0f"         },
                                      "& .line-content": { color: "#735c0f"        }},

            // Stats and summary
            ".diff-stats"         : { display         : "flex"                      ,      // Diff statistics
                                      gap             : "1rem"                      ,
                                      padding         : "0.5rem"                    ,
                                      borderBottom    : "1px solid #dee2e6"         ,
                                      backgroundColor : "#f8f9fa"                   },

            ".stat-item"          : { display         : "flex"                      ,      // Individual stat
                                      alignItems      : "center"                    ,
                                      gap             : "0.25rem"                   ,
                                      fontSize        : "0.75rem"                   },

            ".stat-addition"      : { color           : "#22863a"                   },     // Stat colors
            ".stat-deletion"      : { color           : "#cb2431"                   },
            ".stat-modification"  : { color           : "#735c0f"                   },

            // Change navigation
            ".diff-navigation"    : { position        : "sticky"                    ,      // Navigation controls
                                      bottom          : "0"                         ,
                                      display         : "flex"                      ,
                                      justifyContent  : "center"                    ,
                                      padding         : "0.5rem"                    ,
                                      backgroundColor : "rgba(255,255,255,0.9)"    ,
                                      borderTop       : "1px solid #dee2e6"         ,
                                      backdropFilter  : "blur(4px)"                },

            ".nav-button"         : { padding         : "0.25rem 0.5rem"            ,      // Navigation buttons
                                      fontSize        : "0.75rem"                   ,
                                      color           : "#0366d6"                   ,
                                      border          : "none"                      ,
                                      backgroundColor : "transparent"               ,
                                      cursor          : "pointer"                   },

            ".nav-button:hover"   : { textDecoration  : "underline"                 },     // Button hover

            // Highlighting and focus
            ".highlight-line"     : { backgroundColor : "#fffbdd"                   },     // Highlighted line

            ".focus-section"      : { boxShadow       : "0 0 0 2px #0366d6"        }      // Focused section
        }
    }
}

WebC__Document__Diff.define()