export default class CBR__Session__Event__Handler {
    constructor() {
        this.callbacks = {}
        this.setup_events()
    }

    setup_events() {
        this.events = {
            USER_SESSION_CHANGED     : 'user_session_changed'    ,              // todo: refactor all into CBR__Events class (and use new naming convention, based on cbr::{area}-{action})
            //PERSONA_SESSION_CHANGED  : 'persona_session_changed' ,
            ACTIVE_SESSION_CHANGED   : 'active_session_changed'  ,
            SESSION_ERROR            : 'session_error'           ,
            LOGIN_AS_PERSONA         : 'login_as_persona'        ,
            LOGOUT_PERSONA           : 'logout_persona'          ,
            SESSION_INITIALIZED      : 'session_initialized'     ,
            SWITCH_SESSION           : 'switch_session'          ,
            RELOAD_PAGE              : 'reload_page'
        }
    }

    dispatch(event_name, detail = {}) {
        const event = new CustomEvent(event_name, {
            bubbles   : true    ,
            composed  : true    ,
            detail    : detail
        })
        document.dispatchEvent(event)
    }

    subscribe(event_name, callback) {
        if (!this.callbacks[event_name]) {
            this.callbacks[event_name] = []
        }
        this.callbacks[event_name].push(callback)
        document.addEventListener(event_name, callback)
    }

    unsubscribe(event_name, callback) {
        if (this.callbacks[event_name]) {
            this.callbacks[event_name] = this.callbacks[event_name].filter(cb => cb !== callback)
            document.removeEventListener(event_name, callback)
        }
    }

    unsubscribe_all() {
        Object.keys(this.callbacks).forEach(event_name => {
            this.callbacks[event_name].forEach(callback => {
                document.removeEventListener(event_name, callback)
            })
        })
        this.callbacks = {}
    }
}