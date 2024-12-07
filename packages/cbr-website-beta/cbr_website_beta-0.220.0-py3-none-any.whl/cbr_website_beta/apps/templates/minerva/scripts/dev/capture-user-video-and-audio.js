async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio :true });
    const recorder = new MediaRecorder(stream, { mimeType: 'video/webm' });

    let chunks = [];
    recorder.ondataavailable = e => chunks.push(e.data);

    recorder.onstop = () => {
      const blob = new Blob(chunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);

      // Create video element to play the recording
      const video = document.createElement('video');
      video.src = url;
      video.controls = true;
      document.body.appendChild(video);
      video.play();

      // Create download link for the video
      const downloadLink = document.createElement('a');
      downloadLink.href = url;
      downloadLink.download = 'recordedVideo.webm';
      downloadLink.innerText = 'Download Video';
      document.body.appendChild(downloadLink);
    };

    recorder.start();

    // Stop recording after 10 seconds
    setTimeout(() => {
      recorder.stop();
      // Don't forget to stop the stream to turn off the webcam light
      stream.getTracks().forEach(track => track.stop());
    }, 10000);

  } catch (error) {
    console.error('Error accessing the camera:', error);
  }
}

startRecording();
