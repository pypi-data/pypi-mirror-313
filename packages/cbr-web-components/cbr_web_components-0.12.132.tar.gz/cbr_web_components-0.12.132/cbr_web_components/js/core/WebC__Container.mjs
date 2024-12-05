import Web_Component from "./Web_Component.mjs";

export default class WebC__Container extends Web_Component {

  async connectedCallback() {
    await super.connectedCallback();

    const template = document.createElement('template');
    template.innerHTML = `
      <style>
        :host {
          display: flex;
        }
        ::slotted(*) {
          flex: auto;
          padding: 0px;
          margin: 10px;
        }
      </style>
      <slot></slot>
    `;
    this.shadowRoot.appendChild(template.content.cloneNode(true));
  }
}

WebC__Container.define();
