import streamlit as st
import cv2
import numpy as np
import tempfile
import os

st.set_page_config(
    page_title="AI Vision Suite",
    page_icon="🎥",
    layout="wide"
)


st.markdown("""
    <h1 style="text-align:center; color:#4CAF50; font-size:48px;">
        --SMART VISION APP--
    </h1>
    <p style="text-align:center; font-size:20px; color:#555;">
        All your detection models — in one clean dashboard
    </p>
""", unsafe_allow_html=True)


st.sidebar.markdown("""
    <h2 style="color:#4CAF50;">⚙️ Select Task</h2>
""", unsafe_allow_html=True)

task = st.sidebar.radio(
    "",
    [
        "📸 Face Detection (Image)",
        "👁️ Face + Eye Detection (Image)",
        "🚗 Car Detection (Video)",
        "🚶 Pedestrian Detection (Video)",
        "🎦 Webcam Face + Eye Detection"
    ]
)


def run_image_detection(img_path, face_xml=None, eye_xml=None):
    img = cv2.imread(img_path)
    if img is None:
        st.error("Unable to load image.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if face_xml:
        face_cascade = cv2.CascadeClassifier(face_xml)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 3)

            if eye_xml:
                eye_cascade = cv2.CascadeClassifier(eye_xml)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)

                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 255), 2)

    st.image(img, channels="BGR", caption="Detection Output")


def run_video_detection(video_path, xml_path):
    cascade = cv2.CascadeClassifier(xml_path)
    cap = cv2.VideoCapture(video_path)
    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = cascade.detectMultiScale(gray, 1.2, 3)

        for (x, y, w, h) in detections:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,200), 3)

        stframe.image(frame, channels="BGR")

    cap.release()


# TASK 1 — FACE DETECTION (IMAGE)


if task == "📸 Face Detection (Image)":
    st.header("📸 Face Detection from Image")

    img_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

    if img_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(img_file.read())
        temp.close()          

        run_image_detection(
            temp.name,
            face_xml=r"C:\Users\HP\Downloads\New folder\haarcascade_frontalface_default.xml"
        )


# TASK 2 — FACE + EYE DETECTION


elif task == "👁️ Face + Eye Detection (Image)":
    st.header("👁️ Face + Eye Detection")

    img_file = st.file_uploader("Upload your Image", type=["jpg", "png"])

    if img_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(img_file.read())
        temp.close()

        run_image_detection(
            temp.name,
            face_xml=r"C:\Users\HP\Downloads\New folder\haarcascade_frontalface_default.xml",
            eye_xml=r"C:\Users\HP\Downloads\New folder\haarcascade_eye.xml"
        )

# TASK 3 — CAR DETECTION

elif task == "🚗 Car Detection (Video)":
    st.header("🚗 Car Detection in Video")

    vid = st.file_uploader("Upload Video", type=["mp4","avi"])
    if vid:
        t = tempfile.NamedTemporaryFile(delete=False)
        t.write(vid.read())

        run_video_detection(
            t.name,
            xml_path=r"C:\Users\HP\Downloads\New folder\13th- Haar cascade classifier\Haarcascades\haarcascade_car.xml"
        )

# TASK 4 — PEDESTRIAN DETECTION

elif task == "🚶 Pedestrian Detection (Video)":
    st.header("🚶 Pedestrian Detection")

    vid = st.file_uploader("Upload Video", type=["mp4","avi"])
    if vid:
        t = tempfile.NamedTemporaryFile(delete=False)
        t.write(vid.read())

        run_video_detection(
            t.name,
            xml_path=r"C:\Users\HP\Downloads\New folder\13th- Haar cascade classifier\Haarcascades\haarcascade_fullbody.xml"
        )

# TASK 5 — WEBCAM DETECTION

elif task == "🎦 Webcam Face + Eye Detection":
    st.header("🎦 Webcam Live Detection")

    start = st.button("Start Webcam")

    if start:
        face = cv2.CascadeClassifier(r"C:\Users\HP\Downloads\New folder\haarcascade_frontalface_default.xml")
        eye = cv2.CascadeClassifier(r"C:\Users\HP\Downloads\New folder\haarcascade_eye.xml")

        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)

                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye.detectMultiScale(roi_gray)

                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            stframe.image(frame, channels="BGR")

        cap.release()
