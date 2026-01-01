import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_investments(df: pd.DataFrame):
    """
    Render professional investments tracking page with analytics.
    """
    # Custom CSS with animations
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .investment-hero {
        animation: fadeIn 0.8s ease-out;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.2) 0%, rgba(147, 51, 234, 0.15) 100%);
        border: 1.5px solid rgba(168, 85, 247, 0.4);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 25px;
        text-align: center;
    }
    .investment-card {
        animation: slideInUp 0.6s ease-out;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 20px;
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    .investment-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(168, 85, 247, 0.3);
        border-color: rgba(168, 85, 247, 0.6);
    }
    .investment-section {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="investment-hero">
        <div style="font-size: 42px; margin-bottom: 8px;">📈</div>
        <div style="font-size: 26px; font-weight: 800; background: linear-gradient(120deg, #a855f7, #9333ea); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Investment Portfolio</div>
        <div style="font-size: 13px; color: #94a3b8; margin-top: 5px;">Track your investments and monitor returns</div>
    </div>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No data available.")
        return
        
    df_inv = df[df["Type"] == "Investment"].copy()
    
    if df_inv.empty:
        st.info("💡 No investment records found. Start building your portfolio!")
        return
    
    # Overall Portfolio Stats
    total_invested = df_inv["Amount"].sum()
    num_investments = len(df_inv)
    categories = df_inv["Category"].nunique()
    
    st.markdown('<div class="section-header-pro">💼 Portfolio Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="investment-card">
            <div style="font-size: 24px; margin-bottom: 8px;">💰</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Total Invested</div>
            <div style="font-size: 24px; font-weight: 800; color: #a855f7; margin-top: 5px;">{total_invested:,.0f} EGP</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="investment-card">
            <div style="font-size: 24px; margin-bottom: 8px;">📊</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Total Investments</div>
            <div style="font-size: 24px; font-weight: 800; color: #c084fc; margin-top: 5px;">{num_investments}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="investment-card">
            <div style="font-size: 24px; margin-bottom: 8px;">🎯</div>
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Asset Types</div>
            <div style="font-size: 24px; font-weight: 800; color: #e9d5ff; margin-top: 5px;">{categories}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Investment Breakdown
    st.markdown('<div class="section-header-pro">📊 Investment Breakdown</div>', unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns([1.3, 1])
    
    with col_chart1:
        category_summary = df_inv.groupby("Category")["Amount"].sum().sort_values(ascending=True).reset_index()
        fig_bar = go.Figure()
        
        fig_bar.add_trace(go.Bar(
            x=category_summary["Amount"],
            y=category_summary["Category"],
            orientation='h',
            marker=dict(
                color=category_summary["Amount"],
                colorscale=[
                    [0, "#c084fc"],
                    [0.5, "#a855f7"],
                    [1, "#9333ea"]
                ],
                line=dict(color='#7e22ce', width=1)
            ),
            text=category_summary["Amount"].apply(lambda x: f"{x:,.0f} EGP"),
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Amount: %{x:,.0f} EGP<extra></extra>"
        ))
        
        fig_bar.update_layout(
            title="Investment by Category",
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
        fig_pie = px.pie(
            category_summary,
            values="Amount",
            names="Category",
            title="Portfolio Distribution",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Purples_r
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
    
    # Investment Timeline
    st.markdown('<div class="section-header-pro">📈 Investment Timeline</div>', unsafe_allow_html=True)
    
    df_timeline = df_inv.sort_values("Date").copy()
    df_timeline["Cumulative"] = df_timeline["Amount"].cumsum()
    
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Scatter(
        x=df_timeline["Date"],
        y=df_timeline["Cumulative"],
        mode='lines+markers',
        name='Cumulative Investment',
        line=dict(color='#a855f7', width=3),
        marker=dict(size=8, color='#c084fc', line=dict(width=2, color='#7e22ce')),
        fill='tozeroy',
        fillcolor='rgba(168, 85, 247, 0.2)',
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Cumulative: %{y:,.0f} EGP<extra></extra>"
    ))
    
    fig_timeline.update_layout(
        title="Cumulative Investment Growth",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb", size=11),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.1)",
            title="Date"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.1)",
            title="Cumulative Amount (EGP)"
        ),
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Detailed Breakdown by Category
    st.markdown('<div class="section-header-pro">💎 Detailed Asset Breakdown</div>', unsafe_allow_html=True)
    
    for category in df_inv["Category"].unique():
        cat_data = df_inv[df_inv["Category"] == category]
        cat_total = cat_data["Amount"].sum()
        cat_count = len(cat_data)
        
        # Icon mapping
        icons = {
            "Gold": "🪙",
            "Stock Trading": "📈",
            "Crypto": "₿",
            "Real Estate": "🏢",
            "NFT": "💎"
        }
        icon = icons.get(category, "💼")
        
        with st.expander(f"{icon} {category} - {cat_total:,.0f} EGP ({cat_count} transactions)"):
            col_a, col_b = st.columns([2, 1])
            
            with col_a:
                # Format data
                display_df = cat_data.copy()
                display_df["Date"] = display_df["Date"].dt.strftime("%d %b %Y")
                display_df["Amount"] = display_df["Amount"].apply(lambda x: f"{x:,.0f} EGP")
                
                st.dataframe(
                    display_df[["Date", "Amount", "Source", "Description"]].sort_values("Date", ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
            
            with col_b:
                st.markdown(f"""
                <div style="background: rgba(168, 85, 247, 0.1); padding: 20px; border-radius: 12px; border: 1px solid rgba(168, 85, 247, 0.3);">
                    <div style="font-size: 14px; color: #94a3b8; margin-bottom: 10px;">💰 Total Invested</div>
                    <div style="font-size: 28px; font-weight: 800; color: #a855f7; margin-bottom: 15px;">{cat_total:,.0f} EGP</div>
                    <div style="font-size: 12px; color: #cbd5e1;">
                        <div style="margin-bottom: 8px;">📊 Transactions: {cat_count}</div>
                        <div style="margin-bottom: 8px;">📅 First: {cat_data['Date'].min().strftime('%d %b %Y')}</div>
                        <div>📅 Latest: {cat_data['Date'].max().strftime('%d %b %Y')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Performance Calculator Section
    st.markdown('<div class="section-header-pro">🎯 Performance Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div style="background: rgba(59, 130, 246, 0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(59, 130, 246, 0.2); margin-bottom: 20px;">', unsafe_allow_html=True)
    
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    
    with calc_col1:
        st.metric("Total Capital Deployed", f"{total_invested:,.0f} EGP")
    
    with calc_col2:
        current_value = st.number_input(
            "Current Portfolio Value (EGP)",
            min_value=0.0,
            value=float(total_invested),
            step=100.0,
            help="Enter the current market value of your portfolio"
        )
    
    with calc_col3:
        profit_loss = current_value - total_invested
        pl_pct = (profit_loss / total_invested * 100) if total_invested > 0 else 0
        color = "#22c55e" if profit_loss >= 0 else "#ef4444"
        
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 12px; color: #94a3b8; margin-bottom: 5px;">Unrealized P/L</div>
            <div style="font-size: 26px; font-weight: 800; color: {color};">
                {profit_loss:+,.0f} EGP
            </div>
            <div style="font-size: 14px; color: {color}; margin-top: 5px;">
                {pl_pct:+.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
