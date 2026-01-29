import os
import sys
import subprocess
import venv

VENV_DIR = "venv"

def in_venv():
    return sys.prefix != sys.base_prefix

def setup_venv():
    print("Creating virtual environment...")
    venv.create(VENV_DIR, with_pip=True)

def install_packages():
    pip = os.path.join(VENV_DIR, "Scripts" if os.name=="nt" else "bin", "pip")
    subprocess.check_call([pip, "install", "kafka-python", "opencv-python", "numpy"])

def relaunch():
    python = os.path.join(VENV_DIR, "Scripts" if os.name=="nt" else "bin", "python")
    os.execv(python, [python] + sys.argv)

if not in_venv():
    if not os.path.exists(VENV_DIR):
        setup_venv()
        install_packages()
    relaunch()

# ========== ACTUAL PRODUCER CODE BELOW ==========
import cv2
import time
from kafka import KafkaProducer

BROKERS = ["192.168.1.26:9092","192.168.1.27:9092","192.168.1.28:9092"]
TOPIC = "D1Cam"
SOURCE = 0
FPS_DELAY = 0.03

print("Connecting to Kafka...")
producer = KafkaProducer(
    bootstrap_servers=BROKERS,
    max_request_size=10485760,
    retries=5
)

print("Opening camera...")
cap = cv2.VideoCapture(SOURCE, cv2.CAP_DSHOW if os.name=="nt" else cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Camera failed")
    sys.exit()

print("Producer running... CTRL+C to stop")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera error")
            break

        _, buffer = cv2.imencode(".jpg", frame)
        producer.send(TOPIC, buffer.tobytes())
        time.sleep(FPS_DELAY)

except KeyboardInterrupt:
    pass
finally:
    cap.release()
    producer.flush()
    producer.close()
