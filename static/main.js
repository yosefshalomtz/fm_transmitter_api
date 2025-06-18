var status_span = document.getElementById("status");
var play_button = document.getElementById("play");
var stop_button = document.getElementById("stop");
// thread that always checks the status of the server
var checkStatus = setInterval(function () {
    console.log("Checking server status...");
    fetch("/api/getstatus").then(response => response.text()).then(data => {
        status_span.textContent = data;
    })
        .catch(error => {
            status_span.textContent = "Error checking server status";
        });
}, 500);

play_button.onclick = function () {
    console.log("Play button clicked");
    var url = "/api/play?frq=" + document.getElementById("frq").value + "&uploadedfilename=block.wav";
    fetch(url).then(response => response.json()).then(data => {
        console.log("Play response:", data);
    })
    .catch(error => {
        console.error("Error playing:", error);
    });
}
stop_button.onclick = function () {
    console.log("Stop button clicked");
    fetch("/api/stop").then(response => response.json()).then(data => {
        console.log("Stop response:", data);
    })
    .catch(error => {
        console.error("Error stopping:", error);
    });
}