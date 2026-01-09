# health_platform/app.py
from flask import Flask, render_template, request, jsonify, abort
import json
import os
import subprocess



app = Flask(__name__)

# --- Paths ---
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# --- Load Data ---
def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def load_topics():
    raw = load_json('topic_details.json')
    return {k: {**v, "id": k} for k, v in raw.items()}

def load_schemes():
    with open(os.path.join(DATA_DIR, 'schemes.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

# --- Wellness Articles ---
articles = {
    "meditation": {
    "title": "Mindfulness Meditation for Beginners",
    "content": "This article explains simple meditation techniques to reduce stress and improve mental clarity. "
    "Start with deep breathing, focus on your breath, and practice daily for 5–10 minutes. Try incorporating guided meditations using apps or online videos."
    " Create a quiet and comfortable space to minimize distractions and enhance focus."
    },

    "yoga": {
        "title": "Yoga Poses for Stress Relief",
        "content": "Yoga poses like Child’s Pose, Forward Fold, and Legs-Up-The-Wall help release tension, calm the mind, and relax the body."
    },
    "breathing": {
        "title": "Breathing Exercises for Anxiety",
        "content": "Try 4-7-8 breathing or box breathing to manage anxiety and panic attacks effectively."
    },
    "wellness": {
        "title": "Building Mental Resilience",
        "content": "Resilience is about bouncing back from challenges. Focus on gratitude, positive affirmations, and consistent self-care."
    },
    "nutrition": {
        "title": "Healthy Eating Habits",
        "content": "A balanced diet with fruits, vegetables, whole grains, and lean proteins supports overall health. Limit processed foods and sugary drinks."
    },
    "sleep": {
        "title": "Improving Sleep Quality",
        "content": "Maintain a consistent sleep schedule, create a relaxing bedtime routine, and reduce screen time before bed to improve sleep quality."
    },
    "hydration": {
        "title": "Importance of Staying Hydrated",
        "content": "Drink enough water daily to support digestion, energy levels, and overall wellness. Track your water intake to ensure hydration."
    },
    "exercise": {
        "title": "Daily Physical Activity",
        "content": "Incorporate at least 30 minutes of moderate exercise like walking, cycling, or swimming to boost heart health, mood, and energy."
    },
    "mental_health": {
        "title": "Managing Stress and Anxiety",
        "content": "Identify stress triggers, practice mindfulness, and seek social support. Professional help can also be valuable when needed."
    },
    "self_care": {
        "title": "Daily Self-Care Practices",
        "content": "Set aside time for yourself, whether through journaling, reading, or hobbies, to maintain emotional and mental well-being."
    }
}

# --- Reminders Storage with JSON Persistence ---
REMINDERS_FILE = os.path.join(DATA_DIR, 'reminders.json')

def load_reminders():
    """Load reminders from JSON file"""
    if os.path.exists(REMINDERS_FILE):
        try:
            with open(REMINDERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_reminders(reminders_list):
    """Save reminders to JSON file"""
    with open(REMINDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(reminders_list, f, indent=2, ensure_ascii=False)

# --- Routes ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/topics")
def topics():
    topic_list = [
        {"id": k, "title": v["title"], "category": v["category"], "icon": v["icon"], "brief": v["brief"]}
        for k, v in load_topics().items()
    ]
    return render_template("topics.html", topics=topic_list)

@app.route("/topic/<topic_id>")
def topic_detail(topic_id):
    topics = load_topics()
    if topic_id not in topics:
        abort(404)
    return render_template("topic_detail.html", topic=topics[topic_id])

@app.route("/schemes")
def schemes():
    schemes_data = load_schemes()
    return render_template("schemes.html", schemes=schemes_data)

@app.route("/scheme/<int:scheme_id>")
def scheme_detail(scheme_id):
    schemes_data = load_schemes()
    scheme = next((s for s in schemes_data if s["id"] == scheme_id), None)
    if not scheme:
        abort(404)
    return render_template("scheme_detail.html", scheme=scheme)

# --- Load hospitals data ---
with open(os.path.join(DATA_DIR, "hospital_pune.json"), "r", encoding="utf-8") as f:
    hospitals_json = json.load(f)

# Assign IDs if missing
for i, h in enumerate(hospitals_json):
    h["id"] = h.get("id", i + 1)

# --- Routes ---
@app.route("/hospitals")
def hospital_list():
    return render_template("hospital_list.html", hospitals=hospitals_json)

@app.route("/hospital/<int:hospital_id>")
def hospital_detail(hospital_id):
    hospital = next((h for h in hospitals_json if h["id"] == hospital_id), None)
    if not hospital:
        return "Hospital not found", 404
    return render_template("hospital.html", hospital=hospital)



@app.route("/reminders")
def reminders_page():
    return render_template("reminder.html")

@app.route("/set-reminder", methods=["POST"])
def set_reminder():
    data = request.json
    # Add a unique ID and notified flag
    import uuid
    data['id'] = str(uuid.uuid4())
    data['notified'] = False
    reminders_list = load_reminders()
    reminders_list.append(data)
    save_reminders(reminders_list)
    return jsonify({"status": "success", "message": "Reminder set!"})

@app.route("/get-reminders")
def get_reminders():
    """Get all reminders"""
    return jsonify(load_reminders())

@app.route("/check-reminders", methods=["GET"])
def check_reminders():
    """Check if any reminders are due and return them"""
    from datetime import datetime
    reminders_list = load_reminders()
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    due_reminders = []
    for r in reminders_list:
        if not r.get('notified', False) and r['time'] == current_time and r['date'] == now.strftime("%Y-%m-%d"):
            due_reminders.append(r)
    
    return jsonify(due_reminders)

@app.route("/mark-reminder-notified/<reminder_id>", methods=["POST"])
def mark_reminder_notified(reminder_id):
    """Mark a reminder as notified to prevent duplicate notifications"""
    reminders_list = load_reminders()
    for r in reminders_list:
        if r.get('id') == reminder_id:
            r['notified'] = True
            break
    save_reminders(reminders_list)
    return jsonify({"status": "success"})

@app.route("/delete-reminder/<reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    """Delete a reminder"""
    reminders_list = load_reminders()
    reminders_list = [r for r in reminders_list if r.get('id') != reminder_id]
    save_reminders(reminders_list)
    return jsonify({"status": "success"})


@app.route("/wellness")
def wellness():
    return render_template("wellness.html")

@app.route("/gym")
def gym_trainer():
    return render_template("gym.html")

@app.route("/start-gym", methods=["POST"])
def start_gym():
    try:
        import sys
        import platform
        
        # Get the directory where gym_trainer.py is located
        app_dir = os.path.dirname(os.path.abspath(__file__))
        gym_trainer_path = os.path.join(app_dir, 'gym_trainer.py')
        
        # Verify the script exists
        if not os.path.exists(gym_trainer_path):
            raise FileNotFoundError(f"gym_trainer.py not found at: {gym_trainer_path}")
        
        # Use the same Python interpreter that's running the app
        python_executable = sys.executable
        
        # Verify Python executable exists
        if not os.path.exists(python_executable):
            raise FileNotFoundError(f"Python executable not found at: {python_executable}")
        
        # Log the execution details (for debugging)
        import sys as sys_module
        print(f"[GYM TRAINER] Launching from: {gym_trainer_path}")
        print(f"[GYM TRAINER] Using Python: {python_executable}")
        print(f"[GYM TRAINER] Platform: {platform.system()}")
        
        # Run the gym trainer script
        if platform.system() == 'Windows':
            # On Windows, use CREATE_NEW_CONSOLE to open in a new window
            process = subprocess.Popen(
                [python_executable, gym_trainer_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                stdout=None,
                stderr=None
            )
            print(f"[GYM TRAINER] Process ID: {process.pid}")
        else:
            # On Linux/Mac, use subprocess with new session
            process = subprocess.Popen(
                [python_executable, gym_trainer_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid  # Create new process group on Unix
            )
            print(f"[GYM TRAINER] Process ID: {process.pid}")
        
        return """
        <html>
        <head>
            <title>Gym Trainer</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Poppins', sans-serif; 
                    padding: 40px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .container { 
                    max-width: 600px; 
                    width: 100%;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    padding: 40px;
                }
                .success { 
                    color: white; 
                    background: linear-gradient(135deg, #00b88a 0%, #00d4aa 100%);
                    padding: 20px; 
                    border-radius: 8px; 
                    margin-bottom: 20px; 
                    text-align: center;
                }
                .success h2 { font-size: 24px; margin-bottom: 10px; }
                .info { 
                    background: #f0f7ff; 
                    color: #1976d2; 
                    padding: 20px; 
                    border-radius: 8px; 
                    margin-bottom: 20px;
                    border-left: 4px solid #1976d2;
                    line-height: 1.6;
                }
                .info strong { display: block; font-size: 16px; margin-bottom: 10px; }
                .info ul { margin-left: 20px; }
                .info li { margin: 8px 0; }
                .button-group { 
                    display: flex; 
                    gap: 10px;
                    justify-content: center;
                    margin-top: 20px;
                }
                a { 
                    color: white; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    text-decoration: none; 
                    font-weight: 600;
                    padding: 12px 24px;
                    border-radius: 6px;
                    display: inline-block;
                    transition: transform 0.2s;
                }
                a:hover { 
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                .note {
                    background: #fff3cd;
                    color: #856404;
                    padding: 15px;
                    border-radius: 6px;
                    border-left: 4px solid #ffc107;
                    margin-top: 20px;
                    font-size: 14px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success">
                    <h2>✅ Gym Trainer Started!</h2>
                    <p>A new window is opening with your AI Gym Trainer...</p>
                </div>
                <div class="info">
                    <strong>🎮 Controls:</strong>
                    <ul>
                        <li><strong>1</strong> - Push-ups mode</li>
                        <li><strong>2</strong> - Squats mode</li>
                        <li><strong>3</strong> - Plank mode</li>
                        <li><strong>Q</strong> - Quit application</li>
                    </ul>
                </div>
                <div class="note">
                    <strong>📸 Camera Window:</strong> If the camera window doesn't appear in a few seconds, 
                    check that you've allowed camera access. The window should open in a new console.
                </div>
                <div class="button-group">
                    <a href='/gym'>⬅ Back to Gym Trainer</a>
                    <a href='/' style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">🏠 Home</a>
                </div>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[GYM TRAINER ERROR] {error_details}")
        return f"""
        <html>
        <head>
            <title>Error - Gym Trainer</title>
            <meta charset="UTF-8">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Poppins', sans-serif; 
                    padding: 40px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .container {{ 
                    max-width: 600px; 
                    width: 100%;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    padding: 40px;
                }}
                .error {{ 
                    color: white; 
                    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                    padding: 20px; 
                    border-radius: 8px;
                    margin-bottom: 20px;
                    text-align: center;
                }}
                .error h2 {{ font-size: 24px; margin-bottom: 10px; }}
                .error-details {{ 
                    background: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 6px;
                    border-left: 4px solid #e74c3c;
                    margin-bottom: 20px;
                    overflow-x: auto;
                }}
                .error-details pre {{ 
                    font-size: 12px; 
                    color: #c0392b;
                    font-family: 'Courier New', monospace;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}
                a {{ 
                    color: white; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    text-decoration: none; 
                    font-weight: 600;
                    padding: 12px 24px;
                    border-radius: 6px;
                    display: inline-block;
                    transition: transform 0.2s;
                }}
                a:hover {{ 
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="error">
                    <h2>❌ Error Starting Gym Trainer</h2>
                </div>
                <div class="error-details">
                    <strong>Error Details:</strong>
                    <pre>{error_details}</pre>
                </div>
                <p style="margin-bottom: 20px; color: #555;">
                    <strong>💡 Troubleshooting:</strong><br>
                    1. Make sure all required libraries are installed (opencv-python, mediapipe, numpy)<br>
                    2. Ensure your camera is connected and not in use by another application<br>
                    3. Try restarting the application
                </p>
                <a href='/gym'>⬅ Back to Gym Trainer</a>
            </div>
        </body>
        </html>
        """

@app.route("/finance")
def finance():
    # Finance & Healthcare Services
    services = {
        "insurance": {
            "title": "Health Insurance & Subscriptions",
            "description": "Trusted health insurance plans to protect you and your family",
            "icon": "💳",
            "links": [
                {"name": "PolicyBazaar", "url": "https://www.policybazaar.com/health-insurance/"},
                {"name": "Arogya World", "url": "https://www.arogya.com/"},
                {"name": "Care Health Insurance", "url": "https://www.careinsurance.com/"}
            ]
        },
        "fundraising": {
            "title": "Medical Fundraising",
            "description": "Connect to verified fundraising platforms for medical expenses",
            "icon": "🤝",
            "links": [
                {"name": "Ketto", "url": "https://www.ketto.org/"},
                {"name": "Give India Medical", "url": "https://www.giveindia.org/medical-healthcare"},
                {"name": "ImpactGuru", "url": "https://www.impactguru.com/"}
            ]
        },
        "medicines": {
            "title": "Medicine Orders",
            "description": "Order medicines online from trusted platforms",
            "icon": "💊",
            "links": [
                {"name": "Tata 1mg", "url": "https://www.1mg.com/"},
                {"name": "PharmEasy", "url": "https://www.pharmeasy.in/"},
                {"name": "Medlife", "url": "https://www.medlifestore.com/"}
            ]
        }
    }
    return render_template("finance.html", services=services)


@app.route("/emergency")
def emergency_services():
    emergency_info = {
        "primary": "112",
        "services": [
            {"name": "Ambulance", "number": "102", "icon": "🚑"},
            {"name": "Police", "number": "100", "icon": "🚔"},
            {"name": "Fire", "number": "101", "icon": "🔥"},
            {"name": "National Helpline", "number": "1075", "icon": "☎️"}
        ]
    }
    return render_template("emergency.html", emergency_info=emergency_info)

@app.route("/article/<topic>")
def get_article(topic):
    if topic in articles:
        return jsonify(articles[topic])
    return jsonify({"title": "Not Found", "content": "Article not available."}), 404

if __name__ == "__main__":
    app.run(debug=True, port=8080)