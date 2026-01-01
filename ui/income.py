import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from logic.calculations import filter_data, get_monthly_summary

def render_income(df: pd.DataFrame):
    """
    Render professional income tracking page with animations.
    """
    # Custom CSS with animations
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .income-hero {
        animation: fadeIn 0.8s ease-out;
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(16, 185, 129, 0.15) 100%);
        border: 1.5px solid rgba(34, 197, 94, 0.4);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 25px;
        text-align: center;
    }
    .income-card {
        animation: slideInLeft 0.6s ease-out;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 20px;
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    .income-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(34, 197, 94, 0.3);
        border-color: rgba(34, 197, 94, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="income-hero">
        <div style="font-size: 42px; margin-bottom: 8px;">💰</div>
        <div style="font-size: 26px; font-weight: 800; background: linear-gradient(120deg, #22c55e, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Income Tracking</div>
        <div style="font-size: 13px; color: #94a3b8; margin-top: 5px;">Monitor your earnings and financial growth</div>
    </div>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No data available.")
        return
        
    df_inc = df[df["Type"] == "Income"].copy()
    
    if df_inc.empty:
        st.info("💡 No income records found. Start adding your income transactions!")
        return

    # Total stats with enhanced cards
    total_income = df_inc["Amount"].sum()
    monthly_avg = total_income / max(1, df_inc["Date"].dt.to_period("M").nunique())
    num_transactions = len(df_inc)
    
    # Freelancing stats
    freelance = df_inc[df_inc["Category"].str.contains("Freelanc|Mostaql", case=False, na=False)]
    freelance_total = freelance["Amount"].sum()
    freelance_pct = (freelance_total / total_income * 100) if total_income > 0 else 0
    
    # Enhanced metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="income-card">
            <div style="font-size: 24px; margin-bottom: 8px;">💵</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Total Income</div>
            <div style="font-size: 24px; font-weight: 800; color: #22c55e; margin-top: 5px;">{total_income:,.0f} EGP</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="income-card">
            <div style="font-size: 24px; margin-bottom: 8px;">📊</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Monthly Average</div>
            <div style="font-size: 24px; font-weight: 800; color: #10b981; margin-top: 5px;">{monthly_avg:,.0f} EGP</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="income-card">
            <div style="font-size: 24px; margin-bottom: 8px;">💼</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Freelancing (Mostaql)</div>
            <div style="font-size: 24px; font-weight: 800; color: #3b82f6; margin-top: 5px;">{freelance_total:,.0f} EGP</div>
            <div style="font-size: 10px; color: #64748b; margin-top: 3px;">{freelance_pct:.1f}% of total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="income-card">
            <div style="font-size: 24px; margin-bottom: 8px;">📈</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Transactions</div>
            <div style="font-size: 24px; font-weight: 800; color: #a78bfa; margin-top: 5px;">{num_transactions}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Source Breakdown with enhanced visuals
    st.markdown('<div class="section-header-pro">💳 Income Sources Breakdown</div>', unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns([1.2, 1])
    
    with col_chart1:
        category_summary = df_inc.groupby("Category")["Amount"].sum().sort_values(ascending=True).reset_index()
        fig_bar = go.Figure()
        
        fig_bar.add_trace(go.Bar(
            x=category_summary["Amount"],
            y=category_summary["Category"],
            orientation='h',
            marker=dict(
                color=category_summary["Amount"],
                colorscale=[
                    [0, "#10b981"],
                    [0.5, "#22c55e"],
                    [1, "#84cc16"]
                ],
                line=dict(color='#059669', width=1)
            ),
            text=category_summary["Amount"].apply(lambda x: f"{x:,.0f} EGP"),
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Amount: %{x:,.0f} EGP<extra></extra>"
        ))
        
        fig_bar.update_layout(
            title="Income by Source",
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
            category_summary,
            values="Amount",
            names="Category",
            title="Distribution %",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens_r
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
    
    # Monthly Growth with enhanced visualization
    st.markdown('<div class="section-header-pro">📈 Monthly Growth Trend</div>', unsafe_allow_html=True)
    
    monthly = get_monthly_summary(df_inc)
    if not monthly.empty:
        # Create combination chart
        fig_growth = go.Figure()
        
        # Add bars
        fig_growth.add_trace(go.Bar(
            x=monthly["Month"],
            y=monthly["Amount"],
            name="Monthly Income",
            marker=dict(
                color=monthly["Amount"],
                colorscale=[
                    [0, "#10b981"],
                    [1, "#22c55e"]
                ],
                line=dict(color='#059669', width=1.5)
            ),
            text=monthly["Amount"].apply(lambda x: f"{x:,.0f}"),
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Income: %{y:,.0f} EGP<extra></extra>"
        ))
        
        # Add trend line
        fig_growth.add_trace(go.Scatter(
            x=monthly["Month"],
            y=monthly["Amount"],
            mode='lines+markers',
            name='Trend',
            line=dict(color='#3b82f6', width=3, dash='dash'),
            marker=dict(size=8, color='#60a5fa', line=dict(width=2, color='#1e40af')),
            hovertemplate="<b>%{x}</b><br>Trend: %{y:,.0f} EGP<extra></extra>"
        ))
        
        fig_growth.update_layout(
            title="Monthly Income Progress",
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
        st.plotly_chart(fig_growth, use_container_width=True)
    
    # Recurring Income Details with better formatting
    st.markdown('<div class="section-header-pro">📋 Recurring Income Details</div>', unsafe_allow_html=True)
    
    # Format the dataframe
    df_display = df_inc.copy()
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
    
    if len(df_inc) > 20:
        st.info(f"💡 Showing latest 20 transactions out of {len(df_inc)} total income records")
