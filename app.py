import streamlit as st

st.set_page_config(page_title="損益シミュレーター", layout="wide")

st.title("📊 訪問看護 損益シミュレーター")

st.write("パラメータを変更して損益を試算できます。")

# サイドバー設定
st.sidebar.header("設定項目")
visits = st.sidebar.number_input("月間訪問件数", min_value=0, max_value=1000, value=100, step=10)
unit_price = st.sidebar.number_input("1件あたり単価 (円)", min_value=0, max_value=50000, value=8000, step=500)
fixed_cost = st.sidebar.number_input("月間固定費 (円)", min_value=0, max_value=10000000, value=500000, step=50000)

# 計算処理
sales = visits * unit_price
profit = sales - fixed_cost

# 結果表示
col1, col2, col3 = st.columns(3)
col1.metric("売上高", f"¥{sales:,}")
col2.metric("固定費", f"¥{fixed_cost:,}")
col3.metric("推定利益", f"¥{profit:,}", delta=f"¥{profit:,}")

if profit > 0:
    st.success("黒字見込みです！")
elif profit == 0:
    st.info("トントン（損益分岐点）です。")
else:
    st.error("赤字見込みです。設定を見直してください。")
