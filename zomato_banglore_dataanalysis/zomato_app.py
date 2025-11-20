import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Zomato Data Analysis", layout="wide")

# ---------------------- RESTAURANT BACKGROUND + WATERMARK ----------------------
st.markdown("""
<style>

/* ----- Full Restaurant Background Image ----- */
.stApp {
    background: url('https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=1500&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* ----- Dark Transparent Overlay for readability ----- */
.stApp:before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.55);
    z-index: 0;
}

/* ----- Glass Effect Container ----- */
.block-container {
    position: relative;
    z-index: 2;
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 15px;
    backdrop-filter: blur(8px);
}

/* ----- ZOMATO Watermark ----- */
.stApp::after {
    content: "ZOMATO";
    position: fixed;
    bottom: 18%;
    right: 5%;
    font-size: 150px;
    font-weight: 900;
    color: rgba(255, 255, 255, 0.07);
    z-index: 1;
    transform: rotate(-15deg);
    pointer-events: none;
}

/* ----- Text Colors White ----- */
h1, h2, h3, h4, h5, h6, p, label {
    color: #ffffff !important;
}

/* Data table background for visibility */
.dataframe {
    background-color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------- TITLE ----------------------
st.title("🍽️ Zomato Data Analysis Dashboard")
st.write("Explore Zomato restaurant dataset with filters & visual insights!")

# ---------------------- FILE UPLOAD ----------------------
uploaded_file = st.file_uploader("Upload your Zomato CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Clean rate column (like "4.1/5")
    if "rate" in df.columns:
        df["rate"] = df["rate"].astype(str).str.replace("/5", "", regex=False)
        df["rate"] = pd.to_numeric(df["rate"], errors="coerce")

    # Drop long unnecessary columns
    drop_cols = ["url", "address", "phone", "menu_item", "dish_liked", "reviews_list"]
    df = df.drop(columns=[i for i in drop_cols if i in df.columns], errors="ignore")

    # ---------------------- SIDEBAR FILTERS ----------------------
    st.sidebar.header("🔍 Apply Filters")

    # Search bar
    search_text = st.sidebar.text_input("🔎 Search Restaurant Name")

    # Location filter
    location_filter = st.sidebar.multiselect(
        "📍 Select Location(s)", df["location"].dropna().unique()
    )

    # Type filter
    type_filter = st.sidebar.multiselect(
        "🍽️ Restaurant Type", df["listed_in(type)"].dropna().unique()
    )

    # Online order filter
    online_filter = st.sidebar.selectbox("📦 Online Order", ["All", "Yes", "No"])

    # Table booking filter
    table_filter = st.sidebar.selectbox("🪑 Table Booking", ["All", "Yes", "No"])

    # Rating slider
    min_rating, max_rating = st.sidebar.slider(
        "⭐ Rating Range", 0.0, 5.0, (0.0, 5.0)
    )

    # ---------------------- APPLY FILTERING ----------------------
    filtered_df = df.copy()

    if search_text:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(search_text, case=False, na=False)
        ]

    if location_filter:
        filtered_df = filtered_df[filtered_df["location"].isin(location_filter)]

    if type_filter:
        filtered_df = filtered_df[filtered_df["listed_in(type)"].isin(type_filter)]

    if online_filter != "All":
        filtered_df = filtered_df[filtered_df["online_order"] == online_filter]

    if table_filter != "All":
        filtered_df = filtered_df[filtered_df["book_table"] == table_filter]

    filtered_df = filtered_df[
        (filtered_df["rate"] >= min_rating) & (filtered_df["rate"] <= max_rating)
    ]

    # ---------------------- FILTERED TABLE ----------------------
    st.subheader("📄 Filtered Restaurant Data")
    st.write(f"Showing **{len(filtered_df)}** restaurants after filtering.")
    st.dataframe(filtered_df)

    # ---------------------- VISUALIZATIONS ----------------------
    st.subheader("📈 Visual Insights")

    # Rating distribution
    if "rate" in filtered_df.columns:
        st.markdown("### ⭐ Rating Distribution")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(filtered_df["rate"].dropna(), bins=20, kde=True, ax=ax)
        st.pyplot(fig)

    # Online order vs rating
    if "online_order" in filtered_df.columns:
        st.markdown("### 📦 Online Order vs Rating")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(x="online_order", y="rate", data=filtered_df, ax=ax)
        st.pyplot(fig)

    # Restaurant type count
    if "listed_in(type)" in filtered_df.columns:
        st.markdown("### 🍕 Top Restaurant Types")
        type_counts = filtered_df["listed_in(type)"].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=type_counts.values, y=type_counts.index, ax=ax)
        st.pyplot(fig)

    # Top 10 locations
    if "location" in filtered_df.columns:
        st.markdown("### 📍 Top 10 Locations")
        loc_counts = filtered_df["location"].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=loc_counts.values, y=loc_counts.index, ax=ax)
        st.pyplot(fig)

else:
    st.info("👆 Upload a Zomato dataset CSV to begin analysis.")
