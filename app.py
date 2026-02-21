import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# ==========================================
# 1. アプリの基本設定と漆黒デザイン
# ==========================================
st.set_page_config(page_title="パチンコ・ストラテジスト PRO", page_icon="👺", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stButton>button { width: 100%; font-weight: bold; background-color: #8b0000; color: white; border-radius: 8px; height: 3em; }
    .stButton>button:hover { background-color: #ff0000; border: 1px solid white; }
    h1, h2, h3 { color: #ff4b4b; font-family: 'Helvetica Neue', sans-serif; text-shadow: 2px 2px 4px #000; }
    .stMetric { background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("👺 パチンコ・ストラテジスト PRO")
st.markdown("数値は嘘をつかない。データに基づき**「逆転の裁定」**を下します。")

# ==========================================
# 2. 最新スペックデータベース
# ==========================================
database = {
    "【カスタム入力】": {'main': 319.0, 'rush_entry': 0.50, 'rush_cont': 0.80, 'init': 1500, 'unit': 1500},
    "e Re:ゼロ2 (強欲)": {'main': 349.9, 'rush_entry': 0.55, 'rush_cont': 0.77, 'init': 1500, 'unit': 1500},
    "e地獄少女 7500": {'main': 349.9, 'rush_entry': 0.52, 'rush_cont': 0.81, 'init': 1200, 'unit': 1500},
    "e北斗の拳10": {'main': 348.6, 'rush_entry': 0.80, 'rush_cont': 0.80, 'init': 1000, 'unit': 1500},
    "e花の慶次 傾奇一転": {'main': 319.7, 'rush_entry': 0.52, 'rush_cont': 0.80, 'init': 1500, 'unit': 1500},
    "Pエヴァ16 テーゼ": {'main': 319.7, 'rush_entry': 0.73, 'rush_cont': 0.81, 'init': 450, 'unit': 1500},
    "Pエヴァ15 未来への咆哮": {'main': 319.7, 'rush_entry': 0.70, 'rush_cont': 0.81, 'init': 450, 'unit': 1500},
    "P大海物語5": {'main': 319.6, 'rush_entry': 0.60, 'rush_cont': 0.50, 'init': 1500, 'unit': 1500},
    "Pとある科学の超電磁砲2": {'main': 319.6, 'rush_entry': 0.70, 'rush_cont': 0.77, 'init': 660, 'unit': 1500},
    "Pまどか☆マギカ3": {'main': 199.1, 'rush_entry': 0.55, 'rush_cont': 0.77, 'init': 400, 'unit': 1500},
    "PA大海物語5ブラックLT": {'main': 99.9, 'rush_entry': 0.70, 'rush_cont': 0.62, 'init': 400, 'unit': 880}
}

# ==========================================
# 3. 操作パネル（サイドバー）
# ==========================================
st.sidebar.header("⚙️ スペック設定")
machine_name = st.sidebar.selectbox("機種選択", list(database.keys()))

if machine_name == "【カスタム入力】":
    c_main = st.sidebar.number_input("大当たり確率 1/", value=319.0)
    c_in = st.sidebar.slider("RUSH突入率 (%)", 0, 100, 50) / 100
    c_cont = st.sidebar.slider("RUSH継続率 (%)", 0, 100, 80) / 100
    c_i = st.sidebar.number_input("初当り出玉", value=450)
    c_u = st.sidebar.number_input("右打ち出玉", value=1500)
    spec = {'main': c_main, 'rush_entry': c_in, 'rush_cont': c_cont, 'init': c_i, 'unit': c_u}
else:
    spec = database[machine_name]

st.sidebar.markdown("---")
st.sidebar.header("🎰 実戦データ入力")
total_st_spins = st.sidebar.number_input("本日の総回転数 (通常時)", value=0, step=100)
total_hits = st.sidebar.number_input("本日の初当たり回数", value=0, step=1)
current_spins = st.sidebar.number_input("現在のハマリ回転数", value=0, step=10)

st.sidebar.markdown("---")
st.sidebar.header("💰 投資と目標")
rotation = st.sidebar.slider("1kあたりの回転数", 10.0, 25.0, 17.0, step=0.5)
balance_yen = st.sidebar.number_input("残り予算 (円)", value=10000, step=1000)
minus_yen = st.sidebar.number_input("捲りたい金額 (円)", value=30000, step=1000)

# ==========================================
# 4. 解析実行
# ==========================================
if st.button("裁定を下す"):
    # 基礎計算
    spins = int((balance_yen / 1000) * rotation)
    target_balls = (minus_yen + balance_yen) / 4.0
    prob_hit = (1 - (1 - (1/spec['main']))**spins) * 100
    prob_rush = prob_hit * spec['rush_entry']
    
    # 当日の実戦確率計算
    if total_st_spins > 0 and total_hits > 0:
        actual_prob = total_st_spins / total_hits
    else:
        actual_prob = 0

    # 1. 解析サマリー
    st.subheader("📊 解析サマリー")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("残りの抽選回数", f"{spins}回")
    with col2:
        st.metric("RUSH突入期待度", f"{prob_rush:.1f}%")
    with col3:
        if actual_prob > 0:
            diff = actual_prob - spec['main']
            st.metric("当日実戦確率", f"1/{actual_prob:.1f}", delta=f"{diff:+.1f}", delta_color="inverse")
        else:
            st.metric("当日実戦確率", "データ不足")

    # 2. 軍師の裁定
    st.markdown("---")
    st.subheader("👺 軍師の最終裁定")
    
    # シミュレーション
    sim_results = np.array([spec['init'] + sum(spec['unit'] for _ in range(int(np.random.geometric(1-spec['rush_cont']))-1)) for _ in range(10000)])
    makuri_rate_in_rush = np.sum(sim_results >= target_balls) / 10000
    total_makuri_rate = (prob_rush / 100) * makuri_rate_in_rush * 100

    if total_makuri_rate >= 10:
        st.success(f"【続行】捲り確率 {total_makuri_rate:.1f}%。十分な勝機がある。")
    elif total_makuri_rate >= 3:
        st.warning(f"【慎重】捲り確率 {total_makuri_rate:.1f}%。薄いところを引く覚悟が必要。")
    else:
        st.error(f"【撤退】捲り確率 {total_makuri_rate:.1f}%。絶望的な数値。深追いは厳禁。")

    # 3. 視覚化
    st.markdown("---")
    st.write(f"目標: {target_balls:,.0f}発 / 平均期待出玉: {np.mean(sim_results):,.0f}発")
    fig, ax = plt.subplots(figsize=(10, 4), facecolor='#050505')
    ax.set_facecolor('#050505')
    ax.hist(sim_results, bins=80, color='#ff4b4b', alpha=0.8)
    ax.axvline(target_balls, color='#00ff00', linestyle='--', label='目標ライン')
    ax.tick_params(colors='white')
    for spine in ax.spines.values(): spine.set_color('#333')
    st.pyplot(fig)
    
    st.caption(f"※現在のハマリ（{current_spins}回）から公表分母まで回すには、あと約{(max(0, spec['main']-current_spins)/rotation*1000):,.0f}円必要です。")
