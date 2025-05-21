## 🔍 Project Overview: **AI-Powered Real-Time Weapon Detection and Alert System**

### 🎯 Objective

This project demonstrates a **real-time AI surveillance system** capable of detecting weapons (specifically knives and machetes) using a webcam feed and sending instant alerts via **WhatsApp**, complete with image snapshots. It aims to improve home security, offering a low-cost but intelligent early warning solution for threat detection in domestic settings, particularly in Benin City, Nigeria.

---

## ⚙️ Project Workflow

### 1. **Model Training (Offline Phase)**

* A **convolutional neural network (CNN)** was trained to classify two weapon categories: **Knife** and **Machete**.
* The dataset consisted of 100+ labeled images per class.
* The trained model was saved as `weapon_detector.keras`.

---

### 2. **Real-Time Detection Pipeline (Runtime Phase)**

#### ✅ Input:

* Live video feed from webcam (configured using OpenCV).

#### 📦 Preprocessing:

* Each frame is resized and normalized to fit the model's expected input.
* Frame is converted from BGR to RGB before prediction.

#### 🤖 Prediction:

* The model outputs class probabilities.
* The class with the highest confidence is selected.
* If confidence exceeds the set **threshold (89%)**, it is considered a positive detection.

#### 🟩 On-Screen Feedback:

* Detected class and confidence score are overlaid on the live feed using bounding boxes and text.

---

### 3. **Alerting Mechanism**

#### 🧠 Cooldown Logic:

* To prevent alert spam, a **cooldown window** of **5 minutes** is enforced between alerts.

#### 📸 Snapshot:

* If a weapon is detected with high confidence, a **snapshot is taken** and saved locally in a `snapshots/` folder.

#### ☁️ Upload to Cloud:

* The image is uploaded to **ImgBB** using its API.
* The link to the image is retrieved.

#### 📲 WhatsApp Alert:

* A formatted WhatsApp message is sent to a **pre-configured number** using the **CallMeBot API**.
* The message includes:

  * ⚠️ Alert notice
  * ✅ Detected weapon type
  * 📊 Confidence level
  * 🕐 Detection time
  * 🔗 Snapshot URL

#### 📩 Sample Message:

```
⚠️ A weapon has been detected in your home in Benin City, Nigeria
– Type: Machete
– Confidence: 99.3%
– Time: 09:53 AM
🔗 Snapshot: https://ibb.co/xyz
```

---

## 🛡️ Key Features

| Feature                  | Description                                                 |
| ------------------------ | ----------------------------------------------------------- |
| 🎥 Live Detection        | Constant frame analysis using webcam feed                   |
| 🧠 Intelligent Threshold | Custom confidence threshold to reduce false positives       |
| 📸 Snapshot System       | Captures and stores evidence of each detection              |
| ☁️ Cloud Upload          | Uploads image securely to ImgBB                             |
| 📲 WhatsApp Alerts       | Sends real-time alert messages to a configured phone number |
| ⏲️ Cooldown Logic        | Prevents repetitive alerts within a short time window       |

---

## 🌐 Technologies Used

* **Python**
* **TensorFlow/Keras**
* **OpenCV**
* **Requests (for APIs)**
* **CallMeBot API** (WhatsApp)
* **ImgBB API** (Image hosting)

---

## 📌 Real-World Applications

* Home and small office security
* Remote surveillance systems
* Real-time alerting in smart IoT environments
* Community watch integrations

---

## 🧠 Next Steps (Optional Enhancements)

* Add support for **multiple weapon types**.
* Send **SMS or email alerts** as backup.
* Integrate with **IoT devices** (e.g., auto-door locks or alarms).
* Add **GUI interface** using Streamlit or Tkinter.
* Export detection logs to CSV or a database.

---

## 🧑‍💼 Stakeholder Summary

This solution provides a **cost-effective, AI-driven home security system** using commodity hardware (webcam + PC) and free tools (WhatsApp, imgbb). It offers a practical, real-world use case for AI in community safety and smart home automation.

