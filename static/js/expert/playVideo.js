const video = document.getElementById('videoPlayer');
const playPauseBtn = document.getElementById('playPause');
const currentTimeSpan = document.getElementById('currentTime');
const durationSpan = document.getElementById('duration');
const fullscreenBtn = document.getElementById('fullscreen');
const volumeSlider = document.getElementById('volume');
const speedSelector = document.getElementById('speed');
const progressBar = document.getElementById('progressBar');
const themeToggle = document.getElementById('themeToggle');
const playerContainer = document.getElementById('playerContainer');

// Play/Pause functionality
playPauseBtn.addEventListener('click', () => {
  if (video.paused) {
    video.play();
    playPauseBtn.textContent = '❚❚';
  } else {
    video.pause();
    playPauseBtn.textContent = '►';
  }
});

// Update time displays
video.addEventListener('timeupdate', () => {
  currentTimeSpan.textContent = formatTime(video.currentTime);
  progressBar.value = (video.currentTime / video.duration) * 100;
});

// Set duration when loaded
video.addEventListener('loadedmetadata', () => {
  durationSpan.textContent = formatTime(video.duration);
});

// Seek video
progressBar.addEventListener('input', () => {
  video.currentTime = (progressBar.value / 100) * video.duration;
});

// Volume control
volumeSlider.addEventListener('input', () => {
  video.volume = volumeSlider.value;
});

// Speed control
speedSelector.addEventListener('change', () => {
  video.playbackRate = speedSelector.value;
});

// Fullscreen
fullscreenBtn.addEventListener('click', () => {
  if (video.requestFullscreen) {
    video.requestFullscreen();
  } else if (video.webkitRequestFullscreen) {
    video.webkitRequestFullscreen();
  } else if (video.msRequestFullscreen) {
    video.msRequestFullscreen();
  }
});

// Dark/Light mode toggle
themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('light-mode');
  if (document.body.classList.contains('light-mode')) {
    themeToggle.textContent = '☀️';
  } else {
    themeToggle.textContent = '🌙';
  }
});

// Helper function to format time
function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}