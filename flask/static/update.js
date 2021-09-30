function getLocation() {
    let name = "aalpin_loc=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

var eventSource = new EventSource("/stream");
eventSource.onmessage = function (e) {
    console.log(e.data)
    var data = JSON.parse(e.data);
    var element = document.getElementById(data.location);
    element.style.backgroundColor = data.status;
};

function changeStatus(color) {
    const params = {
        location: getLocation(),
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

function setLocation(location) {
    const d = new Date();
    d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = "aalpin_loc=" + location + ";" + expires + ";path=/";
    console.log("Cookie set")
}