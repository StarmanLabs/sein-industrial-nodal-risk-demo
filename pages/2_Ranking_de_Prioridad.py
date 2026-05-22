from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.append(str(APP_DIR))

from components.data import load_product_layer
from components.filters import priority_filter, robustness_filter, tension_filter
from components.narrative_cards import (
    action_panel,
    insight_grid,
    metric_card,
    page_header,
    priority_system_legend,
    product_sidebar,
    section_header,
)
from components.tables import priority_table


st.set_page_config(page_title="Ranking de Prioridad por Barra", layout="wide")
product_sidebar()
page_header("Ranking de Prioridad por Barra", "¿Qué barras deberían revisarse primero?")

df = load_product_layer()
if df.empty:
    st.error("La capa producto no está disponible.")
    st.stop()

section_header(
    "Filtros de cola de decisión",
    "Ajusta la lista según prioridad, robustez o tensión. La tabla mantiene el orden por score de prioridad.",
)
filter_cols = st.columns([1.25, 1.05, 1.05])
with filter_cols[0]:
    selected_priorities = priority_filter(df, key="ranking_priority")
with filter_cols[1]:
    selected_robustness = robustness_filter(df, key="ranking_robustness")
with filter_cols[2]:
    selected_tension = tension_filter(df, key="ranking_tension")

filtered = df.copy()
if selected_priorities:
    filtered = filtered[filtered["due_diligence_priority"].isin(selected_priorities)]
if selected_robustness:
    robustness_col = "robustness_flag_es" if "robustness_flag_es" in filtered.columns else "robustness_flag"
    filtered = filtered[filtered[robustness_col].astype(str).isin(selected_robustness)]
if selected_tension:
    filtered = filtered[filtered["nivel_tension_kv"].isin(selected_tension)]

filtered = filtered.sort_values("decision_priority_score", ascending=False)

priority_ab_count = int(filtered["due_diligence_priority"].isin(["Priority A", "Priority B"]).sum())
evidence_a_count = int(filtered["evidence_grade"].astype(str).str.upper().eq("A").sum())
context_count = int(
    filtered["topology_context_asset"].astype(str).str.strip().ne("").sum()
    if "topology_context_asset" in filtered.columns
    else 0
)

cols = st.columns(4)
with cols[0]:
    metric_card("Barras filtradas", f"{len(filtered):,.0f}", "universo visible", kind="info")
with cols[1]:
    metric_card(
        "Prioridad A/B",
        f"{priority_ab_count:,.0f}",
        "cola principal",
        kind="warning",
    )
with cols[2]:
    metric_card(
        "Evidencia A",
        f"{evidence_a_count:,.0f}",
        "mapeo cerrado sin forzar",
        kind="good",
    )
with cols[3]:
    metric_card(
        "Contexto actual",
        f"{context_count:,.0f}",
        "activo/conexión trazable",
        kind="good",
    )

insight_grid(
    [
        (
            "Decision question",
            "¿Qué barras merecen el primer bloque de tiempo experto para revisión industrial?",
            "decision",
        ),
        (
            "Main insight",
            "La cola combina señal estrés nodal/prioridad operativa, recurrencia mensual, robustez y evidencia A de activo, conexión, subestación, central o corredor.",
            "evidence",
        ),
        (
            "Recommended action",
            "Usar la columna de acción recomendada como agenda: contrato, demanda, topología, confiabilidad y exposición.",
            "action",
        ),
        (
            "Interpretación",
            "Evidencia A significa que la identidad y el contexto de la barra son publicables para screening; la prioridad decide dónde mirar primero.",
            "caveat",
        ),
    ]
)

section_header("Cómo funcionan las categorías")
priority_system_legend()

section_header(
    "Decision queue por barra",
    "Tabla priorizada para convertir el ranking en una agenda concreta de análisis con contexto técnico/económico de cada barra.",
)
if filtered.empty:
    action_panel(
        "Sin resultados para los filtros activos",
        "Amplía prioridad, evidencia, robustez o tensión para recuperar barras candidatas en la cola de decisión.",
    )
else:
    priority_table(filtered)
    st.download_button(
        "Descargar lista filtrada",
        filtered.to_csv(index=False).encode("utf-8"),
        file_name="sein_barra_due_diligence_worklist.csv",
        mime="text/csv",
    )

action_panel(
    "Siguiente paso sugerido",
    "Toma las primeras barras filtradas y ábrelas en Caso de Estudio. Si la barra también aparece en Exposición Industrial o Watchlist Mensual, gana prioridad para revisión de contrato y demanda.",
)
