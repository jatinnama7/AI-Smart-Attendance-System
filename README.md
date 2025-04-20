<h1 align="center">🎓 AI-Based Face Recognition Attendance System</h1>

<p align="center">
  <img src="https://img.shields.io/github/languages/top/jatinnama7/AI-Smart-Attendance-System?style=for-the-badge&color=blueviolet" />
  <img src="https://img.shields.io/github/stars/jatinnama7/AI-Smart-Attendance-System?style=for-the-badge&color=yellow" />
  <img src="https://img.shields.io/github/forks/jatinnama7/AI-Smart-Attendance-System?style=for-the-badge&color=brightgreen" />
  <img src="https://img.shields.io/github/license/jatinnama7/AI-Smart-Attendance-System?style=for-the-badge&color=orange" />
  <img src="https://img.shields.io/badge/Made%20With-💖-red?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-UI%2FUX%20App-ff4b4b?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/OpenCV-Face%20Detection-5C3EE8?style=for-the-badge&logo=opencv" />
  <img src="https://img.shields.io/badge/MongoDB-Storage-47A248?style=for-the-badge&logo=mongodb" />
  <img src="https://img.shields.io/badge/Face_Recognition-Model-blueviolet?style=for-the-badge" />
</p>

---

> 📸 A real-time attendance system powered by face recognition, MongoDB GridFS storage, and animated Streamlit UI/UX. Designed for seamless check-in/out with admin-secured CSV download and intuitive user experience.

---

## 🚀 Features

✅ Real-Time Face Detection and Recognition  
✅ Animated Popups for Check-In / Check-Out  
✅ GridFS-based Image Storage in MongoDB  
✅ Secure Admin Panel with CSV Download  
✅ Multi-Camera Support  
✅ Emoji-enhanced Interface and Clean UI  
✅ One-click Streamlit Deployment

---

## 📺 Demo Preview

> ✨ _Live check-in/out animations and message popups!_  
> 🎥 Real-time webcam integration with OpenCV  
> 🔒 Password-protected admin download zone

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzlkMzE2ZTQxMzFiN2FiM2MwMzljMDNjYTZkNTY5YzU4ZmVhZWY2YiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/rAIpeNskWfE6wvWyZG/giphy.gif" width="70%" />
</p>
<br>
<br>

## 🖼️ Project Snapshots

<p align="center">
  <img src="demo_images/dashboard.png" alt="👁️ Real-Time Face Detection" width="60%" />
  &nbsp;&nbsp;

<p align="center">
  <b>👁️ Real-Time Face Detection</b> &nbsp;&nbsp;&nbsp;&nbsp;
</p>
<br>
<p align="center">
  <img src="demo_images/secure.jpg" alt="🔐 Admin Panel with CSV Export" width="60%" />
  &nbsp;&nbsp;


<p align="center">
  <b>🔐 Admin Panel with CSV Export</b> &nbsp;&nbsp;&nbsp;&nbsp; 
</p>
<br>
<p align="center">
  <img src="demo_images/UI.jpg" alt="🎉 Animated Check-in/Check-out Popup" width="60%" />
  &nbsp;&nbsp;


<p align="center">
  <b>🎉 Animated Check-in/Check-out Popup</b> &nbsp;&nbsp;&nbsp;&nbsp; 
</p>

---

## 📁 Folder Structure

```bash
📦AI-Smart-Attendance-System
 ┣ 📄 app.py
 ┣ 📄 .env
 ┣ 📄 requirements.txt
 ┣ 📄 attendance.csv
 ┗ 📄 README.md

```

---

## 🧠 How It Works

1. 🔍 Loads face encodings from MongoDB using GridFS.
2. 🎥 Captures live video with OpenCV.
3. 🧬 Matches detected faces using `face_recognition`.
4. 📅 Applies logic for check-in/check-out (1-min buffer).
5. 📤 Triggers popup animations on events.
6. 📝 Logs attendance in a CSV file.
7. 🛡️ Provides admin-only panel to download the report.

---

## ⚙️ Quick Start Guide

### 1. Clone the Repository

```bash
git clone https://github.com/jatinnama7/AI-Smart-Attendance-System.git
cd AI-Smart-Attendance-System
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file:

```env
MONGO_URI=mongodb+srv://your_user:your_pass@cluster.mongodb.net/?retryWrites=true&w=majority
```

> ✅ Ensure MongoDB has:
>
> - `student_data`
> - `attendance_records`
> - `admin_credentials` collections
> - GridFS support enabled

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

---

## 🔐 Admin Access

Only users with admin credentials can access the CSV download section.

> 🔑 Store hashed passwords in MongoDB `admin_credentials` collection:

```json
{
  "username": "admin",
  "password_hash": "$2b$12$abcdefghijk1234567890hashedvalue"
}
```

Use this to hash:

```python
import bcrypt
print(bcrypt.hashpw("yourpassword".encode(), bcrypt.gensalt()).decode())
```

---

## ✨ UI/UX Highlights

| Feature             | Description                   |
| ------------------- | ----------------------------- |
| 🧠 Face Recognition | Fast, reliable & accurate     |
| 🎨 Animations       | Colorful popups & emoji icons |
| 🧰 MongoDB + GridFS | Efficient image handling      |
| 📷 Real-time Video  | Smooth OpenCV camera feed     |
| 🔒 Admin Security   | Password-protected access     |

---

## 👨‍💻 Tech Stack

- **Frontend/UI**: Streamlit, HTML/CSS (within Streamlit)
- **Backend**: Python, OpenCV, face_recognition
- **Database**: MongoDB Atlas + GridFS
- **Security**: Bcrypt password hashing

---

## 🙌 Contributing

Contributions are welcome!  
Feel free to submit a PR or open an issue 💬

```bash
git checkout -b feature/AmazingFeature
git commit -m "Add AmazingFeature"
git push origin feature/AmazingFeature
```

---

## ✉️ Contact

Made with ❤️ by **Jatin**

- 📧 Email: jatinnama7@gmail.com
- 💬 GitHub: [github.com/jatinnama7]

---

## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full info.

---

> ⭐ If you like this project, don't forget to **star** it and share the love!

<p align="center">
  <img src="https://img.shields.io/github/stars/jatinnama7/AI-Smart-Attendance-System?style=social" />
</p>
```

---
