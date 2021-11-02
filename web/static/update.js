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
var myStatus = "";

const switchColors = {
    red: "green",
    green: "red",
};

async function getStatusAll() {
    const response = await fetch('/get_status');
    const status = await response.json();
    return status;
}
function setButton() {
    if (myStatus == "green") {
        document.getElementById("change-status").value = "Abwesend";
    }
    else {
        document.getElementById("change-status").value = "Anwesend";
    }
}

function initStatus() {
    getStatusAll().then(status => {
        for (const [key, value] of Object.entries(status)) {
            document.getElementById(key).style.backgroundColor = value;
        };
        myStatus = status[getLocation()];
        setButton();
    });
}

initStatus();

var eventSource = new EventSource("/stream");
eventSource.onmessage = function (e) {
    console.log(e.data)
    var data = JSON.parse(e.data);
    var element = document.getElementById(data.location);
    element.style.backgroundColor = data.status;
    if (getLocation() == data.location) {
        myStatus = data.status;
        setButton();
    };
};

function changeStatus() {
    const params = {
        location: getLocation(),
        status: switchColors[myStatus]
    };
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    };
    fetch('/update_status', options)
        .then(response => response.text());
}

function setLocation(location) {
    const d = new Date();
    d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = "aalpin_loc=" + location + ";" + expires + ";path=/";
    console.log("Cookie set")
}