import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Load dataset
df = pd.read_csv("CARS.csv")

# Title
st.title("🚗 Car Horsepower Visualization")

# Sidebar options
st.sidebar.header("⚙️ Controls")

# Brand selection (multiple allowed)
brands = df["Make"].unique()
selected_brands = st.sidebar.multiselect("Select Brand(s)", brands, default=[brands[0]])

# Sorting option
sort_option = st.sidebar.radio("Sort by:", ["Model (A-Z)", "Horsepower (High → Low)", "Horsepower (Low → High)"])

# Chart type option
chart_type = st.sidebar.radio("Select Chart Type", ["Bar", "Line"])

# Filtered data
filtered = df[df["Make"].isin(selected_brands)]

# Apply sorting
if sort_option == "Model (A-Z)":
    filtered = filtered.sort_values(by="Model")
elif sort_option == "Horsepower (High → Low)":
    filtered = filtered.sort_values(by="Horsepower", ascending=False)
elif sort_option == "Horsepower (Low → High)":
    filtered = filtered.sort_values(by="Horsepower", ascending=True)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

if chart_type == "Bar":
    sb.barplot(x="Model", y="Horsepower", data=filtered, ax=ax, palette="viridis")
elif chart_type == "Line":
    for brand in selected_brands:
        sub = filtered[filtered["Make"] == brand]
        ax.plot(sub["Model"], sub["Horsepower"], marker="o", label=brand)
    ax.legend()

plt.xticks(rotation=90)
st.pyplot(fig)

# Show raw data toggle
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered)
