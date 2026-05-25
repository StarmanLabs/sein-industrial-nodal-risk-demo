from __future__ import annotations

import pandas as pd
import streamlit as st


COLUMN_LABELS = {
    "barra": "Barra",
    "topology_context_asset": "Activo/conexión",
    "topology_context_type_es": "Tipo de contexto",
    "evidence_family_es": "Rol de evidencia",
    "topology_context_summary": "Contexto actual",
    "external_evidence_summary": "Evidencia externa",
    "zona_geografica": "Zona geográfica",
    "nivel_tension_kv": "Tensión kV",
    "rank_icpi": "Rank estrés nodal",
    "rank_oanri": "Rank prioridad operativa",
    "persistence_category": "Persistencia",
    "persistence_category_es": "Persistencia",
    "episodic_stress_category": "Estrés episódico",
    "episodic_stress_category_es": "Estrés episódico",
    "robustness_flag": "Robustez",
    "robustness_flag_es": "Robustez",
    "evidence_grade": "Soporte de contexto",
    "due_diligence_priority": "Categoría de revisión",
    "due_diligence_priority_es": "Categoría de revisión",
    "recommended_action": "Acción recomendada",
    "decision_priority_score": "Score de revisión",
    "month": "Mes",
    "Estrés nodal": "estrés nodal",
    "Prioridad operativa": "prioridad operativa",
    "avg_icpi": "estrés nodal prom.",
    "avg_oanri": "prioridad operativa prom.",
    "ranking_mensual_v10": "Ranking prioridad operativa mensual",
    "decision_tier": "Categoría mensual",
    "primary_driver": "Driver principal",
    "sector": "Sector",
    "contract_type": "Contrato",
    "avg_industrial_exposure_score": "Score exposición prom.",
    "p90_industrial_exposure_score": "Score exposición p90",
    "priority_months": "Meses revisión inmediata",
    "watchlist_months": "Meses seguimiento",
    "robustness_inclusion_share": "Inclusión robustez",
    "profile_priority_score": "Score de revisión",
    "unique_barras": "Barras únicas",
    "monthly_mwh": "MWh mensual",
    "spot_share": "Participación spot",
    "avg_exposure_score": "Score exposición prom.",
    "p90_exposure_score": "Score exposición p90",
    "priority_rows": "Filas revisión inmediata",
    "watchlist_rows": "Filas seguimiento",
}

VALUE_LABELS = {
    "sector": {
        "agroindustry_seasonal": "Agroindustria estacional",
        "cement_and_heavy_materials": "Cemento y materiales pesados",
        "data_center_or_high_availability": "Alta disponibilidad / data center",
        "general_manufacturing": "Manufactura general",
        "mining_continuous_load": "Minería de carga continua",
    },
    "contract_type": {
        "balanced_30pct_spot_ppa": "Balanceado: 30% spot + PPA",
        "fixed_reference_ppa": "PPA a referencia fija",
        "full_spot_exposure": "Exposición spot completa",
        "hedged_10pct_spot": "Cobertura alta: 10% spot",
        "indexed_50pct_spot": "Indexado: 50% spot",
    },
    "decision_tier": {
        "Priority due diligence": "Revisión inmediata",
        "Watchlist": "Seguimiento mensual",
        "Monitor": "Contexto base",
        "Lower relative exposure": "Menor exposición relativa",
    },
    "primary_driver": {
        "price_level": "Nivel de precio",
        "stress_premium": "Prima de estrés",
        "volatility": "Volatilidad",
    },
    "evidence_grade": {
        "A": "Contexto revisado",
        "B": "Contexto útil",
    },
}

