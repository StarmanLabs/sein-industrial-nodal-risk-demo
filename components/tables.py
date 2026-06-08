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
    "robustness_flag": "Dependencia del criterio",
    "robustness_flag_es": "Dependencia del criterio",
    "signal_stability_label_es": "Dependencia del criterio",
    "score_coverage_class_es": "Cobertura analítica",
    "score_months_observed": "Meses score",
    "source_months_observed": "Meses fuente COES",
    "evidence_grade": "Soporte de contexto",
    "due_diligence_priority": "Tipo de señal",
    "due_diligence_priority_es": "Tipo de señal",
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
    "robustness_inclusion_share": "Inclusión sensibilidad",
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
        "Priority due diligence": "Señal prioritaria",
        "Watchlist": "Señal episódica",
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
    "Baja informacion": "Información por completar",
    "Baja información": "Información por completar",
    "Prioridad A": "Señal prioritaria",
    "Prioridad B": "Señal condicionada",
    "Priority A": "Señal prioritaria",
    "Priority B": "Señal condicionada",
    "Watchlist": "Señal episódica",
    "Monitorear": "Contexto base",
    "Monitor": "Contexto base",
    "Low information": "Información por completar",
    "Revisión inmediata": "Señal prioritaria",
    "Revisión selectiva": "Señal condicionada",
    "Seguimiento mensual": "Señal episódica",
    "Requiere contexto adicional": "Información por completar",
    "Estres episodico": "Estrés episódico",
    "Estabilidad alta": "Baja dependencia",
    "Robustez alta": "Baja dependencia",
    "High robustness": "Baja dependencia",
    "Estabilidad moderada": "Dependencia media",
    "Robustez moderada": "Dependencia media",
    "Moderate robustness": "Dependencia media",
    "Estabilidad baja": "Alta dependencia",
    "Robustez baja": "Alta dependencia",
    "Low robustness": "Alta dependencia",
    "Fuera de top-list de sensibilidad": "Contextual",
    "Not covered by sensitivity top-list": "Contextual",
    "Cobertura analitica completa": "Completa",
    "Cobertura analitica alta": "Alta",
    "Cobertura analitica parcial": "Parcial",
    "Cobertura analitica limitada": "Limitada",
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
        "Señal prioritaria": "background-color: #fde8e6; color: #8e2f2a; font-weight: 700",
        "Señal condicionada": "background-color: #fff1d7; color: #8a5a14; font-weight: 700",
        "Señal episódica": "background-color: #e5f2f7; color: #245a73; font-weight: 700",
        "Contexto base": "background-color: #eef2f6; color: #4f5d6f; font-weight: 700",
        "Información por completar": "background-color: #f1f3f5; color: #6b7280; font-weight: 700",
    }
    stability_colors = {
        "Baja dependencia": "color: #287c67; font-weight: 700",
        "Dependencia media": "color: #d9902f; font-weight: 700",
        "Alta dependencia": "color: #64748b; font-weight: 700",
        "Contextual": "color: #64748b; font-weight: 700",
    }
    coverage_colors = {
        "Completa": "color: #287c67; font-weight: 700",
        "Alta": "color: #168c8c; font-weight: 700",
        "Parcial": "color: #d9902f; font-weight: 700",
        "Limitada": "color: #c5524a; font-weight: 700",
    }

    def style_cell(value: object) -> str:
        text = "" if value is None else str(value)
        if text in priority_colors:
            return priority_colors[text]
        if text in stability_colors:
            return stability_colors[text]
        if text in coverage_colors:
            return coverage_colors[text]
        if text in {"A", "Contexto revisado"}:
            return "color: #287c67; font-weight: 700"
        if text in {"B", "Contexto útil"}:
            return "color: #d9902f; font-weight: 700"
        return ""

    return df.style.map(style_cell).format(precision=2)


def priority_table(df: pd.DataFrame) -> None:
    work = df.sort_values("decision_priority_score", ascending=False).copy()
    work.insert(0, "posicion", range(1, len(work) + 1))
    stability_col = (
        "signal_stability_label_es"
        if "signal_stability_label_es" in work.columns
        else "robustness_flag_es"
    )
    cols = [
        "posicion",
        "barra",
        "decision_priority_score",
        "due_diligence_priority_es",
        "recommended_action",
        stability_col,
        "score_coverage_class_es",
        "avg_icpi",
        "avg_oanri",
    ]
    labels = {"posicion": "#"}
    display = present(work[[c for c in cols if c in work.columns]]).rename(columns=labels)
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

