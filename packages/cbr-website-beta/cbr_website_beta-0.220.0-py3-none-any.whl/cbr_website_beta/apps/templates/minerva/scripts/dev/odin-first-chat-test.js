console.log('[{{version}}] Executing {{script_name}} at {{date_now}}');

var initial_message = 'what instances are running';

function create_target_div() {
    var newTextarea = $('<textarea id="new_div"></textarea>');
    var sendButton = $('<button id="sendRequest">Send Request</button>');
    var responseArea = $('<textarea id="responseArea"></textarea>');

    newTextarea.css({
        'width': '430px',
        'height': '250px',
        'background-color': 'azure',
        'resize': 'none'
    });
    newTextarea.val(initial_message);

    newTextarea.on('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {  // Check if the Enter key is pressed without the Shift key
            e.preventDefault();  // Prevent the default action to avoid newline in textarea
            sendRequest();
            $('#new_div').css({'background-color':'lightblue'})
        }
    });
    sendButton.css({
        'margin-top': '10px'
    });

    $('#dev-area').empty();  // Clear previous contents if any
    $('#dev-area').append(newTextarea, sendButton, responseArea);

    sendButton.on('click', function() {
        sendRequest();
    });
}
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function sendRequest() {
    var userData = $('#new_div').val();  // Capturing the user's input from textarea
    var apiKey = getCookie('api_key');  // Get the API key from the cookie

    $.ajax({
        url: 'https://athena-dev.cyber-boardroom.com/odin/chat/llms/prompt-to-answer',
        type: 'POST',
        contentType: 'application/json',
        headers: {
            'accept': 'application/json',
            'Authorization': apiKey  // Include the API key in the request headers
        },
        data: JSON.stringify({
            chat_thread_id: "039eee52-d3a2-41ee-8cf3-9cdac88cc92f",
            histories: [],
            images: [],
            max_tokens: 4092,
            model: "gpt-3.5-turbo",
            model_provider: "OpenAI",
            seed: 42,
            system_prompts: [],
            temperature: 0,
            user_data: {},
            user_prompt: userData
        }),
        success: function(response) {
            $('#responseArea').val(response);
            $('#new_div').css({'background-color':'azure'})
        },
        error: function(xhr, status, error) {
            $('#responseArea').html("Error: " + xhr.responseText);
        }
    });
}

create_target_div();  // Initialize the UI components
