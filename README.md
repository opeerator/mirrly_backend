# 🧠 Mirrly Backend

This is the backend control system for **Mirrly**, a custom-built humanoid robot designed for child-robot interaction research. The backend runs on a Raspberry Pi 4B and provides real-time control over the robot’s motors, sensors, vision modules, and speech system. It exposes a RESTful API to interface with the companion [Mirrly React Native app](https://github.com/opeerator/mirrly_app) or other client applications.

---

## ⚙️ Features

- 🔧 **Motor Control**
  - Head and neck movement (Dynamixel AX-12A)
  - Hand and shoulder movement (MG90S servo motors)
  - Smooth, coordinated transitions via a central motor module

- 👀 **Computer Vision**
  - Real-time face detection using OpenCV
  - Face tracking and close-face reaction
  - Dual camera handling (left and right eye)

- 🎤 **Speech and Interaction**
  - Speaker control (left/right)
  - Name-calling reaction
  - Integration with ChatGPT (optional)

- 🧭 **Mode Management**
  - Idle, active, and shutdown behavior states
  - Smooth transitions to prevent hardware damage
  - Randomized idle motion and reactive engagement mode

- 🌐 **REST API**
  - Lightweight Flask server
  - Serves endpoints for all controls (motors, vision, speech, sensors)
  - CORS-enabled for mobile and web apps

---

## 🛠️ Architecture

- **Language**: Python 3
- **Platform**: Raspberry Pi 4B with Raspbian OS
- **Libraries & Tools**:
  - `Flask` – REST API server
  - `OpenCV` – Real-time face/object detection
  - `pigpio` – Stable PWM control for servo motors
  - `dynamixel_sdk` – For controlling Dynamixel AX-12A motors
  - `multiprocessing`, `threading` – For asynchronous sensor & motor handling
  - `socket`, `os`, `requests` – Various hardware and web integrations

---

## 📁 Project Structure

mirrly_backend/
├── motor/         # Central motor control system
├── vision/        # OpenCV-based vision module
├── speech/        # Speaker/audio system integration
├── sensors/       # TOF & ultrasonic sensor handling
├── modes/         # Robot state manager
├── api/           # Flask routes
├── utils/         # Shared utilities and helpers
├── main.py        # Entry point
└── requirements.txt  # Dependencies

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/opeerator/mirrly_backend.git
   cd mirrly_backend
2. Install Dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
3. Run pigpiod:
   ```bash
   sudo pigpiod
4. Run main:
  ```bash
  python main.py

