from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection (local)
client = MongoClient("mongodb://localhost:27017")
db = client["github_events"]
collection = db["events"]


@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    # PULL REQUEST & MERGE EVENTS
    if event_type == "pull_request":
        action = payload.get("action")

        # MERGE event (brownie points)
        if action == "closed" and payload["pull_request"]["merged"]:
            author = payload["sender"]["login"]
            from_branch = payload["pull_request"]["head"]["ref"]
            to_branch = payload["pull_request"]["base"]["ref"]
            timestamp = payload["pull_request"]["merged_at"]

            event_data = {
                "event_type": "merge",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

            result = collection.insert_one(event_data)
            print("Inserted MERGE event with id:", result.inserted_id)

            print(
                f'{author} merged branch {from_branch} to {to_branch} on {timestamp}'
            )

        # Normal Pull Request event
        else:
            author = payload["sender"]["login"]
            from_branch = payload["pull_request"]["head"]["ref"]
            to_branch = payload["pull_request"]["base"]["ref"]
            timestamp = payload["pull_request"]["created_at"]

            event_data = {
                "event_type": "pull_request",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

            result = collection.insert_one(event_data)
            print("Inserted PR event with id:", result.inserted_id)

            print(
                f'{author} submitted a pull request from '
                f'{from_branch} to {to_branch} on {timestamp}'
            )

    # PUSH EVENT
    elif event_type == "push":
        author = payload["pusher"]["name"]
        to_branch = payload["ref"].split("/")[-1]
        timestamp = payload["head_commit"]["timestamp"]

        event_data = {
            "event_type": "push",
            "author": author,
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

        result = collection.insert_one(event_data)
        print("Inserted PUSH event with id:", result.inserted_id)

        print(
            f'{author} pushed to {to_branch} on {timestamp}'
        )

    # IGNORE OTHER EVENTS
    else:
        print(f"Ignored event type: {event_type}")

    return jsonify({"status": "received"}), 200


# API FOR UI
@app.route("/events", methods=["GET"])
def get_events():
    events = list(
        collection.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(10)
    )
    return jsonify(events)


# UI ROUTE 
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5000)
