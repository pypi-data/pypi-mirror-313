console.log('[{{version}}] Executing {{script_name}} at {{date_now}}')

let athena_server = 'https://athena-dev.cyber-boardroom.com'

function audio_to_text(audio_base_64) {
     var dataToSend = { "audio_base_64": audio_base_64 };

        $.ajax({
            url: `${athena_server}/open_ai/audio_to_text`, // Adjust the URL if necessary
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(dataToSend),
            success: function(response) {
                console.log('Success:', response);
                // Handle your success case here
            },
            error: function(xhr, status, error) {
                console.error('Error:', status, error);
                // Handle your error case here
            }
        });
}

function text_to_audio(audio_text) {
     var dataToSend = { "audio_text": audio_text };

        $.ajax({
            url: `${athena_server}/open_ai/text_to_audio`, // Adjust the URL if necessary
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(dataToSend),
            success: function(response) {
                let audio_base_64 = response

                console.log('Got text_to_audio:', response.length);
                audio_to_text(audio_base_64)
                window.audio_base_64 = audio_base_64
                // Handle your success case here
            },
            error: function(xhr, status, error) {
                console.error('Error:', status, error);
                // Handle your error case here
            }
        });
}

text_to_audio("Hi , how are you today, how can I help with your cyber security questions?")