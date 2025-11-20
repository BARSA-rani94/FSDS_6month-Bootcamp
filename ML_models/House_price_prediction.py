# House Price Prediction App using Streamlit and Linear Regression

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


# Title
st.title("House Price Prediction App")

# Load dataset
dataset = pd.read_csv(r"C:\Users\HP\Downloads\New folder\22nd, 23rd- slr\22nd, 23rd- slr\SLR - House price prediction\House_data.csv")

# Feature and target
x = dataset['sqft_living'].values.reshape(-1,1)
y = dataset['price'].values

# Split and train model
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=0)
regressor = LinearRegression()
regressor.fit(x_train, y_train)

# R2 score
r2_test = regressor.score(x_test, y_test)
st.write(f"R2 score on test set: {r2_test:.3f}")

# Input from user
house_size = st.number_input("Enter house size (sqft):", min_value=100, max_value=100000, value=1000)

# Predict price
predicted_price = regressor.predict(np.array([[house_size]]))
st.write(f"Predicted price for a house of {house_size} sqft is: ${predicted_price[0]:,.2f}")

# Plotting training data and regression line
fig, ax = plt.subplots()
ax.scatter(x_train, y_train, color='red', alpha=0.5, label='Training data')
ax.plot(x_train, regressor.predict(x_train), color='blue', linewidth=2, label='Regression line')
ax.set_xlabel("Space (sqft)")
ax.set_ylabel("Price")
ax.set_title("Training Set: Space vs Price")
ax.legend()
st.pyplot(fig)

# Optional: plot test data as well
fig2, ax2 = plt.subplots()
ax2.scatter(x_test, y_test, color='green', alpha=0.5, label='Test data')
ax2.plot(x_train, regressor.predict(x_train), color='blue', linewidth=2, label='Regression line')
ax2.set_xlabel("Space (sqft)")
ax2.set_ylabel("Price")
ax2.set_title("Test Set: Space vs Price")
ax2.legend()
st.pyplot(fig2)