function submit_ws_message(event) {
    // Prevent the default form submission
    if (event) event.preventDefault();
    let message = $('#message_to_send').val().trim();
    let command = $('#command_select').val().trim();

    let message_to_send = JSON.stringify({'command': command, 'message': message})
    //console.log(message_to_send)
    ws.send(message_to_send)
}