
import pandas as pd
import numpy as np

def optimize_schedule(df, shuttle_capacity=14, max_wait_minutes=15):
    df["date"] = pd.to_datetime(df["date"])
    df["day_of_week"] = df["date"].dt.day_name()

    demand = df.groupby(["day_of_week", "time_block"])["passenger_count"].sum().reset_index()
    demand["required_shuttles"] = np.ceil(demand["passenger_count"] / shuttle_capacity).astype(int)
    demand["note"] = demand["required_shuttles"].apply(
        lambda x: "OK" if x <= 4 else "Consider adding shuttle"
    )
    return demand
