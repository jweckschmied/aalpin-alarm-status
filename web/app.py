from flask import Flask, render_template, request, Response, redirect, jsonify
import json
from announcer import StatusAnnouncer
import os.path

# Setup
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
announcer = StatusAnnouncer()

LOCATION_NAMES = {
    "office_north": "Büro Nord",
    "office_south": "Büro Süd",
    "warehouse_north": "Lager Nord",
    "warehouse_south": "Lager Süd",
}


def init_status():
    default = {
        "office_north": "green",
        "office_south": "green",
        "warehouse_north": "green",
        "warehouse_south": "green",
    }
    try:
        with open("status.json") as json_file:
            data = json.load(json_file)
            return data
    except ValueError:
        app.logger.warning(
            "ValueError: No JSON object could be decoded. Using default values."
        )
        return default
    except FileNotFoundError:
        app.logger.info("status.json did not exist, created new one.")
        with open("status.json", "w+") as f:
            json.dump(default, f)
        return default


locations = init_status()


@app.route("/")
def index():
    myloc = request.cookies.get("aalpin_loc")
    if myloc in locations.keys():
        return render_template(
            "index.html", locations=locations, names=LOCATION_NAMES, myloc=myloc
        )
    else:
        return redirect("/location")


@app.route("/location")
def location():
    return render_template("locations.html", locations=locations, names=LOCATION_NAMES)


@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.get_json()
    if (
        data["location"] in locations.keys()
        and data["status"] in ["red", "green"]
        and request.cookies.get("aalpin_loc") == data["location"]
    ):
        if data["status"] == locations[data["location"]]:
            return "No changes.", 200
        else:
            locations[data["location"]] = data["status"]
            changed = {"location": data["location"], "status": data["status"]}
            announcer.announce(msg=json.dumps(changed))
            with open("status.json", "w") as f:
                json.dump(locations, f)
            return "Status successfully updated!", 200
    else:
        return (
            "Bad request. Location or status type does not exist, or you tried to change the status of a different location.",
            400,
        )


@app.route("/get_status", methods=["GET"])
def get_status():
    return jsonify(locations)


@app.route("/stream")
def stream():
    def eventStream():
        messages = announcer.listen()
        while True:
            msg = messages.get()
            yield "data: {}\n\n".format(msg)

    return Response(
        eventStream(), mimetype="text/event-stream", headers={"X-Accel-Buffering": "no"}
    )


if __name__ == "__main__":
    app.run()
