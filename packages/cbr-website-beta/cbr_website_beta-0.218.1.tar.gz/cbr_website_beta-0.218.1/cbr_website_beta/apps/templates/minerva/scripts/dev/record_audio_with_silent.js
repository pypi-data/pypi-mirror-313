// needs a bit more improvements, but this is a first good mvp of stopping the recording when there is nobody speaking
//       will be interesting to see if we can do something about background noise
//       still quite trigger-happy to stop but it's works better with the 1x second pause in recordingStartTime
// experiment with a visual clue to the user when it is recording

let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let recordingStartTime = null;

// Function to create and append buttons
function createButton(id, text) {
    const button = document.createElement('button');
    button.id = id;
    button.textContent = text;
    document.body.appendChild(button);
    return button;
}

function createRecordingIndicator() {
    // Use jQuery to create the recording indicator element
    const indicatorHtml = $('<div id="recordingIndicator" style="display: none;">' +
                                '<i class="fas fa-circle text-danger"></i> Recording...' +
                            '</div>');

    // Append the indicator to the body or a specific container
    $('body').append(indicatorHtml);
}

navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    const microphone = audioContext.createMediaStreamSource(stream);
    const scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);
    microphone.connect(analyser);
    analyser.connect(scriptProcessor);
    scriptProcessor.connect(audioContext.destination);

    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = e => {
      audioChunks.push(e.data);
    };

       mediaRecorder.onstop = () => {
           console.log(' .. stopped recording ..')
           $('#recordingIndicator').hide();
       }

      mediaRecorder.onstart = () => {
           console.log(' ** started recording ..')
           $('#recordingIndicator').show();
       }

    add_audio_to_page = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.controls = true;
      document.body.appendChild(audio);
      //audioChunks = []; // Clear the recorded chunks
    };

    // Create and handle Start button
    const startButton = createButton('startButton', 'Start Recording');
    startButton.addEventListener('click', function() {
      if (mediaRecorder.state !== 'recording') {
        mediaRecorder.start();
        isRecording = true;
        console.log('Recording started');
      }
    });

    // Create and handle Stop button
    const stopButton = createButton('stopButton', 'Stop Recording');
    stopButton.addEventListener('click', function() {
      //if (mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
      //}
      // isRecording = false;
      console.log('Stopped recording and added audio to page');
          // Stop the script processor and disconnect all nodes
          scriptProcessor.disconnect();
          analyser.disconnect();
          microphone.disconnect();

          // Stop all media stream tracks to turn off the microphone light
          stream.getTracks().forEach(track => track.stop());
                add_audio_to_page()
        });

    // Silence detection
    scriptProcessor.onaudioprocess = function(event) {
      const input = event.inputBuffer.getChannelData(0);
      let sum = 0.0;
      for (let i = 0; i < input.length; ++i) {
        sum += input[i] * input[i];
      }
      let volume = Math.sqrt(sum / input.length);

        threshold_start = 0.01
        threshold_stop = 0.005
      if (recordingStartTime === null || (Date.now() - recordingStartTime >= 1000)) {
          if (volume > threshold_start && !isRecording && mediaRecorder.state !== 'recording') {
            mediaRecorder.start();
            isRecording = true;
            recordingStartTime = Date.now();
            console.log('Recording automatically started due to detected sound');
          } else if (volume <= threshold_stop && isRecording && mediaRecorder.state === 'recording')        {
            console.log(volume)
            mediaRecorder.stop();
            isRecording = false;
            console.log('Recording automatically stopped due to silence');
          }
      }
    };
      createRecordingIndicator();

  })
  .catch(err => {
    console.error('Error accessing the microphone', err);
  });

