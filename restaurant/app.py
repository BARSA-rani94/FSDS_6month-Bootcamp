# app.py
import streamlit as st
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ---------------- Load model & vectorizer ----------------
model = pickle.load(open("restaurant_review.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------- CSS Styling with Background ----------------
st.markdown("""
    <style>
    /* Background Image */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)),
                    url('https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1d/30/54/b2/bidri-ambience.jpg?w=1200&h=800&s=1');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }

    /* Glass effect container */
    .glass-box {
        background: rgba(255, 255, 255, 0.10);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 45px;
        max-width: 700px;
        margin: 80px auto;
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4);
        color: #fff;
    }

    /* Title & subtitle with glow */
    .main-title {
        font-size: 44px;
        font-weight: 900;
        text-align: center;
        color: #ffffff;
        text-shadow: 0 0 20px #ff9900, 0 0 10px #ff5500;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .sub-text {
        text-align: center;
        font-size: 18px;
        color: #fff5e6;
        text-shadow: 0 0 10px rgba(255,255,255,0.6);
        margin-bottom: 35px;
    }

    /* Input Text Area */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #ff9900 !important;
        background-color: rgba(255,255,255,0.9) !important;
        color: #222 !important;
        font-size: 16px !important;
        padding: 15px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    /* Button styling */
    .stButton>button {
        background-color: #ff7b00;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 35px;
        font-size: 18px;
        font-weight: 600;
        transition: 0.3s ease;
        box-shadow: 0 0 15px rgba(255,123,0,0.6);
    }
    .stButton>button:hover {
        background-color: #ffa733;
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(255,153,0,0.9);
    }

    /* Result box highlight */
    .result-box {
        text-align: center;
        font-size: 22px;
        margin-top: 30px;
        border-radius: 15px;
        padding: 20px;
        font-weight: bold;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.5);
    }
    .positive {
        background: rgba(0,255,100,0.25);
        color: #90ee90;
        text-shadow: 0 0 10px #00ff66;
    }
    .negative {
        background: rgba(255,50,50,0.25);
        color: #ff6666;
        text-shadow: 0 0 10px #ff3333;
    }

    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------- Text Cleaning Function ----------------
def preprocess_review(review):
    ps = PorterStemmer()
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    return ' '.join(review)

# ---------------- Streamlit Frontend ----------------


st.markdown("<h1 class='main-title'>🍽️ Restaurant Sentiment Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Find out if your review is 😍 Positive or 😞 Negative with a single click!</p>", unsafe_allow_html=True)

user_input = st.text_area("✍️ Write your restaurant review:", placeholder="e.g. The biryani was absolutely delicious and the service was fantastic!")

if st.button("🔍 Analyze Sentiment"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a review before analyzing.")
    else:
        cleaned_review = preprocess_review(user_input)
        transformed_review = vectorizer.transform([cleaned_review]).toarray()
        prediction = model.predict(transformed_review)[0]

        if prediction == 1:
            st.markdown("<div class='result-box positive'>✅ Positive Review — Great Experience! 😄</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-box negative'>❌ Negative Review — Needs Improvement 😔</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
