var eventSource = new EventSource("/stream");
eventSource.onmessage = function (e) {
    console.log(e.data)
    var data = JSON.parse(e.data);
    var element = document.getElementById(data.location);
    element.style.color = data.status;
    element.innerHTML = 'Status: ' + data.status
};


function changeStatus(color) {
    const params = {
        location: 'office_north',
        status: color
    };
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    };
    fetch('/update_status', options)
        .then(response => response.json())
        .then(response => {
            // Do something with response.
        });
}
