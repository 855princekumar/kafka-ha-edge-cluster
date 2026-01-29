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

# ========== ACTUAL CONSUMER CODE BELOW ==========
import cv2
import numpy as np
from kafka import KafkaConsumer

BROKERS = ["192.168.1.26:9092","192.168.1.27:9092","192.168.1.28:9092"]
TOPIC = "D1Cam"

print("Connecting to Kafka...")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKERS,
    auto_offset_reset="latest",
    enable_auto_commit=True
)

print("Waiting for frames... Press Q to exit")

for msg in consumer:
    arr = np.frombuffer(msg.value, np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        continue

    cv2.imshow("Kafka Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

consumer.close()
cv2.destroyAllWindows()
