import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go

# Configurazione della pagina
st.set_page_config(page_title="Simulatore Eco-Evolutivo 2075", layout="wide")

st.title("PROIETTORE ECO-EVOLUTIVO 2075")
st.caption("Versione Python - Simulazione di sistemi aperti: crescita e declino delle risorse.")

# Ottimizzazione CSS per Smartphone
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.6rem !important; }
    [data-testid="stMetricLabel"] { font-size: 0.9rem !important; }
    @media (max-width: 640px) {
        .main .block-container { padding-left: 1rem; padding-right: 1rem; }
        [data-testid="stHeader"] { display: none; }
    }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione Session State per evitare errori al primo caricamento
initial_states = {
    'fp_trend': 0.0, 'bc_trend': 0.0,
    'res_war': False, 'tech_bt': False, 'rest_wave': False, 'eco_tip': False,
    'range_res_war': (2030, 2030), 'range_tech_bt': (2035, 2035), 'range_rest_wave': (2040, 2040), 'range_eco_tip': (2045, 2045),
    'val_res_war': 10.0, 'val_tech_bt': -15.0, 'val_rest_wave': 12.0, 'val_eco_tip': -20.0
}
for key, value in initial_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

def reset_years():
    """Ripristina gli anni predefiniti degli shock."""
    st.session_state.range_res_war = (2030, 2030)
    st.session_state.range_tech_bt = (2035, 2035)
    st.session_state.range_rest_wave = (2040, 2040)
    st.session_state.range_eco_tip = (2045, 2045)

def reset_shock_vals():
    """Ripristina le intensità predefinite degli shock."""
    st.session_state.val_res_war = 10.0
    st.session_state.val_tech_bt = -15.0
    st.session_state.val_rest_wave = 12.0
    st.session_state.val_eco_tip = -20.0

def reset_shocks():
    """Resetta gli interruttori degli shock a False."""
    st.session_state.res_war = False
    st.session_state.tech_bt = False
    st.session_state.rest_wave = False
    st.session_state.eco_tip = False
    reset_years()
    reset_shock_vals()

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
    st.write("**Baseline 2026 (Stime Globali):**")
    st.caption("👣 Impronta: 21.736.852.078,6")
    st.caption("🌱 Biocap.: 12.068.507.633,5")
    st.write("🌍 Rapporto: **1.80 Terre**")
    st.divider()
    
    fp_trend = st.slider("Trend Impronta (I) %", -3.0, 5.0, 0.0, 0.01, format="%.2f%%", key="fp_trend",
                         help="Valore positivo = incremento impronta (peggioramento).")
    bc_trend = st.slider("Trend Biocapacità (B) %", -3.0, 3.0, 0.0, 0.01, format="%.2f%%", key="bc_trend",
                         help="Valore positivo = aumento biocapacità (positivo).")
    
    st.header("🚀 Scenari Rapidi")
    col1, col2 = st.columns(2)
    with col1:
        st.button("📉 BAU", on_click=apply_bau, use_container_width=True, help="Business As Usual")
        st.button("🔥 Collasso", on_click=apply_collasso, use_container_width=True)
    with col2:
        st.button("🌿 Verde", on_click=apply_transizione, use_container_width=True)
        st.button("⚪ INVARIATO", on_click=reset_simulation, use_container_width=True)

    st.header("⚠️ Shock di Scenario")
    
    # Shock 1: Inefficienza
    res_war = st.toggle("Inefficienza", key="res_war")
    range_res_war = st.slider("Periodo Inefficienza", 2026, 2075, st.session_state.range_res_war, key="range_res_war", label_visibility="collapsed")
    val_res_war = st.slider("Intensità Inefficienza (%)", 0.0, 50.0, st.session_state.val_res_war, 0.5, format="%.1f%%", key="val_res_war")
    
    # Shock 2: Svolta Tech
    tech_bt = st.toggle("Svolta Tech", key="tech_bt")
    range_tech_bt = st.slider("Periodo Svolta Tech", 2026, 2075, st.session_state.range_tech_bt, key="range_tech_bt", label_visibility="collapsed")
    val_tech_bt = st.slider("Intensità Svolta Tech (%)", -50.0, 0.0, st.session_state.val_tech_bt, 0.5, format="%.1f%%", key="val_tech_bt")
    
    # Shock 3: Riforestazione
    rest_wave = st.toggle("Riforestazione", key="rest_wave")
    range_rest_wave = st.slider("Periodo Riforestazione", 2026, 2075, st.session_state.range_rest_wave, key="range_rest_wave", label_visibility="collapsed")
    val_rest_wave = st.slider("Intensità Riforestazione (%)", 0.0, 50.0, st.session_state.val_rest_wave, 0.5, format="%.1f%%", key="val_rest_wave")
    
    # Shock 4: Punto Critico
    eco_tip = st.toggle("Punto Critico", key="eco_tip")
    range_eco_tip = st.slider("Periodo Punto Critico", 2026, 2075, st.session_state.range_eco_tip, key="range_eco_tip", label_visibility="collapsed")
    val_eco_tip = st.slider("Intensità Punto Critico (%)", -50.0, 0.0, st.session_state.val_eco_tip, 0.5, format="%.1f%%", key="val_eco_tip")

