import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Descriptive Data Analysis", layout="wide")

# Title
st.title("Montly Household Income & Expenditure Data Explorer")

# File uploader
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Load dataset
    df = pd.read_csv(uploaded_file)

    # Dataset Preview 
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    # ---------------- Missing values check ----------------
    st.subheader("❓ Missing Values Check")
    st.write(df.isnull().sum())

    # ---------------- Dataset info ----------------
    st.subheader("🔎 Dataset Info")
    st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    st.write("**Columns:**", list(df.columns))

    # ---------------- Summary statistics ----------------
    st.subheader("📈 Summary Statistics")
    st.write(df.describe())

    # ---------------- Monthly Household Expense Insights ----------------
    st.subheader("🏠 Monthly Household Expense Insights")
    mean_expense = df["Mthly_HH_Expense"].mean()
    median_expense = df["Mthly_HH_Expense"].median()
    mode_expense = df["Mthly_HH_Expense"].mode()[0]
    mode_count = (df["Mthly_HH_Expense"] == mode_expense).sum()

    st.write(f"**Mean Monthly Household Expense:** {mean_expense:.2f}")
    st.write(f"**Median Monthly Household Expense:** {median_expense:.2f}")
    st.write(f"**Most Frequent Expense (Mode):** {mode_expense}  _(appears {mode_count} times)_")

    # Histogram with mean, median, and mode
    fig, ax = plt.subplots()
    df["Mthly_HH_Expense"].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
    ax.axvline(mean_expense, color="red", linestyle="dashed", linewidth=2, label=f"Mean: {mean_expense:.2f}")
    ax.axvline(median_expense, color="green", linestyle="dashed", linewidth=2, label=f"Median: {median_expense:.2f}")
    ax.axvline(mode_expense, color="blue", linestyle="dashed", linewidth=2, label=f"Mode: {mode_expense}")
    ax.set_title("Distribution of Monthly Household Expenses")
    ax.set_xlabel("Monthly Expense")
    ax.set_ylabel("Frequency")
    ax.legend()
    st.pyplot(fig)

    # ---------------- Highest Qualified Member Distribution ----------------
    st.subheader("🎓 Highest Qualified Member Distribution")
    fig, ax = plt.subplots()
    df["Highest_Qualified_Member"].value_counts().plot(kind="bar", ax=ax, color="purple", edgecolor="black")
    ax.set_title("Highest Qualification Distribution")
    st.pyplot(fig)

    # ---------------- Monthly Income vs Expenses ----------------
    st.subheader("📊 Monthly Income vs Expenses")
    st.line_chart(df[["Mthly_HH_Income", "Mthly_HH_Expense"]])

    # ---------------- Standard deviation (first 5 columns) ----------------
    st.subheader("📏 Standard Deviation (First 5 Columns)")
    st.write(df.iloc[:, :5].std(numeric_only=True))

    # ---------------- Variance (first 4 columns) ----------------
    st.subheader("📐 Variance (First 4 Columns)")
    st.write(df.iloc[:, :4].var(numeric_only=True))

    # ---------------- Earning Member Distribution ----------------
    st.subheader("👨‍👩‍👧 Earning Member Distribution")
    fig, ax = plt.subplots()
    df["No_of_Earning_Members"].value_counts().plot(kind="bar", ax=ax, color="teal", edgecolor="black")
    ax.set_title("Earning Member Distribution")
    st.pyplot(fig)

    # ---------------- Correlation heatmap ----------------
    st.subheader("🔥 Correlation Heatmap")
    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        corr = numeric_df.corr()
        st.write(corr)

        fig, ax = plt.subplots()
        cax = ax.matshow(corr, cmap="coolwarm")
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)
        fig.colorbar(cax)
        st.pyplot(fig)
