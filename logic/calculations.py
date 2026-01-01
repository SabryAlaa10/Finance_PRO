import pandas as pd
from datetime import datetime
from typing import Optional, List

def filter_data(df: pd.DataFrame, 
                start_date: Optional[datetime] = None, 
                end_date: Optional[datetime] = None, 
                categories: Optional[List[str]] = None,
                payment_methods: Optional[List[str]] = None,
                txn_type: Optional[str] = None) -> pd.DataFrame:
    """
    Filter the transactions DataFrame based on criteria.
    """
    if df.empty:
        return df
        
    out = df.copy()
    
    if start_date:
        out = out[out["Date"] >= pd.Timestamp(start_date)]
    if end_date:
        out = out[out["Date"] <= pd.Timestamp(end_date)]
        
    if categories:
        out = out[out["Category"].isin(categories)]
        
    if payment_methods:
        out = out[out["Source"].isin(payment_methods)]
        
    if txn_type:
        out = out[out["Type"] == txn_type]
        
    return out

def get_monthly_summary(df: pd.DataFrame, value_col: str = "Amount", agg_func: str = "sum") -> pd.DataFrame:
    """
    Resample data by month and aggregate.
    """
    if df.empty:
        return pd.DataFrame()
        
    # Ensure date index
    temp = df.set_index("Date").sort_index()
    monthly = temp.resample("M")[value_col].agg(agg_func).reset_index()
    monthly["Month"] = monthly["Date"].dt.strftime("%Y-%m")
    return monthly

def group_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group expenses by category for pie/bar charts.
    """
    if df.empty:
        return pd.DataFrame(columns=["Category", "Amount"])
    return df.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount", ascending=False)
