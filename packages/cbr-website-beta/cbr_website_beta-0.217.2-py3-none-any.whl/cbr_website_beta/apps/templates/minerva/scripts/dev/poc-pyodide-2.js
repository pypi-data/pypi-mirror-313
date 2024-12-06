console.log('[{{version}}] Executing {{script_name}} at {{date_now}}')

let initial_script = `print("Hello World from Pyodide via Web Socket!")
import micropip
await micropip.install('requests')
import requests

target_url = "https://athena.thecyberboardroom.com/config/version"
response = requests.get(target_url)
print(response.text)

await micropip.install('pillow')

import io
from js import document
from pyodide.http import open_url, pyfetch
from PIL import Image
import base64


async def fetch_and_display_image():
    url = "https://static.thecyberboardroom.com/assets/cbr/minerva-icon.png"
    response = await pyfetch(url)
    image_bytes = await response.bytes()
    img = Image.open(io.BytesIO(image_bytes))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_data_url = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

    # Create and inject an img element into the DOM
    image_element = document.createElement("img")
    image_element.src = img_data_url
    image_element.style.width="500px"
    document.body.appendChild(image_element)

# Call the function to execute the process
await fetch_and_display_image()


`
function create_target_div() {

    var newTextarea = $('<textarea id="new_div"></textarea>');

    newTextarea.css({
        'width'           : '630px',
        'height'          : '250px',
        'background-color': 'azure',
        'resize'          : 'none'  // Prevent the textarea from being resizable
    });
    newTextarea.val(initial_script)
    // Replace any existing content in #dev-area with the new textarea
    $('#dev-area').html(newTextarea);

}


function add_button__exec_python() {
     // Create a Bootstrap 5 button dynamically
    var button = document.createElement('button');
    button.className     = 'btn btn-primary'; // Bootstrap 5 button class
    button.textContent   = 'Execute python';
    button.style.margin  = '10px'
    button.onclick       = exec_python

    document.getElementById('dev-area').appendChild(button)
}


function install_pyodide(callback) {
    if (typeof loadPyodide !== 'function') {
        // Load the Pyodide script if it's not already loaded
        $.getScript('https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js')
            .done(function() {
                console.log('Pyodide has been loaded successfully!');
                // Initialize Pyodide after loading
                loadPyodide().then(() => {
                    console.log('Pyodide is ready.');
                    callback(); // Execute the callback after Pyodide is ready
                });
            })
            .fail(function() {
                console.log('Failed to load Pyodide.');
            });
    } else {
        console.log('Pyodide is already loaded.');
        callback(); // Execute the callback directly if Pyodide is already initialized
    }
}

async function on_pyodite_install() {
    console.log('executing python  ode')
    const pyodide = await loadPyodide();
    window.pyodide = pyodide

    await pyodide.loadPackage("micropip");
    await pyodide.runPythonAsync(`
        import sys
        sys.version
    `);

    //let python_code = `print("Hello World from Pyodide!")`
    // let python_code = $('#new_div').val()
    // pyodide.runPython(python_code);
    await exec_python()

}

async function exec_python(){
    let python_code = $('#new_div').val()
    await pyodide.runPythonAsync(python_code)
}

create_target_div()
add_button__exec_python()
install_pyodide(on_pyodite_install)