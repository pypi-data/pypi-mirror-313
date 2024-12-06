console.log('[{{version}}] Executing {{script_name}} at {{date_now}}')

let initial_script = `
import js
import datetime
message = "Pyodide with Pandas and Matplotlib"
js.jQuery("h1").html(f'{message} | ' + datetime.datetime.now().strftime("%H:%M:%S"))

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create some data
df = pd.DataFrame({
    "x": range(10),
    "y": np.random.rand(10)
})

# Plot the data
plt.figure(figsize=(4 , 2))
plt.plot(df.x, df.y, marker='o')
plt.title("Random Scatter Plot")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
js.jQuery('#target').html('')   # clear the div
plt.show()
message = "Pyodide with Pandas and Matplotlib"
js.jQuery("h1").html(f'{message} | ' + datetime.datetime.now().strftime("%H:%M:%S"))


`
function create_target_div() {


    // Clear the #dev-area and set it up for flexbox
    $('#dev-area').empty().css({
        'display': 'flex',
        'justify-content': 'space-between', // This spreads out the child elements
        'align-items': 'flex-start' // Aligns items at the start of the flex container
    });

    // Create and style the textarea
    var newTextarea = $('<textarea id="new_div"></textarea>').css({
        'width': '50%',
        'height': '250px',
        'background-color': 'azure',
        'resize': 'none',
        'margin-right': '20px' // Adds space between the textarea and the target div
    }).val(initial_script);

    // Create the target div
    var target_div = $('<div id="target" style="width: 630px; height: 250px; background-color: lightgrey;"></div>');

    // Append both elements to #dev-area
    $('#dev-area').append(newTextarea).append(target_div);
    document.pyodideMplTarget = document.getElementById('target')
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
                callback();
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

    //await pyodide.loadPackage("micropip");
    await pyodide.loadPackage(["pandas", "matplotlib"]);
    await exec_python()

}

async function exec_python(){
    let python_code = $('#new_div').val()
    await pyodide.runPythonAsync(python_code)
}

create_target_div()
add_button__exec_python()
install_pyodide(on_pyodite_install)