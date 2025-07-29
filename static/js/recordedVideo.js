const video = document.getElementById("video");
        const playBtn = document.querySelector(".play-btn");
        const progress = document.querySelector(".progress");
        const progressBar = document.querySelector(".progress-bar");
        const fullscreenBtn = document.querySelector(".fullscreen-btn");

        playBtn.addEventListener("click", () => {
            if (video.paused) {
                video.play();
                playBtn.textContent = "⏸";
            } else {
                video.pause();
                playBtn.textContent = "▶";
            }
        });

        video.addEventListener("timeupdate", () => {
            const percent = (video.currentTime / video.duration) * 100;
            progressBar.style.width = percent + "%";
        });

        progress.addEventListener("click", (e) => {
            const clickX = e.offsetX;
            const width = progress.offsetWidth;
            video.currentTime = (clickX / width) * video.duration;
        });

        fullscreenBtn.addEventListener("click", () => {
            if (video.requestFullscreen) {
                video.requestFullscreen();
            } else if (video.mozRequestFullScreen) {
                video.mozRequestFullScreen();
            } else if (video.webkitRequestFullscreen) {
                video.webkitRequestFullscreen();
            } else if (video.msRequestFullscreen) {
                video.msRequestFullscreen();
            }
        });