# Funzione per calcolare la simulazione
def run_simulation(fp_trend, bc_trend, shocks_active, shock_years, shock_vals):
    current_fp = 1.8
    current_bc = 1.0
    cumulative_debt = 0
    results = []
    
    res_war, tech_bt, rest_wave, eco_tip = shocks_active
    res_war_v, tech_bt_v, rest_wave_v, eco_tip_v = shock_vals

    for year in range(2026, 2076):
        # 1. APPLICAZIONE SHOCK (Variazioni discrete puntuali o durature)
        # Se l'anno corrente è all'interno dell'intervallo e lo shock è attivo
        if shock_years['res_war'][0] <= year <= shock_years['res_war'][1] and res_war: current_fp *= (1 + res_war_v / 100)
        if shock_years['tech_bt'][0] <= year <= shock_years['tech_bt'][1] and tech_bt: current_fp *= (1 + tech_bt_v / 100)
        if shock_years['rest_wave'][0] <= year <= shock_years['rest_wave'][1] and rest_wave: current_bc *= (1 + rest_wave_v / 100)
        if shock_years['eco_tip'][0] <= year <= shock_years['eco_tip'][1] and eco_tip: current_bc *= (1 + eco_tip_v / 100)
        
        # 2. APPLICAZIONE TREND (Crescita composta annuale)
        # Formula: Valore = Valore * (1 + r)
        current_fp *= (1 + fp_trend / 100)
        current_bc *= (1 + bc_trend / 100)
        
        # 3. CALCOLO BILANCIO E DEBITO
        debt = current_fp - current_bc
        cumulative_debt += debt
        
        # 4. CALCOLO OVERSHOOT DAY
        # Proporzione della biocapacità rispetto all'impronta su base 365 giorni
        ratio = current_bc / current_fp
        if ratio < 1:
            days = int(ratio * 365)
            dt = datetime.date(year, 1, 1) + datetime.timedelta(days=days)
            overshoot = dt.strftime("%d %B")
        else:
            overshoot = "Sostenibile"
            
        results.append({
            "Anno": year,
            "Impronta": round(current_fp, 3),
            "Biocapacità": round(current_bc, 3),
            "Debito Accumulato": round(cumulative_debt, 2),
            "Overshoot": overshoot,
            "is_deficit": ratio < 1
        })
    return pd.DataFrame(results)

# --- LOGICA DI ESECUZIONE ---

# Recupero parametri da session_state/sidebar
fp_trend_val = st.session_state.fp_trend
bc_trend_val = st.session_state.bc_trend

# Preparazione shock
shocks_active = (res_war, tech_bt, rest_wave, eco_tip)
shock_years = {
    'res_war': range_res_war,
    'tech_bt': range_tech_bt,
    'rest_wave': range_rest_wave,
    'eco_tip': range_eco_tip
}
shock_vals = (val_res_war, val_tech_bt, val_rest_wave, val_eco_tip)

df = run_simulation(fp_trend_val, bc_trend_val, shocks_active, shock_years, shock_vals)

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

# --- LAYOUT PRINCIPALE ---
col_chart, col_stats = st.columns([3, 1])

with col_chart:
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
    # Configurazione per rendere il grafico touch-friendly
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.subheader("📉 Accumulo del Debito Ecologico")
    st.area_chart(df.set_index("Anno")["Debito Accumulato"], color="#6366f1", height=200)

with col_stats:
    last = df.iloc[-1]
    
    st.metric("Debito al 2075", f"{last['Debito Accumulato']} Terre")
    
    st.divider()
    st.write("**🩺 Stato del Sistema**")
    if last['is_deficit']:
        st.error(f"🔴 DEFICIT CRONICO")
    else:
        st.success(f"🟢 EQUILIBRIO")
        
    st.write("**📅 Overshoot Day 2075**")
    st.info(f"📅 {last['Overshoot']}")

    st.divider()
    st.write("**📊 Valori al 2075 (Terre)**")
    st.write(f"👣 Impronta: **{last['Impronta']:.2f}**")
    st.write(f"🌱 Biocap.: **{last['Biocapacità']:.2f}**")

# Tabella dati (compattata per mobile) e Findings
st.divider()
st.subheader("📋 Dati Decennali di Sintesi")
st.dataframe(df[df['Anno'].isin([2030, 2040, 2050, 2060, 2075])], use_container_width=True, hide_index=True)

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
            st.warning(f"**Deficit Ecologico**\n\nL'impronta ({row['Impronta']:.2f}) supera la capacità rigenerativa ({row['Biocapacità']:.2f}).")
        else:
            st.success(f"**Surplus Ecologico**\n\nIl sistema è in equilibrio. Biocapacità: {row['Biocapacità']:.2f}.")
        
        st.write(f"Debito: **{row['Debito Accumulato']}** Terre.")
        if y == 2075:
            st.caption("Risultato finale della strategia selezionata.")