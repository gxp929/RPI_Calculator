import streamlit as st import requests

--- Input Fields ---

st.title("Investment Property P&L Model")

st.subheader("Currency & FX") manual_fx = st.checkbox("Manually override FX rate?")

if manual_fx: fx_rate = st.number_input("Enter manual FX rate (MYR to NZD):", value=2.5655) else: try: res = requests.get("https://api.exchangerate.host/latest?base=MYR&symbols=NZD") fx_rate = res.json()['rates']['NZD'] st.info(f"Live FX Rate: 1 MYR = {fx_rate:.4f} NZD") except: fx_rate = 2.5655 st.warning("Failed to fetch FX rate. Using default: 2.5655")

st.subheader("Property & Loan Details") spa = st.number_input("SPA Price (MYR)", value=1594000.00) discount1 = st.number_input("Discount 1 (%)", value=10.0) / 100 discount2 = st.number_input("Discount 2 (%)", value=8.0) / 100 red_env_dis3 = st.number_input("Redemption/Environmental Discount (MYR)", value=6888.00) deposit_paid = st.number_input("Initial Deposit Paid (MYR)", value=20000.00) loan_ratio = st.number_input("Loan Ratio (%)", value=70.0) / 100 interest_rate = st.number_input("Interest Rate (%)", value=4.30) / 100 loan_term_years = st.number_input("Loan Term (Years)", value=26, step=1)

--- Price Calculations ---

after_dis1 = spa * (1 - discount1) after_dis2 = after_dis1 * (1 - discount2) net_net_price = after_dis2 - red_env_dis3 max_loan_amount = net_net_price * loan_ratio balance_to_pay = net_net_price - deposit_paid cash_deposit = balance_to_pay - max_loan_amount

--- Loan Calculations ---

monthly_interest_rate = interest_rate / 12 n_months = loan_term_years * 12 monthly_repayment = max_loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -n_months)

--- Upfront Costs ---

consent_fee = st.number_input("Consent Fee (MYR)", value=1000.00) legal_fees = st.number_input("Loan Legal Fees (MYR)", value=7083.16) min_bank_balance = st.number_input("Min Bank A/C Balance (MYR)", value=40000.00) cushion = st.number_input("Cushion (MYR)", value=40000.00) renovation = st.number_input("Renovation Cost (MYR)", value=20000.00)

total_cash_required = cash_deposit + consent_fee + legal_fees + min_bank_balance + cushion + renovation

--- Airbnb Income ---

st.subheader("Rental Income") airbnb_rate = st.number_input("Airbnb Rate per Night (MYR)", value=400.00) utilisation_rate = st.number_input("Utilisation Rate (%)", value=75.0) / 100 mgmt_fee = st.number_input("Airbnb Mgmt Fee per Month (MYR)", value=800.00)

gross_rental_monthly = airbnb_rate * 30 * utilisation_rate net_income_monthly = gross_rental_monthly - mgmt_fee monthly_profit = net_income_monthly - monthly_repayment

--- Outputs ---

st.subheader("Results") st.write(f"Net Net Price: MYR {net_net_price:,.2f} / NZD {net_net_price / fx_rate:,.2f}") st.write(f"Max Loan Amount (70%): MYR {max_loan_amount:,.2f} / NZD {max_loan_amount / fx_rate:,.2f}") st.write(f"Cash Deposit (after loan): MYR {cash_deposit:,.2f} / NZD {cash_deposit / fx_rate:,.2f}") st.write(f"Monthly Repayment: MYR {monthly_repayment:,.2f}") st.write(f"Total Cash Upfront Required: MYR {total_cash_required:,.2f} / NZD {total_cash_required / fx_rate:,.2f}") st.write(f"Gross Rental (Monthly): MYR {gross_rental_monthly:,.2f}") st.write(f"Net Rental Income (Monthly): MYR {net_income_monthly:,.2f}") st.write(f"Profit (Monthly): MYR {monthly_profit:,.2f}")

