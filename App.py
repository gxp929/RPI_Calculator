import streamlit as st import requests import pandas as pd import time

Language dictionary

translations = { "en": { "title": "Rental Property Investment Calculator", "language": "Language", "spa_price": "Sale and Purchase Agreement (SPA) Price (MYR)", "discount1": "Discount 1 (%)", "discount2": "Discount 2 (%)", "discount3": "Discount 3 (MYR)", "deposit_paid": "Deposit Paid (MYR)", "loan_ratio": "Loan Ratio (%)", "interest": "Interest Rate (%)", "years": "Loan Tenure (Years)", "stamp_duty": "Stamp Duty and Other Legal Fees (0.5% of SPA, editable)", "consent": "Consent Fee (MYR)", "legal": "Legal Fee (MYR)", "min_bal": "Minimum Bank Balance (MYR)", "cushion": "Cash Cushion (MYR)", "renov": "Renovation (MYR)", "rate": "Expected Rental Rate (MYR/day)", "util": "Occupancy Rate (%)", "mgmt": "Management Fees (MYR/month)", "currency_section": "Currency Exchange Settings", "manual_fx": "Manual FX Override", "calculate": "Calculate", "results": "Calculation Results", "net_net_price": "Net Net Property Price", "max_loan": "Maximum Loan Amount", "cash_deposit": "Cash Deposit Needed", "monthly_repayment": "Monthly Loan Repayment", "total_cash_required": "Total Cash Required", "gross_rent": "Gross Rental Income (Monthly)", "net_rent": "Net Rental Income (Monthly)", "monthly_profit": "Monthly Profit / Loss", "download_excel": "Download Results as CSV", "in_foreign_currency": "(in foreign currency)" }, "zh": { "title": "房产投资计算器", "language": "语言", "spa_price": "买卖协议价格 (MYR)", "discount1": "折扣 1 (%)", "discount2": "折扣 2 (%)", "discount3": "折扣 3 (MYR)", "deposit_paid": "已付订金 (MYR)", "loan_ratio": "贷款比例 (%)", "interest": "利率 (%)", "years": "贷款年限 (年)", "stamp_duty": "印花税及法律费用 (SPA 的 0.5%，可编辑)", "consent": "同意费 (MYR)", "legal": "法律费用 (MYR)", "min_bal": "最低银行余额 (MYR)", "cushion": "现金缓冲 (MYR)", "renov": "装修费 (MYR)", "rate": "预计租金 (MYR/天)", "util": "入住率 (%)", "mgmt": "管理费 (MYR/月)", "currency_section": "汇率设置", "manual_fx": "手动汇率覆盖", "calculate": "计算", "results": "计算结果", "net_net_price": "净房价", "max_loan": "最高贷款额度", "cash_deposit": "需付现金", "monthly_repayment": "每月贷款还款", "total_cash_required": "所需总现金", "gross_rent": "月租金收入 (总额)", "net_rent": "月租金收入 (净额)", "monthly_profit": "每月盈亏", "download_excel": "下载结果 (CSV)", "in_foreign_currency": "（以外币计）" } }

Language selection

lang = st.sidebar.selectbox("Select Language / 选择语言", ["en", "zh"]) t = translations[lang]

st.title(t["title"])

spa_price = st.number_input(t["spa_price"], value=800000.0) discount1 = st.number_input(t["discount1"], value=10.0) discount2 = st.number_input(t["discount2"], value=5.0) discount3 = st.number_input(t["discount3"], value=10000.0) deposit_paid = st.number_input(t["deposit_paid"], value=50000.0) loan_ratio = st.number_input(t["loan_ratio"], value=90.0) interest = st.number_input(t["interest"], value=5.0) years = st.number_input(t["years"], value=25) stamp_default = 0.005 * spa_price stamp_duty = st.number_input(t["stamp_duty"], value=stamp_default) consent = st.number_input(t["consent"], value=1000.0) legal = st.number_input(t["legal"], value=3000.0) min_bal = st.number_input(t["min_bal"], value=10000.0) cushion = st.number_input(t["cushion"], value=10000.0) renov = st.number_input(t["renov"], value=30000.0) rate = st.number_input(t["rate"], value=300.0) util = st.number_input(t["util"], value=70.0) mgmt = st.number_input(t["mgmt"], value=500.0)

