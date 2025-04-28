import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# Language dictionary (truncated for brevity, keep your full dictionary here)
translations = {
    "en": {
        # ... (your full translation dictionary here)
    },
    "zh": {
        # ... (your full translation dictionary here)
    },
    "ms": {
        # ... (your full translation dictionary here)
    }
}

# Set page configuration
st.set_page_config(
    page_title="Property Investment Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar language selection
lang = st.sidebar.selectbox("Select Language / 选择语言 / Pilih Bahasa", ["en", "zh", "ms"])
t = translations[lang]

# App title
st.title(t["title"])

# Main content in two columns
col1, col2 = st.columns([3, 2])

with col1:
    # Property Details Section
    with st.expander("🏠 " + t["property_section"], expanded=True):
        spa_price = st.number_input(t["spa_price"], value=1594000.00)
        discount1 = st.number_input(t["discount1"], value=10.0)
        discount2 = st.number_input(t["discount2"], value=8.0)
        discount3 = st.number_input(t["discount3"], value=6888.0)
        deposit_paid = st.number_input(t["deposit_paid"], value=20000.0)
        property_size = st.number_input(t["property_size"], value=678.0)
        monthly_service_fee_per_sqf = st.number_input(
            t["monthly_service_fee"], value=0.66, min_value=0.0, format="%.4f"
        )
        property_fee = property_size * monthly_service_fee_per_sqf
        st.info(f"{t['property_fee']}: {property_fee:,.2f} MYR")
        
    # Loan Details Section
    with st.expander("💰 " + t["loan_section"], expanded=True):
        loan_ratio = st.number_input(t["loan_ratio"], value=70.0)
        interest = st.number_input(t["interest"], value=4.3)
        years = st.number_input(t["years"], value=26)
        
    # Legal Fees & Costs Section
    with st.expander("📜 " + t["fees_section"], expanded=True):
        consent = st.number_input(t["consent"], value=1000.0)
        legal = st.number_input(t["legal"], value=7083.16)
        stamp_duty = st.number_input(t["stamp_duty"], value=0.0)  # Editable

    # Cash Requirements Section
    with st.expander("💵 " + t["cash_section"], expanded=True):
        min_bal = st.number_input(t["min_bal"], value=40000.0)
        cushion = st.number_input(t["cushion"], value=40000.0)
        renov = st.number_input(t["renov"], value=20000.0)

    # Rental Expectations Section
    with st.expander("📈 " + t["rental_section"], expanded=True):
        rate = st.number_input(t["rate"], value=400.0)
        util = st.number_input(t["util"], value=75.0)
        mgmt = st.number_input(t["mgmt"], value=800.0)

with col2:
    # Currency section
    with st.expander("💱 " + t["currency_section"], expanded=True):
        foreign_currency = st.text_input(t["foreign_currency"], value="NZD")
        manual_fx = st.checkbox(t["manual_fx"], value=True)
        if manual_fx:
            fx_rate = st.number_input(t["fx_rate"], value=2.5655)
        else:
            try:
                res = requests.get(f"https://api.exchangerate.host/latest?base={foreign_currency}&symbols=MYR")
                fx_rate = res.json()["rates"]["MYR"]
                st.success(f"Current exchange rate: 1 {foreign_currency} = {fx_rate:.4f} MYR")
            except:
                st.error(t["api_error"])
                fx_rate = 2.5655

# Calculate button
if st.button(t["calculate"], type="primary"):
    progress_text = t["processing"]
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()

    # --- Financial calculations ---
    # Property price calculations
    after_dis1 = spa_price * (1 - discount1/100)
    net_price = after_dis1 * (1 - discount2/100)
    net_net_price = net_price - discount3

    # Show net net price as info (make it prominent)
    st.info(f"💡 {t['net_net_price']}: {net_net_price:,.2f} MYR")

    # Loan calculations
    max_loan = spa_price * loan_ratio / 100
    cash_deposit = net_net_price - max_loan - deposit_paid
    balance = net_net_price - deposit_paid

    # Monthly payment calculation
    r = interest / 100 / 12
    n = years * 12
    monthly_repay = max_loan * r * (1 + r)**n / ((1 + r)**n - 1)

    # Cash requirements
    total_cash = cash_deposit + consent + legal + min_bal + cushion + renov

    # Rental income
    days_per_month = 30
    gross_rent = rate * (util / 100) * days_per_month
    net_rent = gross_rent - mgmt - property_fee
    profit = net_rent - monthly_repay

    # --- Display results ---
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
        st.metric(t["monthly_profit"], f"{profit:,.2f} MYR", delta=round(profit, 2))

    # Display foreign currency equivalents
    st.subheader(f"{t['results']} ({foreign_currency})")
    fc_results_col1, fc_results_col2, fc_results_col3 = st.columns(3)
    with fc_results_col1:
        st.metric(t["net_price"], f"{net_price/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["net_net_price"], f"{net_net_price/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["max_loan"], f"{max_loan/fx_rate:,.2f} {foreign_currency}")
    with fc_results_col2:
        st.metric(t["monthly_repayment"], f"{monthly_repay/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["cash_deposit"], f"{cash_deposit/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["total_cash_required"], f"{total_cash/fx_rate:,.2f} {foreign_currency}")
    with fc_results_col3:
        st.metric(t["gross_rent"], f"{gross_rent/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["net_rent"], f"{net_rent/fx_rate:,.2f} {foreign_currency}")
        st.metric(t["monthly_profit"], f"{profit/fx_rate:,.2f} {foreign_currency}", delta=round(profit/fx_rate, 2))

    # --- Graphs and Charts ---
    st.markdown("### 📊 Visualizations")

    # Pie chart: Upfront cash requirements
    labels = ['Cash Deposit', 'Consent Fee', 'Legal Fees', 'Min Bank Balance', 'Cash Cushion', 'Renovation']
    values = [cash_deposit, consent, legal, min_bal, cushion, renov]
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)
    st.caption("Breakdown of Upfront Cash Requirements")

    # Bar chart: Rental income vs. expenses
    rent_labels = ['Gross Rent', 'Mgmt Fee', 'Property Fee', 'Net Rent']
    rent_values = [gross_rent, mgmt, property_fee, net_rent]
    rent_df = pd.DataFrame({'Amount': rent_values}, index=rent_labels)
    st.bar_chart(rent_df)
    st.caption("Monthly Rental Income and Expenses Breakdown")

    # Line chart: Cumulative profit/loss over loan tenure
    months = np.arange(1, n+1)
    cumulative_profit = np.cumsum([profit] * n)
    st.line_chart(pd.DataFrame({'Cumulative Profit/Loss': cumulative_profit}, index=months))
    st.caption("Cumulative Profit/Loss Over Loan Tenure")

    # --- CSV Export ---
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
        t["download_excel"],
        df.to_csv(index=False),
        "property_investment_results.csv",
        mime="text/csv"
    )
