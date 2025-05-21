import cv2
import numpy as np
import tensorflow as tf
import os
import sys
import requests
import datetime
import time

# ===================== CONFIGURATION =====================
MODEL_FILE = "weapon_detector.keras"
CLASS_LABELS = ['Knife', 'Machete']
CAMERA_INDEX = 0
WHATSAPP_NUMBER = '2347059244477'
CALLMEBOT_API_KEY = '7802560'
IMGBB_API_KEY = 'd27a83f4352c0380a25acded858aa992'
SNAPSHOT_FOLDER = "snapshots"
THRESHOLD = 0.89
COOLDOWN_SECONDS = 180  # 3 minutes
# ========================================================

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Create snapshot folder if it doesn't exist
os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)

def load_model_with_retry(model_path):
    possible_paths = [
        model_path,
        os.path.join(os.getcwd(), model_path),
        os.path.join(os.path.expanduser('~'), 'Downloads', model_path),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Loading model from: {path}")
            return tf.keras.models.load_model(path)
    raise FileNotFoundError("Model not found.")

def upload_image_to_imgbb(image_path):
    with open(image_path, "rb") as file:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": IMGBB_API_KEY},
            files={"image": file}
        )
    if response.status_code == 200:
        return response.json()["data"]["url"]
    else:
        return None

def send_whatsapp_alert(message):
    url = f"https://api.callmebot.com/whatsapp.php?phone={WHATSAPP_NUMBER}&text={requests.utils.quote(message)}&apikey={CALLMEBOT_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("WhatsApp alert sent successfully.")
        else:
            print("Failed to send WhatsApp alert.")
    except Exception as e:
        print(f"Error sending WhatsApp alert: {e}")

# Load model
try:
    model = load_model_with_retry(MODEL_FILE)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Failed to load model: {e}")
    sys.exit()

# Open webcam
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("Error: Could not access webcam.")
    sys.exit()

is_running = False
last_alert_time = 0

print("Press 's' to START, 'p' to PAUSE, 'q' to QUIT.")

try:
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            is_running = True
            print("Detection started.")
        elif key == ord('p'):
            is_running = False
            print("Detection paused.")

        ret, frame = cap.read()
        if not ret:
            print("Failed to read from webcam.")
            break

        if not is_running:
            cv2.imshow("Weapon Detection", frame)
            continue

        # Detection pipeline
        target_size = model.input_shape[1:3]
        resized = cv2.resize(frame, target_size)
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        input_tensor = np.expand_dims(rgb / 255.0, axis=0)

        preds = model.predict(input_tensor, verbose=0)
        class_id = int(np.argmax(preds))
        confidence = float(np.max(preds))

        label = f"{CLASS_LABELS[class_id]}: {confidence:.1%}"
        color = (0, 255, 0) if confidence >= THRESHOLD else (0, 0, 255)

        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.rectangle(frame, (10, 40), (int(confidence * 200), 60), color, -1)
        cv2.imshow("Weapon Detection", frame)

        # If detection is confident and cooldown passed
        if confidence >= THRESHOLD and time.time() - last_alert_time > COOLDOWN_SECONDS:
            timestamp = datetime.datetime.now().strftime("%I:%M %p")
            filename = f"{CLASS_LABELS[class_id].lower()}_{int(time.time())}.jpg"
            image_path = os.path.join(SNAPSHOT_FOLDER, filename)

            # Save snapshot
            cv2.imwrite(image_path, frame)
            print(f"Snapshot saved: {image_path}")

            # Upload to imgbb
            image_url = upload_image_to_imgbb(image_path)

            if image_url:
                message = (
                    f"⚠️ A weapon has been detected in your home in Benin City, Nigeria\n"
                    f"– Type: {CLASS_LABELS[class_id]}\n"
                    f"– Confidence: {confidence:.1%}\n"
                    f"– Time: {timestamp}\n"
                    f"🔗 Snapshot: {image_url}"
                )
            else:
                message = (
                    f"⚠️ A weapon has been detected in your home in Benin City, Nigeria\n"
                    f"– Type: {CLASS_LABELS[class_id]}\n"
                    f"– Confidence: {confidence:.1%}\n"
                    f"– Time: {timestamp}\n"
                    f"🔗 Snapshot: Upload failed."
                )

            send_whatsapp_alert(message)
            last_alert_time = time.time()

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Resources released.")
