import streamlit as st
import bcrypt
import os
os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
import cv2
import numpy as np
import face_recognition
import base64
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import gridfs
from bson import ObjectId
from streamlit.components.v1 import html
from dotenv import load_dotenv
load_dotenv()


# ----- MongoDB Config -----
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['student_detail']
users_collection = db['student_data']
attendance_collection = db['attendance_records']
fs = gridfs.GridFS(db)

# ----- Load known faces from MongoDB GridFS -----
@st.cache_resource(show_spinner=False)
def load_known_faces():
    known_encodings = []
    known_names = []

    students = users_collection.find({}, {"name": 1, "Image": 1})
    for student in students:
        name = student.get("name")
        image_id = student.get("Image")
        if not name or not image_id:
            continue
        try:
            image_data = fs.get(ObjectId(image_id)).read()
            np_arr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if img is None:
                continue
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(img_rgb)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(name)
        except Exception as e:
            print(f"Error for {name}: {e}")
    return known_encodings, known_names

# ----- Attendance Logic -----
def get_last_attendance():
    data = {}
    try:
        with open('attendance.csv', 'r') as f:
            lines = f.readlines()[1:]
            for line in lines:
                name, timestamp, status = line.strip().split(',')
                data[name] = (datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'), status)
    except FileNotFoundError:
        with open('attendance.csv', 'w') as f:
            f.write("Name,Time,Status\n")
    return data

def mark_attendance(name):
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')

    data = get_last_attendance()
    last_time, last_status = data.get(name, (None, None))

    if last_time:
        if last_status == "Check-In" and now - last_time < timedelta(minutes=1):
            return False, "Already checked in recently"
        if last_status == "Check-Out" and now - last_time < timedelta(minutes=1):
            return False, "You just checked out. Wait a minute before checking in again."


    status = "Check-Out" if last_status == "Check-In" else "Check-In"

    with open('attendance.csv', 'a') as f:
        f.write(f"{name},{dt_string},{status}\n")

    attendance_collection.insert_one({
        "name": name,
        "time": now,
        "status": status
    })

    return True, f"{status} recorded for {name}"
def get_available_camera_indices(max_index=5):
    available = []
    for index in range(max_index):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # Force stable backend for Windows
        if cap is not None and cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available.append(index)
            cap.release()
    return available


# ----- Main Streamlit App -----
st.set_page_config(page_title="Face Attendance", layout="centered")
st.title("🧑‍🎓AI Attendance System")

# Load face data
with st.spinner("Loading known faces..."):
    known_encodings, known_names = load_known_faces()

# Camera state control
if 'run' not in st.session_state:
    st.session_state.run = False

# Start/Stop buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Camera"):
        st.session_state.run = True
with col2:
    if st.button("⏹️ Stop Camera"):
        st.session_state.run = False

# Camera selection
st.write("📷Select Camera Index")
available_indices = get_available_camera_indices()
selected_camera_index = st.selectbox("Choose Camera Index", available_indices, index=0 if 0 in available_indices else None)

# Add a guard in case no camera is found
if selected_camera_index is None:
    st.error("No working camera found. Please connect a camera.")
    st.stop()

# Webcam display
frame_display = st.empty()
feedback = st.empty()


cap = None
if st.session_state.run:
    cap = cv2.VideoCapture(selected_camera_index, cv2.CAP_DSHOW)

# Message display tracker
last_feedback = {"message": None, "type": None}
while st.session_state.run and cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)

        if len(face_distances) == 0:
            continue

        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]
            success, msg = mark_attendance(name)
            color = (0, 255, 0) if success else (0, 0, 255)


            if last_feedback["message"] != msg or last_feedback["type"] != ("success" if success else "warning"):
                if success:
                    feedback.markdown(f"✅ **{msg}**", unsafe_allow_html=True)
                    last_feedback.update({"message": msg, "type": "success"})

                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    action = "checked in" if "Check-In" in msg else "checked out"
                    emoji = "🎉" if "Check-In" in msg else "👋"
                    color = "#28a745" if "Check-In" in msg else "#007bff"

                    # Show animated welcome popup for both Check-In and Check-Out
                    welcome_animation = f"""
                    <div id="overlay" style="
                        position:fixed;
                        top:0; left:0;
                        width:100%;
                        height:100%;
                        background:linear-gradient(135deg, #f0f9ff, #d4fcf4);
                        z-index:9999;
                        display:flex;
                        justify-content:center;
                        align-items:center;
                        animation: fadein 0.5s;
                    ">
                        <div style="
                            text-align:center;
                            background-color:white;
                            padding:40px;
                            border-radius:20px;
                            box-shadow:0 0 20px rgba(0,0,0,0.3);
                            animation: slideIn 1s ease;
                        ">
                            <h1 style="color:{color};">{emoji} <b>{name}</b> just {action}!</h1>
                            <h3 style="margin-top:10px;">🕒 {now}</h3>
                            <p style="color:#555;">Thank you for using our system! 🚀</p>
                        </div>
                    </div>

                    <script>
                        setTimeout(function() {{
                            var overlay = document.getElementById('overlay');
                            if (overlay) {{
                                overlay.style.transition = 'opacity 1s';
                                overlay.style.opacity = '0';
                                setTimeout(function() {{ overlay.remove(); }}, 1000);
                            }}
                        }}, 8000);
                    </script>

                    <style>
                        @keyframes fadein {{
                            from {{ opacity: 0; }}
                            to {{ opacity: 1; }}
                        }}
                        @keyframes slideIn {{
                            from {{
                                transform: translateY(-50px);
                                opacity: 0;
                            }}
                            to {{
                                transform: translateY(0);
                                opacity: 1;
                            }}
                        }}
                    </style>
                    """
                    html(welcome_animation, height=500)

                else:
                    feedback.markdown(f"⚠️ **{msg}**", unsafe_allow_html=True)
                    last_feedback.update({"message": msg, "type": "warning"})



        else:
            name = "Unknown"
            if last_feedback["message"] != "Face not recognized" or last_feedback["type"] != "error":
                feedback.markdown("❌ **Face not recognized**", unsafe_allow_html=True)
                last_feedback.update({"message": "Face not recognized", "type": "error"})


        # Draw box and label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    frame_display.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

if not st.session_state.run:
    if cap is not None and cap.isOpened():
        cap.release()


# ----- Admin Secure CSV Download Section -----
admin_collection = db['admin_credentials']
stored_admin = admin_collection.find_one({"username": "admin"})

st.sidebar.title("🔐 Secure CSV Download")

csv_password = st.sidebar.text_input("Enter admin password", type="password")
download_ready = False

if csv_password and stored_admin:
    hashed_pw = stored_admin.get("password_hash")
    if bcrypt.checkpw(csv_password.encode(), hashed_pw.encode()):
        st.sidebar.success("✅ Password verified!")
        download_ready = True
    else:
        st.sidebar.warning("❌ Incorrect password")

if download_ready:
    try:
        with open("attendance.csv", "rb") as file:
            st.sidebar.download_button(
                label="📥 Download Attendance CSV",
                data=file,
                file_name="attendance.csv",
                mime="text/csv"
            )
    except FileNotFoundError:
        st.sidebar.error("❗ attendance.csv not found. No records yet.")