DISPLAY_TEXT_REPLACEMENTS = {
    "Baja informacion": "Baja información",
    "Prioridad A": "Revisión inmediata",
    "Prioridad B": "Revisión selectiva",
    "Priority A": "Revisión inmediata",
    "Priority B": "Revisión selectiva",
    "Watchlist": "Seguimiento mensual",
    "Monitorear": "Contexto base",
    "Monitor": "Contexto base",
    "Low information": "Requiere contexto adicional",
    "Estres episodico": "Estrés episódico",
    "Episodico": "Episódico",
    "Senal": "Señal",
    "senal": "señal",
    "senales": "señales",
    "estres": "estrés",
    "topologico": "topológico",
    "topologica": "topológica",
    "revision": "revisión",
    "Revision": "Revisión",
    "accion": "acción",
    "Accion": "Acción",
    "analitico": "analítico",
    "decision": "decisión",
    "explicitos": "explícitos",
    "exposicion": "exposición",
    "ubicacion": "ubicación",
    "electricos": "eléctricos",
    "electrica": "eléctrica",
    "conclusion": "conclusión",
    "ingenieria": "ingeniería",
    "contratacion": "contratación",
    "informacion": "información",
}


def _display_text(value: object) -> object:
    if not isinstance(value, str):
        return value
    text = value
    for raw, display in DISPLAY_TEXT_REPLACEMENTS.items():
        text = text.replace(raw, display)
    return text


def present(df: pd.DataFrame) -> pd.DataFrame:
    display = df.copy()
    if "month" in display.columns:
        display["month"] = pd.to_datetime(display["month"], errors="coerce").dt.strftime("%Y-%m")
    for column, mapping in VALUE_LABELS.items():
        if column in display.columns:
            display[column] = display[column].map(lambda value: mapping.get(value, value))
    for column in display.select_dtypes(include="object").columns:
        display[column] = display[column].map(_display_text)
    return display.rename(columns={k: v for k, v in COLUMN_LABELS.items() if k in display})


def _style_table(df: pd.DataFrame):
    priority_colors = {
        "Revisión inmediata": "background-color: #fde8e6; color: #8e2f2a; font-weight: 700",
        "Revisión selectiva": "background-color: #fff1d7; color: #8a5a14; font-weight: 700",
        "Seguimiento mensual": "background-color: #e5f2f7; color: #245a73; font-weight: 700",
        "Contexto base": "background-color: #eef2f6; color: #4f5d6f; font-weight: 700",
        "Requiere contexto adicional": "background-color: #f1f3f5; color: #6b7280; font-weight: 700",
    }
    robustness_colors = {
        "Robustez alta": "color: #287c67; font-weight: 700",
        "Robustez moderada": "color: #d9902f; font-weight: 700",
        "Robustez baja": "color: #c5524a; font-weight: 700",
    }

    def style_cell(value: object) -> str:
        text = "" if value is None else str(value)
        if text in priority_colors:
            return priority_colors[text]
        if text in robustness_colors:
            return robustness_colors[text]
        if text in {"A", "Contexto revisado"}:
            return "color: #287c67; font-weight: 700"
        if text in {"B", "Contexto útil"}:
            return "color: #d9902f; font-weight: 700"
        return ""

    return df.style.map(style_cell).format(precision=2)


def priority_table(df: pd.DataFrame) -> None:
    cols = [
        "barra",
        "nivel_tension_kv",
        "topology_context_asset",
        "topology_context_type_es",
        "evidence_family_es",
        "decision_priority_score",
        "rank_icpi",
        "rank_oanri",
        "avg_icpi",
        "avg_oanri",
        "robustness_flag_es",
        "evidence_grade",
        "due_diligence_priority_es",
        "recommended_action",
    ]
    display = present(df[[c for c in cols if c in df.columns]])
    st.dataframe(
        _style_table(display),
        use_container_width=True,
        hide_index=True,
        height=438,
    )


def compact_table(df: pd.DataFrame, columns: list[str]) -> None:
    display = present(df[[c for c in columns if c in df.columns]])
    st.dataframe(
        _style_table(display),
        use_container_width=True,
        hide_index=True,
        height=430,
    )

