var status_span = document.getElementById("status");
// thread that always checks the status of the server
var checkStatus = setInterval(function() {
    console.log("Checking server status...");
    fetch("/getstatus").then(response=>response.text()).then(data => {
            status_span.textContent = data;
        })
        .catch(error => {
            status_span.textContent = "Error checking server status";
        });
}, 500);