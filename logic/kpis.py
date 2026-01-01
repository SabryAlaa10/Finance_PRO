import pandas as pd

def calculate_kpis(df: pd.DataFrame):
    """
    Calculate headline KPIs from the dataframe.
    Returns a dictionary of metrics.
    """
    if df.empty:
        return {
            "total_income": 0.0,
            "total_expenses": 0.0,
            "net_balance": 0.0,
            "wallet_balance": 0.0,
            "bank_balance": 0.0,
            "investments_value": 0.0
        }
        
    # 1. Income & Expenses (Cash Flow)
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expenses = df[df["Type"] == "Expense"]["Amount"].sum()
    net = income - expenses
    
    # 2. Balances (Calculated from inflows/outflows per source)
    # We need to consider Transfer logic if implemented. 
    # For now, simplest approach: 
    # Balance = (Initial + Incoming) - Outgoing
    # We assume 'Income' adds to source, 'Expense' subtracts. 
    # 'Investment' might subtract from Cash source (Buying gold) or add (Selling).
    # 'Transfer' subtracts from Source, adds to Description (if Description holds target).
    # Since Transfer logic can be complex, we'll do a simple aggregation by Source for now.
    
    # Let's pivot slightly:
    # Income -> +Amount to Source
    # Expense -> -Amount from Source
    # Investment -> -Amount from Source (Buying)
    # Transfer -> -Amount from Source
    
    # This assumes 'Investment' transactions in the main DF represent *spending money to buy assets*.
    # If we track the *value* of investments, that might be separate or estimated. 
    # The requirement says "Total Investments Value".
    # We can sum up 'Investment' amounts as "Cost Basis" for now. 
    # Or strict 'Type' == 'Investment' means we put money into it.
    
    # Let's derive current wallet/bank balances:
    # Sources: Vodafone Cash, InstaPay, Banks.
    
    # Create a signed amount column
    # Expenses & Investments are negative flow for the *Source*. 
    # Income is positive flow.
    
    # NOTE: "Investment" type reduces cash in wallet/bank, but increases "Investment Portfolio".
    
    df_calc = df.copy()
    df_calc['signed_amount'] = df_calc.apply(
        lambda row: row['Amount'] if row['Type'] == 'Income' else -row['Amount'], axis=1
    )
    
    # Group by Source to get balances
    source_balances = df_calc.groupby("Source")["signed_amount"].sum()
    
    # Define groups
    wallets = ["Vodafone Cash", "InstaPay", "Wallet"]
    banks = ["Bank A", "Bank B"] # User can add more, but these are defaults
    
    wallet_bal = source_balances[source_balances.index.isin(wallets)].sum()
    
    # Identify bank sources (anything containing 'Bank' or 'Banque')
    bank_bal = source_balances[source_balances.index.str.contains("Bank|Banque|Ahly|Misr", case=False, na=False)].sum()
    
    # 3. Investment Value
    # Sum of all 'Investment' type transactions (Cost basis)
    # Ideally user updates this with current market value, but for now sum of invested capital is a good start.
    invested_capital = df[df["Type"] == "Investment"]["Amount"].sum()
    
    return {
        "total_income": income,
        "total_expenses": expenses,
        "net_balance": net,
        "wallet_balance": wallet_bal,
        "bank_balance": bank_bal,
        "investments_value": invested_capital
    }
