import streamlit as st
import requests
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px
from streamlit_extras.stylable_container import stylable_container

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
        "monthly_service_fee": "Monthly Property Service Fee per sqf (MYR)",
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
        "api_error": "FX API Error, using default rate",
        "charts_section": "Financial Charts",
        "cash_flow_chart": "Monthly Cash Flow",
        "price_breakdown": "Price Breakdown",
        "expenses_chart": "Monthly Expenses",
        "income_chart": "Monthly Income",
        "loan_amortization": "Loan Amortization",
        "roi_chart": "Return on Investment",
        "year": "Year",
        "cumulative_profit": "Cumulative Profit",
        "profit_after_years": "Profit after {} years",
        "investment_breakdown": "Investment Breakdown",
        "expense_breakdown": "Monthly Expense Breakdown",
        "income_breakdown": "Monthly Income Breakdown",
        "summary_metrics": "Summary Metrics",
        "roi_percent": "ROI after {} years",
        "monthly_profit_value": "Monthly Profit/Loss"
    },
    "zh": {
        "title": "房产投资计算器",
        "language": "语言",
        "property_section": "房产详情",
        "spa_price": "买卖协议价格 (MYR)",
        "discount1": "折扣 1 (%)",
        "discount2": "折扣 2 (%)",
        "discount3": "折扣 3 (MYR) - 红包",
        "deposit_paid": "已支付订金 (MYR)",
        "loan_section": "贷款详情",
        "loan_ratio": "贷款比例 (%)",
        "interest": "利率 (%)",
        "years": "贷款期限 (年)",
        "fees_section": "法律费用及成本",
        "stamp_duty": "印花税及其他法律费用 (可修改)",
        "consent": "外国人购买许可费 (MYR)",
        "legal": "贷款文件法律费用 (MYR)",
        "cash_section": "现金需求",
        "min_bal": "最低银行余额要求 (MYR)",
        "cushion": "额外现金储备 (MYR)",
        "renov": "装修费用 (MYR)",
        "property_details": "房产详细信息",
        "property_size": "房产面积 (平方英尺)",
        "property_fee": "房产费用 (每月)",
        "monthly_service_fee": "每平方英尺每月管理费 (MYR)",
        "rental_section": "租金预期",
        "rate": "Airbnb 收费 (MYR/晚)",
        "util": "使用率 (%)",
        "mgmt": "Airbnb 管理费的成本 (MYR/月)",
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
        "api_error": "汇率接口出错，使用默认汇率",
        "charts_section": "财务图表",
        "cash_flow_chart": "每月现金流",
        "price_breakdown": "价格明细",
        "expenses_chart": "每月支出",
        "income_chart": "每月收入",
        "loan_amortization": "贷款摊销",
        "roi_chart": "投资回报率",
        "year": "年",
        "cumulative_profit": "累计利润",
        "profit_after_years": "{}年后利润",
        "investment_breakdown": "投资明细",
        "expense_breakdown": "每月支出明细",
        "income_breakdown": "每月收入明细",
        "summary_metrics": "汇总指标",
        "roi_percent": "{}年后投资回报率",
        "monthly_profit_value": "每月盈亏"
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
        "monthly_service_fee": "Yuran Perkhidmatan Hartanah/bulan/kaki persegi (MYR)",
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
        "api_error": "Ralat API FX, menggunakan kadar lalai",
        "charts_section": "Carta Kewangan",
        "cash_flow_chart": "Aliran Tunai Bulanan",
        "price_breakdown": "Perincian Harga",
        "expenses_chart": "Perbelanjaan Bulanan",
        "income_chart": "Pendapatan Bulanan",
        "loan_amortization": "Pelunasan Pinjaman",
        "roi_chart": "Pulangan Pelaburan",
        "year": "Tahun",
        "cumulative_profit": "Keuntungan Kumulatif",
        "profit_after_years": "Keuntungan selepas {} tahun",
        "investment_breakdown": "Perincian Pelaburan",
        "expense_breakdown": "Perincian Perbelanjaan Bulanan",
        "income_breakdown": "Perincian Pendapatan Bulanan",
        "summary_metrics": "Metrik Ringkasan",
        "roi_percent": "ROI selepas {} tahun",
        "monthly_profit_value": "Keuntungan/Kerugian Bulanan"
    }
}

# Icons for section headers
icons = {
    "property_section": "🏠",
    "loan_section": "💰",
    "fees_section": "⚖️",
    "cash_section": "💵",
    "rental_section": "🔑",
    "currency_section": "💱",
    "charts_section": "📊"
}

