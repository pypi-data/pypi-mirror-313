export default class CBR__Session__State__Manager {
    constructor() {
        this.reset_state()
    }

    reset_state() {
        this.state = {
            user_session    : null ,
            persona_session : null ,
            active_session  : null ,
            is_initialized  : false,
            error          : null
        }
    }
    update_state(new_state) {
        this.state = { ...this.state, ...new_state }
        return this.state
    }

    set_user_session(session) {
        return this.update_state({ user_session: session })
    }

    set_persona_session(session) {
        return this.update_state({ persona_session: session })
    }

    set_active_session(session) {
        return this.update_state({ active_session: session })
    }

    clear_persona_session() {
        return this.update_state({ persona_session: null })
    }

    set_error(error) {
        return this.update_state({ error })
    }

    set_initialized(is_initialized = true) {
        return this.update_state({ is_initialized })
    }

    get_state() {
        return { ...this.state }
    }

    has_active_persona() {
        return !!this.state.persona_session
    }

    is_initialized() {
        return this.state.is_initialized
    }

    is_active_session(session) {
        return this.state.active_session?.user_name === session?.user_name
    }

    get_active_session() {
        return this.state.active_session
    }
}