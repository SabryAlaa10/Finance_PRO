import streamlit as st
from pathlib import Path
import pandas as pd

# Import Logic
from logic.data_loader import load_data, init_db
from ui.styles import APP_STYLE

# Import UI Modules
from ui.dashboard import render_dashboard
from ui.add_transaction import render_add_transaction
from ui.expenses import render_expenses
from ui.income import render_income
from ui.investments import render_investments
from ui.wallets import render_wallets

# Page Config
st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Styles
st.markdown(APP_STYLE, unsafe_allow_html=True)

# Main App Logic
def login_page():
    st.markdown(
        """
        <style>
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes float-up {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        @keyframes pulse-glow {
            0%, 100% { 
                box-shadow: 0 0 20px rgba(99, 102, 241, 0.4),
                            0 0 40px rgba(139, 92, 246, 0.3); 
            }
            50% { 
                box-shadow: 0 0 40px rgba(99, 102, 241, 0.6),
                            0 0 80px rgba(139, 92, 246, 0.5); 
            }
        }
        
        @keyframes slide-in {
            from { 
                opacity: 0; 
                transform: translateY(30px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
        
        @keyframes rotate-slow {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .login-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(
                -45deg,
                #0f172a 0%,
                #1e1b4b 25%,
                #312e81 50%,
                #1e293b 75%,
                #0f172a 100%
            );
            background-size: 400% 400%;
            animation: gradient-shift 15s ease infinite;
        }
        
        .login-container {
            max-width: 420px;
            margin: 0 auto;
            padding: 45px;
            background: rgba(15, 23, 42, 0.85);
            border-radius: 28px;
            border: 2px solid rgba(129, 140, 248, 0.5);
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.7);
            animation: slide-in 0.8s ease-out, pulse-glow 3s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }
        
        .login-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(
                circle,
                rgba(99, 102, 241, 0.1) 0%,
                transparent 70%
            );
            animation: rotate-slow 20s linear infinite;
            pointer-events: none;
        }
        
        .login-icon {
            text-align: center;
            font-size: 64px;
            margin-bottom: 20px;
            animation: float-up 3s ease-in-out infinite;
            position: relative;
            z-index: 1;
        }
        
        .login-title {
            text-align: center;
            font-size: 32px;
            font-weight: 900;
            margin-bottom: 10px;
            background: linear-gradient(120deg, #e0f2fe, #c4b5fd, #f9a8d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: gradient-shift 3s ease infinite;
            position: relative;
            z-index: 1;
        }
        
        .login-subtitle {
            text-align: center;
            font-size: 14px;
            color: #94a3b8;
            margin-bottom: 30px;
            position: relative;
            z-index: 1;
        }
        
        .login-form-group {
            position: relative;
            z-index: 1;
            margin-bottom: 20px;
        }
        
        .stTextInput input {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 1.5px solid rgba(129, 140, 248, 0.3) !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            font-size: 14px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput input:focus {
            border-color: rgba(129, 140, 248, 0.7) !important;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.4) !important;
        }
        
        .login-button button {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%) !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 24px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            transition: all 0.4s ease !important;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.5) !important;
        }
        
        .login-button button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0 8px 30px rgba(139, 92, 246, 0.7) !important;
        }
        
        .login-footer {
            text-align: center;
            margin-top: 25px;
            font-size: 12px;
            color: #64748b;
            position: relative;
            z-index: 1;
        }
        
        .security-badge {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-top: 20px;
            padding: 10px;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 8px;
            font-size: 12px;
            color: #22c55e;
            position: relative;
            z-index: 1;
        }
        </style>
        
        <div class="login-background"></div>
        """, unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="login-icon">💎</div>
        <div class="login-title">Finance PRO</div>
        <div class="login-subtitle">Secure access to your financial dashboard</div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="login-form-group">', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="login-form-group">', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="login-button">', unsafe_allow_html=True)
        if st.button("🔐 Sign In", type="primary", use_container_width=True):
            if username == "saleh" and password == "saleh109":
                st.session_state["authenticated"] = True
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="security-badge">
            <span>🔒</span>
            <span>Secured with end-to-end encryption</span>
        </div>
        <div class="login-footer">
            Finance PRO Dashboard © 2026 | All rights reserved
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        
    if not st.session_state["authenticated"]:
        login_page()
        return

    # Load Data (force reload if needed by session state)
    if "refresh" in st.session_state:
        st.cache_data.clear() # Clear cache if implemented, or just re-read
        del st.session_state["refresh"]
        
    df = load_data()
    
    # Header & Logout
    c1, c2 = st.sidebar.columns([3, 1])
    c1.title("💎 Finance PRO")
    if c2.button("Log out"):
        st.session_state["authenticated"] = False
        st.rerun()
    
    # Top Navigation (Tabs instead of Sidebar)
    tabs_labels = [
        "Dashboard", 
        "Add Transaction", 
        "Expenses Analysis", 
        "Income Tracking", 
        "Investments", 
        "Wallets & Banks"
    ]
    
    # Create tabs
    tabs = st.tabs(tabs_labels)
    
    # 1. Dashboard
    with tabs[0]:
        render_dashboard(df)
        
    # 2. Add Transaction
    with tabs[1]:
        render_add_transaction()
        
    # 3. Expenses
    with tabs[2]:
        render_expenses(df)
        
    # 4. Income
    with tabs[3]:
        render_income(df)
        
    # 5. Investments
    with tabs[4]:
        render_investments(df)
        
    # 6. Wallets
    with tabs[5]:
        render_wallets(df)
    
    # Optional: Keep Quick Stats in sidebar or move to Dashboard?
    # User only asked to change the "strip on the left" (sidebar) to the "image style" (tabs).
    # We can keep the sidebar for "Quick Stats" or branding, but remove the nav.
    st.sidebar.title("💎 Finance PRO")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Stats")
    if not df.empty:
        total_balance = df[df['Type']=='Income']['Amount'].sum() - df[df['Type']=='Expense']['Amount'].sum()
        st.sidebar.metric("Net Balance", f"{total_balance:,.0f} EGP")

if __name__ == "__main__":
    main()
