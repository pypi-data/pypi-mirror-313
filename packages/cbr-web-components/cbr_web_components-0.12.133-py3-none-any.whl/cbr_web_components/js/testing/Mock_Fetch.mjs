export class Mock_Fetch {
    constructor() {
        this.responses = new Map()
    }

    static apply_mock(target_class) {                                    // Much simpler now - just patch and go
        target_class.prototype.fetch_url = function(...args) {
            return mock.fetch_url.apply(mock, args)
        }
        return mock
    }

    static restore_original(target_class, original) {                    // Optional restore if needed
        if (original) {
            target_class.prototype.fetch_url = original
        }
    }

    async fetch_url(url) {
        if (!this.responses.has(url)) {
            throw new Error(`No mock response set for URL: ${url}`)
        }

        const response = this.responses.get(url)
        if (typeof response === 'function') {
            return response({ url, response });
        }
        return {
            ok     : response.status === 200   ,
            status : response.status || 200    ,
            json   : async () => response.data ,
            body   : response.body             ,
            headers: response.headers || {}
        }
    }

    set_response(url, data, status = 200) {
        this.responses.set(url, { data, status })
    }

    set_stream_response(url, chunks, status = 200, stream=true) {
        this.responses.set(url, { ok: status === 200              ,
                                  status                          ,
                                  body: new StreamResponse({chunks, stream})});
    }
}

export const mock = new Mock_Fetch()                                    // Single instance for convenience

export function set_mock_response(url, data, status = 200) {           // Helper function
    mock.set_response(url, data, status)
}

class StreamResponse {
    constructor({chunks, stream=true}) {
        if (typeof chunks === 'function') {
            this.callback = chunks
            this.chunks   = []
        }
        else {
            this.callback = null
            if (Array.isArray(chunks)) {
                this.chunks = chunks
            } else {
                chunks = [chunks]
            }
        }
        this.encoder = new TextEncoder();
        this.stream = stream
    }

    getReader() {
        let index = 0;
        if (this.callback) {
            this.callback();
        }
        return {
            read: async () => {
                if (this.stream === false) {
                    return {done: true, value: this.encoder.encode(this.chunks)}
                }
                if (index >= this.chunks.length) {
                    return { done: true };
                }
                return {
                    value: this.encoder.encode(this.chunks[index++]),
                    done: false
                };
            }
        };
    }
}