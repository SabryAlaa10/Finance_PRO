import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from ui.styles import kpi_card_html
from logic.kpis import calculate_kpis
from logic.report_generator import generate_pdf_report

def render_dashboard(df):
    """
    Render the main dashboard view.
    """
    # Hero Section
    st.markdown(
        """
        <div class="hero-premium">
            <div class="hero-title-pro">Personal Finance Dashboard</div>
            <div class="hero-subtitle-pro">
                Track expenses, monitor investments, and optimize your financial growth.
                Real-time insights for better decision making.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # KPIs
    kpis = calculate_kpis(df)
    
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(
            kpi_card_html("💰", "Total Income", f"{kpis['total_income']:,.0f} EGP", "Cumulative"),
            unsafe_allow_html=True
        )
    with k2:
        st.markdown(
            kpi_card_html("💸", "Total Expenses", f"{kpis['total_expenses']:,.0f} EGP", "Cumulative"),
            unsafe_allow_html=True
        )
    with k3:
        net = kpis['net_balance']
        trend_color = "#22c55e" if net >= 0 else "#f87171"
        st.markdown(
            kpi_card_html("📈", "Net Balance", f"{net:,.0f} EGP", f"<span style='color:{trend_color}'>{'Positive' if net>=0 else 'Negative'} flow</span>"),
            unsafe_allow_html=True
        )
    with k4:
        st.markdown(
            kpi_card_html("🪙", "Investments", f"{kpis['investments_value']:,.0f} EGP", "Total Invested"),
            unsafe_allow_html=True
        )
    
    # Report Download Section
    st.markdown('<div class="section-header-pro">📄 Generate Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc-pro">Download comprehensive financial reports in PDF format</div>', unsafe_allow_html=True)
    
    # Info box explaining report types
    st.info("""
    **📊 Report Types:**
    
    - **Weekly Report**: Includes last 7 days of transactions (rolling window)
    - **Monthly Report**: Includes all transactions from 1st of current month to today
    
    *Note: If today is within the first 7 days of the month, both reports may show similar data.*
    """)
    
    # Show report period info
    from datetime import datetime, timedelta
    today = datetime.now()
    week_start = (today - timedelta(days=7)).strftime('%d %b')
    month_start = today.replace(day=1).strftime('%d %b')
    today_str = today.strftime('%d %b %Y')
    
    rep_col1, rep_col2, rep_col3 = st.columns([1, 1, 2])
    
    with rep_col1:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 10px; padding: 10px; background: rgba(59, 130, 246, 0.1); border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.3);">
            <div style="font-size: 11px; color: #94a3b8;">Weekly Period</div>
            <div style="font-size: 13px; color: #60a5fa; font-weight: 600;">{week_start} - {today_str}</div>
            <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">Last 7 Days</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 Download Weekly Report", type="primary", use_container_width=True):
            with st.spinner("Generating weekly report..."):
                try:
                    pdf_buffer = generate_pdf_report(df, period_type="weekly")
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_buffer,
                        file_name=f"Weekly_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("✅ Weekly report generated!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with rep_col2:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 10px; padding: 10px; background: rgba(34, 197, 94, 0.1); border-radius: 8px; border: 1px solid rgba(34, 197, 94, 0.3);">
            <div style="font-size: 11px; color: #94a3b8;">Monthly Period</div>
            <div style="font-size: 13px; color: #22c55e; font-weight: 600;">{month_start} - {today_str}</div>
            <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">Month to Date</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 Download Monthly Report", type="primary", use_container_width=True):
            with st.spinner("Generating monthly report..."):
                try:
                    pdf_buffer = generate_pdf_report(df, period_type="monthly")
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_buffer,
                        file_name=f"Monthly_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("✅ Monthly report generated!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with rep_col3:
        st.markdown("""
        <div style="padding: 15px; background: rgba(168, 85, 247, 0.1); border-radius: 12px; border: 1px solid rgba(168, 85, 247, 0.3);">
            <div style="font-size: 14px; font-weight: 700; color: #e5e7eb; margin-bottom: 10px;">💡 How Reports Work</div>
            <ul style="font-size: 12px; color: #cbd5e1; line-height: 1.6; margin: 0; padding-left: 20px;">
                <li><strong>Weekly:</strong> Last 7 days transactions</li>
                <li><strong>Monthly:</strong> Current month up to today</li>
                <li>✅ Download anytime during the month!</li>
                <li>📊 Includes charts, stats & details</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
        
    # High-level overview
    st.markdown('<div class="section-header-pro">💼 Financial Overview</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.info("No transactions found. Add some data to see charts.")
        return

    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Enhanced Income vs Expense chart
        df_chart = df.copy()
        df_chart["Month"] = df_chart["Date"].dt.strftime("%Y-%m")
        grouped = df_chart.groupby(["Month", "Type"])["Amount"].sum().reset_index()
        
        # Filter for only Income and Expense
        grouped_main = grouped[grouped["Type"].isin(["Income", "Expense"])]
        
        if not grouped_main.empty:
            fig = go.Figure()
            
            # Add Income bars
            income_data = grouped_main[grouped_main["Type"] == "Income"]
            if not income_data.empty:
                fig.add_trace(go.Bar(
                    x=income_data["Month"],
                    y=income_data["Amount"],
                    name="Income",
                    marker=dict(
                        color="#22c55e",
                        line=dict(color='#16a34a', width=1.5)
                    ),
                    text=income_data["Amount"].apply(lambda x: f"{x:,.0f}"),
                    textposition='outside',
                    hovertemplate="<b>%{x}</b><br>Income: %{y:,.0f} EGP<extra></extra>"
                ))
            
            # Add Expense bars
            expense_data = grouped_main[grouped_main["Type"] == "Expense"]
            if not expense_data.empty:
                fig.add_trace(go.Bar(
                    x=expense_data["Month"],
                    y=expense_data["Amount"],
                    name="Expenses",
                    marker=dict(
                        color="#ef4444",
                        line=dict(color='#dc2626', width=1.5)
                    ),
                    text=expense_data["Amount"].apply(lambda x: f"{x:,.0f}"),
                    textposition='outside',
                    hovertemplate="<b>%{x}</b><br>Expenses: %{y:,.0f} EGP<extra></extra>"
                ))
            
            fig.update_layout(
                title="Monthly Income vs Expenses",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e5e7eb", size=11),
                xaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(148, 163, 184, 0.1)",
                    title=""
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(148, 163, 184, 0.1)",
                    title="Amount (EGP)"
                ),
                barmode='group',
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    bgcolor="rgba(15, 23, 42, 0.8)",
                    bordercolor="rgba(148, 163, 184, 0.3)",
                    borderwidth=1
                ),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No income/expense data to plot.")

    with col2:
        # Enhanced expense distribution pie chart
        df_exp = df[df["Type"] == "Expense"]
        if not df_exp.empty:
            exp_by_cat = df_exp.groupby("Category")["Amount"].sum().sort_values(ascending=False).reset_index()
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=exp_by_cat["Category"],
                values=exp_by_cat["Amount"],
                hole=0.5,
                marker=dict(
                    colors=px.colors.sequential.Reds_r,
                    line=dict(color='#1e293b', width=2)
                ),
                textposition='auto',
                textinfo='label+percent',
                hovertemplate="<b>%{label}</b><br>%{value:,.0f} EGP<br>%{percent}<extra></extra>"
            )])
            
            fig_pie.update_layout(
                title="Expense Distribution",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e5e7eb", size=10),
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    bgcolor="rgba(15, 23, 42, 0.8)",
                    bordercolor="rgba(148, 163, 184, 0.3)",
                    borderwidth=1
                )
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expenses found.")
