import streamlit as st
import requests
import pandas as pd
import time

# Language dictionary
translations = {
    "en": {
        "title": "Rental Property Investment Calculator",
        "language": "Language",
        "property_section": "Property Details",
        "spa_price": "Sale and Purchase Agreement (SPA) Price (MYR)",
        "discount1": "Discount 1 (%)",
        "discount2": "Discount 2 (%)",
        "discount3": "Discount 3 (MYR) - Environmental Fee",
        "deposit_paid": "Deposit Paid (MYR)",
        "loan_section": "Loan Details",
        "loan_ratio": "Loan Ratio (%)",
        "interest": "Interest Rate (%)",
        "years": "Loan Tenure (Years)",
        "fees_section": "Legal Fees & Costs",
        "stamp_duty": "Stamp Duty and Other Legal Fees (editable)",
        "consent": "Consent Fee (MYR)",
        "legal": "Loan Documentation Legal Fees (MYR)",
        "cash_section": "Cash Requirements",
        "min_bal": "Required Minimum Bank Balance (MYR)",
        "cushion": "Cash Cushion (MYR)",
        "renov": "Renovation Cost (MYR)",
        "property_details": "Property Details",
        "property_size": "Property Size (sqf)",
        "property_fee": "Property Fee (per Month)",
        "rental_section": "Rental Expectations",
        "rate": "Airbnb Rate (MYR/night)",
        "util": "Utilisation Rate (%)",
        "mgmt": "Cost incl. Airbnb Management Fee (MYR/month)",
        "currency_section": "Currency Exchange Settings",
        "foreign_currency": "Foreign Currency Code (e.g., NZD, SGD)",
        "manual_fx": "Manual FX Override",
        "fx_rate": "Exchange Rate (Foreign Currency → MYR)",
        "calculate": "Calculate",
        "results": "Calculation Results",
        "net_price": "Net Price (after Discount 1 & 2)",
        "net_net_price": "Net Net Price (after all discounts)",
        "max_loan": "Maximum Loan Amount",
        "cash_deposit": "Cash Deposit Needed",
        "monthly_repayment": "Monthly Loan Repayment",
        "total_cash_required": "Total Cash Upfront Required",
        "gross_rent": "Gross Rental Income (Monthly)",
        "net_rent": "Net Rental Income (Monthly)",
        "monthly_profit": "Monthly Profit / Loss",
        "download_excel": "Download Results as CSV",
        "in_foreign_currency": "(in foreign currency)",
        "processing": "Processing inputs, please wait...",
        "api_error": "FX API Error, using default rate"
    },
    "zh": {
        "title": "房产投资计算器",
        "language": "语言",
        "property_section": "房产详情",
        "spa_price": "买卖协议价格 (MYR)",
        "discount1": "折扣 1 (%)",
        "discount2": "折扣 2 (%)",
        "discount3": "折扣 3 (MYR) - 环境费",
        "deposit_paid": "已支付订金 (MYR)",
        "loan_section": "贷款详情",
        "loan_ratio": "贷款比例 (%)",
        "interest": "利率 (%)",
        "years": "贷款期限 (年)",
        "fees_section": "法律费用及成本",
        "stamp_duty": "印花税及其他法律费用 (可修改)",
        "consent": "同意费 (MYR)",
        "legal": "贷款文件法律费用 (MYR)",
        "cash_section": "现金需求",
        "min_bal": "最低银行余额要求 (MYR)",
        "cushion": "额外现金储备 (MYR)",
        "renov": "装修费用 (MYR)",
        "property_details": "房产详细信息",
        "property_size": "房产面积 (平方英尺)",
        "property_fee": "房产费用 (每月)",
        "rental_section": "租金预期",
        "rate": "爱彼迎收费 (MYR/晚)",
        "util": "使用率 (%)",
        "mgmt": "包含爱彼迎管理费的成本 (MYR/月)",
        "currency_section": "汇率设置",
        "foreign_currency": "外币代码 (例如 NZD, SGD)",
        "manual_fx": "手动输入汇率",
        "fx_rate": "外币兑换 MYR 汇率",
        "calculate": "开始计算",
        "results": "计算结果",
        "net_price": "净价格 (应用折扣 1 和 2 后)",
        "net_net_price": "最终净价格 (应用所有折扣后)",
        "max_loan": "最高贷款额",
        "cash_deposit": "需支付现金",
        "monthly_repayment": "每月贷款还款额",
        "total_cash_required": "总前期现金需求",
        "gross_rent": "租金总收入 (月)",
        "net_rent": "租金净收入 (月)",
        "monthly_profit": "每月盈亏",
        "download_excel": "下载结果 (CSV 文件)",
        "in_foreign_currency": "（以外币计）",
        "processing": "正在处理，请稍候...",
        "api_error": "汇率接口出错，使用默认汇率"
    },
    "ms": {
        "title": "Kalkulator Pelaburan Hartanah Sewa",
        "language": "Bahasa",
        "property_section": "Butiran Hartanah",
        "spa_price": "Harga Perjanjian Jual Beli (SPA) (MYR)",
        "discount1": "Diskaun 1 (%)",
        "discount2": "Diskaun 2 (%)",
        "discount3": "Diskaun 3 (MYR) - Yuran Alam Sekitar",
        "deposit_paid": "Deposit Telah Dibayar (MYR)",
        "loan_section": "Butiran Pinjaman",
        "loan_ratio": "Nisbah Pinjaman (%)",
        "interest": "Kadar Faedah (%)",
        "years": "Tempoh Pinjaman (Tahun)",
        "fees_section": "Yuran Undang-undang & Kos",
        "stamp_duty": "Duti Setem dan Yuran Undang-undang Lain (boleh diedit)",
        "consent": "Yuran Kebenaran (MYR)",
        "legal": "Yuran Undang-undang Dokumentasi Pinjaman (MYR)",
        "cash_section": "Keperluan Tunai",
        "min_bal": "Baki Bank Minimum yang Diperlukan (MYR)",
        "cushion": "Simpanan Tunai Tambahan (MYR)",
        "renov": "Kos Pengubahsuaian (MYR)",
        "property_details": "Butiran Hartanah",
        "property_size": "Saiz Hartanah (kaki persegi)",
        "property_fee": "Yuran Hartanah (sebulan)",
        "rental_section": "Jangkaan Sewaan",
        "rate": "Kadar Airbnb (MYR/malam)",
        "util": "Kadar Penggunaan (%)",
        "mgmt": "Kos termasuk Yuran Pengurusan Airbnb (MYR/bulan)",
        "currency_section": "Tetapan Pertukaran Mata Wang",
        "foreign_currency": "Kod Mata Wang Asing (cth. NZD, SGD)",
        "manual_fx": "Tetapan Manual Kadar Pertukaran",
        "fx_rate": "Kadar Pertukaran (Mata Wang Asing → MYR)",
        "calculate": "Kira",
        "results": "Keputusan Pengiraan",
        "net_price": "Harga Bersih (selepas Diskaun 1 & 2)",
        "net_net_price": "Harga Bersih Akhir (selepas semua diskaun)",
        "max_loan": "Jumlah Pinjaman Maksimum",
        "cash_deposit": "Deposit Tunai Diperlukan",
        "monthly_repayment": "Bayaran Balik Pinjaman Bulanan",
        "total_cash_required": "Jumlah Tunai Pendahuluan Diperlukan",
        "gross_rent": "Pendapatan Sewa Kasar (Bulanan)",
        "net_rent": "Pendapatan Sewa Bersih (Bulanan)",
        "monthly_profit": "Keuntungan / Kerugian Bulanan",
        "download_excel": "Muat Turun Keputusan sebagai CSV",
        "in_foreign_currency": "(dalam mata wang asing)",
        "processing": "Memproses input, sila tunggu...",
        "api_error": "Ralat API FX, menggunakan kadar lalai"
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
    with st.expander(t["property_section"], expanded=True):
        spa_price = st.number_input(t["spa_price"], value=1594000.00)
        discount1 = st.number_input(t["discount1"], value=10.0)
        discount2 = st.number_input(t["discount2"], value=8.0)
        discount3 = st.number_input(t["discount3"], value=6888.0)
        deposit_paid = st.number_input(t["deposit_paid"], value=20000.0)
        property_size = st.number_input(t["property_size"], value=678.0)
        property_fee = st.number_input(t["property_fee"], value=447.48)
    
    # Loan Details Section
    with st.expander(t["loan_section"], expanded=True):
        loan_ratio = st.number_input(t["loan_ratio"], value=70.0)
        interest = st.number_input(t["interest"], value=4.3)
        years = st.number_input(t["years"], value=26)
    
    # Legal Fees & Costs Section
    with st.expander(t["fees_section"], expanded=True):
        consent = st.number_input(t["consent"], value=1000.0)
        legal = st.number_input(t["legal"], value=7083.16)
        stamp_duty = st.number_input(t["stamp_duty"], value=0.0) # This will be calculated later
    
    # Cash Requirements Section
    with st.expander(t["cash_section"], expanded=True):
        min_bal = st.number_input(t["min_bal"], value=40000.0)
        cushion = st.number_input(t["cushion"], value=40000.0)
        renov = st.number_input(t["renov"], value=20000.0)
    
    # Rental Expectations Section
    with st.expander(t["rental_section"], expanded=True):
        rate = st.number_input(t["rate"], value=400.0)
        util = st.number_input(t["util"], value=75.0)
        mgmt = st.number_input(t["mgmt"], value=800.0)

with col2:
    # Currency section
    with st.expander(t["currency_section"], expanded=True):
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

        # Financial calculations
        # Property price calculations
        after_dis1 = spa_price * (1 - discount1/100)
        net_price = after_dis1 * (1 - discount2/100)
        net_net_price = net_price - discount3
        
        # Loan calculations
        max_loan = net_net_price * loan_ratio / 100
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

        # Display results
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

        # CSV Export
        df = pd.DataFrame({
            "Category": [
                t["spa_price"], t["discount1"], t["discount2"], t["discount3"],
                t["deposit_paid"], t["loan_ratio"], t["interest"], t["years"],
                t["net_price"], t["net_net_price"], t["max_loan"],
                t["cash_deposit"], t["monthly_repayment"], t["total_cash_required"],
                t["gross_rent"], t["net_rent"], t["monthly_profit"]
            ],
            "MYR Amount": [
                spa_price, f"{discount1}%", f"{discount2}%", discount3,
                deposit_paid, f"{loan_ratio}%", f"{interest}%", years,
                net_price, net_net_price, max_loan,
                cash_deposit, monthly_repay, total_cash,
                gross_rent, net_rent, profit
            ],
            f"{foreign_currency} Amount": [
                spa_price/fx_rate, f"{discount1}%", f"{discount2}%", discount3/fx_rate,
                deposit_paid/fx_rate, f"{loan_ratio}%", f"{interest}%", years,
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
