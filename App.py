import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import plotly.express as px

# Load dataset
df = pd.read_csv("CARS.csv")

# Streamlit Page Config
st.set_page_config(page_title="Car Horsepower Dashboard 🚗", layout="wide")

# Title
st.markdown(
    "<h1 style='text-align:center; color:#FF6F61;'>🚗 Car Horsepower Dashboard</h1>",
    unsafe_allow_html=True
)

# Sidebar controls
st.sidebar.header("⚙️ Dashboard Controls")

# Brand selection
brands = df["Make"].unique()
selected_brands = st.sidebar.multiselect("Select Brand(s)", brands, default=[brands[0]])

# Model search
model_search = st.sidebar.text_input("🔍 Search Model (optional)").strip()

# Top N filter
top_n = st.sidebar.slider("Show Top N Cars by Horsepower", min_value=5, max_value=50, value=10)

# Sorting
sort_option = st.sidebar.radio("Sort by:", ["Model (A-Z)", "Horsepower (High → Low)", "Horsepower (Low → High)"])

# Chart type
chart_type = st.sidebar.radio("Select Chart Type", ["Bar (2D)", "Bar (3D)", "Line", "Scatter"])

# Color palette
palette_option = st.sidebar.selectbox(
    "🎨 Choose Color Palette",
    ["viridis", "plasma", "mako", "coolwarm", "Spectral", "icefire"]
)

# Filter data
filtered = df[df["Make"].isin(selected_brands)]
if model_search:
    filtered = filtered[filtered["Model"].str.contains(model_search, case=False)]

# Sorting
if sort_option == "Model (A-Z)":
    filtered = filtered.sort_values(by="Model")
elif sort_option == "Horsepower (High → Low)":
    filtered = filtered.sort_values(by="Horsepower", ascending=False)
elif sort_option == "Horsepower (Low → High)":
    filtered = filtered.sort_values(by="Horsepower", ascending=True)

# Limit Top N
filtered = filtered.head(top_n)

# Main chart
st.subheader("📊 Visualization")

if chart_type == "Bar (2D)":
    fig, ax = plt.subplots(figsize=(12, 6))
    sb.barplot(x="Model", y="Horsepower", data=filtered, palette=palette_option, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

elif chart_type == "Bar (3D)":
    fig = px.bar(
        filtered,
        x="Model",
        y="Horsepower",
        color="Horsepower",
        color_continuous_scale=palette_option,
        title="3D Bar Chart of Horsepower",
    )
    fig.update_traces(marker=dict(line=dict(width=0)))
    fig.update_layout(scene=dict(zaxis=dict(title="Horsepower")))
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Line":
    fig = px.line(
        filtered,
        x="Model",
        y="Horsepower",
        color="Make",
        markers=True,
        title="Line Chart of Horsepower"
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Scatter":
    fig = px.scatter(
        filtered,
        x="Model",
        y="Horsepower",
        size="Horsepower",
        color="Make",
        color_continuous_scale=palette_option,
        title="Scatter Plot of Horsepower"
    )
    st.plotly_chart(fig, use_container_width=True)

# Data Table
st.subheader("📑 Filtered Data")
st.dataframe(filtered)

# Download Button
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_cars.csv",
    mime="text/csv"
)

# Footer
st.markdown(
    "<hr><p style='text-align:center; color:gray;'>✨ Built with Streamlit, Seaborn & Plotly ✨</p>",
    unsafe_allow_html=True
)
