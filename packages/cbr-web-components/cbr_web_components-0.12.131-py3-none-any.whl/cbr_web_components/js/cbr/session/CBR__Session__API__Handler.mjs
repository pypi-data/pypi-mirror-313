import API__Invoke from "../../data/API__Invoke.mjs"

export default class CBR__Session__API__Handler {
    constructor() {
        this.api_invoke = new API__Invoke()
        this.base_path = '/api/user-session'
    }

    async get_current_session() {
        try {
            return await this.api_invoke.invoke_api(
                `${this.base_path}/session/current-session`,
                'GET'
            )
        } catch (error) {
            //console.error('Error fetching current session:', error)
            throw error
        }
    }

    async get_session_details(session_id) {
        try {
            return await this.api_invoke.invoke_api(
                `${this.base_path}/session/session-details?session_id=${session_id}`,
                'GET'
            )
        } catch (error) {
            //console.error('Error fetching session details:', error)
            throw error
        }
    }

    async login_as_persona(persona_id) {
        try {
            return await this.api_invoke.invoke_api(
                `${this.base_path}/guest/login-as-persona?persona_id=${persona_id}`,
                'POST'
            )
        } catch (error) {
            //console.error('Error logging in as persona:', error)
            throw error
        }
    }

    async logout_persona() {
        try {
            return await this.api_invoke.invoke_api(
                `${this.base_path}/guest/logout-persona`,
                'POST'
            )
        } catch (error) {
            //console.error('Error logging out persona:', error)
            throw error
        }
    }

    async logout_all() {
        try {
            return await this.api_invoke.invoke_api(
                `${this.base_path}/guest/logout-all`,
                'POST'
            )
        } catch (error) {
            //console.error('Error logging out all sessions:', error)
            throw error
        }
    }

    async set_active_session(session_id) {
        document.cookie = `CBR__SESSION_ID__ACTIVE=${session_id};path=/`
    }

    async set_active_persona(session_id) {
        document.cookie = `CBR__SESSION_ID__PERSONA=${session_id};path=/`
    }

    delete_cookie(name) {
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
    }

    get_cookie(name) {
        const value = `; ${document.cookie}`
        const parts = value.split(`; ${name}=`)
        if (parts.length === 2) {
            return parts.pop().split(';').shift()
        }
        return null
    }
    set_cookie(name, value) {
        document.cookie = `${name}=${value};path=/`
    }

    get_user_session_id() {
        return this.get_cookie('CBR__SESSION_ID__USER')
    }

    get_persona_session_id() {
        return this.get_cookie('CBR__SESSION_ID__PERSONA')
    }

    get_active_session_id() {
        return this.get_cookie('CBR__SESSION_ID__ACTIVE')
    }

    async switch_to_session(session_id) {
        await this.set_active_session(session_id)
        return await this.get_session_details(session_id)
    }
}