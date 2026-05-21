from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DATA = ROOT / "data" / "public_demo"

PRIORITY_ES = {
    "Priority A": "Prioridad A",
    "Priority B": "Prioridad B",
    "Watchlist": "Watchlist",
    "Monitor": "Monitorear",
    "Low information": "Baja informacion",
}

ROBUSTNESS_ES = {
    "High robustness": "Robustez alta",
    "Moderate robustness": "Robustez moderada",
    "Low robustness": "Robustez baja",
}

DRIVER_ES = {
    "Price level": "Nivel de precio",
    "Stress premium": "Prima de estres",
    "Volatility": "Volatilidad",
}

CONTEXT_TYPE_ES = {
    "Transmission substation": "Subestacion de transmision",
    "Generation node": "Nodo de generacion",
    "Industrial / demand node": "Nodo industrial o demanda",
}

SECTORS = {
    "mining_continuous_load": {
        "monthly_mwh": 42000,
        "sensitivity": 1.10,
    },
    "cement_and_heavy_materials": {
        "monthly_mwh": 32000,
        "sensitivity": 0.96,
    },
    "data_center_or_high_availability": {
        "monthly_mwh": 21000,
        "sensitivity": 1.18,
    },
    "general_manufacturing": {
        "monthly_mwh": 16000,
        "sensitivity": 0.84,
    },
    "agroindustry_seasonal": {
        "monthly_mwh": 12000,
        "sensitivity": 0.78,
    },
}

CONTRACTS = {
    "full_spot_exposure": 1.00,
    "indexed_50pct_spot": 0.50,
    "balanced_30pct_spot_ppa": 0.30,
    "hedged_10pct_spot": 0.10,
    "fixed_reference_ppa": 0.04,
}


@st.cache_data(show_spinner=False)
def load_csv(path: str) -> pd.DataFrame:
    file_path = ROOT / path
    if not file_path.exists():
        return pd.DataFrame()
    return pd.read_csv(file_path)


def _priority_order(value: object) -> int:
    return {
        "Priority A": 1,
        "Priority B": 2,
        "Watchlist": 3,
        "Monitor": 4,
        "Low information": 5,
    }.get(str(value), 9)


