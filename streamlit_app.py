import streamlit as st
import requests

# Din API-nøgle fra TheOddsAPI
API_KEY = "aad52ecc7febfdb6a9317aff12d49980"

st.title("⚽ Live Sports Betting Analyse")
st.markdown("Henter odds fra **flere bookmakere** og viser dig value bets i realtid.")

# Vælg sportsgren og område
sport = st.selectbox("Vælg sport", [
    "soccer_epl", "soccer_uefa_champs_league", "soccer_denmark_superliga",
    "basketball_nba", "tennis_atp", "mma_mixed_martial_arts"
])
region = st.selectbox("Vælg region", ["eu", "uk", "us", "au"])
market = st.selectbox("Vælg marked", ["h2h", "spreads", "totals"])

# Hent oddsdata
url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions={region}&markets={market}"
response = requests.get(url)

if response.status_code != 200:
    st.error(f"Kunne ikke hente odds. Fejlkode: {response.status_code}")
else:
    odds_data = response.json()
    st.write(f"✅ Fundet {len(odds_data)} kampe")

    for match in odds_data:
        st.subheader(f"{match['home_team']} vs {match['away_team']}")

        for bookmaker in match['bookmakers']:
            st.markdown(f"📊 **{bookmaker['title']}**")
            for m in bookmaker['markets']:
                for outcome in m['outcomes']:
                    navn = outcome['name']
                    odds = outcome['price']
                    sandsynlighed = st.slider(
                        f"Sæt sandsynlighed (%) for '{navn}' i kampen '{match['home_team']} vs {match['away_team']}'",
                        0, 100, 50, key=f"{navn}-{match['id']}"
                    )
                    ev = (sandsynlighed / 100) * odds - 1
                    st.write(f"• {navn} @ {odds} → EV: `{ev:.2f}`")
                    if ev > 0.05:
                        st.success("✅ Potentielt value bet!")
                    elif ev > 0:
                        st.info("⚠️ Lille positiv EV")
                    else:
                        st.warning("❌ Ikke et godt bet")
