import streamlit as st
import pandas as pd
import requests

# --- Page Config ---
st.set_page_config(page_title="Investment Property P&L Calculator", layout="centered")

# --- Language Toggle ---
language = st.selectbox("Choose Language / 选择语言", ["English", "中文"], index=0)

# --- Text Dictionary ---
text = {
    "English": {
        "title": "Investment Property P&L Model",
        "currency_section": "Currency & FX Settings",
        "manual_fx": "Manually override FX rate?",
        "enter_fx": "Enter manual FX rate (MYR to NZD):",
        "property_section": "Property and Loan Details",
        "spa_price": "SPA Price (MYR)",
        "discount1": "Discount 1 (%)",
        "discount2": "Discount 2 (%)",
        "discount3": "Other Discount or Cashback (MYR)",
        "deposit_paid": "Initial Deposit Paid (MYR)",
        "loan_ratio": "Loan Ratio (%)",
        "interest_rate": "Interest Rate (%)",
        "loan_term": "Loan Term (Years)",
        "upfront_fees": "Upfront Costs",
        "stamp_duty": "Stamp Duty and Other Legal Fees (MYR)",
        "consent_fee": "Consent Fees (MYR)",
        "legal_fees": "Loan Legal Fees (MYR)",
        "min_bank_balance": "Minimum Bank Balance (MYR)",
        "cushion": "Cash Cushion (MYR)",
        "renovation": "Renovation Costs (MYR)",
        "rental_income": "Rental Income Estimation",
        "airbnb_rate": "Airbnb Rate per Night (MYR)",
        "utilisation_rate": "Utilisation Rate (%)",
        "mgmt_fee": "Airbnb Management Fee (Monthly MYR)",
        "results": "Results",
        "calculate": "Calculate",
        "reset": "Reset All Inputs",
        "net_net_price": "Net Net Price",
        "max_loan": "Maximum Loan Amount",
        "cash_deposit": "Cash Deposit (after loan)",
        "monthly_repayment": "Monthly Loan Repayment",
        "total_cash_required": "Total Cash Required (including all costs)",
        "gross_rent": "Gross Rental Income (Monthly)",
        "net_rent": "Net Rental Income (Monthly)",
        "monthly_profit": "Monthly Net Profit",
        "download_excel": "Download Results as Excel"
    },
    "中文": {
        "title": "投资房产盈亏模型",
        "currency_section": "货币与汇率设置",
        "manual_fx": "手动覆盖汇率？",
        "enter_fx": "输入手动汇率（马币兑纽币）:",
        "property_section": "房产与贷款详情",
        "spa_price": "买卖协议价格（MYR）",
        "discount1": "折扣1（%）",
        "discount2": "折扣2（%）",
        "discount3": "其他折扣或回扣（MYR）",
        "deposit_paid": "已支付定金（MYR）",
        "loan_ratio": "贷款比例（%）",
        "interest_rate": "贷款利率（%）",
        "loan_term": "贷款年限（年）",
        "upfront_fees": "前期费用设置",
        "stamp_duty": "印花税及其他法律费用（MYR）",
        "consent_fee": "同意书费用（MYR）",
        "legal_fees": "贷款律师费（MYR）",
        "min_bank_balance": "银行最低存款余额（MYR）",
        "cushion": "预备金（MYR）",
        "renovation": "装修费用（MYR）",
        "rental_income": "租金收入估算",
        "airbnb_rate": "Airbnb 每晚租金（MYR）",
        "utilisation_rate": "入住率（%）",
        "mgmt_fee": "Airbnb 管理费（每月MYR）",
        "results": "结果展示",
        "calculate": "点击计算",
        "reset": "重置所有输入",
        "net_net_price": "净净价格",
        "max_loan": "最大贷款金额",
        "cash_deposit": "贷款后现金支付",
        "monthly_repayment": "每月贷款还款",
        "total_cash_required": "总现金需求（包括所有费用）",
        "gross_rent": "每月毛租金收入",
        "net_rent": "每月净租金收入",
        "monthly_profit": "每月净盈利",
        "download_excel": "下载结果为Excel"
    }
}
t = text[language]

# --- App Title ---
st.title(t["title"])

