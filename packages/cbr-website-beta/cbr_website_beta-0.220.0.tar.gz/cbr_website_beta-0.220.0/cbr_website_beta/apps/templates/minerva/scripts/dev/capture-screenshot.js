console.log('[{{version}}] Executing {{script_name}} at {{date_now}}')

function create_target_div() {

    var newTextarea = $('<textarea id="new_div"></textarea>');

    // Apply CSS styles to the new textarea
    newTextarea.css({
        'width'           : '630px',
        'height'          : '250px',
        'background-color': 'azure',
        'resize'          : 'none'  // Prevent the textarea from being resizable
    });
    newTextarea.val("Going to capture a screenshot")
    // Replace any existing content in #dev-area with the new textarea
    $('#dev-area').html(newTextarea);

}
function install_html2canvas(callback) {
    if (typeof html2canvas !== 'function') {
        $.getScript('https://html2canvas.hertzen.com/dist/html2canvas.js', function() {
            console.log('html2canvas has been loaded successfully!');
            callback()
        })
    }
    else {
        console.log('html2canvas was already loaded ');
        callback()
    }
}

function take_screenshot() {
    html2canvas(document.querySelector("body")).then(canvas => {

        // // Append the canvas to the body (optional)
        // document.body.appendChild(canvas);


        // Create an image element
        var img = new Image();
        img.src = canvas.toDataURL("image/png");

        // canvas.toBlob(blob => {
        //     console.log('screenshot created', blob)
        //     // todo: send this back to the server, or send a message saying that there is an screenshot avaialable
        // })


        // here is a nice way to debug the screenshot and create an image for the user
        var link = document.createElement('a');
        link.download = 'screenshot.png';
        link.href = img.src;
        link.click();
    });
}
create_target_div()
install_html2canvas(take_screenshot)


