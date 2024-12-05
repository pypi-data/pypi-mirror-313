HTMLElement.prototype.add_class = function(...classNames) {         // Adds class to current element
    this.classList.add(...classNames);
    return this
};

HTMLElement.prototype.disable = function() {      // Disables the element
    this.setAttribute('disabled', 'true');
    return this;
};

HTMLElement.prototype.enable = function() {       // Enables the element
    this.removeAttribute('disabled');
    return this;
};

HTMLElement.prototype.hide = function() {                           // Hides element
    this.style.display = 'none';
    return this
};

HTMLElement.prototype.is_disabled = function() {
    return !this.is_enabled();
};

HTMLElement.prototype.is_enabled = function() {
    return !this.hasAttribute('disabled');
};

HTMLElement.prototype.is_hidden = function() {
    return window.getComputedStyle(this).display === 'none';
};

HTMLElement.prototype.is_visible = function() {
    return !this.is_hidden();
};

HTMLElement.prototype.remove_class = function(...classNames) {      // Removes class from current element
    this.classList.remove(...classNames);
    return this
};

HTMLElement.prototype.show = function() {
    this.style.display = '';                                        // Resets display to default
    return this
};

