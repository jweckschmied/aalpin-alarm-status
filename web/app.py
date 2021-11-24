from flask import Flask, render_template, request, Response, redirect, jsonify
import json
import os.path
from datetime import datetime

# Setup
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

LOCATION_NAMES = {
    "office_north": "Büro Nord",
    "office_south": "Büro Süd",
    "warehouse_north": "Lager Nord",
    "warehouse_south": "Lager Süd",
}


def init_status():
    time_now = datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
    default = {
        "office_north": {"status": "green", "timestamp": time_now},
        "office_south": {"status": "green", "timestamp": time_now},
        "warehouse_north": {"status": "green", "timestamp": time_now},
        "warehouse_south": {"status": "green", "timestamp": time_now},
    }
    try:
        with open("static/status.json") as json_file:
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
        if data["status"] == locations[data["location"]]["status"]:
            return "No changes.", 200
        else:
            locations[data["location"]] = {
                "status": data["status"],
                "timestamp": datetime.now().strftime("%d.%m.%Y, %H:%M:%S"),
            }
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


if __name__ == "__main__":
    app.run()
