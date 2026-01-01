import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from logic.calculations import filter_data, get_monthly_summary, group_by_category

def render_expenses(df: pd.DataFrame):
    """
    Render professional expenses analysis page with animations.
    """
    # Custom CSS with animations
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .expense-hero {
        animation: fadeIn 0.8s ease-out;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.15) 100%);
        border: 1.5px solid rgba(239, 68, 68, 0.4);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 25px;
        text-align: center;
    }
    .expense-card {
        animation: slideInRight 0.6s ease-out;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 20px;
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    .expense-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
        border-color: rgba(239, 68, 68, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="expense-hero">
        <div style="font-size: 42px; margin-bottom: 8px;">💸</div>
        <div style="font-size: 26px; font-weight: 800; background: linear-gradient(120deg, #ef4444, #dc2626); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Expense Analysis</div>
        <div style="font-size: 13px; color: #94a3b8; margin-top: 5px;">Track and control your spending habits</div>
    </div>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No data available.")
        return
    
    # Filter only Expenses
    df_exp = df[df["Type"] == "Expense"].copy()
    
    if df_exp.empty:
        st.info("💡 No expense records found. Start tracking your expenses!")
        return
        
    # Filters with better styling
    st.markdown('<div class="section-header-pro">🔍 Filter Options</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        start_date = st.date_input("From Date", df_exp["Date"].min())
    with c2:
        end_date = st.date_input("To Date", df_exp["Date"].max())
    with c3:
        all_cats = list(df_exp["Category"].dropna().unique())
        cats = st.multiselect("Categories", all_cats, default=all_cats)
    
    # Apply filters
    filtered = filter_data(df_exp, start_date=start_date, end_date=end_date)
    if cats:
        filtered = filtered[filtered["Category"].isin(cats)]
        
    if filtered.empty:
        st.warning("⚠️ No matching expenses found for selected filters.")
        return
    
    # Calculate statistics
    total = filtered["Amount"].sum()
    avg_transaction = filtered["Amount"].mean()
    num_transactions = len(filtered)
    daily_avg = total / max(1, (filtered["Date"].max() - filtered["Date"].min()).days + 1)
    
    # Top category
    top_category = filtered.groupby("Category")["Amount"].sum().idxmax()
    top_category_amount = filtered.groupby("Category")["Amount"].sum().max()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enhanced metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="expense-card">
            <div style="font-size: 24px; margin-bottom: 8px;">💰</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Total Expenses</div>
            <div style="font-size: 24px; font-weight: 800; color: #ef4444; margin-top: 5px;">{total:,.0f} EGP</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="expense-card">
            <div style="font-size: 24px; margin-bottom: 8px;">📊</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Avg Transaction</div>
            <div style="font-size: 24px; font-weight: 800; color: #f97316; margin-top: 5px;">{avg_transaction:,.0f} EGP</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="expense-card">
            <div style="font-size: 24px; margin-bottom: 8px;">🎯</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Top Category</div>
            <div style="font-size: 16px; font-weight: 800; color: #f59e0b; margin-top: 5px;">{top_category}</div>
            <div style="font-size: 10px; color: #64748b; margin-top: 3px;">{top_category_amount:,.0f} EGP</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="expense-card">
            <div style="font-size: 24px; margin-bottom: 8px;">📈</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Daily Average</div>
            <div style="font-size: 24px; font-weight: 800; color: #a78bfa; margin-top: 5px;">{daily_avg:,.0f} EGP</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Category Breakdown with enhanced visuals
    st.markdown('<div class="section-header-pro">📊 Expenses by Category</div>', unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns([1.2, 1])
    
    with col_chart1:
        by_cat = group_by_category(filtered).sort_values("Amount", ascending=True)
        fig_bar = go.Figure()
        
        fig_bar.add_trace(go.Bar(
            x=by_cat["Amount"],
            y=by_cat["Category"],
            orientation='h',
            marker=dict(
                color=by_cat["Amount"],
                colorscale=[
                    [0, "#fca5a5"],
                    [0.5, "#f87171"],
                    [1, "#dc2626"]
                ],
                line=dict(color='#b91c1c', width=1)
            ),
            text=by_cat["Amount"].apply(lambda x: f"{x:,.0f} EGP"),
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Amount: %{x:,.0f} EGP<extra></extra>"
        ))
        
        fig_bar.update_layout(
            title="Expenses by Category",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e5e7eb", size=11),
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(148, 163, 184, 0.1)",
                title="Amount (EGP)"
            ),
            yaxis=dict(
                showgrid=False,
                title=""
            ),
            height=350,
            margin=dict(l=10, r=80, t=40, b=40),
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_chart2:
        # Pie chart for distribution
        fig_pie = px.pie(
            by_cat,
            values="Amount",
            names="Category",
            title="Distribution %",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e5e7eb", size=10),
            height=350,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} EGP<br>%{percent}<extra></extra>"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Monthly Trend with enhanced visualization
    st.markdown('<div class="section-header-pro">📈 Monthly Expense Trend</div>', unsafe_allow_html=True)
    
    monthly = get_monthly_summary(filtered)
    if not monthly.empty:
        fig_trend = go.Figure()
        
        # Add bars
        fig_trend.add_trace(go.Bar(
            x=monthly["Month"],
            y=monthly["Amount"],
            name="Monthly Expenses",
            marker=dict(
                color=monthly["Amount"],
                colorscale=[
                    [0, "#fca5a5"],
                    [1, "#dc2626"]
                ],
                line=dict(color='#b91c1c', width=1.5)
            ),
            text=monthly["Amount"].apply(lambda x: f"{x:,.0f}"),
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Expenses: %{y:,.0f} EGP<extra></extra>"
        ))
        
        # Add trend line
        fig_trend.add_trace(go.Scatter(
            x=monthly["Month"],
            y=monthly["Amount"],
            mode='lines+markers',
            name='Trend',
            line=dict(color='#f97316', width=3, dash='dash'),
            marker=dict(size=8, color='#fb923c', line=dict(width=2, color='#ea580c')),
            hovertemplate="<b>%{x}</b><br>Trend: %{y:,.0f} EGP<extra></extra>"
        ))
        
        fig_trend.update_layout(
            title="Monthly Expense Progress",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e5e7eb", size=11),
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(148, 163, 184, 0.1)",
                title="Month"
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(148, 163, 184, 0.1)",
                title="Amount (EGP)"
            ),
            height=400,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Transaction Details with better formatting
    st.markdown('<div class="section-header-pro">📋 Transaction Details</div>', unsafe_allow_html=True)
    
    # Format the dataframe
    df_display = filtered.copy()
    df_display["Date"] = df_display["Date"].dt.strftime("%d %b %Y")
    df_display["Amount"] = df_display["Amount"].apply(lambda x: f"{x:,.0f} EGP")
    
    # Select and reorder columns
    display_columns = ["Date", "Category", "Amount", "Source", "Description"]
    df_display = df_display[display_columns].sort_values("Date", ascending=False)
    
    # Style the dataframe
    st.dataframe(
        df_display.head(20),
        use_container_width=True,
        hide_index=True
    )
    
    if len(filtered) > 20:
        st.info(f"💡 Showing latest 20 transactions out of {len(filtered)} total expense records")
