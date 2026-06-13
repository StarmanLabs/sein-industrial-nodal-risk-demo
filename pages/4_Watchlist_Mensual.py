from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.append(str(APP_DIR))

from components.charts import barra_month_line, watchlist_heatmap
from components.data import load_monthly_panel, load_product_layer, load_watchlist
from components.filters import barra_selector, priority_filter
from components.narrative_cards import (
    action_panel,
    insight_grid,
    metric_card,
    page_header,
    product_sidebar,
    section_header,
)
from components.tables import compact_table


def classify_pattern(rows) -> str:
    if rows.empty:
        return "Patrón sin información suficiente para lectura temporal."
    priority_months = int((rows["decision_tier"] == "Priority due diligence").sum())
    watchlist_months = int((rows["decision_tier"] == "Watchlist").sum())
    total = max(len(rows), 1)
    if priority_months / total >= 0.35:
        return "Señal persistente: aparece de forma recurrente en meses de prioridad y merece seguimiento mensual estructurado."
    if priority_months + watchlist_months >= 4:
        return "Señal episódica recurrente: no domina todos los meses, pero reaparece lo suficiente para mantenerla en seguimiento mensual."
    if priority_months > 0:
        return "Episodio puntual relevante: conviene revisar el mes específico y contrastarlo con contrato, demanda y contexto operativo."
    return "Señal baja o intermitente: útil como referencia de contexto dentro del universo analítico."


st.set_page_config(page_title="Seguimiento Mensual", layout="wide")
product_sidebar()
page_header("Seguimiento Mensual", "¿Cuándo aparecen episodios de estrés y son persistentes o episódicos?")

watchlist = load_watchlist()
panel = load_monthly_panel()
profiles = load_product_layer()
if watchlist.empty:
    st.error("La capa de seguimiento mensual no está disponible.")
    st.stop()

priority_col = next((column for column in ["Prioridad operativa", "OANRI_v10", "prioridad_operativa"] if column in watchlist.columns), None)
stress_col = next((column for column in ["Estrés nodal", "ICPI_v8", "estres_nodal"] if column in watchlist.columns), None)
if priority_col is None or stress_col is None:
    st.error("La vista mensual requiere columnas de estrés nodal y prioridad operativa.")
    st.stop()

section_header(
    "Filtros temporales y de prioridad",
    "Ordena el mapa por prioridad del producto para ver primero las barras más relevantes. Cada fila es una barra y cada columna es un mes.",
)
filter_cols = st.columns([1.1, 1.2])
with filter_cols[0]:
    selected_priorities = priority_filter(
        profiles,
        key="watchlist_priority",
        label="Tipo de señal",
        placeholder="Todas las categorías",
    ) if not profiles.empty else []
with filter_cols[1]:
    top_n = st.slider("Barras visibles en heatmap", min_value=10, max_value=50, value=25, step=5)

filtered_profiles = profiles.copy()
if selected_priorities:
    filtered_profiles = filtered_profiles[filtered_profiles["due_diligence_priority"].isin(selected_priorities)]

ordered_barras = (
    filtered_profiles.sort_values("decision_priority_score", ascending=False)["barra"].head(top_n).tolist()
    if not filtered_profiles.empty
    else watchlist["barra"].value_counts().head(top_n).index.tolist()
)
heatmap_data = watchlist[watchlist["barra"].isin(ordered_barras)]

cols = st.columns(4)
with cols[0]:
    metric_card("Barras en mapa", f"{heatmap_data['barra'].nunique():,.0f}", "top por prioridad", kind="info")
with cols[1]:
    metric_card("Meses en seguimiento", f"{watchlist['month'].nunique():,.0f}", "cobertura mensual")
with cols[2]:
    metric_card("Observaciones top", f"{len(watchlist):,.0f}", "barra-mes")
with cols[3]:
    metric_card("Máx. prioridad operativa", f"{pd.to_numeric(watchlist[priority_col], errors='coerce').max():.1f}", "episodio más alto", kind="warning")

insight_grid(
    [
        (
            "Decision question",
            "¿La señal aparece una sola vez o se repite durante varios meses?",
            "decision",
        ),
        (
            "Cómo leer el color",
            "Color más intenso significa prioridad operativa mensual más alto: ese mes la barra tuvo mayor prioridad relativa dentro del sistema.",
            "evidence",
        ),
        (
            "Cómo leer la fila",
            "Una fila con varios meses intensos sugiere señal recurrente. Una fila con un solo bloque intenso sugiere episodio puntual.",
            "action",
        ),
        (
            "Qué decisión habilita",
            "Persistencia eleva prioridad de seguimiento. Episodios puntuales se revisan si coinciden con exposición contractual o industrial sensible.",
            "caveat",
        ),
    ]
)

section_header(
    "Mapa mensual de seguimiento",
    "Léelo de izquierda a derecha. Si una barra mantiene colores fuertes en varios meses, no es ruido visual: es una candidata para seguimiento mensual.",
)
st.plotly_chart(watchlist_heatmap(heatmap_data, order=ordered_barras), use_container_width=True)

section_header(
    "Lectura por barra",
    "Selecciona una barra para ver evolución estrés nodal/prioridad operativa y clasificar persistencia vs episodios.",
)
selected_barra = barra_selector(heatmap_data, key="watchlist_barra")
if selected_barra and not panel.empty:
    selected_rows = panel[panel["barra"] == selected_barra].sort_values("month")
    action_panel("Interpretación automática", classify_pattern(selected_rows))
    st.plotly_chart(barra_month_line(panel, selected_barra), use_container_width=True)

section_header("Top mensual de señales")
compact_table(
    watchlist.sort_values(["month", "ranking_mensual_v10"]).head(120),
    [
        "month",
        "barra",
        stress_col,
        priority_col,
        "ranking_mensual_v10",
        "decision_tier",
        "primary_driver",
    ],
)
