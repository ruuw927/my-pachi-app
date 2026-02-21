import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# ==========================================
# 1. アプリの基本設定とデザイン（権威の演出）
# ==========================================
st.set_page_config(page_title="パチンコ・ストラテジスト PRO", page_icon="👺", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stButton>button { width: 100%; font-weight: bold; background-color: #8b0000; color: white; border-radius: 8px; }
    .stButton>button:hover { background-color: #ff0000; color: white; }
    h1, h2, h3 { color: #ff4b4b; font-family: 'Helvetica Neue', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("👺 パチンコ・ストラテジスト PRO")
st.markdown("現在の戦況と機種スペックから、冷徹な確率論で**「逆転の裁定」**を下します。")

# ==========================================
# 2. 最新・稼働主要機種データベース
# ==========================================
# ※ここの数値を書き換えれば、自由にスペックを変更できます
database = {
    "【カスタム機種】(自分で数値を入力)": {'main': 319.0, 'charge': 9999, 'rush_entry': 0.50, 'rush_cont': 0.80, 'init': 1500, 'unit': 1500},
    "e Re:ゼロ2 (強欲)": {'main': 349.9, 'charge': 499.0, 'rush_entry': 0.55, 'rush_cont': 0.77, 'init': 1500, 'unit': 1500},
    "e地獄少女 7500": {'main': 349.9, 'charge': 429.0, 'rush_entry': 0.52, 'rush_cont': 0.81, 'init': 1200, 'unit': 1500},
    "e北斗の拳10": {'main': 348.6, 'charge': 9999, 'rush_entry': 0.80, 'rush_cont': 0.80, 'init': 1000, 'unit': 1500},
    "e花の慶次 傾奇一転": {'main': 319.7, 'charge': 9999, 'rush_entry': 0.52, 'rush_cont': 0.80, 'init': 1500, 'unit': 1500},
    "Pエヴァ16 テーゼ": {'main': 319.7, 'charge': 9999, 'rush_entry': 0.73, 'rush_cont': 0.81, 'init': 450, 'unit': 1500},
    "Pエヴァ15 未来への咆哮": {'main': 319.7, 'charge': 9999, 'rush_entry': 0.70, 'rush_cont': 0.81, 'init': 450, 'unit': 1500},
    "P大海物語5": {'main': 319.6, 'charge': 9999, 'rush_entry': 0.60, 'rush_cont': 0.50, 'init': 1500, 'unit': 1500},
    "P牙狼11 冴島大河": {'main': 319.6, 'charge': 9999, 'rush_entry': 0.63, 'rush_cont': 0.81, 'init': 1500, 'unit': 1500},
    "Pとある科学の超電磁砲2": {'main': 319.6, 'charge': 9999, 'rush_entry': 0.70, 'rush_cont': 0.77, 'init': 660, 'unit': 1500},
    "Pまどか☆マギカ3": {'main': 199.1, 'charge': 9999, 'rush_entry': 0.55, 'rush_cont': 0.77, 'init': 400, 'unit': 1500},
    "PA大海物語5ブラックLT": {'main': 99.9, 'charge': 9999, 'rush_entry': 0.70, 'rush_cont': 0.62, 'init': 400, 'unit': 880}
}

# ==========================================
# 3. 操作パネル（サイドバー構成）
# ==========================================
st.sidebar.header("⚙️ 戦況パラメーター")

# 機種選択
machine_name = st.sidebar.selectbox("▶ 機種を選択", list(database.keys()))

# カスタム機種が選ばれた場合のみ、詳細入力欄を表示
if machine_name == "【カスタム機種】(自分で数値を入力)":
    st.sidebar.markdown("---")
    st.sidebar.caption("🔧 カスタムスペック設定")
    c_main = st.sidebar.number_input("大当たり確率 (1/〇)", value=319.0)
    c_rush_in = st.sidebar.slider("RUSH突入率 (%)", 0, 100, 50) / 100
    c_rush_cont = st.sidebar.slider("RUSH継続率 (%)", 0, 100, 80) / 100
    c_init = st.sidebar.number_input("初当たり出玉 (発)", value=450)
    c_unit = st.sidebar.number_input("RUSH中の出玉 (発)", value=1500)
    spec = {'main': c_main, 'charge': 9999, 'rush_entry': c_rush_in, 'rush_cont': c_rush_cont, 'init': c_init, 'unit': c_unit}
else:
    spec = database[machine_name]

st.sidebar.markdown("---")
st.sidebar.caption("💰 投資と状況")
rotation = st.sidebar.slider("1k(1000円)あたりの回転数", 10.0, 25.0, 17.5, step=0.5)
balance_yen = st.sidebar.number_input("勝負できる残り残高 (円)", value=10000, step=1000)
minus_yen = st.sidebar.number_input("本日の負け額・目標額 (円)", value=30000, step=1000)

# ==========================================
# 4. 解析・シミュレーション実行エンジン
# ==========================================
if st.button(f"【{machine_name}】で逆転の裁定を下す"):
    
    # 計算ロジック
    spins = int((balance_yen / 1000) * rotation)
    target_balls = (minus_yen + balance_yen) / 4.0 # 等価交換想定
    
    # 確率計算（チャージ非考慮の純粋な図柄揃い）
    prob_hit = (1 - (1 - (1/spec['main']))**spins) * 100
    prob_rush = prob_hit * spec['rush_entry']
    
    st.markdown("---")
    st.subheader("📊 解析レポート")
    
    # メトリクス表示
    col1, col2, col3 = st.columns(3)
    col1.metric("残り抽選回数", f"{spins} 回転")
    col2.metric("本当たりを引く確率", f"{prob_hit:.1f} %")
    col3.metric("RUSHを射止める確率", f"{prob_rush:.1f} %")
    
    st.markdown(f"目標捲りライン: **{target_balls:,.0f} 発**")
    
    # RUSH出玉シミュレーション（1万回実行して精度を高める）
    sim_count = 10000
    sim_results = []
    for _ in range(sim_count):
        balls = spec['init']
        while random.random() < spec['rush_cont']:
            balls += spec['unit']
        sim_results.append(balls)
        
    sim_results = np.array(sim_results)
    
    # 捲れる確率（RUSH突入確率 × RUSH内で目標出玉を超える確率）
    rush_success_rate = np.sum(sim_results >= target_balls) / sim_count * 100
    total_makuri_rate = (prob_rush / 100) * (rush_success_rate / 100) * 100
    avg_rush_balls = np.mean(sim_results)

    # ==========================================
    # 5. 最終判定と権威あるアドバイス
    # ==========================================
    st.subheader("👺 軍師の最終裁定")
    if total_makuri_rate >= 10:
        st.success(f"【勝機あり】捲り確率は **{total_makuri_rate:.2f}％** です。RUSHの平均期待出玉（約{avg_rush_balls:,.0f}発）が目標ラインに届く射程圏内です。勝負を続行してください。")
    elif total_makuri_rate >= 2:
        st.warning(f"【警戒戦】捲り確率は **{total_makuri_rate:.2f}％**。RUSHに入れても、上位数％の「上振れ」が必要です。過度な期待は禁物です。")
    else:
        st.error(f"【撤退推奨】捲り確率は **{total_makuri_rate:.2f}％**。奇跡が起きない限り捲れません。この残高は次回の軍資金として温存すべきです。")

    # ==========================================
    # 6. 視覚化グラフ（プロ仕様）
    # ==========================================
    st.markdown("##### RUSH突入時の獲得出玉シミュレーション（1万回）")
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # ヒストグラムの描画
    ax.hist(sim_results, bins=100, color='#ff4b4b', alpha=0.8, edgecolor='black')
    ax.axvline(target_balls, color='#00ff00', linestyle='--', linewidth=2, label=f'捲りライン ({target_balls:,.0f}発)')
    ax.axvline(avg_rush_balls, color='white', linestyle=':', linewidth=2, label=f'平均期待値 ({avg_rush_balls:,.0f}発)')
    
    # グラフのデザイン調整（漆黒テーマ）
    ax.set_facecolor('#050505')
    fig.patch.set_facecolor('#050505')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(facecolor='#050505', labelcolor='white', edgecolor='white')
    
    st.pyplot(fig)
