function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function send_prompt_to_api() {
    $('#prompt-text').css({'background-color':'#85AE82FF'})
    $('#output-area').css({'background-color':'#000000'})
    $('#output-area').text('...sending message to odin ....')
    $('#ask-button' ).html(`<span class="spinner-border spinner-border" role="status" aria-hidden="true"></span>`)

    var userData = $('#prompt-text').val();                  // Capturing the user's input from textarea
    var apiKey = getCookie('api_key');  // Get the API key from the cookie

    $.ajax({
        //url: 'http://localhost:5111/odin/chat/llms/prompt-to-answer',
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
            if (window.marked === undefined) {
                odin_message =  response.replace(/\n/g, '<br>');
                }
                else {
                    odin_message =  marked.marked(response)
                }

            $('#output-area').html(odin_message);
                $('#output-area'   ).css({'background-color':'#001f3f'})
                $('#output-area table'   ).css({border:'2px solid', 'padding': '5px'})
                $('#output-area table td').css({border:'2px solid', 'padding': '5px'})
                $('#output-area table th').css({border:'2px solid', 'padding': '5px'})
                $('#output-area h3').css({'padding': '10px'})
                $('#output-area p'   ).css({'padding-top':'10px'})
            $('#prompt-text').css({'background-color':'azure'})
            $('#ask-button' ).text('Ask Odin')
        },
        error: function(xhr, status, error) {
            $('#output-area').html("Error: " + xhr.responseText);
        }
    });
}