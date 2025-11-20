import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Color Detection App", layout="wide")


gradient_style = """
<style>
/* Full Page Gradient Background */
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298, #5f93e8);
    background-attachment: fixed;
}

/* Translucent white container */
.block-container {
    background: rgba(255, 255, 255, 0.15);
    padding: 2rem;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}
</style>
"""
st.markdown(gradient_style, unsafe_allow_html=True)


st.markdown("<h1 style='text-align:center; color:white;'>🎨 Color Detection App</h1>", unsafe_allow_html=True)


st.sidebar.header("Select Color to Detect")
choice = st.sidebar.radio(
    "Choose a color",
    ("Red", "Green", "Blue", "All Colors"),
    index=0
)


COLOR_RANGES = {
    "Red": ([161, 155, 84], [179, 255, 255]),
    "Green": ([40, 70, 70], [80, 255, 255]),
    "Blue": ([94, 80, 2], [126, 255, 255]),
    "All Colors": ([0, 42, 0], [179, 255, 255])
}

low, high = COLOR_RANGES[choice]
low = np.array(low)
high = np.array(high)

start = st.button("Start Camera")
stop = st.button("Stop Camera")

frame_placeholder = st.empty()
result_placeholder = st.empty()

if start:
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("⚠️ Failed to access webcam")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, low, high)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        frame_placeholder.image(frame_rgb, channels="RGB", caption="Live Webcam")
        result_placeholder.image(result_rgb, channels="RGB", caption=f"{choice} Detection")

        if stop:
            cap.release()
            break
