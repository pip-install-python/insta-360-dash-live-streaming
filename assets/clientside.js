window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        updateVideoSource: function(n_intervals) {
            var videoElement = document.querySelector('video');
            if (videoElement && videoElement.src) {
                var currentSrc = new URL(videoElement.src);
                var oldTimestamp = currentSrc.searchParams.get('_');
                var newTimestamp = Date.now();

                // Only update if more than 30 seconds have passed
                if (!oldTimestamp || (newTimestamp - oldTimestamp > 30000)) {
                    currentSrc.searchParams.set('_', newTimestamp);

                    // Create a new video element
                    var newVideo = document.createElement('video');
                    newVideo.src = currentSrc.toString();

                    // Set the same style as the original video
                    newVideo.style.cssText = videoElement.style.cssText;

                    // Replace the old video with the new one
                    videoElement.parentNode.replaceChild(newVideo, videoElement);

                    // Start playing the new video
                    newVideo.play().catch(function(error) {
                        console.log("Error attempting to play:", error);
                    });
                }
            }
            return Date.now();
        }
    }
});