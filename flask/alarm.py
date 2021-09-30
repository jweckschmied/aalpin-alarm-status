from flask import Flask, render_template, request, Response
import json
from announcer import StatusAnnouncer
import os.path

# Setup
app = Flask(__name__)
announcer = StatusAnnouncer()


def init_status():
    default = {
        "office_north": "green",
        "office_south": "green",
        "warehouse_north": "green",
        "warehouse_south": "green",
    }
    if os.path.isfile("status.json"):
        try:
            with open("status.json") as json_file:
                data = json.load(json_file)
        except ValueError:
            app.logger.error(
                "ValueError: Failed to load status.json. No JSON object could be decoded"
            )
            return default
    else:
        return default


locations = init_status()


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
            with open("status.json", "w+") as f:
                json.dump(locations, f)
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
