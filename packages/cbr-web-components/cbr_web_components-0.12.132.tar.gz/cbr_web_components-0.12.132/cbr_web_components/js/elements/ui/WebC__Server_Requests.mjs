import WebC__API_To_Table from "../api/WebC__API_To_Table.mjs";

export default class WebC__Server_Requests extends WebC__API_To_Table {

    constructor() {
        super();
    }

    async invoke_api_path() {
        let response = await super.invoke_api_path()
        for (let value of response.rows) {                 // todo: find a better way to do this (since at the moment we are hardcoding in code the location and target link)
            if (response.rows.length > 3) {
                let column_id = 0
                let request_id = value[column_id]
                value[column_id] = `<a href="docs/dev/web-components/server-request?request_id=${request_id}">${request_id}</a>`
            }
        }
        return response
    }
}

WebC__Server_Requests.define()