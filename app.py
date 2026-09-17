import streamlit as st

st.set_page_config(page_title="訪問看護ステーション 損益シミュレーター", layout="wide")

st.title("📊 訪問看護ステーション 損益シミュレーター")
st.caption("体制（人員・訪問数）に応じたリアルな損益を試算できます。")

# サイドバー設定
st.sidebar.header("1. 人員・訪問設定")
num_nurses = st.sidebar.number_input("看護師人数 (名)", min_value=1, max_value=50, value=5, step=1)
visits_per_nurse = st.sidebar.number_input("看護師1人あたりの月間訪問件数 (件)", min_value=0, max_value=200, value=80, step=5)
num_office = st.sidebar.number_input("事務員人数 (名)", min_value=0, max_value=10, value=1, step=1)
unit_price = st.sidebar.number_input("1件あたり平均単価 (円)", min_value=0, max_value=30000, value=8500, step=100)

st.sidebar.header("2. 人件費設定")
nurse_salary = st.sidebar.number_input("看護師1人の月給 (円)", min_value=0, max_value=1000000, value=350000, step=10000)
office_salary = st.sidebar.number_input("事務員1人の月給 (円)", min_value=0, max_value=1000000, value=220000, step=10000)
social_insurance_rate = st.sidebar.slider("法定福利費・事業主負担割合 (%)", min_value=0, max_value=30, value=15)

st.sidebar.header("3. その他固定費 (家賃・車・システム等)")
other_fixed_cost = st.sidebar.number_input("月間その他固定費 (円)", min_value=0, max_value=5000000, value=300000, step=10000)

# 計算処理
total_visits = num_nurses * visits_per_nurse
total_sales = total_visits * unit_price

nurse_labor_cost = num_nurses * nurse_salary
office_labor_cost = num_office * office_salary
total_base_salary = nurse_labor_cost + office_labor_cost
total_labor_cost = int(total_base_salary * (1 + social_insurance_rate / 100))

total_cost = total_labor_cost + other_fixed_cost
profit = total_sales - total_cost
profit_margin = (profit / total_sales * 100) if total_sales > 0 else 0

# メイン表示
st.subheader("📈 試算結果サマリー")
col1, col2, col3, col4 = st.columns(4)
col1.metric("総訪問件数 / 月", f"{total_visits:,} 件")
col2.metric("予想売上高", f"¥{total_sales:,}")
col3.metric("総費用 (人件費+固定費)", f"¥{total_cost:,}")
col4.metric("推定営業利益", f"¥{profit:,}", delta=f"{profit_margin:.1f}% (利益率)")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.write("### 💰 費用内訳")
    st.write(f"- **看護師人件費 (5%法定負担込目安):** ¥{int(nurse_labor_cost * (1 + social_insurance_rate/100)):,}")
    st.write(f"- **事務員人件費 (法定負担込目安):** ¥{int(office_labor_cost * (1 + social_insurance_rate/100)):,}")
    st.write(f"- **その他固定費 (家賃・車両等):** ¥{other_fixed_cost:,}")

with col_right:
    st.write("### 💡 診断コメント")
    if profit > 0:
        st.success(f"手元に月間 **¥{profit:,}** の利益が残る計算です。健全な運営ラインです。")
    elif profit == 0:
        st.warning("損益分岐点（トントン）です。訪問件数を増やすか固定費の見直しを検討できます。")
    else:
        st.error(f"月間 **¥{abs(profit):,}** の赤字です。人件費割合か訪問稼働率を見直してください。")
