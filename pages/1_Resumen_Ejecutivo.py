from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.append(str(APP_DIR))

from components.charts import system_regime_line, top_bar_chart
from components.data import load_monthly_panel, load_product_layer, load_system_regime
from components.narrative_cards import (
    action_panel,
    insight_grid,
    metric_card,
    page_header,
    product_sidebar,
    section_header,
)


st.set_page_config(page_title="Resumen Ejecutivo", layout="wide")
product_sidebar()
page_header("Resumen Ejecutivo", "¿Dónde están las señales más fuertes de due diligence?")

profiles = load_product_layer()
panel = load_monthly_panel()
regime = load_system_regime()

if profiles.empty:
    st.error("La capa producto no está disponible.")
    st.stop()

cols = st.columns(5)
with cols[0]:
    metric_card("Barras analizadas", f"{profiles['barra'].nunique():,.0f}", "capa producto", kind="info")
with cols[1]:
    metric_card("Meses analizados", f"{panel['month'].nunique() if not panel.empty else 0}", "panel histórico")
with cols[2]:
    metric_card(
        "Revisión inmediata",
        f"{(profiles['due_diligence_priority'] == 'Priority A').sum():,.0f}",
        "primera cola",
        kind="danger",
    )
with cols[3]:
    metric_card(
        "Revisión selectiva",
        f"{(profiles['due_diligence_priority'] == 'Priority B').sum():,.0f}",
        "segunda revisión",
        kind="warning",
    )
with cols[4]:
    metric_card(
        "Seguimiento mensual",
        f"{(profiles['due_diligence_priority'] == 'Watchlist').sum():,.0f}",
        "monitoreo activo",
        kind="info",
    )

priority_ab = profiles[profiles["due_diligence_priority"].isin(["Priority A", "Priority B"])]
top_oanri = profiles.sort_values("rank_oanri", na_position="last").head(1).iloc[0]
top_icpi = profiles.sort_values("rank_icpi", na_position="last").head(1).iloc[0]

insight_grid(
    [
        (
            "Hallazgo ejecutivo",
            f"{len(priority_ab):,.0f} barras entran a la cola de revisión. Lideran {top_oanri['barra']} por prioridad operativa y {top_icpi['barra']} por estrés nodal.",
            "decision",
        ),
        (
            "Por qué importa",
            "estrés nodal captura señal nodal relativa; prioridad operativa añade lectura de régimen operativo para priorizar revisión.",
            "evidence",
        ),
        (
            "Siguiente acción",
            "Abrir revisión inmediata, contrastar exposición industrial y revisar contexto topológico antes de bajar a casos.",
            "action",
        ),
        (
            "Lectura correcta",
            "El ranking ordena una cola de due diligence: sirve para decidir dónde mirar primero y con qué hipótesis.",
            "caveat",
        ),
    ]
)

section_header(
    "Barras que dominan la cola ejecutiva",
    "Top 10 por prioridad operativa muestra prioridad ajustada; Top 10 por estrés nodal muestra estrés nodal relativo puro.",
)
left, right = st.columns(2)
with left:
    st.plotly_chart(
        top_bar_chart(profiles, "avg_oanri", "barra", "Top 10 barras por prioridad operativa"),
        use_container_width=True,
    )
with right:
    st.plotly_chart(
        top_bar_chart(profiles, "avg_icpi", "barra", "Top 10 barras por estrés nodal"),
        use_container_width=True,
    )

if not regime.empty:
    section_header(
        "Régimen operativo mensual",
        "Contexto sistémico usado para interpretar cuándo una señal nodal gana relevancia operativa.",
    )
    st.plotly_chart(system_regime_line(regime), use_container_width=True)

action_panel(
    "Lectura ejecutiva",
    "Usa esta vista como entrada ejecutiva: identifica las barras que concentran señal, valida si aparecen en la cola de revisión y luego baja al caso específico para revisar contrato, demanda industrial, contexto topológico y recurrencia mensual.",
)
