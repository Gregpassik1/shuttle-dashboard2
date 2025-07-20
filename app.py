
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
    df["month"] = df["date"].dt.strftime('%B')

    # Raw data by location and time block
    st.subheader("📊 Raw Passenger Volume (Grouped by Pickup & Time Block)")
    grouped = df.groupby(["pickup_location", "time_block"])["passenger_count"].sum().reset_index()
    pivot = grouped.pivot(index="pickup_location", columns="time_block", values="passenger_count").fillna(0)
    st.dataframe(pivot)

    # Passenger volume by day of week and time block
    st.subheader("📈 Passenger Volume by Day of Week and Time Block")
    heatmap_data = df.groupby(["day_of_week", "time_block"])["passenger_count"].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="day_of_week", columns="time_block", values="passenger_count").fillna(0)
    st.dataframe(heatmap_pivot)

    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x="Time Block", y="Day of Week", color="Passengers"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index
    )
    st.plotly_chart(fig)

    # 📆 Monthly Average View
    st.subheader("📆 Monthly Average Passenger Volume by Time Block")
    month_selected = st.selectbox("Select Month", df["month"].unique())
    month_df = df[df["month"] == month_selected]

    daily_avg = (
        month_df.groupby(["date", "time_block"])["passenger_count"].sum().reset_index()
        .groupby("time_block")["passenger_count"].mean().reset_index()
    )
    daily_avg_pivot = daily_avg.pivot(index="time_block", values="passenger_count")
    st.dataframe(daily_avg_pivot)

    bar_fig = px.bar(daily_avg, x="time_block", y="passenger_count", title=f"Average Daily Volume in {month_selected}")
    st.plotly_chart(bar_fig)

    # Optimizer output
    st.subheader("🧠 Optimized Shuttle Schedule")
    schedule_df = optimize_schedule(df)
    st.dataframe(schedule_df)
