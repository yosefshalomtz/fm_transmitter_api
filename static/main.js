const { stat } = require("node:fs");

var status_span = document.getElementById("status");
var play_button = document.getElementById("play");
var stop_button = document.getElementById("stop");
var frequency_input = document.getElementById("frequency");


play_button.onclick = function () {
    console.log("Play button clicked");
    var url = "/api/play?frq=" + frequency_input.value + "&uploadedfilename=block.wav";
    fetch(url).then(response => response.json()).then(data => {
        console.log("Play response:", data);
        // set status text
        if(data.status==="success") status_span.textContent = "Playing sound at " + frequency_input.value + " Hz";
        else status_span.textContent = "Failed: " + data.status;
    })
    .catch(error => {
        console.error("Error playing:", error);
        status_span.textContent = "Error playing sound";
        // set status text
    });
}
stop_button.onclick = function () {
    console.log("Stop button clicked");
    fetch("/api/stop").then(response => response.json()).then(data => {
        console.log("Stop response:", data);
        // set status text
        if(data.status==="success") status_span.textContent = "Sound stopped";
        else status_span.textContent = "Failed: " + data.status;
    })
    .catch(error => {
        console.error("Error stopping:", error);
        // set status text
        status_span.textContent = "Error stopping sound";
    });
}