import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# ==========================================
# 1. アプリ設定 & 漆黒の軍師デザイン
# ==========================================
st.set_page_config(page_title="パチ・スロ究極解析軍師", page_icon="👺", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stButton>button { width: 100%; font-weight: bold; background-color: #8b0000; color: white; border-radius: 8px; height: 3.5em; border: 1px solid #444; }
    .stButton>button:hover { background-color: #ff0000; border: 1px solid #fff; }
    h1, h2, h3 { color: #ff4b4b; text-shadow: 2px 2px 4px #000; font-family: 'Hiragino Mincho ProN', serif; }
    .stMetric { background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .sidebar .sidebar-content { background-color: #111; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 2025年4月〜最新・全機種データベース
# ==========================================
p_db = {
    "【カスタム入力(P)】": {'main': 319.0, 'rush_entry': 0.50, 'rush_cont': 0.80, 'init': 1500, 'unit': 1500},
    # --- 2025年以降 最新・主力P機 ---
    "e Re:ゼロ2 (強欲)": {'main': 349.9, 'rush_entry': 0.55, 'rush_cont': 0.77, 'init': 1500, 'unit': 1500},
    "e地獄少女 7500": {'main': 349.9, 'rush_entry': 0.52, 'rush_cont': 0.81, 'init': 1200, 'unit': 1500},
    "e北斗の拳10": {'main': 348.6, 'rush_entry': 0.80, 'rush_cont': 0.80, 'init': 1000, 'unit': 1500},
    "Pエヴァ16 テーゼ": {'main': 319.7, 'rush_entry': 0.73, 'rush_cont': 0.81, 'init': 450, 'unit': 1500},
    "P大海物語5 SPECIAL": {'main': 319.6, 'rush_entry': 0.60, 'rush_cont': 0.50, 'init': 1500, 'unit': 1500},
    "e花の慶次 傾奇一転": {'main': 319.7, 'rush_entry': 0.52, 'rush_cont': 0.80, 'init': 1500, 'unit': 1500},
    "Pまどか☆マギカ3 (LT)": {'main': 199.1, 'rush_entry': 0.55, 'rush_cont': 0.77, 'init': 400, 'unit': 1500},
    "Pアズールレーン (LT)": {'main': 199.0, 'rush_entry': 0.61, 'rush_cont': 0.90, 'init': 530, 'unit': 700},
    "P牙狼11 冴島大河": {'main': 319.6, 'rush_entry': 0.63, 'rush_cont': 0.81, 'init': 1500, 'unit': 1500},
    "Pルパン三世 14": {'main': 319.9, 'rush_entry': 0.60, 'rush_cont': 0.81, 'init': 1500, 'unit': 1500},
}

s_db = {
    "【カスタム入力(S)】": [97.5, 98.5, 100.5, 104.0, 108.0, 112.0],
    # --- 2025年以降 最新・主力S機 ---
    "スマスロ北斗の拳": [98.0, 99.0, 101.0, 105.0, 110.0, 113.0],
    "Lヴァルヴレイヴ": [97.3, 98.3, 100.8, 103.2, 107.9, 114.9],
    "LモンキーターンV": [97.9, 99.1, 102.1, 105.4, 110.1, 114.8],
    "L主役は銭形4": [97.6, 98.8, 102.1, 105.4, 110.2, 114.1],
    "Lからくりサーカス": [97.5, 98.6, 101.5, 105.5, 111.0, 114.9],
    "マイジャグラーV": [97.0, 98.0, 99.9, 102.8, 105.3, 109.4],
    "アイムジャグラーEX": [97.0, 98.0, 99.5, 101.1, 103.3, 105.5],
    "L聖闘士星矢 海皇覚醒": [97.5, 98.7, 101.2, 105.3, 110.1, 114.9],
}

# ==========================================
# 3. 共通・軍師の裁定システム (20通り)
# ==========================================
def get_comment(rate, is_pachinko=True):
    if rate >= 15:
        return random.choice(["【至上の勝機】数値は圧倒的。この好機、逃す手はないぞ。", "【全軍突撃】捲り確率は極めて高い。あとは引くだけの作業だ。", "【軍師の予言】今、台が呼んでいる。確実な勝利を掴み取れ。", "【盤石の布陣】期待値・確率ともに申し分なし。迷わず打ち抜け！"])
    elif rate >= 8:
        return random.choice(["【好機到来】捲り確率は十分。一撃で戦況をひっくり返せる。", "【反撃の狼煙】ここが分かれ目。一気に捲り上げるぞ。", "【攻勢維持】数値は悪くない。己のヒキを信じるのみ。", "【逆転の好機】RUSH一発で届く。強気に攻める場面だ。"])
    elif rate >= 3:
        return random.choice(["【薄氷の攻防】確率は低いがゼロではない。覚悟はあるか？", "【乾坤一擲】ヒキだけで勝負する領域。深追いは禁物だ。", "【忍耐の時】確率は厳しいが、一撃の性能次第では目がある。", "【背水の陣】この予算が尽きれば敗北。奇跡を祈れ。"])
    else:
        return random.choice(["【即時撤退】無謀な勝負。兵（金）を温存せよ。", "【敗北の裁定】確率は絶望的。冷静に席を立つ勇気を持て。", "【絶望の淵】奇跡を期待する段階は終わった。現実を見ろ。", "【軍資金死守】ここで止めるのが最善。明日の自分へ繋げ。", "【無念の帰還】今日の運命はここまで。深追いは破滅の道。"])

# ==========================================
# 4. モード切り替え & 画面構築
# ==========================================
mode = st.sidebar.radio("🔥 兵法選択", ["パチンコ解析", "スロット解析"])

if mode == "パチンコ解析":
    st.title("👺 パチンコ・逆転の裁定")
    machine = st.selectbox("機種選択", list(p_db.keys()))
    spec = p_db[machine]
    
    col1, col2 = st.columns(2)
    with col1:
        total_spins = st.number_input("本日の通常時総回転数", value=0)
        total_hits = st.number_input("本日の初当たり回数", value=0)
    with col2:
        current_hamari = st.number_input("現在のハマリ回転数", value=0)
        rotation = st.slider("1kあたりの回転数", 10.0, 25.0, 17.0)

    balance = st.sidebar.number_input("残り予算 (円)", value=10000)
    minus = st.sidebar.number_input("捲りたい金額 (円)", value=30000)
    
    if st.button("パチンコ解析実行"):
        # 計算
        spins = int((balance / 1000) * rotation)
        target_balls = (minus + balance) / 4.0
        prob_hit = (1 - (1 - (1/spec['main']))**spins) * 100
        prob_rush = prob_hit * spec['rush_entry']
        
        # 期待出玉シミュレーション
        sim = np.array([spec['init'] + sum(spec['unit'] for _ in range(int(np.random.geometric(1-spec['rush_cont']))-1)) for _ in range(5000)])
        total_makuri_rate = (prob_rush / 100) * (np.sum(sim >= target_balls) / 5000) * 100
        
        # 表示
        st.subheader("📊 解析レポート")
        c1, c2, c3 = st.columns(3)
        c1.metric("当り期待度", f"{prob_hit:.1f}%")
        c2.metric("RUSH期待度", f"{prob_rush:.1f}%")
        c3.metric("捲り成功率", f"{total_makuri_rate:.1f}%")
        
        comment = get_comment(total_makuri_rate)
        if total_makuri_rate >= 8: st.success(comment)
        elif total_makuri_rate >= 3: st.warning(comment)
        else: st.error(comment)
        
        st.caption(f"※{spec['main']}回まで回すには、あと約{max(0, spec['main']-current_hamari)/rotation*1000:,.0f}円必要です。")

else:
    st.title("🎰 スロット・期待値判定")
    s_machine = st.selectbox("機種選択", list(s_db.keys()))
    rates = s_db[s_machine]
    
    col1, col2 = st.columns(2)
    with col1:
        s_target = st.slider("想定設定", 1, 6, 4)
        s_time = st.number_input("残り稼働時間 (h)", value=3.0)
    with col2:
        s_diff = st.number_input("現在の差枚数", value=0)
    
    if st.button("スロット解析実行"):
        exp_rate = rates[s_target-1] / 100
        exp_yen = (s_time * 750 * 3) * (exp_rate - 1) * 20
        
        st.subheader("📊 期待値レポート")
        c1, c2 = st.columns(2)
        c1.metric(f"設定{s_target} 機械割", f"{rates[s_target-1]}%")
        c2.metric("今後の見込み収支", f"{exp_yen:+,.0f} 円")
        
        if exp_yen > 5000: st.success("【勝機】期待値は十分。閉店まで回し切れ。")
        elif exp_yen > 0: st.warning("【拮抗】期待値はプラスだが微量。ヒキ勝負だ。")
        else: st.error("【撤退】設定判別が正しいなら、打つほど損をするぞ。")
