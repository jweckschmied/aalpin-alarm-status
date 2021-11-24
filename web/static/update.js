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
var myLoc = getLocation();


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

function updateStatusPoll() {
    getStatusAll().then(status => {
        for (const [key, value] of Object.entries(status)) {
            document.getElementById(key).style.backgroundColor = value["status"];
            var id = key + "-ts"
            document.getElementById(id).innerHTML = "seit: " + value["timestamp"];
        };
        myStatus = status[myLoc]["status"];
        setButton();
        setTimeout(updateStatusPoll, 5000);
    });
}

// initial call, or just call refresh directly
updateStatusPoll();

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
        .then(response => {
            response.json().then(json => {
                document.getElementById(myLoc).style.backgroundColor = json["status"];
                var id = myLoc + "-ts"
                document.getElementById(id).innerHTML = "seit: " + json["timestamp"];
                myStatus = json["status"];
                setButton()
            });
        });
}

function setLocation(location) {
    const d = new Date();
    d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = "aalpin_loc=" + location + ";" + expires + ";path=/";
}