from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.append(str(APP_DIR))

from components.charts import barra_component_profile, barra_month_line, barra_profile_score_bars
from components.data import load_monthly_panel, load_product_layer
from components.filters import barra_selector
from components.narrative_cards import (
    action_panel,
    decision_summary_card,
    humanize_analytical_text,
    insight_grid,
    metric_card,
    page_header,
    product_sidebar,
    section_header,
)


st.set_page_config(page_title="Caso de Estudio por Barra", layout="wide")
product_sidebar()
page_header("Caso de Estudio por Barra", "¿Por qué esta barra merece atención?")

profiles = load_product_layer()
panel = load_monthly_panel()
if profiles.empty:
    st.error("La capa producto no está disponible.")
    st.stop()

barra = barra_selector(profiles, key="case_barra")
if not barra:
    st.stop()

row = profiles[profiles["barra"] == barra].iloc[0]
priority_label = row.get("due_diligence_priority_es", row["due_diligence_priority"])
priority_kind = {
    "Prioridad A": "priority-a",
    "Prioridad B": "priority-b",
    "Watchlist": "info",
    "Monitorear": "neutral",
}.get(str(priority_label), "neutral")


def _clean(value: object, fallback: str = "No disponible en la capa producto") -> str:
    text = "" if value is None else str(value).strip()
    if not text or text.lower() in {"nan", "none", "nat"}:
        return fallback
    return humanize_analytical_text(text)


cols = st.columns(5)
with cols[0]:
    metric_card("Prioridad", priority_label, "decisión sugerida", kind=priority_kind)
with cols[1]:
    metric_card("Score", f"{row['decision_priority_score']:.1f}", "0-100 relativo", kind="warning")
with cols[2]:
    metric_card("Rank ICPI", f"{row['rank_icpi']:.0f}", "1 = mayor señal", kind="info")
with cols[3]:
    metric_card("Rank OANRI", f"{row['rank_oanri']:.0f}", "1 = mayor prioridad", kind="info")
with cols[4]:
    metric_card("Evidencia", row["evidence_grade"], "soporte revisado", kind="good")

decision_summary_card(
    priority_label,
    f"{row['decision_priority_score']:.1f}/100",
    row["priority_reason"],
    row["recommended_action"],
    (
        f"Evidencia {row['evidence_grade']}; "
        f"{humanize_analytical_text(row.get('robustness_flag_es', row['robustness_flag']))}."
    ),
)

section_header(
    "Contexto actual de la barra",
    "La evidencia A no reemplaza un estudio eléctrico: cierra identidad, tensión y contexto útil para decidir qué revisar hoy.",
)
price_window = (
    f"{_clean(row.get('coes_price_key_first_month'), 'sin inicio')} a "
    f"{_clean(row.get('coes_price_key_last_month'), 'sin fin')}"
)
insight_grid(
    [
        (
            "Activo o conexión relevante",
            _clean(row.get("topology_context_asset"), row["barra"]),
            "decision",
        ),
        (
            "Tipo de contexto",
            f"{_clean(row.get('topology_context_type_es'))}. Rol: {_clean(row.get('evidence_family_es'))}.",
            "evidence",
        ),
        (
            "Cobertura COES",
            f"Serie mensual usada para ICPI/OANRI: {price_window}; meses observados: {_clean(row.get('coes_price_key_months_observed'), '0')}.",
            "action",
        ),
        (
            "Límite de lectura",
            _clean(row.get("decision_claim_boundary")),
            "caveat",
        ),
    ]
)
action_panel(
    "Por qué este contexto importa",
    _clean(row.get("topology_context_summary")),
)
if _clean(row.get("external_evidence_summary"), ""):
    action_panel(
        "Evidencia externa usada",
        _clean(row.get("external_evidence_summary")),
    )

insight_grid(
    [
        (
            "Why it appears here",
            humanize_analytical_text(row["priority_reason"]),
            "decision",
        ),
        (
            "Support quality",
            f"Evidencia {row['evidence_grade']} y {humanize_analytical_text(row.get('robustness_flag_es', row['robustness_flag']))}.",
            "evidence",
        ),
        (
            "What to do next",
            humanize_analytical_text(row["recommended_action"]),
            "action",
        ),
        (
            "Interpretación",
            "La barra se lee como candidata de revisión: el valor está en contrastar señal, recurrencia, exposición y contexto.",
            "caveat",
        ),
    ]
)

section_header(
    "Componentes de la señal",
    "Scores en escala relativa 0-100. Valores más altos indican mayor intensidad dentro del universo analizado.",
)
left, right = st.columns(2)
with left:
    st.plotly_chart(barra_profile_score_bars(row), use_container_width=True)
with right:
    if not panel.empty:
        st.plotly_chart(barra_component_profile(panel, barra), use_container_width=True)

section_header(
    "Evolución mensual",
    "Permite diferenciar señal persistente, episódica o puntual antes de decidir la siguiente revisión.",
)
if not panel.empty:
    st.plotly_chart(barra_month_line(panel, barra), use_container_width=True)

section_header("Due-diligence checklist")
check_cols = st.columns(2)
with check_cols[0]:
    action_panel(
        "Validaciones analíticas",
        "1. Confirmar si la señal es persistente o episódica. 2. Revisar meses con mayor OANRI. 3. Comparar ranking ICPI/OANRI. 4. Verificar robustez y evidencia.",
    )
with check_cols[1]:
    action_panel(
        "Preguntas de negocio",
        "1. ¿Existe demanda industrial cercana? 2. ¿La exposición es spot, indexada o cubierta? 3. ¿La evidencia topológica soporta revisión adicional? 4. ¿Hay indicadores de confiabilidad relevantes?",
    )
