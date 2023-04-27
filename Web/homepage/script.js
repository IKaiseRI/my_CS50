var aud = document.getElementById("myAudio");

function mute() {
    aud.muted = true;
    aud.pause();
}
function unmute() {
    aud.muted = false;
    aud.play();
}

var vid = document.getElementById("myVideo");

function play() {
    vid.play();
}
function pause() {
    vid.pause();
}

var dur = document.getElementById("myVideo");

function toStart() {
    dur.currentTime = 0;
}

function toEnd() {
    dur.currentTime = dur.duration;
}