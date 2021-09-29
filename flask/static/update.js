var eventSource = new EventSource("/stream");
eventSource.onmessage = function (e) {
    console.log(e.data)
    var data = JSON.parse(e.data);
    document.getElementById(data.location).style.color = data.status;
};


function changeStatus() {
    const params = {
        location: "warehouse_north",
        status: "red"
    };
    const options = {
        method: 'POST',
        body: JSON.stringify(params)
    };
    fetch('/update_status', options)
        .then(response => response.json())
        .then(response => {
            // Do something with response.
        });
}
