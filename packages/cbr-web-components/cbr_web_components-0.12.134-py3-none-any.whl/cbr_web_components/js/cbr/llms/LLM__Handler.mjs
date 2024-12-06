// LLM__Handler.mjs
import CBR_Events from "../CBR_Events.mjs";

export default class LLM__Handler {
    constructor(config = {}) {
        this.default_platform = config.platform || 'Groq (Free)'
        this.default_provider = config.provider || '1. Meta'
        this.default_model    = config.model    || 'llama-3.1-70b-versatile'
        this.api_path         = config.api_path || '/api/llms/chat/completion'
    }

    create_payload(user_prompt, system_prompts = [], config = {}) {
        return {
            chat_thread_id   : this.random_uuid()                ,
            temperature      : config.temperature || 0           ,
            user_prompt      : user_prompt                      ,
            images          : []                                ,
            system_prompts  : system_prompts                    ,
            histories       : []                                ,
            user_data       : {
                session_id        : this.random_uuid()          ,
                selected_platform : this.default_platform       ,
                selected_provider : this.default_provider       ,
                selected_model    : this.default_model
            },
            stream: true
        }
    }
    /* istanbul ignore next */
    async fetch_url(path, payload) {
        return await fetch(path, {
            method  : 'POST',
            headers : { 'Accept': 'application/json', 'Content-Type': 'application/json' },
            body    : JSON.stringify(payload)
        })
    }
    async stream_response(user_prompt, system_prompts = [], callbacks = {}, config = {}) {
        const payload = this.create_payload(user_prompt, system_prompts, config)

        try {
            this.raise_event__llm_request_started()
            const response = await this.fetch_url(this.api_path, payload)

            const reader  = response.body.getReader()
            const decoder = new TextDecoder('utf-8')
            let message  = ''

            while (true) {
                const { value, done } = await reader.read()
                if (done) break

                const decoded_value = decoder.decode(value, { stream: true })
                const fixed_value  = decoded_value.replace(/[\r\n]+/g, '')
                message += fixed_value

                if (callbacks.onChunk) {
                    callbacks.onChunk(message)
                }
            }

            if (callbacks.onComplete) {
                callbacks.onComplete(message)
            }
            this.raise_event__llm_request_finished()
            return message
        } catch (error) {
            if (callbacks.onError) {
                callbacks.onError(error)
            }
            this.raise_event__llm_request_error({error})
            throw error
        }
    }

    random_uuid() {
        return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
            (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
        )
    }

    raise_event__on_window(event_name, event_detail={}) {
        const options      =  { bubbles: true, composed: true, detail: event_detail}
        const custom_event = new CustomEvent(event_name, options)
        window.dispatchEvent(custom_event);
        return custom_event
    }

    raise_event__llm_request_error({error}) {
        this.raise_event__on_window(CBR_Events.CBR__LLM__REQUEST__ERROR, {error})
    }

    raise_event__llm_request_finished() {
        this.raise_event__on_window(CBR_Events.CBR__LLM__REQUEST__FINISHED)
    }

    raise_event__llm_request_started() {
        this.raise_event__on_window(CBR_Events.CBR__LLM__REQUEST__STARTED)
    }
}
