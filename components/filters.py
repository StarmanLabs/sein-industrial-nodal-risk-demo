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
    "Baja informacion": "Información por completar",
    "Baja información": "Información por completar",
    "Low information": "Información por completar",
    "Priority A": "Revisión prioritaria",
    "Priority B": "Revisión selectiva",
    "Watchlist": "Seguimiento activo",
    "Monitor": "Referencia comparativa",
    "Prioridad A": "Revisión prioritaria",
    "Prioridad B": "Revisión selectiva",
    "Revisión inmediata": "Revisión prioritaria",
    "Revisión selectiva": "Revisión selectiva",
    "Seguimiento mensual": "Seguimiento activo",
    "Monitorear": "Referencia comparativa",
    "Contexto base": "Referencia comparativa",
    "Requiere contexto adicional": "Información por completar",
}

PRIORITY_ORDER = {
    "Priority A": 1,
    "Priority B": 2,
    "Watchlist": 3,
    "Monitor": 4,
    "Low information": 5,
}


def priority_filter(
    df: pd.DataFrame,
    key: str = "priority",
    label: str = "Categoría de revisión",
    placeholder: str = "Seleccionar categorías",
) -> list[str]:
    if "due_diligence_priority_es" in df.columns:
        options = df[["due_diligence_priority", "due_diligence_priority_es"]].drop_duplicates()
        options["priority_order"] = options["due_diligence_priority"].map(PRIORITY_ORDER).fillna(99)
        options = options.sort_values("priority_order")
        options["display_label"] = options["due_diligence_priority_es"].map(
            lambda value: PRIORITY_DISPLAY_LABELS.get(value, value)
        )
        selected_labels = st.multiselect(
            label,
            options["display_label"].tolist(),
            default=options["display_label"].tolist(),
            placeholder=placeholder,
            key=key,
        )
        return options[options["display_label"].isin(selected_labels)]["due_diligence_priority"].tolist()
    priorities = sorted(df["due_diligence_priority"].dropna().unique())
    return st.multiselect(
        label,
        priorities,
        default=priorities,
        placeholder=placeholder,
        key=key,
    )


def evidence_filter(df: pd.DataFrame, key: str = "evidence") -> list[str]:
    if "evidence_grade" not in df.columns:
        return []
    options = sorted(df["evidence_grade"].dropna().astype(str).unique())
    return st.multiselect("Soporte de contexto", options, default=options, placeholder="Seleccionar soporte", key=key)


def robustness_filter(
    df: pd.DataFrame,
    key: str = "robustness",
    label: str = "Estabilidad de señal",
    placeholder: str = "Seleccionar estabilidad",
    display_map: dict[str, str] | None = None,
) -> list[str]:
    column = (
        "signal_stability_label_es"
        if "signal_stability_label_es" in df.columns
        else "robustness_flag_es"
        if "robustness_flag_es" in df.columns
        else "robustness_flag"
    )
    if column not in df.columns:
        return []
    options = sorted(df[column].dropna().astype(str).unique())
    if display_map:
        label_rows = pd.DataFrame({"raw": options})
        label_rows["display"] = label_rows["raw"].map(lambda value: display_map.get(value, value))
        label_rows = label_rows.drop_duplicates("display")
        selected_labels = st.multiselect(
            label,
            label_rows["display"].tolist(),
            default=label_rows["display"].tolist(),
            placeholder=placeholder,
            key=key,
        )
        return label_rows[label_rows["display"].isin(selected_labels)]["raw"].tolist()
    return st.multiselect(label, options, default=options, placeholder=placeholder, key=key)


def tension_filter(
    df: pd.DataFrame,
    key: str = "tension",
    label: str = "Tensión kV",
    placeholder: str = "Seleccionar tensión",
) -> list[float]:
    if "nivel_tension_kv" not in df.columns:
        return []
    values = sorted(df["nivel_tension_kv"].dropna().unique())
    return st.multiselect(label, values, default=values, placeholder=placeholder, key=key)


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
