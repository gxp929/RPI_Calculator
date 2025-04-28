import streamlit as st
import pandas as pd
import requests

# ----------------- Language Dictionary ------------------
def load_translations():
    return {
        "en": {...},
        "zh": {...},
        "ms": {...}
    }

translations = load_translations()

# ----------------- Helper Functions ------------------
def calculate_stamp_duty(price):
    if price <= 100000:
        return price * 0.01
    elif price <= 500000:
        return 1000 + (price - 100000) * 0.02
    elif price <= 1000000:
        return 9000 + (price - 500000) * 0.03
    else:
        return 24000 + (price - 1000000) * 0.04

def monthly_repayment(principal, annual_rate, tenure_years):
    r = annual_rate / 100 / 12
    n = tenure_years * 12
    return principal * r * (1 + r)**n / ((1 + r)**n - 1)

def fetch_fx_rate(base_currency):
    try:
        res = requests.get(f"https://api.exchangerate.host/latest?base={base_currency}&symbols=MYR", timeout=5)
        return res.json()["rates"]["MYR"]
    except:
        return None

# ----------------- Main App ------------------
st.set_page_config(page_title="Property Investment Calculator", layout="wide")

lang = st.sidebar.selectbox("Select Language / 选择语言 / Pilih Bahasa", ["en", "zh", "ms"])
t = translations[lang]

st.title(t["title"])

col1, col2 = st.columns([3,2])

with col1:
    spa_price = st.number_input(t["spa_price"], value=1594000.0)
    discount1 = st.number_input(t["discount1"], value=10.0, format="%.2f")
    discount2 = st.number_input(t["discount2"], value=8.0, format="%.2f")
    discount3 = st.number_input(t["discount3"], value=6888.0)
    deposit_paid = st.number_input(t["deposit_paid"], value=20000.0)
    property_size = st.number_input(t["property_size"], value=678.0)
    monthly_service_fee_per_sqf = st.number_input(t["monthly_service_fee"], value=0.66, format="%.4f")
    property_fee = property_size * monthly_service_fee_per_sqf
    st.caption(f"{t['property_fee']}: {property_fee:,.2f} MYR")

    loan_ratio = st.number_input(t["loan_ratio"], value=70.0, format="%.2f")
    interest = st.number_input(t["interest"], value=4.3, format="%.2f")
    years = st.number_input(t["years"], value=26)

    consent = st.number_input(t["consent"], value=1000.0)
    legal = st.number_input(t["legal"], value=7083.16)
    stamp_duty_input = st.number_input(t["stamp_duty"], value=0.0)

    min_bal = st.number_input(t["min_bal"], value=40000.0)
    cushion = st.number_input(t["cushion"], value=40000.0)
    renov = st.number_input(t["renov"], value=20000.0)

    rate = st.number_input(t["rate"], value=400.0)
    util = st.number_input(t["util"], value=75.0, format="%.2f")
    mgmt = st.number_input(t["mgmt"], value=800.0)

with col2:
    foreign_currency = st.text_input(t["foreign_currency"], value="NZD")
    manual_fx = st.checkbox(t["manual_fx"], value=True)
    fx_rate = st.number_input(t["fx_rate"], value=2.5655) if manual_fx else fetch_fx_rate(foreign_currency) or 2.5655

# ----------------- Calculations ------------------

after_dis1 = spa_price * (1 - discount1/100)
net_price = after_dis1 * (1 - discount2/100)
net_net_price = net_price - discount3

stamp_duty = stamp_duty_input if stamp_duty_input > 0 else calculate_stamp_duty(net_net_price)

max_loan = spa_price * loan_ratio / 100
cash_deposit = net_net_price - max_loan - deposit_paid
monthly_repay = monthly_repayment(max_loan, interest, years)
total_cash = cash_deposit + consent + legal + stamp_duty + min_bal + cushion + renov

