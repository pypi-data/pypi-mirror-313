export default class LLM__Response__Handler {
    constructor(config = {}) {
        this.markdown_enabled = config.markdown_enabled ?? true
    }

    format_response(response) {
        if (this.markdown_enabled && window.marked) {
            return marked.marked(response)
        }
        return response || ''
    }

    create_response_element(response, className = '') {
        const formatted = this.format_response(response)
        return `<div class="llm-response ${className}">${formatted}</div>`
    }
}