FX Section

with st.expander(t["currency_section"], expanded=True): foreign_currency = st.text_input("Foreign Currency Code (e.g., NZD, SGD)", value="NZD") manual_fx = st.checkbox(t["manual_fx"]) if manual_fx: fx_rate = st.number_input(f"{foreign_currency} to MYR Exchange Rate", value=3.25) else: try: res = requests.get(f"https://api.exchangerate.host/latest?base={foreign_currency}&symbols=MYR") fx_rate = res.json()["rates"]["MYR"] except: st.error("FX API Error, using default rate") fx_rate = 3.25

if st.button(t["calculate"]): progress_text = "Processing inputs, please wait..." my_bar = st.progress(0, text=progress_text) for percent_complete in range(100): time.sleep(0.005) my_bar.progress(percent_complete + 1, text=progress_text) my_bar.empty()

net_price = spa_price * (1 - discount1/100) * (1 - discount2/100) - discount3
max_loan = net_price * loan_ratio / 100
cash_deposit = net_price - max_loan - deposit_paid
loan_amt = max_loan
r = interest / 100 / 12
n = years * 12
monthly_repay = loan_amt * r * (1 + r)**n / ((1 + r)**n - 1)
total_cash = (cash_deposit + stamp_duty + consent + legal + min_bal + cushion + renov)
gross_rent = rate * (util / 100) * 30
net_rent = gross_rent - mgmt
profit = net_rent - monthly_repay

st.subheader(t["results"])
st.metric(t["net_net_price"], f"{net_price:,.2f} MYR ({net_price/fx_rate:,.2f} {foreign_currency})")
st.metric(t["max_loan"], f"{max_loan:,.2f} MYR ({max_loan/fx_rate:,.2f} {foreign_currency})")
st.metric(t["cash_deposit"], f"{cash_deposit:,.2f} MYR ({cash_deposit/fx_rate:,.2f} {foreign_currency})")
st.metric(t["monthly_repayment"], f"{monthly_repay:,.2f} MYR ({monthly_repay/fx_rate:,.2f} {foreign_currency})")
st.metric(t["total_cash_required"], f"{total_cash:,.2f} MYR ({total_cash/fx_rate:,.2f} {foreign_currency})")
st.metric(t["gross_rent"], f"{gross_rent:,.2f} MYR ({gross_rent/fx_rate:,.2f} {foreign_currency})")
st.metric(t["net_rent"], f"{net_rent:,.2f} MYR ({net_rent/fx_rate:,.2f} {foreign_currency})")
st.metric(t["monthly_profit"], f"{profit:,.2f} MYR ({profit/fx_rate:,.2f} {foreign_currency})")

df = pd.DataFrame({
    "Category": [
        t["net_net_price"], t["max_loan"], t["cash_deposit"],
        t["monthly_repayment"], t["total_cash_required"],
        t["gross_rent"], t["net_rent"], t["monthly_profit"]
    ],
    "MYR Amount": [
        net_price, max_loan, cash_deposit, monthly_repay,
        total_cash, gross_rent, net_rent, profit
    ],
    f"{foreign_currency} Amount": [
        net_price/fx_rate, max_loan/fx_rate, cash_deposit/fx_rate,
        monthly_repay/fx_rate, total_cash/fx_rate,
        gross_rent/fx_rate, net_rent/fx_rate, profit/fx_rate
    ]
})

st.download_button(t["download_excel"], df.to_csv(index=False), "results.csv")

