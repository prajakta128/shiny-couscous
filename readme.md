# 🏥 HealthHub – Comprehensive Health & Wellness Platform

> **HealthHub** is a modern, feature-rich healthcare and wellness platform that integrates AI-powered fitness tracking, hospital discovery, government health schemes, and personalized wellness management into a single, user-friendly web application.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-lightblue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Project Overview

HealthHub is designed to simplify access to healthcare information and promote a healthier lifestyle using technology. It combines **AI-based fitness assistance**, **verified healthcare resources**, and **personalized wellness tools** into one cohesive platform.

The project is suitable for:

* Students and academic projects
* Hackathons and demos
* Local healthcare assistance platforms
* AI-integrated web application showcases

---

## 🎯 Core Objectives

* Provide easy access to trusted healthcare information
* Encourage fitness and wellness using AI-based tools
* Centralize hospitals, government schemes, and health topics
* Offer a clean, professional, and user-friendly interface
* Ensure local data processing with privacy in mind

---

## ✨ Key Features

### 🤖 AI Gym Trainer

* Real-time pose detection using **MediaPipe**
* Automatic repetition counting
* Supported exercises:

  * Push-ups
  * Squats
  * Plank (time-based)
* Live camera feed with performance feedback
* Keyboard-based controls for exercise switching

---

### 🏥 Hospital Directory

* 50+ verified hospitals in Pune
* Search by hospital name or locality
* Detailed hospital profiles:

  * Address
  * Contact details
  * Specialties
* One-click calling support

---

### 🏛️ Government Health Schemes

* 20+ Indian government healthcare schemes
* Clear eligibility criteria
* Detailed benefits and coverage
* Simple browsing and filtering

---

### 📚 Health Topics Library

* 100+ curated health and wellness articles
* Categories:

  * Prevention
  * Mental Health
  * Lifestyle
  * Nutrition
* Searchable and easy-to-read content

---

### 💆 Wellness Hub

* Wellness-focused guidance on:

  * Meditation
  * Yoga
  * Nutrition
  * Sleep
  * Stress management
* Practical, easy-to-follow advice

---

### 🔔 Smart Health Reminders

* Create personalized reminders for:

  * Medication
  * Fitness
  * Wellness activities
* Date & time-based alerts
* Audio and visual notifications
* Persistent storage using local JSON files

---

### 🌙 Dark Mode Support

* Fully implemented across all pages
* Eye-friendly UI for night usage
* Smooth and consistent theme design

---

## 🛠️ Technology Stack

### Backend

* **Python 3.8+**
* **Flask** – Web framework
* **JSON** – Lightweight data storage

### Frontend

* **HTML5**, **CSS3**, **JavaScript**
* **Bootstrap 4** – Responsive UI
* **Jinja2** – Template engine

### AI / Computer Vision

* **MediaPipe** – Pose estimation
* **OpenCV (cv2)** – Camera handling
* **NumPy** – Angle and numerical calculations

---

## 📁 Project Structure

```
health_platform-main/
│
├── health_platform/
│   ├── app.py                # Main Flask application
│   ├── gym_trainer.py        # AI gym trainer logic
│   ├── data/                 # JSON data storage
│   ├── templates/            # HTML templates
│   └── static/               # CSS, JS, audio assets
│
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites

* Python 3.8 or higher
* pip package manager
* Webcam (for AI Gym Trainer)

### Steps

```bash
# Navigate to project folder
cd health_platform-main

# Install dependencies
pip install -r requirements.txt

# Run the application
cd health_platform
python app.py
```

Open in browser:

```
http://127.0.0.1:8080
```

---

## 📖 Usage Guide

* **Homepage** – Explore all services via cards
* **AI Gym Trainer** – Launch and perform exercises using webcam
* **Hospitals** – Search and contact hospitals
* **Health Topics** – Read articles and preventive tips
* **Schemes** – Learn about government health programs
* **Reminders** – Set and manage health alerts
* **Wellness Hub** – Improve lifestyle with guided content

---

## 🐛 Troubleshooting

### Camera Not Working

* Ensure webcam is connected
* Close other apps using the camera
* Run `gym_trainer.py` directly to test

### Port Already in Use

* Change the port in `app.py`
* Or stop the process using port 8080

### Reminders Not Triggering

* Enable browser notifications
* Allow audio playback
* Restart the Flask server

---

## 🔐 Privacy & Security

* All data is stored locally
* No personal data is sent to external servers
* Camera feed is processed locally only
* Suitable for offline and demo usage

---

## 📈 Future Enhancements

* More AI exercise detection
* Voice-based AI coaching
* User authentication & profiles
* Cloud database integration
* Mobile-friendly PWA version

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👩‍💻 Author

**Prajakta Kamble**
Computer Engineering Student | AI & Full Stack Developer

---

## ✅ Project Status

✔ Stable
✔ Feature Complete
✔ Ready for Academic / Hackathon Submission

---

**Last Updated:** January 2026