gross_rent = rate * (util/100) * 30
net_rent = gross_rent - mgmt - property_fee
profit = net_rent - monthly_repay

# ----------------- Display Results ------------------

st.subheader(t["results"])

colA, colB, colC = st.columns(3)
with colA:
    st.metric(t["net_price"], f"{net_price:,.2f} MYR")
    st.metric(t["net_net_price"], f"{net_net_price:,.2f} MYR")
    st.metric(t["max_loan"], f"{max_loan:,.2f} MYR")
with colB:
    st.metric(t["monthly_repayment"], f"{monthly_repay:,.2f} MYR")
    st.metric(t["cash_deposit"], f"{cash_deposit:,.2f} MYR")
    st.metric(t["total_cash_required"], f"{total_cash:,.2f} MYR")
with colC:
    st.metric(t["gross_rent"], f"{gross_rent:,.2f} MYR")
    st.metric(t["net_rent"], f"{net_rent:,.2f} MYR")
    st.metric(t["monthly_profit"], f"{profit:,.2f} MYR", delta=profit)

st.subheader(f"{t['results']} ({foreign_currency})")

colFA, colFB, colFC = st.columns(3)
with colFA:
    st.metric(t["net_price"], f"{net_price/fx_rate:,.2f} {foreign_currency}")
    st.metric(t["net_net_price"], f"{net_net_price/fx_rate:,.2f} {foreign_currency}")
    st.metric(t["max_loan"], f"{max_loan/fx_rate:,.2f} {foreign_currency}")
with colFB:
    st.metric(t["monthly_repayment"], f"{monthly_repay/fx_rate:,.2f} {foreign_currency}")
    st.metric(t["cash_deposit"], f"{cash_deposit/fx_rate:,.2f} {foreign_currency}")
    st.metric(t["total_cash_required"], f"{total_cash/fx_rate:,.2f} {foreign_currency}")
with colFC:
    st.metric(t["gross_rent"], f"{gross_rent/fx_rate:,.2f} {foreign_currency}")
    st.metric(t["net_rent"], f"{net_rent/fx_rate:,.2f} {foreign_currency}")
    st.metric(t["monthly_profit"], f"{profit/fx_rate:,.2f} {foreign_currency}", delta=profit/fx_rate)

# ----------------- CSV Download ------------------

df = pd.DataFrame({
    "Category": [
        "SPA Price", "Discount 1", "Discount 2", "Discount 3", "Deposit Paid",
        "Loan Ratio", "Interest Rate", "Loan Tenure (Years)",
        "Property Size (sqf)", "Monthly Service Fee (per sqf)", "Property Fee",
        "Net Price", "Net Net Price", "Maximum Loan", "Cash Deposit", 
        "Monthly Repayment", "Total Cash Required", "Gross Rent", "Net Rent", "Monthly Profit"
    ],
    "MYR": [
        spa_price, f"{discount1}%", f"{discount2}%", discount3, deposit_paid,
        f"{loan_ratio}%", f"{interest}%", years,
        property_size, monthly_service_fee_per_sqf, property_fee,
        net_price, net_net_price, max_loan, cash_deposit,
        monthly_repay, total_cash, gross_rent, net_rent, profit
    ],
    f"{foreign_currency}": [
        spa_price/fx_rate, f"{discount1}%", f"{discount2}%", discount3/fx_rate, deposit_paid/fx_rate,
        f"{loan_ratio}%", f"{interest}%", years,
        property_size, monthly_service_fee_per_sqf, property_fee/fx_rate,
        net_price/fx_rate, net_net_price/fx_rate, max_loan/fx_rate, cash_deposit/fx_rate,
        monthly_repay/fx_rate, total_cash/fx_rate, gross_rent/fx_rate, net_rent/fx_rate, profit/fx_rate
    ]
})

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label=t["download_excel"],
    data=csv,
    file_name="property_investment_summary.csv",
    mime="text/csv",
)
