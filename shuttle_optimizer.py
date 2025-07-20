
import pandas as pd

def optimize_schedule(df):
    avg_by_block = df.groupby("time_block")["passenger_count"].mean().reset_index()
    avg_by_block["shuttles_needed"] = (avg_by_block["passenger_count"] / 14).apply(lambda x: max(1, round(x)))
    return avg_by_block
