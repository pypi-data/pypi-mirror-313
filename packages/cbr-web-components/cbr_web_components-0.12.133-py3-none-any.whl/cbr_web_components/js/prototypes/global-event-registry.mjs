// Global registry for all captured events
window._globalEventRegistry = new Map();

// Extend EventTarget.prototype to capture events
EventTarget.prototype.addEventListener = (function (originalAddEventListener) {
    return function (type, listener, options) {
        // Initialize registry for this target
        if (!window._globalEventRegistry.has(this)) {
            window._globalEventRegistry.set(this, {});
        }
        const events = window._globalEventRegistry.get(this);

        // Track the listener
        if (!events[type]) {
            events[type] = [];
        }
        events[type].push({ listener, options });
        // Call the original addEventListener
        return originalAddEventListener.call(this, type, listener, options);
    };
})(EventTarget.prototype.addEventListener);

// Extend removeEventListener to update the registry
EventTarget.prototype.removeEventListener = (function (originalRemoveEventListener) {
    return function (type, listener, options) {
        if (window._globalEventRegistry.has(this)) {
            const events = window._globalEventRegistry.get(this);
            if (events[type]) {

                events[type] = events[type].filter(
                    (entry) => entry.listener !== listener || entry.options !== options
                );

                // Remove the event type if no listeners remain
                if (events[type].length === 0) {
                    delete events[type];
                }

                // Remove the target if no event types remain
                if (Object.keys(events).length === 0) {
                    window._globalEventRegistry.delete(this);
                }
            }
        }

        // Call the original removeEventListener
        return originalRemoveEventListener.call(this, type, listener, options);
    };
})(EventTarget.prototype.removeEventListener);

// Function to get all globally captured events
// function getAllCapturedEvents() {
//     const capturedEvents = [];
//     for (const [target, events] of window._globalEventRegistry.entries()) {
//         capturedEvents.push({ target, events });
//     }
//     return capturedEvents;
// }
