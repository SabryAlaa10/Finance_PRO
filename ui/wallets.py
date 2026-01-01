import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data(show_spinner=False)
def calculate_balances(df_hash):
    """Calculate balances for each source (cached for performance)"""
    df = df_hash['df']
    df_calc = df.copy()
    df_calc['signed_amount'] = df_calc.apply(
        lambda row: row['Amount'] if row['Type'] == 'Income' else -row['Amount'], axis=1
    )
    balances = df_calc.groupby("Source")["signed_amount"].sum().sort_values(ascending=False).reset_index()
    balances.columns = ["Source", "Balance"]
    return balances

@st.cache_data(show_spinner=False)
def get_source_transactions(df_hash, selected_source):
    """Get and process transactions for a specific source (cached)"""
    df = df_hash['df']
    source_txns = df[df["Source"] == selected_source].sort_values("Date", ascending=False)
    
    if source_txns.empty:
        return None, None
    
    # Calculate cumulative for chart
    source_txns_sorted = source_txns.sort_values("Date")
    source_txns_sorted['signed_amount'] = source_txns_sorted.apply(
         lambda row: row['Amount'] if row['Type'] == 'Income' else -row['Amount'], axis=1
    )
    source_txns_sorted['cumulative'] = source_txns_sorted['signed_amount'].cumsum()
    
    return source_txns, source_txns_sorted

def render_wallets(df: pd.DataFrame):
    """
    Render wallets and banks status.
    """
    st.markdown('<div class="section-header-pro">Wallets & Banks</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.info("No data available.")
        return
    
    # Create hashable version for caching
    df_hash = {'df': df, 'hash': hash(pd.util.hash_pandas_object(df).sum())}
    
    # Calculate balances using cache
    balances = calculate_balances(df_hash)
    
    # Overall Cards
    st.markdown("### 💳 Current Balances")
    
    # Display as metrics in a grid
    cols = st.columns(3)
    for i, row in balances.iterrows():
        with cols[i % 3]:
            st.metric(
                row["Source"], 
                f"{row['Balance']:,.0f} EGP", 
                help="Net calculated from tracked transactions"
            )
            
    st.divider()
    
    # Flow Analysis
    st.markdown("### 🌊 Flow Analysis")
    
    selected_source = st.selectbox("Select Source for Details", balances["Source"].unique(), key="wallet_source_select")
    
    # Get source transactions using cache
    source_txns, source_txns_sorted = get_source_transactions(df_hash, selected_source)
    
    if source_txns is not None and not source_txns.empty:
        # Mini chart of flow over time for this source
        fig = px.line(source_txns_sorted, x="Date", y="cumulative", title=f"{selected_source} Balance Trend (Calculated)")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e5e7eb"),
            hovermode="x unified",
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(148, 163, 184, 0.1)",
                zeroline=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(148, 163, 184, 0.1)",
                zeroline=True,
                zerolinecolor="rgba(148, 163, 184, 0.3)",
                zerolinewidth=1
            ),
            margin=dict(l=10, r=10, t=40, b=10)
        )
        # Use cyan color matching the design with enhanced visibility
        fig.update_traces(
            line_color="#00f2ff", 
            line_width=3,
            mode='lines+markers',
            marker=dict(size=8, color="#00f2ff", line=dict(width=2, color="#0891b2")),
            hovertemplate="<b>Date:</b> %{x|%b %d, %Y}<br><b>Balance:</b> %{y:,.0f} EGP<extra></extra>"
        )
        st.plotly_chart(fig, use_container_width=True, key=f"wallet_chart_{selected_source}")
        
        st.markdown('<div class="section-header-pro">📋 Recent Activity</div>', unsafe_allow_html=True)
        
        # Format dataframe with proper date formatting
        display_df = source_txns.copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%d %b %Y")
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"{x:,.0f} EGP")
        
        st.dataframe(
            display_df[["Date", "Type", "Category", "Amount", "Description"]].head(20),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(f"No transactions found for {selected_source}")
