from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.append(str(APP_DIR))

from components.charts import contract_comparison_chart, sector_exposure_bar_chart
from components.data import load_contract_scenarios, load_sector_profiles, load_simulator_sample
from components.filters import CONTRACT_LABELS, SECTOR_LABELS, contract_selector, sector_selector
from components.narrative_cards import action_panel, insight_grid, metric_card, page_header, product_sidebar, section_header
from components.tables import compact_table


st.set_page_config(page_title="Exposición Industrial", layout="wide")
product_sidebar()
page_header(
    "Exposición Industrial",
    "¿Qué combinaciones sector-barra-contrato merecen revisión bajo supuestos explícitos?",
)

sector_df = load_sector_profiles()
contract_df = load_contract_scenarios()
sample = load_simulator_sample()

if sector_df.empty:
    st.error("Los perfiles sector-barra no están disponibles.")
    st.stop()

section_header(
    "Simulador de screening sectorial",
    "Selecciona un arquetipo sectorial y contractual. El resultado ordena combinaciones sector-barra para due diligence, no pagos esperados.",
)
left, right = st.columns(2)
with left:
    sector = sector_selector(sector_df)
with right:
    contract = contract_selector(sector_df)

filtered = sector_df.copy()
if sector:
    filtered = filtered[filtered["sector"] == sector]
if contract:
    filtered = filtered[filtered["contract_type"] == contract]
filtered = filtered.sort_values("profile_priority_score", ascending=False)

sector_label = SECTOR_LABELS.get(sector, sector) if sector else "Todos los sectores"
contract_label = CONTRACT_LABELS.get(contract, contract) if contract else "Todos los contratos"

scenario_cols = st.columns(4)
with scenario_cols[0]:
    metric_card("Perfiles filtrados", f"{len(filtered):,.0f}", "sector-contrato-barra", kind="info")
with scenario_cols[1]:
    metric_card("Barras únicas", f"{filtered['barra'].nunique():,.0f}", "candidatas")
with scenario_cols[2]:
    metric_card("Score promedio", f"{filtered['avg_industrial_exposure_score'].mean():.1f}", "exposición media", kind="warning")
with scenario_cols[3]:
    metric_card("Score p90", f"{filtered['p90_industrial_exposure_score'].mean():.1f}", "cola del escenario", kind="danger")

leader = filtered.iloc[0] if not filtered.empty else None
leader_text = (
    f"Bajo {sector_label} y {contract_label}, {leader['barra']} lidera el escenario con score {leader['profile_priority_score']:.1f}."
    if leader is not None
    else "No hay combinaciones para el filtro activo."
)

insight_grid(
    [
        ("Pregunta de decisión", "¿Qué combinación sector-barra debe revisarse primero bajo supuestos explícitos de exposición?", "decision"),
        ("Hallazgo principal", leader_text, "evidence"),
        ("Acción recomendada", "Revisar cobertura contractual, participación spot, demanda mensual y sensibilidad operativa del sector seleccionado.", "action"),
        ("Caveat metodológico", "Los escenarios son salidas de screening basadas en supuestos; se interpretan como cola de revisión, no como forecast de factura.", "caveat"),
    ]
)

section_header(
    "Ranking sector-barra",
    "Bajo supuestos explícitos de exposición, esta combinación sector-barra merece mayor prioridad de due diligence.",
)
if filtered.empty:
    action_panel("Sin resultados para el escenario", "Cambia sector o contrato para recuperar perfiles de exposición industrial.")
else:
    st.plotly_chart(sector_exposure_bar_chart(filtered), use_container_width=True)
    compact_table(
        filtered.head(50),
        [
            "sector",
            "contract_type",
            "barra",
            "avg_industrial_exposure_score",
            "p90_industrial_exposure_score",
            "priority_months",
            "watchlist_months",
            "signal_stability_label_es",
            "dominant_driver",
            "profile_priority_score",
        ],
    )

if not contract_df.empty:
    section_header("Sensibilidad contractual", "Comparación agregada por tipo de contrato para entender cómo cambia la prioridad del escenario.")
    selected_contract_df = contract_df[contract_df["sector"] == sector] if sector else contract_df
    st.plotly_chart(contract_comparison_chart(selected_contract_df), use_container_width=True)
    compact_table(
        selected_contract_df,
        ["sector", "contract_type", "unique_barras", "monthly_mwh", "spot_share", "avg_exposure_score", "p90_exposure_score", "priority_rows", "watchlist_rows"],
    )

if not sample.empty:
    st.download_button(
        "Descargar muestra del simulador",
        sample.head(500).to_csv(index=False).encode("utf-8"),
        file_name="industrial_exposure_sample.csv",
        mime="text/csv",
    )

action_panel(
    "Lectura del escenario",
    "Una combinación con mayor score merece más atención porque reúne señal nodal, prioridad mensual, participación spot, consumo y supuestos sectoriales. Es un screening bajo supuestos explícitos: no debe interpretarse como forecast de factura ni valorización financiera.",
)
