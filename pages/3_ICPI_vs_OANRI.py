from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.append(str(APP_DIR))

from components.charts import icpi_oanri_scatter
from components.data import load_monthly_panel, load_product_layer
from components.narrative_cards import (
    action_panel,
    context_summary_panel,
    decision_matrix,
    insight_grid,
    page_header,
    product_sidebar,
    section_header,
)
from components.tables import compact_table


def _fmt_number(value: float) -> str:
    return f"{value:,.1f}"


st.set_page_config(page_title="Mapa de Señales", layout="wide")
product_sidebar()
page_header(
    "Mapa de Señales",
    "¿Qué barras combinan estrés nodal relativo con relevancia ajustada por régimen operativo?",
)

df = load_product_layer()
panel = load_monthly_panel()
if df.empty:
    st.error("La capa producto no está disponible.")
    st.stop()

start_month = "no disponible"
end_month = "no disponible"
month_count = 0
if not panel.empty and "month" in panel.columns:
    valid_months = panel["month"].dropna()
    if not valid_months.empty:
        start_month = valid_months.min().strftime("%Y-%m")
        end_month = valid_months.max().strftime("%Y-%m")
        month_count = int(valid_months.nunique())

priority_ab = int(df["due_diligence_priority"].isin(["Priority A", "Priority B"]).sum())
evidence_a = int(df["evidence_grade"].astype(str).str.upper().eq("A").sum())
high_priority_share = priority_ab / max(len(df), 1)

context_summary_panel(
    "Mapa de decisión: señal local vs prioridad ajustada",
    (
        f"Panel COES mensual {start_month} a {end_month}. Cada punto es una barra; "
        "la posición muestra estrés nodal y prioridad operativa promedio, el color muestra prioridad y "
        "el tamaño resume el score de due diligence."
    ),
    [
        ("Barras SEIN", f"{df['barra'].nunique():,.0f}", "unidad de análisis"),
        ("Prioridad A/B", f"{priority_ab:,.0f}", f"{high_priority_share:.0%} del universo"),
        ("Mediana estrés nodal", _fmt_number(float(df["avg_icpi"].median())), "línea vertical"),
        ("Evidencia A", f"{evidence_a:,.0f}", "identidad y contexto cerrados"),
    ],
)

insight_grid(
    [
        (
            "Decision question",
            "¿Qué barras combinan señal local alta con relevancia operativa ajustada?",
            "decision",
        ),
        (
            "Main insight",
            "El cuadrante superior derecho concentra las candidatas más fuertes para due diligence estructurada.",
            "evidence",
        ),
        (
            "Recommended action",
            "Empezar por el cuadrante superior derecho y contrastar con caso de barra, watchlist y exposición industrial.",
            "action",
        ),
        (
            "Uso correcto",
            "La matriz ordena la investigación: ayuda a decidir dónde mirar primero y qué hipótesis contrastar con contexto industrial, contractual y topológico.",
            "caveat",
        ),
    ]
)

section_header(
    "Mapa de señal estrés nodal/prioridad operativa",
    "Visual principal del producto: separa estrés nodal relativo de prioridad ajustada por régimen.",
)
st.plotly_chart(icpi_oanri_scatter(df), use_container_width=True)

section_header("Cómo leer los cuadrantes")
decision_matrix(
    [
        (
            "estrés nodal alto + prioridad operativa alto",
            "Candidata fuerte. La señal local y la lectura ajustada por sistema apuntan en la misma dirección.",
            "high",
        ),
        (
            "estrés nodal alto + prioridad operativa menor",
            "Señal local relevante. Revisar persistencia, meses extremos, contrato y evidencia topológica.",
            "local",
        ),
        (
            "estrés nodal menor + prioridad operativa alto",
            "Sensibilidad a régimen. Revisar si la prioridad aparece en meses de presión sistémica.",
            "system",
        ),
        (
            "estrés nodal menor + prioridad operativa menor",
            "Monitoreo base. Útil para contexto y comparación dentro del universo completo.",
            "monitor",
        ),
    ]
)

section_header(
    "Candidatas principales",
    "Lista corta ordenada por combinación de rankings prioridad operativa y estrés nodal para bajar a revisión por barra.",
)
top_candidates = df.sort_values(["rank_oanri", "rank_icpi"], na_position="last").head(15)
compact_table(
    top_candidates,
    [
        "barra",
        "nivel_tension_kv",
        "rank_icpi",
        "rank_oanri",
        "avg_icpi",
        "avg_oanri",
        "decision_priority_score",
        "robustness_flag_es",
        "evidence_grade",
        "due_diligence_priority_es",
    ],
)

action_panel(
    "What to do next",
    "Selecciona una barra del cuadrante superior derecho, revisa si su señal es persistente en Watchlist Mensual y luego evalúa si algún sector/contrato aumenta su prioridad en Exposición Industrial.",
)
