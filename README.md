# PROIETTORE ECO-EVOLUTIVO 2075

Questo simulatore Python (Streamlit) è uno strumento di analisi proiettiva per lo studio della sostenibilità globale fino al 2075.

## 🎯 Obiettivo
Analizzare l'evoluzione del rapporto tra l'Impronta Ecologica umana e la Biocapacità del pianeta, calcolando il debito ecologico accumulato e l'Overshoot Day.

## 🛠 Funzionalità Principali

### 📈 Simulazione Dinamica
* **Baseline 2026**: Basata sul rapporto tra l'Impronta Totale stimata (21.736.852.078,6) e la Biocapacità Totale (12.068.507.633,5), che determina il punto di partenza di **1.80 Terre**.
* **Controllo Trend**: Slider con precisione 0.01% per modellare cambiamenti sottili ma determinanti nel lungo periodo.

### 🚀 Scenari e Shock
* **Scenari Rapidi**: Attivazione immediata di modelli predefiniti (BAU, Verde, Collasso).
* **Shock Temporali**: Possibilità di inserire eventi dirompenti (Svolte tech, punti critici, inefficienze) scegliendo l'anno esatto dell'accadimento.

### 📊 Visualizzazione e Metriche
* **Grafici Interattivi**: Utilizzo di Plotly per un'analisi granulare anno per anno.
* **Overshoot Day**: Calcolo dinamico del giorno di superamento delle risorse.
* **Findings Decennali**: Analisi automatizzata dei risultati per gli anni 2035, 2050 e 2075.

## 💻 Requisiti Tecnici
Il simulatore richiede le seguenti librerie Python:
* `streamlit`
* `pandas`
* `plotly`

## 📥 Esportazione Dati
Tutti i risultati della simulazione possono essere esportati in formato CSV tramite il pulsante dedicato nella sidebar.
