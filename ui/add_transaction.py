import streamlit as st
import datetime
import pandas as pd
from logic.data_loader import save_transaction, load_data

def get_user_id():
    """Get current user_id from session"""
    return st.session_state.get('user_id', 1)

def render_add_transaction():
    """
    Render the professional 'Add Transaction' form with animations and visual enhancements.
    """
    # Advanced Custom CSS with animations
    st.markdown("""
    <style>
    @keyframes fadeInUp {
        from { 
            opacity: 0; 
            transform: translateY(30px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }
        50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.6); }
    }
    
    @keyframes slideInRight {
        from { 
            opacity: 0; 
            transform: translateX(50px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .txn-hero {
        animation: fadeInUp 0.8s ease-out;
        background: linear-gradient(
            135deg,
            rgba(99, 102, 241, 0.3) 0%,
            rgba(139, 92, 246, 0.25) 50%,
            rgba(236, 72, 153, 0.2) 100%
        );
        border: 1.5px solid rgba(129, 140, 248, 0.5);
        padding: 35px;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        margin-bottom: 30px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .txn-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(129, 140, 248, 0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    .txn-title {
        font-size: 32px;
        font-weight: 900;
        background: linear-gradient(120deg, #e0f2fe 0%, #c4b5fd 50%, #f9a8d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
    }
    
    .txn-subtitle {
        font-size: 14px;
        color: #cbd5e1;
        position: relative;
        z-index: 1;
    }
    
    .txn-form-container {
        animation: fadeInUp 1s ease-out 0.2s backwards;
        background: radial-gradient(
            circle at top left, 
            rgba(30, 41, 59, 0.7), 
            rgba(15, 23, 42, 0.95)
        );
        border: 1.5px solid rgba(99, 102, 241, 0.4);
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.4);
        backdrop-filter: blur(12px);
        margin-bottom: 25px;
    }
    
    .form-section-title {
        font-size: 18px;
        font-weight: 700;
        color: #e5e7eb;
        margin: 25px 0 15px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(99, 102, 241, 0.5);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .stats-mini-card {
        animation: slideInRight 0.8s ease-out;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(129, 140, 248, 0.3);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stats-mini-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
        border-color: rgba(129, 140, 248, 0.6);
    }
    
    .stats-label {
        font-size: 11px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 5px;
    }
    
    .stats-value {
        font-size: 22px;
        font-weight: 800;
        background: linear-gradient(120deg, #e0f2fe, #c4b5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%) !important;
        border: none !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        padding: 12px 32px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6) !important;
        animation: glow 2s ease-in-out infinite;
    }
    
    /* Custom form field styling */
    .stSelectbox, .stDateInput, .stNumberInput, .stTextInput {
        animation: fadeInUp 0.6s ease-out backwards;
    }
    
    div[data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border-color: rgba(129, 140, 248, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(129, 140, 248, 0.6) !important;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    .success-animation {
        animation: fadeInUp 0.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section with Icon
    st.markdown("""
    <div class="txn-hero">
        <div style="font-size: 48px; margin-bottom: 10px;">💳</div>
        <div class="txn-title">Add New Transaction</div>
        <div class="txn-subtitle">Track your finances seamlessly • Keep your budget on track</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats Section
    try:
        df = load_data()
        if not df.empty:
            today = datetime.date.today()
            this_month = df[df["Date"].dt.month == today.month]
            
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            
            with col_s1:
                month_income = this_month[this_month["Type"] == "Income"]["Amount"].sum()
                st.markdown(f"""
                <div class="stats-mini-card">
                    <div style="font-size: 24px; margin-bottom: 5px;">📈</div>
                    <div class="stats-label">This Month Income</div>
                    <div class="stats-value">{month_income:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_s2:
                month_expenses = this_month[this_month["Type"] == "Expense"]["Amount"].sum()
                st.markdown(f"""
                <div class="stats-mini-card">
                    <div style="font-size: 24px; margin-bottom: 5px;">💸</div>
                    <div class="stats-label">This Month Expenses</div>
                    <div class="stats-value">{month_expenses:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_s3:
                total_transactions = len(this_month)
                st.markdown(f"""
                <div class="stats-mini-card">
                    <div style="font-size: 24px; margin-bottom: 5px;">📊</div>
                    <div class="stats-label">Total Transactions</div>
                    <div class="stats-value">{total_transactions}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_s4:
                net_balance = month_income - month_expenses
                balance_color = "#22c55e" if net_balance >= 0 else "#f87171"
                st.markdown(f"""
                <div class="stats-mini-card">
                    <div style="font-size: 24px; margin-bottom: 5px;">💰</div>
                    <div class="stats-label">Net Balance</div>
                    <div class="stats-value" style="background: linear-gradient(120deg, {balance_color}, {balance_color}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{net_balance:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
    except:
        pass
    
    # Main Form Container
    st.markdown('<div class="txn-form-container">', unsafe_allow_html=True)
    
    # Transaction Type Selection (outside form for dynamic updates)
    st.markdown('<div class="form-section-title">📅 Basic Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        date = st.date_input(
            "Transaction Date", 
            datetime.date.today(),
            help="Select the date of the transaction",
            key="txn_date"
        )
        
    with col2:
        txn_type = st.selectbox(
            "Transaction Type", 
            ["💸 Expense", "💰 Income", "📈 Investment", "🔄 Transfer"],
            help="Choose the type of transaction",
            key="txn_type_select"
        )
        # Remove emoji for processing - fix to handle all cases
        if "Expense" in txn_type:
            txn_type_clean = "Expense"
        elif "Income" in txn_type:
            txn_type_clean = "Income"
        elif "Investment" in txn_type:
            txn_type_clean = "Investment"
        else:
            txn_type_clean = "Transfer"
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dynamic categories based on selected type
    if txn_type_clean == "Expense":
        cats = ["🛒 Personal", "🎓 University", "🍔 Food", "🚗 Transport", "📱 Subscriptions", "🎮 Entertainment", "💊 Health", "📚 Books", "🏠 Rent", "⚡ Bills", "🎁 Gifts", "🔧 Other"]
    elif txn_type_clean == "Income":
        cats = ["💼 Freelancing (Mostaql)", "💰 Pocket Money", "💵 Salary", "🎁 Gift", "📊 Business", "🏆 Bonus", "💸 Refund", "🔧 Other"]
    elif txn_type_clean == "Investment":
        cats = ["🪙 Gold", "📈 Stock Trading", "₿ Crypto", "🏢 Real Estate", "💎 NFT", "🔧 Other"]
    else:  # Transfer
        cats = ["🔄 Transfer"]
    
    with st.form("transaction_form", clear_on_submit=True):
        # Section 2: Details
        st.markdown('<div class="form-section-title">💳 Transaction Details</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            amount = st.number_input(
                "Amount (EGP)", 
                min_value=0.0, 
                step=10.0,
                help="Enter the transaction amount"
            )
            
        with col4:
            # Category dropdown now uses dynamic list from above
            category = st.selectbox(
                "Category", 
                cats,
                help="Select the transaction category"
            )
            # Remove emoji for processing
            category_clean = " ".join(category.split(" ")[1:])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Section 3: Payment Method
        st.markdown('<div class="form-section-title">💳 Payment Method & Notes</div>', unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        
        with col5:
            # Source with icons
            sources = [
                "📱 Vodafone Cash", 
                "💳 InstaPay", 
                "🏦 National Bank of Egypt", 
                "🏦 Banque Misr",
                "🏦 CIB Bank",
                "🍎 Apple Pay",
                "💵 Cash", 
                "👛 Wallet",
                "💳 Credit Card",
                "🔧 Other"
            ]
            source = st.selectbox(
                "Source / Payment Method", 
                sources,
                help="Choose payment method or account source"
            )
            # Remove emoji for processing
            source_clean = " ".join(source.split(" ")[1:])
        
        with col6:
            description = st.text_input(
                "Description (Optional)",
                placeholder="Add notes or details...",
                help="Optional description for this transaction"
            )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Submit Button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            submitted = st.form_submit_button(
                "✨ Save Transaction", 
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            if amount > 0:
                success = save_transaction(
                    date, 
                    txn_type_clean, 
                    category_clean, 
                    source_clean, 
                    amount, 
                    description,
                    user_id=get_user_id()
                )
                if success:
                    st.markdown("""
                    <div class="success-animation">
                        <div style="text-align: center; padding: 20px; background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 12px; margin-top: 20px;">
                            <div style="font-size: 48px; margin-bottom: 10px;">✅</div>
                            <div style="font-size: 18px; font-weight: 700; color: #22c55e;">Transaction Saved Successfully!</div>
                            <div style="font-size: 13px; color: #94a3b8; margin-top: 5px;">Your transaction has been recorded</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state["refresh"] = True
                    st.balloons()
                else:
                    st.error("❌ Failed to save transaction. Please try again.")
            else:
                st.warning("⚠️ Please enter a valid amount greater than 0.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Tips Section
    st.markdown("""
    <div style="margin-top: 25px; padding: 20px; background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px;">
        <div style="font-size: 16px; font-weight: 700; color: #e5e7eb; margin-bottom: 10px;">💡 Quick Tips</div>
        <ul style="color: #cbd5e1; font-size: 13px; line-height: 1.8;">
            <li><strong>Freelancing (Mostaql):</strong> Track your freelance income from Mostaql platform</li>
            <li><strong>Regular Updates:</strong> Add transactions daily for accurate tracking</li>
            <li><strong>Categories:</strong> Use specific categories to analyze spending patterns</li>
            <li><strong>Descriptions:</strong> Add notes to remember transaction details later</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
