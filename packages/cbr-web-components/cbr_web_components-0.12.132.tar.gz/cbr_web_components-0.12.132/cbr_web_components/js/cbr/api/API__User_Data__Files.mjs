// API__User_Data__Files.mjs

import API__Invoke from '../../data/API__Invoke.mjs'

export default class API__User_Data__Files {

    constructor() {
        this.api_invoke = new API__Invoke()
    }

    // File content operations
    async get_file_contents(file_id) {
        const response = await this.api_invoke.invoke_api(
            `/api/user-data/files/file-contents?file_id=${file_id}`, 'GET'
        )
        if (!response.data?.file_bytes__base64) {
            throw new Error('Invalid file content response')
        }
        return {
            content     : this.decode_base64_content(response.data.file_bytes__base64),
            file_data   : response.data.file_data
        }
    }

    async update_file(file_id, content) {
        const base64_content = this.encode_content_to_base64(content)
        return await this.api_invoke.invoke_api(
            '/api/user-data/files/update-file',
            'PUT',
            {
                file_id            : file_id,
                file_bytes__base64 : base64_content
            }
        )
    }

    // Version management
    async get_file_versions(file_id) {
        const response = await this.api_invoke.invoke_api(
            `/api/user-data/files/file-versions?file_id=${file_id}`, 'GET'
        )
        return response.data || []
    }

    async get_version_content(file_id, version_id) {
        const response = await this.api_invoke.invoke_api(
            `/api/user-data/files/file-bytes?file_id=${file_id}&version_id=${version_id}`, 'GET'
        )
        if (!response.data?.file_bytes__base64) {
            throw new Error('Invalid version content response')
        }
        return this.decode_base64_content(response.data.file_bytes__base64)
    }

    // Helper methods
    decode_base64_content(base64_content) {
        const binary_content = atob(base64_content)
        const bytes = Uint8Array.from(binary_content, char => char.charCodeAt(0))
        return new TextDecoder('utf-8').decode(bytes)
    }

    encode_content_to_base64(content) {
        const encoder = new TextEncoder()
        const utf8_bytes = encoder.encode(content)
        return btoa(Array.from(utf8_bytes)
            .map(byte => String.fromCharCode(byte))
            .join(''))
    }
}