# Set page configuration
st.set_page_config(
    page_title="Property Investment Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stExpander {
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    h1 {
        color: #2c3e50;
    }
    h2 {
        color: #34495e;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
    }
    h3 {
        color: #7f8c8d;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar language selection
lang = st.sidebar.selectbox("Select Language / 选择语言 / Pilih Bahasa", ["en", "zh", "ms"])
t = translations[lang]

# App title
st.title(t["title"])

# Main content in two columns
col1, col2 = st.columns([3, 2])

with col1:
    # Property Details Section
    with st.expander(f"{icons['property_section']} {t['property_section']}", expanded=True):
        spa_price = st.number_input(t["spa_price"], value=1594000.00)
        discount1 = st.number_input(t["discount1"], value=10.0)
        discount2 = st.number_input(t["discount2"], value=8.0)
        discount3 = st.number_input(t["discount3"], value=6888.0)
        deposit_paid = st.number_input(t["deposit_paid"], value=20000.0)
        property_size = st.number_input(t["property_size"], value=678.0)
        monthly_service_fee_per_sqf = st.number_input(
            t["monthly_service_fee"], value=0.66, min_value=0.0, format="%.4f"
        )
        
        # Calculate property fee and show it
        property_fee = property_size * monthly_service_fee_per_sqf
        st.info(f"{t['property_fee']}: {property_fee:,.2f} MYR")
        
        # Calculate and display net price after all discounts
        after_dis1 = spa_price * (1 - discount1/100)
        net_price = after_dis1 * (1 - discount2/100)
        net_net_price = net_price - discount3
        st.info(f"{t['net_net_price']}: {net_net_price:,.2f} MYR")

    # Loan Details Section
    with st.expander(f"{icons['loan_section']} {t['loan_section']}", expanded=True):
        loan_ratio = st.number_input(t["loan_ratio"], value=70.0)
        interest = st.number_input(t["interest"], value=4.3)
        years = st.number_input(t["years"], value=26)

    # Legal Fees & Costs Section
    with st.expander(f"{icons['fees_section']} {t['fees_section']}", expanded=True):
        consent = st.number_input(t["consent"], value=1000.0)
        legal = st.number_input(t["legal"], value=7083.16)
        stamp_duty = st.number_input(t["stamp_duty"], value=0.0) # This will be calculated later

    # Cash Requirements Section
    with st.expander(f"{icons['cash_section']} {t['cash_section']}", expanded=True):
        min_bal = st.number_input(t["min_bal"], value=40000.0)
        cushion = st.number_input(t["cushion"], value=40000.0)
        renov = st.number_input(t["renov"], value=20000.0)

    # Rental Expectations Section
    with st.expander(f"{icons['rental_section']} {t['rental_section']}", expanded=True):
        rate = st.number_input(t["rate"], value=400.0)
        util = st.number_input(t["util"], value=75.0)
        mgmt = st.number_input(t["mgmt"], value=800.0)

with col2:
    # Currency section
    with st.expander(f"{icons['currency_section']} {t['currency_section']}", expanded=True):
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
        
        # Calculate loan amortization and ROI for charts
        loan_balance = [max_loan]
        for i in range(1, years * 12 + 1):
            interest_payment = loan_balance[-1] * r
            principal_payment = monthly_repay - interest_payment
            new_balance = loan_balance[-1] - principal_payment
            loan_balance.append(max(0, new_balance))
        
        # Calculate yearly cumulative profit for ROI chart
        yearly_profit = profit * 12
        cumulative_profit = [yearly_profit * i for i in range(1, years + 1)]
        roi_percentages = [(profit * 12 * i) / total_cash * 100 for i in range(1, years + 1)]

        # Display main results
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

        # CHARTS SECTION
        st.subheader(f"{icons['charts_section']} {t['charts_section']}")
        
        tab1, tab2, tab3, tab4 = st.tabs([t["price_breakdown"], t["cash_flow_chart"], t["roi_chart"], t["summary_metrics"]])
        
        with tab1:
            # Price breakdown pie chart
            price_data = {
                "Category": [t["net_price"], t["discount3"], t["discount1"] + " & " + t["discount2"]],
                "Value": [net_net_price, discount3, spa_price - net_price]
            }
            price_df = pd.DataFrame(price_data)
            
            fig_price = px.pie(price_df, values="Value", names="Category", title=t["price_breakdown"],
                              color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_price, use_container_width=True)
            
            # Investment breakdown pie chart
            investment_data = {
                "Category": [t["cash_deposit"], t["consent"], t["legal"], t["renov"], t["min_bal"], t["cushion"]],
                "Value": [cash_deposit, consent, legal, renov, min_bal, cushion]
            }
            investment_df = pd.DataFrame(investment_data)
            
            fig_investment = px.pie(investment_df, values="Value", names="Category", title=t["investment_breakdown"],
                                  color_discrete_sequence=px.colors.qualitative.Bold)
            st.plotly_chart(fig_investment, use_container_width=True)
        
        with tab2:
            col_cf1, col_cf2 = st.columns(2)
            
            with col_cf1:
                # Monthly expense breakdown
                expense_data = {
                    "Category": [t["monthly_repayment"], t["mgmt"], t["property_fee"]],
                    "Value": [monthly_repay, mgmt, property_fee]
                }
                expense_df = pd.DataFrame(expense_data)
                
                fig_expense = px.pie(expense_df, values="Value", names="Category", title=t["expense_breakdown"],
                                   color_discrete_sequence=px.colors.qualitative.Safe)
                st.plotly_chart(fig_expense, use_container_width=True)
            
            with col_cf2:
                # Monthly cash flow diagram
                cash_flow_data = {
                    "Category": [t["gross_rent"], t["monthly_repayment"], t["mgmt"], t["property_fee"], t["monthly_profit"]],
                    "Type": ["Income", "Expense", "Expense", "Expense", "Profit/Loss"],
                    "Value": [gross_rent, -monthly_repay, -mgmt, -property_fee, profit]
                }
                cash_flow_df = pd.DataFrame(cash_flow_data)
                
                # Create a waterfall chart for cash flow
                fig_waterfall = go.Figure(go.Waterfall(
                    name="Cash flow", orientation="v",
                    measure=["relative", "relative", "relative", "relative", "total"],
                    x=cash_flow_df["Category"],
                    y=cash_flow_df["Value"],
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                    increasing={"marker": {"color": "green"}},
                    decreasing={"marker": {"color": "red"}},
                    text=[f"{abs(val):,.2f} MYR" for val in cash_flow_df["Value"]],
                    textposition="outside"
                ))
                
                fig_waterfall.update_layout(
                    title=t["cash_flow_chart"],
                    showlegend=False
                )
                
                st.plotly_chart(fig_waterfall, use_container_width=True)
        
        with tab3:
            col_roi1, col_roi2 = st.columns(2)
            
            with col_roi1:
                # Return on Investment chart
                years_range = list(range(1, years + 1))
                roi_data = {
                    t["year"]: years_range,
                    t["cumulative_profit"]: cumulative_profit,
                    "ROI %": roi_percentages
                }
                roi_df = pd.DataFrame(roi_data)
                
                fig_roi = px.line(roi_df, x=t["year"], y=t["cumulative_profit"], 
                                 title=t["profit_after_years"].format(years),
                                 markers=True)
                fig_roi.update_traces(line=dict(width=3))
                st.plotly_chart(fig_roi, use_container_width=True)
            
            with col_roi2:
                # ROI percentage chart
                fig_roi_percent = px.bar(roi_df, x=t["year"], y="ROI %",
                                       title=t["roi_percent"].format(years),
                                       color="ROI %", color_continuous_scale="Viridis")
                st.plotly_chart(fig_roi_percent, use_container_width=True)
        
        with tab4:
            col_sum1, col_sum2 = st.columns(2)
            
            with col_sum1:
                # Loan amortization chart (first 5 years)
                annual_balance = [loan_balance[i*12] for i in range(min(6, years+1))]
                loan_years = list(range(min(6, years+1)))
                
                fig_loan = px.line(x=loan_years, y=annual_balance, markers=True,
                                 title=t["loan_amortization"] + " (5 " + t["year"] + ")")
                fig_loan.update_layout(xaxis_title=t["year"], yaxis_title="MYR")
                st.plotly_chart(fig_loan, use_container_width=True)
            
            with col_sum2:
                # Summary gauge chart for monthly profit
                max_gauge = max(abs(profit) * 2, 1000)
                
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=profit,
                    title={"text": t["monthly_profit_value"]},
                    gauge={
                        "axis": {"range": [-max_gauge, max_gauge]},
                        "bar": {"color": "darkblue"},
                        "steps": [
                            {"range": [-max_gauge, 0], "color": "lightcoral"},
                            {"range": [0, max_gauge], "color": "lightgreen"}
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": 0
                        }
                    }
                ))
                
                st.plotly_chart(fig_gauge, use_container_width=True)

         # CSV Export
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
