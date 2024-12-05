export default class API__Web__Forms {

    /* istanbul ignore next */
    async fetch_url(url, options) {
        const response = await fetch(url, options)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`)
        }
        return response
    }

    async submit_form(form_data, endpoint) {
        const urlEncodedData = new URLSearchParams(form_data).toString()
        const options = { method : 'POST'                                                ,
                          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                          body   : urlEncodedData                                        }

        return await this.fetch_url(endpoint, options)
    }
}