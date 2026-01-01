APP_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Main Background */
.stApp {
    background: radial-gradient(circle at top, #151a2f 0, #020617 45%, #020617 100%);
    color: #e5e7eb;
    font-family: 'Inter', sans-serif;
}

.main .block-container {
    max-width: 1600px;
    padding-top: 1.5rem;
}

/* Hero Section */
.hero-premium {
    padding: 30px 34px;
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        rgba(88, 80, 236, 0.35) 0%,
        rgba(236, 72, 153, 0.22) 55%,
        rgba(15, 23, 42, 0.98) 100%
    );
    border: 1px solid rgba(129, 140, 248, 0.55);
    box-shadow:
        0 20px 70px rgba(15, 23, 42, 0.9),
        0 0 120px rgba(129, 140, 248, 0.4);
    backdrop-filter: blur(16px);
    margin-bottom: 26px;
    text-align: center;
}

.hero-title-pro {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: 0.02em;
    background: linear-gradient(120deg, #e5e7eb 0%, #e0f2fe 30%, #f9a8d4 60%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.hero-subtitle-pro {
    font-size: 15px;
    color: #cbd5e1;
    line-height: 1.7;
    margin: 0 auto;
    max-width: 840px;
}

/* KPI Cards */
.kpi-premium {
    padding: 22px 20px;
    border-radius: 20px;
    background: radial-gradient(circle at top left, rgba(129, 140, 248, 0.16), rgba(15, 23, 42, 0.96));
    border: 1px solid rgba(148, 163, 184, 0.5);
    box-shadow: 0 14px 40px rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(12px);
    transition: all 0.22s ease;
    height: 100%;
}

.kpi-premium:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 60px rgba(30, 64, 175, 0.7);
}

.kpi-icon {
    font-size: 26px;
    margin-bottom: 6px;
}

.kpi-label-pro {
    font-size: 11px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600;
    margin-bottom: 6px;
}

.kpi-value-pro {
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(130deg, #e5e7eb 0%, #bfdbfe 40%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.kpi-trend {
    font-size: 11px;
    color: #22c55e;
    margin-top: 2px;
}

/* Section Headers */
.section-header-pro {
    font-size: 22px;
    font-weight: 800;
    color: #e5e7eb;
    margin: 24px 0 6px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.5);
}

.section-desc-pro {
    font-size: 13px;
    color: #9ca3af;
    margin-bottom: 16px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: radial-gradient(circle at top, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.9));
    padding: 8px;
    border-radius: 999px;
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 999px;
    padding: 8px 24px;
    background: transparent;
    color: #9ca3af;
    font-size: 14px;
    font-weight: 600;
    border: none;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    color: #f9fafb !important;
    box-shadow: 0 4px 16px rgba(129, 140, 248, 0.6);
}

/* UI Elements overrides */
div[data-testid="stMetricValue"] {
    font-size: 20px;
}
</style>
"""

def kpi_card_html(icon, label, value, trend=""):
    return f"""
    <div class="kpi-premium">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label-pro">{label}</div>
        <div class="kpi-value-pro">{value}</div>
        <div class="kpi-trend">{trend}</div>
    </div>
    """
