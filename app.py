import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt

# --- アプリ設定 ---
st.set_page_config(page_title="パチンコ軍師", page_icon="👺", layout="centered")

# カスタムCSSで「アプリ感」を出す（漆黒デザイン）
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff0000; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("👺 逆転の裁定シミュレータ")

# --- 入力セクション ---
with st.container():
    st.subheader("現在の戦況")
    minus_yen = st.number_input("これまでの負け額 (円)", value=30000, step=1000)
    balance_yen = st.number_input("残り残高 (円)", value=10000, step=1000)
    rotation = st.slider("1kあたりの回転数", 10.0, 25.0, 17.5)

# --- スペック（地獄少女7500想定） ---
spec = {'prob': 1/349.9, 'rush_in': 0.52, 'rush_cont': 0.81, 'init': 1200, 'unit': 1500}

if st.button("逆転確率を算出する"):
    # 1. 抽選回数
    spins = int((balance_yen / 1000) * rotation)
    
    # 2. 当たる確率
    prob_hit = (1 - (1 - spec['prob'])**spins) * 100
    prob_rush = prob_hit * spec['rush_in']
    
    # 3. 捲りライン（出玉）
    target_balls = (minus_yen + balance_yen) / 4
    
    # --- 表示エリア ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("🎯 当たる確率", f"{prob_hit:.1f}%")
    col2.metric("🔥 RUSH突入率", f"{prob_rush:.1f}%")
    
    st.write(f"残り **{spins}回転** での勝負です。")
    
    # 4. RUSHシミュレーション
    sim_results = []
    for _ in range(5000):
        balls = spec['init']
        while random.random() < spec['rush_cont']:
            balls += spec['unit']
        sim_results.append(balls)
    
    success_rate = np.sum(np.array(sim_results) >= target_balls) / 5000 * 100
    total_success = (prob_rush / 100) * (success_rate / 100) * 100

    st.subheader("【結論】")
    if total_success > 5:
        st.success(f"捲り（プラ転）の可能性は **{total_success:.2f}%** です。行く価値あり！")
    else:
        st.error(f"捲り確率は **{total_success:.2f}%**。極めて厳しい戦いです。")

    # グラフ
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(sim_results, bins=50, color='crimson', alpha=0.7)
    ax.axvline(target_balls, color='white', linestyle='--', label='捲りライン')
    ax.set_title("RUSH期待出玉の分布")
    ax.set_facecolor('#000000')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    st.pyplot(fig)