def _parse_month_label(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "month_label" in out.columns:
        out["month"] = pd.to_datetime(out["month_label"] + "-01", errors="coerce")
    elif "month" in out.columns:
        out["month"] = pd.to_datetime(out["month"], errors="coerce")
    return out


@st.cache_data(show_spinner=False)
def load_product_layer() -> pd.DataFrame:
    profiles = load_csv("data/public_demo/barra_profile_demo.csv")
    if profiles.empty:
        return profiles

    monthly = load_monthly_panel()
    out = profiles.copy()
    out["nivel_tension_kv"] = out["voltage_kv"]
    out["topology_context_asset"] = out["topology_context"]
    out["topology_context_type_es"] = out["topology_context_type"].map(
        lambda value: CONTEXT_TYPE_ES.get(str(value), str(value))
    )
    out["evidence_family_es"] = "Contexto publico revisado"
    out["avg_icpi"] = out["nodal_price_stress_score"]
    out["avg_oanri"] = out["system_adjusted_nodal_risk_score"]
    out["p90_oanri"] = out["avg_oanri"]
    out["decision_priority_score"] = out["priority_score"]
    out["due_diligence_priority"] = out["due_diligence_tier"]
    out["due_diligence_priority_es"] = out["due_diligence_priority"].map(
        lambda value: PRIORITY_ES.get(str(value), str(value))
    )
    out["robustness_flag"] = out["robustness_label"]
    out["robustness_flag_es"] = out["robustness_flag"].map(
        lambda value: ROBUSTNESS_ES.get(str(value), str(value))
    )
    out["evidence_grade"] = out["topology_evidence_grade"]
    out["priority_reason"] = out["public_story_angle"]
    out["recommended_action"] = out["recommended_next_step"]
    out["decision_claim_boundary"] = out["claim_boundary"]
    out["interpretation_caveat"] = out["claim_boundary"]
    out["persistence_category"] = out["persistence_label"]
    out["persistence_category_es"] = out["persistence_label"].replace(
        {"Persistent": "Persistente", "Episodic": "Episodica"}
    )
    out["episodic_stress_category"] = out["persistence_label"]
    out["episodic_stress_category_es"] = out["persistence_category_es"]
    out["primary_driver"] = out["main_driver"]
    out["primary_driver_es"] = out["main_driver"].map(
        lambda value: DRIVER_ES.get(str(value), str(value))
    )
    out["topology_context_summary"] = (
        out["topology_context_asset"].fillna(out["barra"])
        + " funciona como contexto de subestacion, central, conexion o corredor para revisar la senal nodal actual."
    )
    out["external_evidence_summary"] = (
        "Caso incluido en la muestra publica tras control de publicacion; la evidencia completa permanece en la capa privada auditada."
    )

    out["rank_icpi"] = out["avg_icpi"].rank(ascending=False, method="min")
    out["rank_oanri"] = out["avg_oanri"].rank(ascending=False, method="min")

    if not monthly.empty:
        grouped = monthly.groupby("barra", dropna=False)
        first_month = grouped["month"].min().dt.strftime("%Y-%m")
        last_month = grouped["month"].max().dt.strftime("%Y-%m")
        months = grouped["month"].nunique()
        p90_oanri = grouped["OANRI_v10"].quantile(0.90)
        priority_months = grouped.apply(
            lambda data: int(data["decision_tier"].eq("Priority due diligence").sum()),
            include_groups=False,
        )
        watchlist_months = grouped.apply(
            lambda data: int(data["decision_tier"].eq("Watchlist").sum()),
            include_groups=False,
        )
        out["coes_price_key_first_month"] = out["barra"].map(first_month)
        out["coes_price_key_last_month"] = out["barra"].map(last_month)
        out["coes_price_key_months_observed"] = out["barra"].map(months).fillna(0).astype(int)
        out["p90_oanri"] = out["barra"].map(p90_oanri).fillna(out["avg_oanri"])
        out["priority_months"] = out["barra"].map(priority_months).fillna(0).astype(int)
        out["watchlist_months"] = out["barra"].map(watchlist_months).fillna(0).astype(int)
    else:
        out["coes_price_key_first_month"] = "no disponible"
        out["coes_price_key_last_month"] = "no disponible"
        out["coes_price_key_months_observed"] = 0
        out["priority_months"] = 0
        out["watchlist_months"] = 0

    out["priority_order"] = out["due_diligence_priority"].map(_priority_order)
    return out.sort_values(["priority_order", "decision_priority_score"], ascending=[True, False])


@st.cache_data(show_spinner=False)
def load_topology_readiness() -> pd.DataFrame:
    return load_product_layer()


@st.cache_data(show_spinner=False)
def load_monthly_panel() -> pd.DataFrame:
    df = load_csv("data/public_demo/barra_month_demo.csv")
    if df.empty:
        return df

    out = _parse_month_label(df)
    out["ICPI_v8"] = out["nodal_price_stress_score"]
    out["OANRI_v10"] = out["system_adjusted_nodal_risk_score"]
    out["ranking_mensual_v10"] = out["monthly_nodal_stress_rank"]
    out["decision_tier"] = out["due_diligence_tier"].map(
        {
            "Priority A": "Priority due diligence",
            "Priority B": "Priority due diligence",
            "Watchlist": "Watchlist",
            "Monitor": "Monitor",
            "Low information": "Lower relative exposure",
        }
    )
    out["quality_score_v10"] = out["data_quality_score"]
    out["flag_low_info_v10"] = out["low_information_flag"]
    out["primary_driver"] = out["main_driver"].str.lower().str.replace(" ", "_")
    out["nivel_tension_kv"] = out["voltage_kv"]
    out["std_price"] = out["volatility_metric"]
    out["duracion_total_critica_h"] = out["critical_window_hours"]
    out["block_cost_v10"] = (out["mean_price"].rank(pct=True)).fillna(0)
    out["block_volatility_v10"] = (out["volatility_metric"].rank(pct=True)).fillna(0)
    out["block_stress_v10"] = (out["p95_price"].rank(pct=True)).fillna(0)
    out["block_criticality_v10"] = (out["critical_window_hours"].rank(pct=True)).fillna(0)
    out["system_regime_v10_0_1"] = (out["OANRI_v10"] / 100).clip(0, 1)
    return out


@st.cache_data(show_spinner=False)
def load_watchlist() -> pd.DataFrame:
    panel = load_monthly_panel()
    if panel.empty:
        return panel
    return panel.sort_values(["month", "ranking_mensual_v10"], ascending=[True, True])


@st.cache_data(show_spinner=False)
def load_system_regime() -> pd.DataFrame:
    df = load_csv("data/public_demo/monthly_system_context_demo.csv")
    if df.empty:
        return df
    out = _parse_month_label(df)
    out["system_regime_v10_0_1"] = out["system_regime_score"]
    return out


def _build_sector_rows() -> pd.DataFrame:
    profiles = load_product_layer()
    if profiles.empty:
        return profiles

    rows = []
    for _, row in profiles.iterrows():
        for sector, sector_meta in SECTORS.items():
            for contract_type, spot_share in CONTRACTS.items():
                sector_weight = sector_meta["sensitivity"]
                exposure_score = (
                    row["avg_oanri"] * 0.50
                    + row["avg_icpi"] * 0.22
                    + row["decision_priority_score"] * 0.18
                    + spot_share * 10
                ) * sector_weight
                profile_score = min(100, exposure_score)
                rows.append(
                    {
                        "sector": sector,
                        "contract_type": contract_type,
                        "barra": row["barra"],
                        "avg_industrial_exposure_score": round(profile_score * 0.88, 2),
                        "p90_industrial_exposure_score": round(min(100, profile_score * 1.08), 2),
                        "priority_months": int(row.get("priority_months", 0)),
                        "watchlist_months": int(row.get("watchlist_months", 0)),
                        "robustness_inclusion_share": 1.0
                        if row.get("robustness_label") == "High robustness"
                        else 0.65,
                        "dominant_driver": str(row.get("main_driver", "")).lower().replace(" ", "_"),
                        "profile_priority_score": round(profile_score, 2),
                        "monthly_mwh": sector_meta["monthly_mwh"],
                        "spot_share": spot_share,
                    }
                )
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def load_sector_profiles() -> pd.DataFrame:
    return _build_sector_rows()


@st.cache_data(show_spinner=False)
def load_contract_scenarios() -> pd.DataFrame:
    sector_rows = _build_sector_rows()
    if sector_rows.empty:
        return sector_rows
    return (
        sector_rows.groupby(["sector", "contract_type"], as_index=False)
        .agg(
            unique_barras=("barra", "nunique"),
            monthly_mwh=("monthly_mwh", "mean"),
            spot_share=("spot_share", "mean"),
            avg_exposure_score=("avg_industrial_exposure_score", "mean"),
            p90_exposure_score=("p90_industrial_exposure_score", "quantile"),
            priority_rows=("priority_months", "sum"),
            watchlist_rows=("watchlist_months", "sum"),
        )
        .assign(
            avg_exposure_score=lambda data: data["avg_exposure_score"].round(2),
            p90_exposure_score=lambda data: data["p90_exposure_score"].round(2),
        )
    )


@st.cache_data(show_spinner=False)
def load_simulator_sample() -> pd.DataFrame:
    panel = load_monthly_panel()
    profiles = load_product_layer()
    if panel.empty or profiles.empty:
        return pd.DataFrame()

    profile_cols = profiles[
        ["barra", "decision_priority_score", "due_diligence_priority", "avg_oanri"]
    ]
    sample = panel.merge(profile_cols, on="barra", how="left")
    sample["sector"] = "mining_continuous_load"
    sample["contract_type"] = "balanced_30pct_spot_ppa"
    sample["industrial_exposure_score"] = (
        sample["OANRI_v10"] * 0.55
        + sample["ICPI_v8"] * 0.20
        + sample["decision_priority_score"] * 0.20
        + 3
    ).round(2)
    return sample


def require_data(df: pd.DataFrame, label: str) -> bool:
    if df.empty:
        st.warning(f"{label} no esta disponible en la muestra publica.")
        return False
    return True
