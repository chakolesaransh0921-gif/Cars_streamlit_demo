import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Load dataset
df = pd.read_csv("../DataSets/CARS.csv")

# Streamlit title
st.title("Car Brand Horsepower Visualization")

# Show available brands
brands = df["Make"].unique()
brand = st.selectbox("Select a Brand", brands)

# Filter data based on brand
filtered = df[df["Make"] == brand]

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
sb.barplot(x="Model", y="Horsepower", data=filtered, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)
