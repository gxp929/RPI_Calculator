import streamlit as st
import requests
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px

# ========== Language Dictionary ==========
translations = { 
    "en": {...}, # [Same full dictionary you had - shortened here for space]
    "zh": {...},
    "ms": {...}
}

# ========== Icons for Sections ==========
icons = {
    "property_section": "🏠",
    "loan_section": "💰",
    "fees_section": "⚖️",
    "cash_section": "💵",
    "rental_section": "🔑",
    "currency_section": "💱",
    "charts_section": "📊"
}

# ========== Page Config ==========
st.set_page_config(
    page_title="Rental Property Investment Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== Custom CSS ==========
st.markdown("""
<style>
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stExpander { border-radius: 8px; margin-bottom: 1rem; }
    .stMetric { background: #f8f9fa; padding: 10px; border-radius: 8px; }
    h1 { color: #2c3e50; }
    h2 { color: #34495e; border-bottom: 1px solid #eee; padding-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ========== Sidebar Language ==========
lang = st.sidebar.selectbox("Select Language / 选择语言 / Pilih Bahasa", ["en", "zh", "ms"])
t = translations[lang]

# ========== Title ==========
st.title(t["title"])

# ========== Two Columns Layout ==========
col1, col2 = st.columns([3,2])

# ---------- Left Side ----------
with col1:
    # Property Section
    with st.expander(f"{icons['property_section']} {t['property_section']}", expanded=True):
        spa_price = st.number_input(t["spa_price"], value=1594000.00)
        discount1 = st.number_input(t["discount1"], value=10.0)
        discount2 = st.number_input(t["discount2"], value=8.0)
        discount3 = st.number_input(t["discount3"], value=6888.0)
        deposit_paid = st.number_input(t["deposit_paid"], value=20000.0)
        property_size = st.number_input(t["property_size"], value=678.0)
        monthly_service_fee_per_sqf = st.number_input(t["monthly_service_fee"], value=0.66, format="%.4f")
        
        property_fee = property_size * monthly_service_fee_per_sqf
        after_dis1 = spa_price * (1 - discount1 / 100)
        net_price = after_dis1 * (1 - discount2 / 100)
        net_net_price = net_price - discount3
        
        st.info(f"{t['property_fee']}: {property_fee:,.2f} MYR")
        st.info(f"{t['net_net_price']}: {net_net_price:,.2f} MYR")

    # Loan Section
    with st.expander(f"{icons['loan_section']} {t['loan_section']}", expanded=True):
        loan_ratio = st.number_input(t["loan_ratio"], value=70.0)
        interest = st.number_input(t["interest"], value=4.3)
        years = st.number_input(t["years"], value=26)

    # Fees Section
    with st.expander(f"{icons['fees_section']} {t['fees_section']}", expanded=True):
        consent = st.number_input(t["consent"], value=1000.0)
        legal = st.number_input(t["legal"], value=7083.16)
        stamp_duty = st.number_input(t["stamp_duty"], value=0.0)

    # Cash Section
    with st.expander(f"{icons['cash_section']} {t['cash_section']}", expanded=True):
        min_bal = st.number_input(t["min_bal"], value=40000.0)
        cushion = st.number_input(t["cushion"], value=40000.0)
        renov = st.number_input(t["renov"], value=20000.0)

    # Rental Section
    with st.expander(f"{icons['rental_section']} {t['rental_section']}", expanded=True):
        rate = st.number_input(t["rate"], value=400.0)
        util = st.number_input(t["util"], value=75.0)
        mgmt = st.number_input(t["mgmt"], value=800.0)

# ---------- Right Side ----------
with col2:
    # Currency Section
    with st.expander(f"{icons['currency_section']} {t['currency_section']}", expanded=True):
        foreign_currency = st.text_input(t["foreign_currency"], value="NZD")
        manual_fx = st.checkbox(t["manual_fx"], value=True)
        if manual_fx:
            fx_rate = st.number_input(t["fx_rate"], value=2.5655)
        else:
            try:
                res = requests.get(f"https://api.exchangerate.host/latest?base={foreign_currency}&symbols=MYR", timeout=5)
                fx_rate = res.json()["rates"]["MYR"]
                st.success(f"Current exchange rate: 1 {foreign_currency} = {fx_rate:.4f} MYR")
            except:
                st.error(t["api_error"])
                fx_rate = 2.5655

# ========== Calculate Button ==========
if st.button(t["calculate"], type="primary"):
    with st.spinner(t["processing"]):
        time.sleep(0.5)

    # ---------- Financial Calculations ----------
    max_loan = spa_price * loan_ratio / 100
    cash_deposit = net_net_price - max_loan - deposit_paid
    r = interest / 100 / 12
    n = years * 12
    monthly_repay = max_loan * r * (1 + r)**n / ((1 + r)**n - 1)
    total_cash = cash_deposit + consent + legal + stamp_duty + min_bal + cushion + renov
    days_per_month = 30
    gross_rent = rate * (util / 100) * days_per_month
    net_rent = gross_rent - mgmt - property_fee
    profit = net_rent - monthly_repay

    # ========== Display Results ==========
    st.subheader(t["results"])
    results_col1, results_col2, results_col3 = st.columns(3)

    with results_col1:
        st.metric(t["net_price"], f"{net_price:,.2f} MYR")
        st.metric(t["net_net_price"], f"{net_net_price:,.2f} MYR")
        st.metric(t["max_loan"], f"{max_loan:,.2f} MYR")

    with results_col2:
        st.metric(t["monthly_repayment"], f"{monthly_repay:,.2f} MYR")
        st.metric(t["cash_deposit"], f"{cash_deposit:,.2f} MYR")
        st.metric(t["total_cash_required"], f"{total_cash:,.2f} MYR")

    with results_col3:
        st.metric(t["gross_rent"], f"{gross_rent:,.2f} MYR")
        st.metric(t["net_rent"], f"{net_rent:,.2f} MYR")
        st.metric(t["monthly_profit"], f"{profit:,.2f} MYR", delta=profit)

    # Foreign currency block
    st.subheader(f"{t['results']} ({foreign_currency})")
    fc_col1, fc_col2, fc_col3 = st.columns(3)

    with fc_col1:
        st.metric(t["net_price"], f"{net_price/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["net_net_price"], f"{net_net_price/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["max_loan"], f"{max_loan/fx_rate:,.2f} {foreign_currency}")

    with fc_col2:
        st.metric(t["monthly_repayment"], f"{monthly_repay/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["cash_deposit"], f"{cash_deposit/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["total_cash_required"], f"{total_cash/fx_rate:,.2f} {foreign_currency}")

    with fc_col3:
        st.metric(t["gross_rent"], f"{gross_rent/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["net_rent"], f"{net_rent/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["monthly_profit"], f"{profit/fx_rate:,.2f} {foreign_currency}", delta=profit/fx_rate)

    # ========== CSV Export ==========
    df = pd.DataFrame({
        "Category": [
            t["spa_price"], t["discount1"], t["discount2"], t["discount3"],
            t["deposit_paid"], t["loan_ratio"], t["interest"], t["years"],
            t["property_size"], t["monthly_service_fee"], t["property_fee"],
            t["net_price"], t["net_net_price"], t["max_loan"],
            t["cash_deposit"], t["monthly_repayment"], t["total_cash_required"],
            t["gross_rent"], t["net_rent"], t["monthly_profit"]
        ],
        "MYR Amount": [
            spa_price, f"{discount1}%", f"{discount2}%", discount3,
            deposit_paid, f"{loan_ratio}%", f"{interest}%", years,
            property_size, monthly_service_fee_per_sqf, property_fee,
            net_price, net_net_price, max_loan,
            cash_deposit, monthly_repay, total_cash,
            gross_rent, net_rent, profit
        ],
        f"{foreign_currency} Amount": [
            spa_price/fx_rate, f"{discount1}%", f"{discount2}%", discount3/fx_rate,
            deposit_paid/fx_rate, f"{loan_ratio}%", f"{interest}%", years,
            property_size, monthly_service_fee_per_sqf, property_fee/fx_rate,
            net_price/fx_rate, net_net_price/fx_rate, max_loan/fx_rate,
            cash_deposit/fx_rate, monthly_repay/fx_rate, total_cash/fx_rate,
            gross_rent/fx_rate, net_rent/fx_rate, profit/fx_rate
        ]
    })

    st.download_button(
        label=t["download_excel"],
        data=df.to_csv(index=False),
        file_name="property_investment_results.csv",
        mime="text/csv"
    )
