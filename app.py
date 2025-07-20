
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from shuttle_optimizer import optimize_schedule

st.set_page_config(layout="wide")
st.title("🚌 Shuttle Volume Dashboard + Optimizer")

uploaded_file = st.file_uploader("Upload Shuttle Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["date"] = pd.to_datetime(df["date"])
    df["day_of_week"] = df["date"].dt.day_name()

    st.subheader("📊 Raw Passenger Volume (Grouped by Pickup & Time Block)")
    grouped = df.groupby(["pickup_location", "time_block"])["passenger_count"].sum().reset_index()
    pivot = grouped.pivot(index="pickup_location", columns="time_block", values="passenger_count").fillna(0)
    st.dataframe(pivot)

    st.subheader("📈 Passenger Volume by Day of Week and Time Block")
    heatmap_data = df.groupby(["day_of_week", "time_block"])["passenger_count"].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="day_of_week", columns="time_block", values="passenger_count").fillna(0)
    st.dataframe(heatmap_pivot)

    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x="Time Block", y="Day of Week", color="Passengers"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        aspect="auto"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🧠 Optimized Shuttle Schedule")
    schedule_df = optimize_schedule(df)
    st.dataframe(schedule_df)
