async function startRecording() {
  try {
    // Request access to the webcam and microphone
    const cameraStream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true
    });

    // Request access to the screen
    const screenStream = await navigator.mediaDevices.getDisplayMedia({
      video: true
    });

    // Record both streams
    const cameraRecorder = new MediaRecorder(cameraStream, { mimeType: 'video/webm' });
    const screenRecorder = new MediaRecorder(screenStream, { mimeType: 'video/webm' });

    let cameraChunks = [];
    let screenChunks = [];

    cameraRecorder.ondataavailable = e => cameraChunks.push(e.data);
    screenRecorder.ondataavailable = e => screenChunks.push(e.data);

    window.camera_chunks = cameraChunks

    cameraRecorder.onstop = async () => {
      const blob = new Blob(cameraChunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);
      const downloadLink = document.createElement('a');
      downloadLink.href = url;
      downloadLink.download = 'webcamRecording.webm';
      downloadLink.textContent = 'Download Webcam Video';
      document.body.appendChild(downloadLink);
    };

    screenRecorder.onstop = async () => {
      const blob = new Blob(screenChunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);
      const downloadLink = document.createElement('a');
      downloadLink.href = url;
      downloadLink.download = 'screenRecording.webm';
      downloadLink.textContent = 'Download Screen Video';
      document.body.appendChild(downloadLink);

      // Start merging the videos after both are recorded
      mergeVideos(blob, cameraChunks, cameraStream);
    };

    // Start recording both streams
    cameraRecorder.start();
    screenRecorder.start();

    // Stop recording after a specific duration
    setTimeout(() => {
      cameraRecorder.stop();
      screenRecorder.stop();
      cameraStream.getTracks().forEach(track => track.stop());
      screenStream.getTracks().forEach(track => track.stop());
    }, 10000);  // e.g., 20 seconds

  } catch (error) {
    console.error('Failed to capture media:', error);
  }
}


// Function to merge videos on a canvas
// todo: fix the bug that is happening on the creation of the merged video.
//       it is almost working perfectly, camera video is recorded with audio, screenshare is captured ok, new merged video is created ok, but it is just the audio that is not working
function mergeVideos(screenBlob, cameraChunks, cameraStream) {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const videoScreen = document.createElement('video');
  const videoCamera = document.createElement('video');
  videoScreen.src = URL.createObjectURL(screenBlob);
  const cameraBlob = new Blob(cameraChunks, { type: 'video/webm' });
  videoCamera.src = URL.createObjectURL(cameraBlob);

  document.body.appendChild(canvas);  // For demonstration purposes

  videoScreen.onloadedmetadata = () => {
    videoCamera.onloadedmetadata = () => {
      canvas.width = videoScreen.videoWidth / 5;
      canvas.height = videoScreen.videoHeight / 5;

      videoScreen.play();
      videoCamera.play();

      function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(videoScreen, 0, 0, canvas.width, canvas.height);
        ctx.drawImage(videoCamera, canvas.width - videoCamera.videoWidth / 4 - 20,
                                   canvas.height - videoCamera.videoHeight / 4 - 20,
                                   videoCamera.videoWidth / 4,
                                   videoCamera.videoHeight / 4);  // Smaller overlay for the webcam
        requestAnimationFrame(draw);
      }
      draw();

      const finalStream = canvas.captureStream(30); // 30 FPS

      window.cameraStream = cameraStream
      // Add the audio tracks from the camera to the final stream
      const audioTracks = cameraStream.getAudioTracks();
      audioTracks.forEach(track => finalStream.addTrack(track));

      const finalRecorder = new MediaRecorder(finalStream, { mimeType: 'video/webm' });
      let finalChunks = [];
      finalRecorder.ondataavailable = e => finalChunks.push(e.data);

      finalRecorder.onstop = async () => {
        const finalBlob = new Blob(finalChunks, { type: 'video/webm' });
        const finalUrl = URL.createObjectURL(finalBlob);
        const finalDownloadLink = document.createElement('a');
        finalDownloadLink.href = finalUrl;
        finalDownloadLink.download = 'combinedRecording.webm';
        finalDownloadLink.textContent = 'Download Combined Video';
        document.body.appendChild(finalDownloadLink);
      };

      finalRecorder.start();
      window.final_recorder = finalRecorder     // trying to debug why the audio is not saved in the merged video
      window.final_stream = finalStream
      window.final_chunks = finalChunks

      // Stop final recording a bit after videos have ended
            setTimeout(() => {
        finalRecorder.stop();
        // Stop the canvas stream as well
        finalStream.getTracks().forEach(track => track.stop());
      }, 10000); // Stop recording 5 seconds after videos have played
    };
      videoCamera.load();
  };

  videoScreen.load();

}

startRecording();
