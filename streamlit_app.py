import streamlit as st

# Titel og introduktion
st.title("⚽ Sports Betting Analyseværktøj")
st.markdown("Indtast kampnavn, odds og estimeret sandsynlighed for at få en analyse af bettets værdi.")

# Inputfelter til brugeren
kampnavn = st.text_input("Kampnavn", "Manchester City vs Arsenal")
odds = st.number_input("Odds (decimal)", min_value=1.01, step=0.01, value=1.75)
sandsynlighed_procent = st.slider("Sandsynlighed for udfald (%)", 0, 100, 65)

# Beregning af Expected Value (EV)
sandsynlighed = sandsynlighed_procent / 100
expected_value = (sandsynlighed * odds) - 1

# Vis resultatet
st.write(f"🔍 **Expected Value (EV):** `{expected_value:.2f}`")

# Vurdering baseret på EV
if expected_value > 0.05:
    st.success("✅ Dette ser ud til at være et *value bet*!")
elif expected_value > 0:
    st.info("⚠️ Muligt value bet, men med lav margin.")
else:
    st.warning("❌ Ikke et anbefalet bet baseret på dine input.")

# Ekstra information
st.markdown("---")
st.markdown("💡 *Expected Value (EV) > 0 betyder, at bettet statistisk set har positiv forventet profit på lang sigt.*")