# --- FX Section ---
with st.expander(t["currency_section"], expanded=True):
    manual_fx = st.checkbox(t["manual_fx"])
    if manual_fx:
        fx_rate = st.number_input(t["enter_fx"], value=0.31)
    else:
        try:
            res = requests.get("https://api.exchangerate.host/latest?base=MYR&symbols=NZD")
            fx_rate = res.json()["rates"]["NZD"]
        except:
            st.error("FX API Error, using default 0.31")
            fx_rate = 0.31

# --- Property Section ---
with st.expander(t["property_section"], expanded=True):
    spa_price = st.number_input(t["spa_price"], value=800000)
    col1, col2 = st.columns(2)
    with col1:
        discount1 = st.number_input(t["discount1"], value=10.0)
    with col2:
        discount2 = st.number_input(t["discount2"], value=5.0)
    discount3 = st.number_input(t["discount3"], value=0)
    deposit_paid = st.number_input(t["deposit_paid"], value=10000)
    loan_ratio = st.number_input(t["loan_ratio"], value=70.0)
    col3, col4 = st.columns(2)
    with col3:
        interest = st.number_input(t["interest_rate"], value=5.0)
    with col4:
        years = st.number_input(t["loan_term"], value=25)

# --- Upfront Costs Section ---
with st.expander(t["upfront_fees"], expanded=False):
    default_stamp = round(spa_price * 0.005, 2)
    stamp_duty = st.number_input(t["stamp_duty"], value=default_stamp)
    consent = st.number_input(t["consent_fee"], value=1000)
    legal = st.number_input(t["legal_fees"], value=3000)
    min_bal = st.number_input(t["min_bank_balance"], value=5000)
    cushion = st.number_input(t["cushion"], value=10000)
    renov = st.number_input(t["renovation"], value=15000)

# --- Rental Estimation Section ---
with st.expander(t["rental_income"], expanded=False):
    rate = st.number_input(t["airbnb_rate"], value=150)
    utilisation_col, mgmt_col = st.columns(2)
    with utilisation_col:
        util = st.number_input(t["utilisation_rate"], value=60.0)
    with mgmt_col:
        mgmt = st.number_input(t["mgmt_fee"], value=500)

# --- Calculate Button ---
if st.button(t["calculate"]):
    with st.spinner("Calculating..."):
        net_price = spa_price * (1 - discount1/100) * (1 - discount2/100) - discount3
        max_loan = net_price * loan_ratio / 100
        cash_deposit = net_price - max_loan - deposit_paid
        loan_amt = max_loan
        r = interest / 100 / 12
        n = years * 12
        monthly_repay = loan_amt * r * (1 + r)**n / ((1 + r)**n - 1)
        total_cash = (cash_deposit + stamp_duty + consent + legal +
                      min_bal + cushion + renov)
        gross_rent = rate * (util / 100) * 30
        net_rent = gross_rent - mgmt
        profit = net_rent - monthly_repay

        # --- Results ---
        st.subheader(t["results"])
        st.metric(t["net_net_price"], f"{net_price:,.2f} MYR")
        st.metric(t["max_loan"], f"{max_loan:,.2f} MYR")
        st.metric(t["cash_deposit"], f"{cash_deposit:,.2f} MYR")
        st.metric(t["monthly_repayment"], f"{monthly_repay:,.2f} MYR")
        st.metric(t["total_cash_required"], f"{total_cash:,.2f} MYR")
        st.metric(t["gross_rent"], f"{gross_rent:,.2f} MYR")
        st.metric(t["net_rent"], f"{net_rent:,.2f} MYR")
        st.metric(t["monthly_profit"], f"{profit:,.2f} MYR")

        # --- Download as Excel ---
        df = pd.DataFrame({
            "Category": [
                t["net_net_price"], t["max_loan"], t["cash_deposit"],
                t["monthly_repayment"], t["total_cash_required"],
                t["gross_rent"], t["net_rent"], t["monthly_profit"]
            ],
            "MYR Amount": [
                net_price, max_loan, cash_deposit, monthly_repay,
                total_cash, gross_rent, net_rent, profit
            ]
        })
        st.download_button(t["download_excel"], df.to_csv(index=False), "results.csv")

# --- Reset Button ---
if st.button(t["reset"]):
    st.experimental_rerun()
