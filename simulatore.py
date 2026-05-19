import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go

# Configurazione della pagina
st.set_page_config(page_title="Simulatore Eco-Evolutivo 2075", layout="wide")

st.title("PROIETTORE ECO-EVOLUTIVO 2075")
st.caption("Versione Python - Simulazione di sistemi aperti: crescita e declino delle risorse.")

# Inizializzazione Session State per evitare errori al primo caricamento
initial_states = {
    'fp_trend': 0.0, 'bc_trend': 0.0,
    'res_war': False, 'tech_bt': False, 'rest_wave': False, 'eco_tip': False,
    'year_res_war': 2030, 'year_tech_bt': 2035, 'year_rest_wave': 2040, 'year_eco_tip': 2045
}
for key, value in initial_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

def reset_years():
    """Ripristina gli anni predefiniti degli shock."""
    st.session_state.year_res_war = 2030
    st.session_state.year_tech_bt = 2035
    st.session_state.year_rest_wave = 2040
    st.session_state.year_eco_tip = 2045

def reset_shocks():
    """Resetta gli interruttori degli shock a False."""
    st.session_state.res_war = False
    st.session_state.tech_bt = False
    st.session_state.rest_wave = False
    st.session_state.eco_tip = False
    reset_years()

def reset_simulation():
    """Riporta la simulazione allo stato INVARIATO."""
    st.session_state.fp_trend = 0.0
    st.session_state.bc_trend = 0.0
    reset_shocks()

def apply_bau():
    # BAU: +0.2% impronta (peggioramento), -0.4% biocapacità
    st.session_state.fp_trend = 0.2
    st.session_state.bc_trend = -0.4
    reset_shocks()

def apply_transizione():
    # Transizione Verde: -1.2% impronta (miglioramento), +0.8% biocapacità
    st.session_state.fp_trend = -1.2
    st.session_state.bc_trend = 0.8
    reset_shocks()

def apply_collasso():
    # Collasso Ecologico: +0.5% impronta (peggioramento), -0.5% biocapacità
    st.session_state.fp_trend = 0.5
    st.session_state.bc_trend = -0.5
    reset_shocks()

# Sidebar per i controlli (Dinamiche di Trend e Shock)
with st.sidebar:
    st.header("⚙️ Dinamiche di Trend")
    st.write("**Base Line 2026 (gha):**")
    st.write("👣 Impronta: **1.75** | 🌱 Biocap.: **1.00**")
    
    fp_trend = st.slider("Trend Impronta (I) %", -3.0, 5.0, 0.0, 0.01, format="%.2f%%", key="fp_trend",
                         help="Valore positivo = incremento impronta (peggioramento).")
    bc_trend = st.slider("Trend Biocapacità (B) %", -3.0, 3.0, 0.0, 0.01, format="%.2f%%", key="bc_trend",
                         help="Valore positivo = aumento biocapacità (positivo).")
    
    st.header("⚠️ Shock di Scenario")
    
    # Shock 1: Inefficienza
    c1, c2 = st.columns([2, 1])
    res_war = c1.toggle("Inefficienza (+10% I)", key="res_war")
    year_res_war = c2.number_input("Anno", 2026, 2075, 2030, key="year_res_war", label_visibility="collapsed")
    
    # Shock 2: Svolta Tech
    c1, c2 = st.columns([2, 1])
    tech_bt = c1.toggle("Svolta Tech (-15% I)", key="tech_bt")
    year_tech_bt = c2.number_input("Anno", 2026, 2075, 2035, key="year_tech_bt", label_visibility="collapsed")
    
    # Shock 3: Riforestazione
    c1, c2 = st.columns([2, 1])
    rest_wave = c1.toggle("Riforestazione (+12% B)", key="rest_wave")
    year_rest_wave = c2.number_input("Anno", 2026, 2075, 2040, key="year_rest_wave", label_visibility="collapsed")
    
    # Shock 4: Punto Critico
    c1, c2 = st.columns([2, 1])
    eco_tip = c1.toggle("Punto Critico (-20% B)", key="eco_tip")
    year_eco_tip = c2.number_input("Anno", 2026, 2075, 2045, key="year_eco_tip", label_visibility="collapsed")

    st.header("🚀 Scenari Rapidi")
    col1, col2 = st.columns(2)
    with col1:
        st.button("📉 BAU", on_click=apply_bau, use_container_width=True, help="Business As Usual")
        st.button("🔥 Collasso", on_click=apply_collasso, use_container_width=True)
    with col2:
        st.button("🌿 Verde", on_click=apply_transizione, use_container_width=True)
        st.button("⚪ INVARIATO", on_click=reset_simulation, use_container_width=True)

