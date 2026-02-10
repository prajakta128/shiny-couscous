from flask import Flask, render_template, request, jsonify, abort
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REMINDERS_FILE = os.path.join(DATA_DIR, "reminders.json")

# ---------------- HELPERS ----------------
def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)

def load_topics():
    raw = load_json("topic_details.json")
    return {k: {**v, "id": k} for k, v in raw.items()}

def load_schemes():
    return load_json("schemes.json")

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        try:
            with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_reminders(data):
    with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STATIC DATA ----------------
articles = {
    "meditation": {
        "title": "Mindfulness Meditation for Beginners",
        "content": "Simple breathing and focus techniques to reduce stress."
    },
    "yoga": {
        "title": "Yoga for Stress Relief",
        "content": "Child’s pose, forward fold, legs-up-the-wall."
    }
}

# ---------------- LOAD HOSPITALS ----------------
with open(os.path.join(DATA_DIR, "hospital_pune.json"), "r", encoding="utf-8") as f:
    hospitals_json = json.load(f)

for i, h in enumerate(hospitals_json):
    h["id"] = h.get("id", i + 1)

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/topics")
def topics():
    topics = [
        {
            "id": k,
            "title": v["title"],
            "category": v["category"],
            "icon": v["icon"],
            "brief": v["brief"]
        }
        for k, v in load_topics().items()
    ]
    return render_template("topics.html", topics=topics)

@app.route("/topic/<topic_id>")
def topic_detail(topic_id):
    topics = load_topics()
    if topic_id not in topics:
        abort(404)
    return render_template("topic_detail.html", topic=topics[topic_id])

@app.route("/schemes")
def schemes():
    return render_template("schemes.html", schemes=load_schemes())

@app.route("/scheme/<int:scheme_id>")
def scheme_detail(scheme_id):
    schemes = load_schemes()
    scheme = next((s for s in schemes if s["id"] == scheme_id), None)
    if not scheme:
        abort(404)
    return render_template("scheme_detail.html", scheme=scheme)

@app.route("/hospitals")
def hospital_list():
    return render_template("hospital_list.html", hospitals=hospitals_json)

@app.route("/hospital/<int:hospital_id>")
def hospital_detail(hospital_id):
    hospital = next((h for h in hospitals_json if h["id"] == hospital_id), None)
    if not hospital:
        abort(404)
    return render_template("hospital.html", hospital=hospital)

# ---------------- REMINDERS ----------------
@app.route("/reminders")
def reminders_page():
    return render_template("reminder.html")

@app.route("/set-reminder", methods=["POST"])
def set_reminder():
    data = request.json
    data["id"] = str(uuid.uuid4())
    data["notified"] = False
    reminders = load_reminders()
    reminders.append(data)
    save_reminders(reminders)
    return jsonify({"status": "success"})

@app.route("/get-reminders")
def get_reminders():
    return jsonify(load_reminders())

@app.route("/check-reminders")
def check_reminders():
    reminders = load_reminders()
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    today = now.strftime("%Y-%m-%d")

    due = [
        r for r in reminders
        if not r.get("notified") and r["time"] == current_time and r["date"] == today
    ]
    return jsonify(due)

@app.route("/mark-reminder-notified/<rid>", methods=["POST"])
def mark_reminder_notified(rid):
    reminders = load_reminders()
    for r in reminders:
        if r["id"] == rid:
            r["notified"] = True
    save_reminders(reminders)
    return jsonify({"status": "success"})

@app.route("/delete-reminder/<rid>", methods=["DELETE"])
def delete_reminder(rid):
    reminders = [r for r in load_reminders() if r["id"] != rid]
    save_reminders(reminders)
    return jsonify({"status": "success"})

# ---------------- GYM TRAINER (DISABLED) ----------------
@app.route("/gym")
def gym_trainer():
    return render_template("gym.html")

@app.route("/start-gym", methods=["POST"])
def start_gym():
    return """
    <h2>⚠ Gym Trainer not available on cloud</h2>
    <p>This feature works only on your local machine due to camera access.</p>
    <a href="/">Go Home</a>
    """

# ---------------- OTHER ----------------
@app.route("/wellness")
def wellness():
    return render_template("wellness.html")

@app.route("/finance")
def finance():
    return render_template("finance.html")

@app.route("/emergency")
def emergency():
    return render_template("emergency.html")

@app.route("/article/<topic>")
def article(topic):
    return jsonify(articles.get(topic, {"title": "Not Found"}))

# ---------------- START ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
