import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Income & Expenditure Data Explorer")

# File uploader
uploaded_file = st.file_uploader(r"C:\Users\HP\VSCODE_PROJECT\streamlit of stats.py", type=["csv"])    

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    st.subheader("📊 Dataset Preview")
    st.write(df.head())

    # Show basic info
    st.subheader("🔎 Dataset Info")
    st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    st.write("Columns:", list(df.columns))

    # Statistics
    st.subheader("📈 Summary Statistics")
    st.write(df.describe())

    # Select column for visualization
    st.subheader("📊 Column Visualization")
    column = st.selectbox("Select a column to plot:", df.columns)

    if pd.api.types.is_numeric_dtype(df[column]):
        fig, ax = plt.subplots()
        df[column].hist(ax=ax, bins=20)
        ax.set_title(f"Distribution of {column}")
        st.pyplot(fig)
    else:
        st.write(df[column].value_counts())
        fig, ax = plt.subplots()
        df[column].value_counts().plot(kind="bar", ax=ax)
        ax.set_title(f"Frequency of {column}")
        st.pyplot(fig)

    # Correlation heatmap
    st.subheader("🔥 Correlation Heatmap")
    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        st.write(numeric_df.corr())
        fig, ax = plt.subplots()
        cax = ax.matshow(numeric_df.corr(), cmap="coolwarm")
        plt.xticks(range(len(numeric_df.columns)), numeric_df.columns, rotation=90)
        plt.yticks(range(len(numeric_df.columns)), numeric_df.columns)
        fig.colorbar(cax)
        st.pyplot(fig)
