// this captures the user's screen and the system audio

async function startScreenAndMicRecording() {
  try {
    // Request screen media without audio for the screen capture
    const videoStream = await navigator.mediaDevices.getDisplayMedia({ video: true, audio: true });

    // Request microphone access
    const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Combine the video and audio streams
    const tracks = [...videoStream.getVideoTracks(), ...audioStream.getAudioTracks()];
    const combinedStream = new MediaStream(tracks);

    const recorder = new MediaRecorder(combinedStream, { mimeType: 'video/webm' });

    let chunks = [];
    recorder.ondataavailable = e => chunks.push(e.data);

    recorder.onstop = () => {
      const blob = new Blob(chunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);

      // Create video element to play the recording
      const video = document.createElement('video');
      video.src = url;
      video.controls = true;
      video.style.width = "500px"
      document.body.appendChild(video);
      video.play();

      // Create download link for the video
      const downloadLink = document.createElement('a');
      downloadLink.href = url;
      downloadLink.download = 'recordedScreenAndMic.webm';
      downloadLink.innerText = 'Download Video';
      document.body.appendChild(downloadLink);
    };

    recorder.start();

    // Stop recording after a certain amount of time or interaction
    setTimeout(() => {
      recorder.stop();
      // Stop the streams to release the screen capture and microphone
      videoStream.getTracks().forEach(track => track.stop());
      audioStream.getTracks().forEach(track => track.stop());
    }, 10000);

  } catch (error) {
    console.error('Error accessing the screen or microphone:', error);
  }
}

startScreenAndMicRecording();


// code below captures the audio from the system, not the user's audio

// async function startScreenRecording() {
//   try {
//     // Request screen media instead of camera
//     const stream = await navigator.mediaDevices.getDisplayMedia({ video: true, audio: true });
//     const recorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
//
//     let chunks = [];
//     recorder.ondataavailable = e => chunks.push(e.data);
//
//     recorder.onstop = () => {
//       const blob = new Blob(chunks, { type: 'video/webm' });
//       const url = URL.createObjectURL(blob);
//
//       // Create video element to play the recording
//       const video = document.createElement('video');
//       video.src = url;
//       video.controls = true;
//       document.body.appendChild(video);
//       video.play();
//
//       // Create download link for the video
//       const downloadLink = document.createElement('a');
//       downloadLink.href = url;
//       downloadLink.download = 'recordedScreen.webm';
//       downloadLink.innerText = 'Download Video';
//       document.body.appendChild(downloadLink);
//     };
//
//     recorder.start();
//
//     // Stop recording after 10 seconds
//     setTimeout(() => {
//       recorder.stop();
//       // Stop the stream to release the screen capture
//       stream.getTracks().forEach(track => track.stop());
//     }, 10000);
//
//   } catch (error) {
//     console.error('Error accessing the screen capture:', error);
//   }
// }
//
// startScreenRecording();
