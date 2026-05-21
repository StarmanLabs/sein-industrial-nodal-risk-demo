from __future__ import annotations

import streamlit as st

from components.data import load_monthly_panel, load_product_layer, load_system_regime
from components.narrative_cards import (
    action_panel,
    badge_row,
    due_diligence_definition_grid,
    evidence_definition_grid,
    hero_header,
    indicator_definition_grid,
    insight_grid,
    methodology_definition_grid,
    metric_card,
    priority_system_legend,
    product_sidebar,
    section_header,
)


st.set_page_config(
    page_title="SEIN Industrial Nodal Risk Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)

product_sidebar()

hero_header(
    "Convierte señales nodales del SEIN en una cola de due diligence industrial",
    "Integra precios marginales COES, ICPI/OANRI, robustez, watchlists mensuales, "
    "escenarios industriales y evidencia topológica revisada para decidir qué barras "
    "merecen revisión primero.",
)

profiles = load_product_layer()
panel = load_monthly_panel()
regime = load_system_regime()

if profiles.empty:
    st.error(
        "No se encontró la capa pública del producto. Revisa que `data/public_demo` esté incluido en el despliegue."
    )
    st.stop()

cols = st.columns(5)
with cols[0]:
    metric_card("Barras", f"{profiles['barra'].nunique():,.0f}", "universo analítico", kind="info")
with cols[1]:
    metric_card("Meses", f"{panel['month'].nunique() if not panel.empty else 0:,.0f}", "2023-2025", kind="neutral")
with cols[2]:
    metric_card(
        "Evidencia A",
        f"{profiles['evidence_grade'].astype(str).str.upper().eq('A').sum():,.0f}",
        "muestra pública auditada",
        kind="good",
    )
with cols[3]:
    metric_card(
        "Prioridad A/B",
        f"{profiles['due_diligence_priority'].isin(['Priority A', 'Priority B']).sum():,.0f}",
        "cola principal",
        kind="warning",
    )
with cols[4]:
    metric_card(
        "Watchlist",
        f"{(profiles['due_diligence_priority'] == 'Watchlist').sum():,.0f}",
        "seguimiento mensual",
        kind="info",
    )

badge_row(
    [
        ("Decision-support system", "watchlist"),
        ("Relative nodal marginal-price stress", "monitor"),
        ("Evidence-informed prioritization", "evidence-a"),
        ("Industrial exposure screening", "priority-b"),
    ]
)

section_header(
    "Qué decisión habilita",
    "La página de inicio debe responder en menos de un minuto qué hace el producto, cómo leer sus métricas y dónde empezar la revisión.",
)
insight_grid(
    [
        (
            "Qué ordena",
            "Barras del SEIN según señales relativas de estrés marginal nodal y relevancia ajustada por régimen operativo.",
            "decision",
        ),
        (
            "Qué prioriza",
            "Casos A/B para revisión contractual, topológica, industrial o de confiabilidad, usando la muestra pública con evidencia A de contexto.",
            "evidence",
        ),
        (
            "A quién sirve",
            "Analistas económicos, energía, industria, minería, consultoría, planeamiento y equipos BI orientados a due diligence.",
            "action",
        ),
        (
            "Uso correcto",
            "Funciona como triage analítico. Las decisiones finales se contrastan con contrato, ingeniería, operación y evidencia externa.",
            "caveat",
        ),
    ]
)

section_header(
    "Qué significa due diligence en este dashboard",
    "No es un término decorativo: es el proceso de decidir qué barras merecen revisión más profunda y por qué.",
)
due_diligence_definition_grid()

section_header(
    "Con qué datos se construyen ICPI y OANRI",
    "Ambos indicadores nacen de precios marginales por barra del COES, agregados y comparados de forma mensual para crear señales relativas.",
)
methodology_definition_grid()

section_header("Guía rápida de lectura")
indicator_definition_grid()
evidence_definition_grid()
priority_system_legend()

action_panel(
    "Ruta recomendada de uso",
    "Empieza en Resumen Ejecutivo para ubicar las señales dominantes. Luego usa Ranking de Prioridad como cola de trabajo, ICPI vs OANRI como mapa estratégico, Watchlist para persistencia temporal, Exposición Industrial para escenarios sectoriales y Caso de Estudio para justificar una barra específica.",
)
