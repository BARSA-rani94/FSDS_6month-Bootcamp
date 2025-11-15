import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import base64

# ------------------------------
# 🎨 Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Mood Classifier 😊",
    page_icon="😊",
    layout="centered"
)

# ------------------------------
# 🖼️ Background Image Setup
# ------------------------------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    page_bg = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

# 👉 Add your background image (make sure it's in the same folder)
add_bg_from_local("v953-mynt-59.jpg")   # e.g. a nice blurred gradient or emotion theme

# ------------------------------
# 🧠 Load Trained Model
# ------------------------------
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("cnn_mood_model.h5")  # Make sure this file is present
    return model

model = load_model()

# ------------------------------
# 🌟 App Title and Description
# ------------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #00008B;'>😊 Mood Classification App</h1>
    <p style='text-align: center; color: #006400; font-size: 18px;'>
        Upload a face image to detect if the person looks <b>Happy</b> or <b>Sad</b>.
    </p>
    """,
    unsafe_allow_html=True
)


# ------------------------------
# 📷 Image Upload
# ------------------------------
uploaded_file = st.file_uploader("Upload a Face Image", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # Display uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

    # ------------------------------
    # 🔍 Preprocess Image
    # ------------------------------
    img = img.resize((200, 200))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 200.0   # Rescale same as training

    # ------------------------------
    # 🤖 Prediction
    # ------------------------------
    prediction = model.predict(img_array)[0][0]

    # ------------------------------
    # 💬 Display Result
    # ------------------------------
    if prediction < 0.5:
        st.success("😊 **Mood: Happy!** 🎉")
    else:
        st.error("😢 **Mood: Sad!** 💔")

    st.write(f"**Model confidence:** {float(abs(prediction - 0.5) * 2):.2f}")

else:
    st.info("⬆️ Please upload a face image to analyze mood.")
