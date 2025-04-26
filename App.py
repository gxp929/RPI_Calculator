import streamlit as st
import requests

# --- 语言选择 / Language Toggle ---
language = st.selectbox("Choose Language / 选择语言", ["English", "中文"], index=0)

# --- 文本字典 / Text Dictionary ---
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
        "net_net_price": "Net Net Price",
        "max_loan": "Maximum Loan Amount (70%)",
        "cash_deposit": "Cash Deposit (after loan)",
        "monthly_repayment": "Monthly Loan Repayment",
        "total_cash_required": "Total Cash Required (including all costs)",
        "gross_rent": "Gross Rental Income (Monthly)",
        "net_rent": "Net Rental Income (Monthly)",
        "monthly_profit": "Monthly Net Profit"
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
        "net_net_price": "净净价格",
        "max_loan": "最大贷款金额 (70%)",
        "cash_deposit": "贷款后现金支付",
        "monthly_repayment": "每月贷款还款",
        "total_cash_required": "总现金需求（包括所有费用）",
        "gross_rent": "每月毛租金收入",
        "net_rent": "每月净租金收入",
        "monthly_profit": "每月净盈利"
    }
}

t = text[language]

# --- 应用标题 ---
st.title(t["title"])

# --- 货币与汇率设置 ---
st.subheader(t["currency_section"])
manual_fx = st.checkbox(t["manual_fx"])

if manual_fx:
    fx_rate = st.number_input(t["enter_fx"], value=2.5655, format="%.4f", step=0.0001, help="Enter manual FX rate", key="manual_fx",  use_container_width=True)
else:
    try:
        res = requests.get("https://api.exchangerate.host/latest?base=MYR&symbols=NZD")
        fx_rate = res.json()['rates']['NZD']
        st.info(f"Live FX rate: 1 MYR = {fx_rate:.4f} NZD")
    except:
        fx_rate = 2.5655
        st.warning("Failed to fetch live FX. Default 2.5655 used.")

# --- 房产与贷款详情 ---
st.subheader(t["property_section"])
spa = st.number_input(t["spa_price"], value=1594000.00, step=10000.0, use_container_width=True)
discount1 = st.number_input(t["discount1"], value=10.0, step=0.1, use_container_width=True) / 100
discount2 = st.number_input(t["discount2"], value=8.0, step=0.1, use_container_width=True) / 100
red_env_dis3 = st.number_input(t["discount3"], value=6888.00, step=100.0, use_container_width=True)
deposit_paid = st.number_input(t["deposit_paid"], value=20000.00, step=1000.0, use_container_width=True)
loan_ratio = st.number_input(t["loan_ratio"], value=70.0, step=1.0, use_container_width=True) / 100
interest_rate = st.number_input(t["interest_rate"], value=4.30, step=0.01, use_container_width=True) / 100
loan_term_years = st.number_input(t["loan_term"], value=26, step=1, use_container_width=True)

# --- 价格计算 ---
after_dis1 = spa * (1 - discount1)
after_dis2 = after_dis1 * (1 - discount2)
net_net_price = after_dis2 - red_env_dis3
max_loan_amount = net_net_price * loan_ratio
balance_to_pay = net_net_price - deposit_paid
cash_deposit = balance_to_pay - max_loan_amount

# --- 前期费用 ---
st.subheader(t["upfront_fees"])
# Stamp duty pre-calculate
default_stamp_duty = spa * 0.005
stamp_duty = st.number_input(t["stamp_duty"], value=default_stamp_duty, step=100.0, use_container_width=True)
consent_fee = st.number_input(t["consent_fee"], value=1000.00, step=100.0, use_container_width=True)
legal_fees = st.number_input(t["legal_fees"], value=7083.16, step=100.0, use_container_width=True)
min_bank_balance = st.number_input(t["min_bank_balance"], value=40000.00, step=1000.0, use_container_width=True)
cushion = st.number_input(t["cushion"], value=40000.00, step=1000.0, use_container_width=True)
renovation = st.number_input(t["renovation"], value=20000.00, step=1000.0, use_container_width=True)

total_cash_required = cash_deposit + stamp_duty + consent_fee + legal_fees + min_bank_balance + cushion + renovation

# --- 租金收入估算 ---
st.subheader(t["rental_income"])
airbnb_rate = st.number_input(t["airbnb_rate"], value=400.00, step=10.0, use_container_width=True)
utilisation_rate = st.number_input(t["utilisation_rate"], value=75.0, step=1.0, use_container_width=True) / 100
mgmt_fee = st.number_input(t["mgmt_fee"], value=800.00, step=50.0, use_container_width=True)

gross_rental_monthly = airbnb_rate * 30 * utilisation_rate
net_income_monthly = gross_rental_monthly - mgmt_fee
monthly_profit = net_income_monthly - monthly_repayment

# --- 输出结果 ---
st.subheader(t["results"])
st.write(f"**{t['net_net_price']}:** MYR {net_net_price:,.2f} / NZD {net_net_price / fx_rate:,.2f}")
st.write(f"**{t['max_loan']}:** MYR {max_loan_amount:,.2f} / NZD {max_loan_amount / fx_rate:,.2f}")
st.write(f"**{t['cash_deposit']}:** MYR {cash_deposit:,.2f} / NZD {cash_deposit / fx_rate:,.2f}")
st.write(f"**{t['monthly_repayment']}:** MYR {monthly_repayment:,.2f}")
st.write(f"**{t['total_cash_required']}:** MYR {total_cash_required:,.2f} / NZD {total_cash_required / fx_rate:,.2f}")
st.write(f"**{t['gross_rent']}:** MYR {gross_rental_monthly:,.2f}")
st.write(f"**{t['net_rent']}:** MYR {net_income_monthly:,.2f}")
st.write(f"**{t['monthly_profit']}:** MYR {monthly_profit:,.2f}")
