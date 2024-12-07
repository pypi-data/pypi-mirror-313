
var table;

function set_method_kwargs(method_kwargs) {

    // Clear any existing data
    table.clear();

    // Add new data from `method_kwargs`
    for (var key in method_kwargs) {
        if (method_kwargs.hasOwnProperty(key)) {
            table.row.add([
                '<input type="text" class="form-control" name="key[]" value="' + key + '">',
                '<input type="text" class="form-control" name="value[]" value="' + method_kwargs[key] + '">',
                '<button type="button" class="form-control btn btn-outline-secondary remove-row">Remove</button>'
            ]).draw(false);
        }
    }

    // Reattach the event handler for the remove button in the new rows
    $('.remove-row').on('click', function() {
        table.row($(this).parents('tr')).remove().draw();
    });
}


$(document).ready(function() {
    // Initialize the DataTable with empty array
    var table_config = { "dom": 'rt'}
    table = $('#kwargsTable').DataTable(table_config);

    set_method_kwargs(method_kwargs);

    // Handle the addition of new rows
    $('#addRow').click(function() {
        table.row.add([
            '<input type="text"    class="form-control" name="key[]">',
            '<input type="text"    class="form-control" name="value[]">',
            '<button type="button" class="form-control btn btn-outline-secondary remove-row">Remove</button>'
        ]).draw(false);
    });

    // Handle the removal of rows
    $('#kwargsTable tbody').on('click', 'button.remove-row', function() {
        table.row($(this).parents('tr')).remove().draw();
    });
});

function toInteger(str) {
    var num = Number(str); // Convert the string to a number
    if (Number.isInteger(num)) {
        return num;
    } else {
        return str; // Return the original string if it's not an integer
    }
}


function submit_debug_view_form(event) {
    // Prevent the default form submission
    if (event) event.preventDefault();


    // Capture the input values
    var class_name   = document.getElementById('class_name').value;
    var method_name   = document.getElementById('method_name').value;

    let method_kwargs = {};
    // Iterate over each row and build the dictionary from inputs
    $('#kwargsTable tbody tr').each(function() {
        var key = $(this).find('input[name="key[]"]').val();
        var value = $(this).find('input[name="value[]"]').val();
        if(key && value) { // Make sure the key and value are not empty
            method_kwargs[key] = toInteger(value);
        }
    });
    // Create a JSON object
    var data = {
        class_name    : class_name,
        method_name   : method_name,
        method_kwargs : method_kwargs
    };
    submit_data(data);

}
function submit_data(data) {
    showSpinner(true)
    let post_data = JSON.stringify(data)

    $.ajax({
                url: '/dev/dev-panel',
                type: 'POST',
                contentType: 'application/json',
                data: post_data,
                success: handleSuccess,
                error: handleError
            });
    }

 // Function to update form fields based on the selected method
function updateFormFields() {
    // Get the selected value from the listbox
    var selectedMethod = document.getElementById('method_selector').value;
    var methodParts = selectedMethod.split('.');

    // Assuming class_name is the first part and method_name is the second
    var class_name = methodParts[0];
    var method_name = methodParts[1];

    // Update the input fields
    document.getElementById('class_name').value = class_name;
    document.getElementById('method_name').value = method_name;

    // Clear the current kwargs table
    var tableBody = document.getElementById('kwargsTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';

    // Assuming you have a JSON object that contains the method kwargs information
    var method_kwargs = views_mappings[class_name][method_name];
    set_method_kwargs(method_kwargs)
}

   var autoReloadTimer = null;

    // The `reload_data` function that needs to be called on an interval
    function reload_data() {
        var interval = document.getElementById('autoReloadInterval').value;
        console.log(`reloading data after ${interval} seconds `);
        submit_debug_view_form()
        // Your data reloading code goes here
    }

    // Listen for changes on the toggle switch
    document.getElementById('autoReloadToggle').addEventListener('change', function() {
        if (this.checked) {
            // Get the selected interval in seconds
            var interval = document.getElementById('autoReloadInterval').value * 1000;
            // Set the timer to call `reload_data` at the selected interval
            autoReloadTimer = setInterval(reload_data, interval);
            console.log('Auto reload started with an interval of ' + interval/1000 + ' seconds.');
        } else {
            // If the toggle is switched off, clear the timer
            clearInterval(autoReloadTimer);
            console.log('Auto reload stopped.');
        }
    });

    // Listen for changes on the interval dropdown to update the interval
    document.getElementById('autoReloadInterval').addEventListener('change', function() {
        // If the auto-reload is enabled, reset the timer with the new interval
        if (document.getElementById('autoReloadToggle').checked) {
            clearInterval(autoReloadTimer);
            var interval = this.value * 1000;
            autoReloadTimer = setInterval(reload_data, interval);
            console.log('Auto reload interval changed to ' + interval/1000 + ' seconds.');
        }
    });