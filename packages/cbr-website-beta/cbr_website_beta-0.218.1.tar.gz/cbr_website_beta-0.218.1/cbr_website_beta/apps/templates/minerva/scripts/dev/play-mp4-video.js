console.log('[{{version}}] Executing {{script_name}} at {{date_now}}')

let target_div = 'target_div'

function play_video(video_to_play) {
    video_options= { src     : video_to_play,
                     autoplay: false ,
                     muted   : true  ,
                     controls: true ,
                     width   : 500  }
    let video = $('<video>', video_options);

    $('#dev-area').html(video);

    window.my_video = video
}

function play_video_using_canvas(target_video, icon_url) {
    // Create a new canvas element
    let canvas = $('<canvas></canvas>');
    let ctx = canvas[0].getContext('2d');

    // Set canvas size
    canvas.attr('width', 640);  // Example width
    canvas.attr('height', 380); // Example height

    // Create the video element
    let video = document.createElement('video');
    video.src = target_video;
    video.muted = true
    video.controls = true
    video.play();
    //video.loop = true;

    let divContainer = $('<div></div>');  // Create a container div for better layout control
    divContainer.append(canvas);
    divContainer.append(video);
    // Append the canvas to the #dev-area div
    $('#dev-area').html(divContainer);


    let frameCount = 0;
    const icon = new Image();
    icon.src = icon_url; // Your icon URL

    let draw = function () {

        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            ctx.drawImage(video, 0, 0, canvas.width(), canvas.height());

            frameCount++;

            // Set styles for the frame counter
            ctx.font = '20px Arial';
            ctx.fillStyle = 'yellow';
            ctx.textAlign = 'left';
            ctx.textBaseline = 'top';

            // Draw frame count
            ctx.fillText('Frame: ' + frameCount, 10, 10);
            //Draw the icon onto the canvas
            ctx.drawImage(icon, canvas.width() - 200, canvas.height() - 150, 200, 142); // Adjust position and size as needed


        }
        if (!video.ended) {
            requestAnimationFrame(draw);
        } else {
            console.log("Video ended. Total frames drawn: " + frameCount);
        }
    };

    // Call the draw loop
    draw();
}


athena_video = 'https://static.thecyberboardroom.com/assets/videos/video-tcb-introduction__27-feb.mp4'
sample_video = "https://file-examples.com/storage/fe4996602366316ffa06467/2017/04/file_example_MP4_480_1_5MG.mp4"
//play_video(athena_video)
minerva_icon_url = 'https://static.thecyberboardroom.com/assets/cbr/minerva-icon.png'
minerva_icon_url_reserved = 'https://static.thecyberboardroom.com/assets/cbr/minerva-icon-reversed-out.png'
//play_video(sample_video)
//play_video_using_canvas(sample_video, minerva_icon_url_reserved)
play_video_using_canvas(athena_video, minerva_icon_url)