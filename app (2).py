
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
    df["month"] = df["date"].dt.strftime("%B")
    df["time_block"] = pd.Categorical(df["time_block"], ordered=True, categories=sorted(df["time_block"].unique()))

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
        y=heatmap_pivot.index
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📅 Monthly Average Passenger Volume by Time Block")
    selected_month = st.selectbox("Select Month", df["month"].unique())
    month_df = df[df["month"] == selected_month]
    if not month_df.empty:
        total_days = month_df["date"].nunique()
        daily_avg = month_df.groupby(["time_block", "pickup_location"])["passenger_count"].sum().reset_index()
        daily_avg["passenger_count"] = daily_avg["passenger_count"] / total_days

        if not daily_avg.empty and {"time_block", "pickup_location", "passenger_count"}.issubset(daily_avg.columns):
            daily_avg_pivot = daily_avg.pivot(index="time_block", columns="pickup_location", values="passenger_count").fillna(0)
            st.dataframe(daily_avg_pivot)
        else:
            st.warning("No data available for the selected month or required columns are missing.")
    else:
        st.warning("No data available for the selected month.")

    st.subheader("🚍 Optimized Shuttle Schedule")
    optimized_schedule = optimize_schedule(df)
    st.dataframe(optimized_schedule)
