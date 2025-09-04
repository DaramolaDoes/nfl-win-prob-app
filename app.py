import json, requests, streamlit as st
from datetime import datetime

st.set_page_config(page_title="NFL 2025 • AI Win Probability", layout="wide")
st.title("🏈 NFL 2025 • AI Win Probability (Pre-game)")

st.caption("Shows 2025 matchups & model probabilities computed from 2024 results. "
           "Upload your own JSON or point to a hosted URL.")

# --- Controls ---
col1, col2 = st.columns([1,2])
with col1:
    week = st.selectbox("Select Week", list(range(1,19)), index=0)
with col2:
    json_url = st.text_input("Hosted JSON URL (optional)", value="")

uploaded = st.file_uploader("Or upload your JSON", type=["json"], accept_multiple_files=False)

# --- Load data ---
def load_data():
    # priority: uploaded > url > local fallback
    if uploaded:
        return json.load(uploaded)
    if json_url:
        r = requests.get(json_url, timeout=10)
        r.raise_for_status()
        return r.json()
    # local fallback
    try:
        import os, json
        with open("data/nfl_2025_ai_predictions.json","r") as f:
            return json.load(f)
    except Exception:
        return {
            "season": 2025,
            "updated_at": "2025-08-20",
            "weeks": [
                {"week": 1, "games": [
                    {"game_id":"2025W1-PHI-DAL","date":"2025-09-07","home":"PHI","away":"DAL","spread_home":-2.5,"win_proba_home":0.61},
                    {"game_id":"2025W1-KC-BUF","date":"2025-09-07","home":"KC","away":"BUF","spread_home":-1.5,"win_proba_home":0.55}
                ]},
                {"week": 2, "games": [
                    {"game_id":"2025W2-NYJ-NE","date":"2025-09-14","home":"NYJ","away":"NE","spread_home":-3.0,"win_proba_home":0.58}
                ]}
            ]
        }

data = load_data()
st.caption(f"Season: **{data.get('season','2025')}** • Updated: {data.get('updated_at','—')}")

TEAM_NAME = {
  "ARI":"Arizona Cardinals","ATL":"Atlanta Falcons","BAL":"Baltimore Ravens","BUF":"Buffalo Bills",
  "CAR":"Carolina Panthers","CHI":"Chicago Bears","CIN":"Cincinnati Bengals","CLE":"Cleveland Browns",
  "DAL":"Dallas Cowboys","DEN":"Denver Broncos","DET":"Detroit Lions","GB":"Green Bay Packers",
  "HOU":"Houston Texans","IND":"Indianapolis Colts","JAX":"Jacksonville Jaguars","KC":"Kansas City Chiefs",
  "LV":"Las Vegas Raiders","LAC":"Los Angeles Chargers","LAR":"Los Angeles Rams","MIA":"Miami Dolphins",
  "MIN":"Minnesota Vikings","NE":"New England Patriots","NO":"New Orleans Saints","NYG":"New York Giants",
  "NYJ":"New York Jets","PHI":"Philadelphia Eagles","PIT":"Pittsburgh Steelers","SEA":"Seattle Seahawks",
  "SF":"San Francisco 49ers","TB":"Tampa Bay Buccaneers","TEN":"Tennessee Titans","WAS":"Washington Commanders"
}

weeks = {w["week"]: w for w in data.get("weeks", [])}
wk = weeks.get(week, {"games": []})

st.subheader(f"Week {week} Matchups")
if not wk["games"]:
    st.info("No games found for this week in your JSON.")
else:
    for g in wk["games"]:
        home = TEAM_NAME.get(g["home"], g["home"])
        away = TEAM_NAME.get(g["away"], g["away"])
        p_home = float(g.get("win_proba_home", 0.5))
        p_away = max(0.0, min(1.0, 1.0 - p_home))
        date_str = g.get("date", "TBD")
        spread = g.get("spread_home", None)

        with st.container(border=True):
            c1, c2, c3 = st.columns([2,1,2])
            with c1:
                st.markdown("**Away**")
                st.markdown(f"{away} ({g['away']})")
            with c2:
                st.markdown(f"**Week {week}**")
                st.caption(f"Date: {date_str}")
                if spread is not None:
                    s = f"+{spread}" if spread > 0 else f"{spread}"
                    st.caption(f"Spread (home): {s}")
            with c3:
                st.markdown("**Home**")
                st.markdown(f"{home} ({g['home']})")

            st.progress(p_home, text=f"Home Win Probability: {p_home*100:.1f}%")
            st.progress(p_away, text=f"Away Win Probability: {p_away*100:.1f}%")

st.divider()
with st.expander("Plain-English guide"):
    st.markdown("""
- **Win Probability**: estimated chance a team wins if this game were played many times under similar conditions.
- **How it’s built**: uses 2024 results (recent form, point diff, spread, home/away) to estimate 2025 matchups.
- **Calibration**: probabilities are adjusted so 60% ≈ 60 wins out of 100 historically.
""")
