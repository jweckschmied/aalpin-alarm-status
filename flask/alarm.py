from flask import Flask, render_template, request, Response
from collections import UserDict
import queue
import json

app = Flask(__name__)


class StatusAnnouncer:
    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]


announcer = StatusAnnouncer()

locations = {
    "office_north": "red",
    "office_south": "green",
    "warehouse_north": "red",
    "warehouse_south": "red",
}


@app.route("/")
def index():
    return render_template("index.html", locations=locations)


@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.get_json()
    if data["location"] in locations.keys() and data["status"] in ["red", "green"]:
        if data["status"] == locations[data["location"]]:
            return "No changes.", 200
        else:
            locations[data["location"]] = data["status"]
            changed = {"location": data["location"], "status": data["status"]}
            announcer.announce(msg=json.dumps(changed))
            return "Status successfully updated!", 200
    else:
        return "Bad request. Location or status type does not exist.", 400


@app.route("/stream")
def stream():
    def eventStream():
        messages = announcer.listen()
        while True:
            msg = messages.get()
            yield "data: {}\n\n".format(msg)

    return Response(eventStream(), mimetype="text/event-stream")
