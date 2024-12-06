class MyComponent extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: 'open'});
        this.date_obj = new Date();
        this.date_now = this.date_obj.getHours() + ":" + this.date_obj.getMinutes() + ":" + this.date_obj.getSeconds();
    }

    connectedCallback() {

        const message  = this.getAttribute('message') || "Hello from HTMLElement!"
        this.shadowRoot.innerHTML = `
<br>
<hr/>
inside shadow 
<h2 id="output">${message}</h2>
${this.date_now}
<hr/>`;
    }
}

function generateRandomName() {
    const prefix = 'my-component';
    return `${prefix}-${Math.random().toString(36).substr(2, 9)}`;
}

function clear_target() {
    $('#dev-area').html('');
}

function add_element(element_name, message) {
    const new_element = document.createElement(element_name);

    // Set the 'message' attribute if provided
    if (message) {
        new_element.setAttribute('message', message);
    }
    $('#dev-area').append(new_element);
}

console.log('[{{version}}] Executing {{script_name}} at {{date_now}}')

let element_name = generateRandomName()
console.log(`new element will have the name of ${element_name}`)
customElements.define(element_name, MyComponent);

clear_target()
add_element(element_name)
add_element(element_name, "message 1")
add_element(element_name, "message 2")