# Funzione per calcolare la simulazione
def run_simulation(fp_trend, bc_trend, shocks_active, shock_years):
    current_fp = 1.75
    current_bc = 1.0
    cumulative_debt = 0
    results = []
    
    res_war, tech_bt, rest_wave, eco_tip = shocks_active

    for year in range(2026, 2076):
        # Applicazione Shock
        if year == shock_years['res_war'] and res_war: current_fp *= 1.10
        if year == shock_years['tech_bt'] and tech_bt: current_fp *= 0.85
        if year == shock_years['rest_wave'] and rest_wave: current_bc *= 1.12
        if year == shock_years['eco_tip'] and eco_tip: current_bc *= 0.80
        
        # Applicazione Trend
        current_fp *= (1 + fp_trend / 100)
        current_bc *= (1 + bc_trend / 100)
        
        debt = current_fp - current_bc
        cumulative_debt += debt
        
        ratio = current_bc / current_fp
        if ratio >= 1:
            overshoot = "Sostenibile"
        else:
            days = int(ratio * 365)
            dt = datetime.date(year, 1, 1) + datetime.timedelta(days=days)
            overshoot = dt.strftime("%d %B")
            
        results.append({
            "Anno": year,
            "Impronta": round(current_fp, 3),
            "Biocapacità": round(current_bc, 3),
            "Debito Accumulato": round(cumulative_debt, 2),
            "Overshoot": overshoot,
            "is_deficit": ratio < 1
        })
    return pd.DataFrame(results)

# Esecuzione simulazione con parametri espliciti
shocks_active = (res_war, tech_bt, rest_wave, eco_tip)
shock_years = {
    'res_war': st.session_state.year_res_war,
    'tech_bt': st.session_state.year_tech_bt,
    'rest_wave': st.session_state.year_rest_wave,
    'eco_tip': st.session_state.year_eco_tip
}

df = run_simulation(fp_trend, bc_trend, shocks_active, shock_years)

# Aggiunta pulsante download nella sidebar (ora che il dataframe df è pronto)
with st.sidebar:
    st.subheader("💾 Esportazione")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Scarica Dati (CSV)",
        data=csv,
        file_name=f'simulazione_eco_{datetime.datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        use_container_width=True
    )

# Layout principale con colonne
col_chart, col_stats = st.columns([3, 1])

with col_chart:
    st.subheader("📈 Analisi Proiettiva 2026-2075")
    
    # Grafico Avanzato con Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Anno"], y=df["Impronta"], name="Impronta (I)", 
                             line=dict(color='#ef4444', width=3), fill='tonexty'))
    fig.add_trace(go.Scatter(x=df["Anno"], y=df["Biocapacità"], name="Biocapacità (B)", 
                             line=dict(color='#10b981', width=3), fill='tozeroy'))
    
    # Linea di riferimento capacità base
    fig.add_hline(y=1.0, line_dash="dash", line_color="rgba(100, 116, 139, 0.5)", 
                  annotation_text="Soglia Rigenerazione 2026")

    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=40, b=0),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📉 Accumulo del Debito Ecologico")
    st.area_chart(df.set_index("Anno")["Debito Accumulato"], color="#6366f1", height=250)

with col_stats:
    last = df.iloc[-1]
    
    st.metric("Debito al 2075", f"{last['Debito Accumulato']} Terre")
    
    st.write("---")
    st.write("**🩺 Stato del Sistema**")
    if last['is_deficit']:
        st.error(f"🔴 DEFICIT CRONICO")
    else:
        st.success(f"🟢 EQUILIBRIO")
        
    st.write("**📅 Overshoot Day 2075**")
    st.info(f"📅 {last['Overshoot']}")

    st.write("---")
    st.write("**📊 Ettari pro capite (gha) al 2075**")
    st.write(f"👣 Impronta: **{last['Impronta']:.2f}**")
    st.write(f"🌱 Biocap.: **{last['Biocapacità']:.2f}**")

# Tabella dati per consultazione rapida
st.subheader("📋 Dati Decennali di Sintesi")
st.dataframe(df[df['Anno'].isin([2030, 2040, 2050, 2060, 2075])], use_container_width=True)

st.divider()
st.subheader("🔍 Analisi degli Scenari (Findings)")
f_col1, f_col2, f_col3 = st.columns(3)

findings_years = [2035, 2050, 2075]
cols = [f_col1, f_col2, f_col3]
titles = ["Punto di Controllo 2035", "Bilancio Metà Secolo 2050", "Lascito Finale 2075"]

for y, col, title in zip(findings_years, cols, titles):
    row = df[df['Anno'] == y].iloc[0]
    with col:
        st.markdown(f"### {title}")
        if row['is_deficit']:
            st.warning(f"**Deficit Ecologico**\n\nL'impronta ({row['Impronta']:.2f} gha) supera la capacità rigenerativa ({row['Biocapacità']:.2f} gha).")
        else:
            st.success(f"**Surplus Ecologico**\n\nIl sistema è in equilibrio. Biocapacità: {row['Biocapacità']:.2f} gha.")
        
        st.write(f"Debito: **{row['Debito Accumulato']}** Terre.")
        if y == 2075:
            st.caption("Risultato finale della strategia selezionata.")