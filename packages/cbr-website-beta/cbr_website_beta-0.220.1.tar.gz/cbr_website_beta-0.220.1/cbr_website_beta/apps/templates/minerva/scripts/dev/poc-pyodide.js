console.log('[{{version}}] Executing {{script_name}} at {{date_now}} | ')

let initial_script = `
import datetime
import js
print("Hello World from Pyodide via Web Socket!")
js.jQuery("h1").html('Executed Python Code at ' + datetime.datetime.now().strftime("%H:%M:%S"))
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
                callback()
            })
            .fail(function() {
                console.log('Failed to loaded Pyodide.');
            });
    } else {
        console.log('Pyodide is already loaded.');
        callback(); // Execute the callback directly if Pyodide is already initialized
    }
}

async function on_pyodite_install() {
    let startTime = new Date(); // Capture start time for loading Pyodide
    console.log('loadPyodide start')
    const pyodide = await loadPyodide();
    let endTime_1 = new Date();
    console.log('loadPyodide end')
    console.log(`Loading Pyodide took ${(endTime_1 - startTime)} ms`); // Calculate and log the duration

    window.pyodide = pyodide

    await exec_python()
    let endTime_2 = new Date();
    console.log(`Executing Python code took ${(endTime_2 - startTime)} ms`); // Calculate and log the duration

}

async function exec_python(){
    let python_code = $('#new_div').val()
    await pyodide.runPythonAsync(python_code)
}

create_target_div()
add_button__exec_python()
install_pyodide(on_pyodite_install)