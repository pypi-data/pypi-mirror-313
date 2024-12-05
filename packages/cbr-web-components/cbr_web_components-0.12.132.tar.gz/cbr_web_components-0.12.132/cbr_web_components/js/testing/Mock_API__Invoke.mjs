import API__Invoke from '../data/API__Invoke.mjs'

let originalInvokeApi = null                                       // Store the original method

export class Mock_API__Invoke {
    constructor() {
        this.responses = new Map()
    }

    static apply_mock() {                                         // New static method to apply mock
        if (!originalInvokeApi) {
            originalInvokeApi = API__Invoke.prototype.invoke_api   // Store original only once
            API__Invoke.prototype.invoke_api = function(...args) {
                return mock.invoke_api.apply(mock, args)
            }
        }
    }

    static restore_original() {                                   // New method to restore original
        if (originalInvokeApi) {
            API__Invoke.prototype.invoke_api = originalInvokeApi
            originalInvokeApi = null
        }
    }

    async invoke_api(url, method='GET', data=null) {
        const key = `${method}:${url}`
        if (this.responses.has(key)) {
            const response = this.responses.get(key)
            if (response === null) {
                throw new Error(`Mock response is null for ${key}`)
            }
            if (typeof response === 'function') {
                return response({ url, method, data });
            }
            return response
        }
        throw new Error(`No mock response set for ${key}`)
    }

    setResponse(url, method, response) {
        const key = `${method}:${url}`
        this.responses.set(key, response)
    }
}

export const mock = new Mock_API__Invoke()

export function set_mock_response(url, method, response) {
    mock.setResponse(url, method, response)
}