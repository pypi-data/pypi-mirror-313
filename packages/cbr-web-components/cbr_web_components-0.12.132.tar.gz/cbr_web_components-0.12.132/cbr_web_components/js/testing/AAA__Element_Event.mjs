export default class AAA__Element_Event {
    constructor({ element, event_name , raise_after_act }) {
        this.element         = element    || document.createElement('div')
        this.event_name      = event_name || 'test_event'
        this.raise_after_act = raise_after_act ?? true
    }

    // methods to override
    async arrange() {
        // Default implementation
    }

    async act() {
        // Default implementation
    }

    assert(event) {
        // Default implementation
    }

    add_event_listener() {
        this.element.addEventListener(this.event_name, this.assert);
    }

    raise_event(detail = {}) {
        this.element.dispatchEvent(new CustomEvent(this.event_name, { detail }));
    }

    remove_event_listener() {
        this.element.removeEventListener(this.event_name, this.assert);
    }

    async aaa() {
        this.add_event_listener();
        await this.arrange();
        try {
            await this.act();
            if (this.raise_after_act) {
                this.raise_event()}
        } finally {
            this.remove_event_listener();
        }
        return this
    }

    static async test({ element, event_name, raise_after_act, arrange, act, assert }) {
        const instance = new AAA__Element_Event({ element, event_name , raise_after_act});       // Create an instance of the class

        if (arrange) instance.arrange = arrange.bind(instance);                 // Dynamically override methods if provided
        if (act    ) instance.act     = act    .bind(instance);
        if (assert) instance.assert   = assert .bind(instance);

        return instance.aaa();                                                  // Run the sequence
    }
}