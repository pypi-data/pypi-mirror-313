export default class API__Invoke {
    constructor(channel) {
        this.channel               = channel || this.random_id('api_invoke_')
        this.on_error_return_value = null
    }

    // Method to invoke the API asynchronously using fetch
    async invoke_api(api_path, method = 'GET', data = null, auth_header = null) {
        const url     = `${api_path}`;
        const options = { method,  headers: { 'Content-Type': 'application/json' }};

        if (auth_header)                                     { options.headers['Authorization'] = auth_header; }
        if (data && (method === 'POST' || method === 'PUT')) { options.body = JSON.stringify(data);            }

        try {

            const response = await fetch(url, options);

            if (!response.ok) {
                if (this.on_error_return_value) { return this.on_error_return_value }
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error invoking API:', error, api_path);
            throw error;
        }
    }

    // utils methods
    random_id(prefix='random') {
        const random_part = Math.random().toString(36).substring(2, 7); // Generate a random string.
        return `${prefix}_${random_part}`;
    }
}