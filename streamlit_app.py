import streamlit as st
import requests

st.set_page_config(page_title="Sports Betting Analyse", layout="wide")
st.title("⚽ Live Sports Betting Analyse")

API_KEY = "aad52ecc7febfdb6a9317aff12d49980"

sport = st.selectbox("🎯 Vælg sport", [
    "soccer_epl", "soccer_uefa_champs_league", "soccer_denmark_superliga",
    "basketball_nba", "tennis_atp", "mma_mixed_martial_arts"
])
region = st.selectbox("🌍 Vælg region", ["eu", "uk", "us", "au"])
market = st.selectbox("📈 Vælg marked", ["h2h", "spreads", "totals"])

url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions={region}&markets={market}"
response = requests.get(url)

if response.status_code != 200:
    st.error(f"Kunne ikke hente odds. Fejlkode: {response.status_code}")
else:
    odds_data = response.json()
    st.write(f"✅ Fundet {len(odds_data)} kampe")

    for match in odds_data:
        st.markdown("---")
        st.subheader(f"🆚 {match['home_team']} vs {match['away_team']}")

        for bookmaker in match['bookmakers']:
            st.markdown(f"📊 **{bookmaker['title']}**")

            for m in bookmaker['markets']:
                for outcome in m['outcomes']:
                    navn = outcome['name']
                    odds = outcome['price']
                    
                    # Unik nøgle med odds for at undgå duplicates
                    unique_key = f"{match['id']}_{bookmaker['key']}_{navn}_{odds}"

                    sandsynlighed = st.slider(
                        f"Vurderet sandsynlighed for **{navn}** i {match['home_team']} vs {match['away_team']} (@ {bookmaker['title']})",
                        0, 100, 50, key=unique_key
                    )

                    ev = (sandsynlighed / 100) * odds - 1
                    st.write(f"• Odds: `{odds}` | Din EV: `{ev:.2f}`")

                    if ev > 0.05:
                        st.success("✅ Potentielt value bet!")
                    elif ev > 0:
                        st.info("⚠️ Lille positiv EV")
                    else:
                        st.warning("❌ Ikke et godt bet")
