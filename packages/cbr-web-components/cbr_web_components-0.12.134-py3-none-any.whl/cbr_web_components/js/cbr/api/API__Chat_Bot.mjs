import API__Invoke from '../../data/API__Invoke.mjs'

export default class API__Chat_Bot {
    constructor() {
        this.api_invoke = new API__Invoke()
    }

    url_current_user_add_chat_id = '/api/user-data/chats/chat-add?chat_path='

    async add_chat_id(cbr_chat_id) {
        try {
            return await this.api_invoke.invoke_api(`${this.url_current_user_add_chat_id}/${cbr_chat_id}`, 'POST')
        } catch (error) {
            //console.error('Error saving chat:', error)
            return { chat_path: null }                          // Return object with null path to trigger error state
        }
    }
}