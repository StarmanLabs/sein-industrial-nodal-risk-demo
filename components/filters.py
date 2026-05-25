from __future__ import annotations

import pandas as pd
import streamlit as st


SECTOR_LABELS = {
    "agroindustry_seasonal": "Agroindustria estacional",
    "cement_and_heavy_materials": "Cemento y materiales pesados",
    "data_center_or_high_availability": "Alta disponibilidad / data center",
    "general_manufacturing": "Manufactura general",
    "mining_continuous_load": "Minería de carga continua",
}

CONTRACT_LABELS = {
    "balanced_30pct_spot_ppa": "Balanceado: 30% spot + PPA",
    "fixed_reference_ppa": "PPA a referencia fija",
    "full_spot_exposure": "Exposición spot completa",
    "hedged_10pct_spot": "Cobertura alta: 10% spot",
    "indexed_50pct_spot": "Indexado: 50% spot",
}

PRIORITY_DISPLAY_LABELS = {
    "Baja informacion": "Requiere contexto adicional",
    "Baja información": "Requiere contexto adicional",
    "Low information": "Requiere contexto adicional",
    "Priority A": "Revisión inmediata",
    "Priority B": "Revisión selectiva",
    "Watchlist": "Seguimiento mensual",
    "Monitor": "Contexto base",
    "Prioridad A": "Revisión inmediata",
    "Prioridad B": "Revisión selectiva",
    "Monitorear": "Contexto base",
}

PRIORITY_ORDER = {
    "Priority A": 1,
    "Priority B": 2,
    "Watchlist": 3,
    "Monitor": 4,
    "Low information": 5,
}


def priority_filter(df: pd.DataFrame, key: str = "priority") -> list[str]:
    if "due_diligence_priority_es" in df.columns:
        options = df[["due_diligence_priority", "due_diligence_priority_es"]].drop_duplicates()
        options["priority_order"] = options["due_diligence_priority"].map(PRIORITY_ORDER).fillna(99)
        options = options.sort_values("priority_order")
        options["display_label"] = options["due_diligence_priority_es"].map(
            lambda value: PRIORITY_DISPLAY_LABELS.get(value, value)
        )
        selected_labels = st.multiselect(
            "Categoría de revisión",
            options["display_label"].tolist(),
            default=options["display_label"].tolist(),
            key=key,
        )
        return options[options["display_label"].isin(selected_labels)]["due_diligence_priority"].tolist()
    priorities = sorted(df["due_diligence_priority"].dropna().unique())
    return st.multiselect(
        "Categoría de revisión",
        priorities,
        default=priorities,
        key=key,
    )


def evidence_filter(df: pd.DataFrame, key: str = "evidence") -> list[str]:
    if "evidence_grade" not in df.columns:
        return []
    options = sorted(df["evidence_grade"].dropna().astype(str).unique())
    return st.multiselect("Soporte de contexto", options, default=options, key=key)


def robustness_filter(df: pd.DataFrame, key: str = "robustness") -> list[str]:
    column = "robustness_flag_es" if "robustness_flag_es" in df.columns else "robustness_flag"
    if column not in df.columns:
        return []
    options = sorted(df[column].dropna().astype(str).unique())
    return st.multiselect("Robustez de señal", options, default=options, key=key)


def tension_filter(df: pd.DataFrame, key: str = "tension") -> list[float]:
    if "nivel_tension_kv" not in df.columns:
        return []
    values = sorted(df["nivel_tension_kv"].dropna().unique())
    return st.multiselect("Tensión kV", values, default=values, key=key)


def barra_selector(df: pd.DataFrame, key: str = "barra") -> str | None:
    barras = sorted(df["barra"].dropna().unique())
    if not barras:
        return None
    return st.selectbox("Barra", barras, key=key)


def sector_selector(df: pd.DataFrame, key: str = "sector") -> str | None:
    sectors = sorted(df["sector"].dropna().unique()) if "sector" in df else []
    if not sectors:
        return None
    label_to_value = {SECTOR_LABELS.get(value, value): value for value in sectors}
    selected_label = st.selectbox(
        "Arquetipo sectorial",
        list(label_to_value.keys()),
        key=key,
    )
    return label_to_value[selected_label]


def contract_selector(df: pd.DataFrame, key: str = "contract") -> str | None:
    contracts = sorted(df["contract_type"].dropna().unique()) if "contract_type" in df else []
    if not contracts:
        return None
    label_to_value = {CONTRACT_LABELS.get(value, value): value for value in contracts}
    selected_label = st.selectbox(
        "Arquetipo contractual",
        list(label_to_value.keys()),
        key=key,
    )
    return label_to_value[selected_label]
