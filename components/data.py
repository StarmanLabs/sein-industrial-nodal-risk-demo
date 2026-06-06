from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DATA = ROOT / "data" / "public_demo"

PRIORITY_ES = {
    "Priority A": "Revisión inmediata",
    "Priority B": "Revisión selectiva",
    "Watchlist": "Seguimiento mensual",
    "Monitor": "Contexto base",
    "Low information": "Requiere contexto adicional",
}

PRIORITY_EN = {
    "Prioridad A": "Priority A",
    "Prioridad B": "Priority B",
    "Revisión inmediata": "Priority A",
    "Revision inmediata": "Priority A",
    "Revisión selectiva": "Priority B",
    "Revision selectiva": "Priority B",
    "Seguimiento mensual": "Watchlist",
    "Seguimiento": "Watchlist",
    "Watchlist": "Watchlist",
    "Monitorear": "Monitor",
    "Contexto base": "Monitor",
    "Requiere contexto adicional": "Low information",
    "Información limitada": "Low information",
    "Baja informacion": "Low information",
    "Baja información": "Low information",
    "Low information": "Low information",
}

ROBUSTNESS_ES = {
    "High robustness": "Estabilidad alta",
    "Moderate robustness": "Estabilidad moderada",
    "Low robustness": "Estabilidad baja",
    "Robustez alta": "Estabilidad alta",
    "Robustez moderada": "Estabilidad moderada",
    "Robustez baja": "Estabilidad baja",
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
    if "tension_kv" in out.columns:
        out["nivel_tension_kv"] = out["tension_kv"]
        out["topology_context_asset"] = out["contexto_topologico"]
        out["topology_context_type_es"] = out["tipo_contexto"]
        out["evidence_family_es"] = out.get("rol_evidencia", "Contexto público revisado")
        out["avg_icpi"] = out["estres_nodal"]
        out["avg_oanri"] = out["prioridad_operativa"]
        out["p90_oanri"] = out.get("prioridad_operativa_p90", out["avg_oanri"])
        out["rank_icpi"] = out["ranking_estres_nodal"]
        out["rank_oanri"] = out["ranking_prioridad_operativa"]
        out["decision_priority_score"] = out["score_revision"]
        out["due_diligence_priority"] = out["prioridad"].map(
            lambda value: PRIORITY_EN.get(str(value), str(value))
        )
        out["due_diligence_priority_es"] = out["due_diligence_priority"].map(
            lambda value: PRIORITY_ES.get(str(value), str(value))
        )
        out["robustness_flag_es"] = out.get("estabilidad_senal", out["robustez"])
        out["robustness_flag"] = out["robustez"]
        out["signal_stability_label_es"] = out.get(
            "estabilidad_senal", out["robustness_flag_es"]
        )
        out["signal_stability_score"] = out.get("score_estabilidad", pd.NA)
        out["monthly_top20_months"] = out.get("meses_top20_mensual", 0)
        out["monthly_top20_share"] = out.get("share_top20_mensual", 0)
        out["monthly_attention_label_es"] = out.get("zona_mensual", "Fuera de zona mensual")
        out["monthly_attention_interpretation"] = out.get(
            "lectura_zona_mensual",
            "El Top 20 mensual se usa como zona ejecutiva de seguimiento, no como universo metodologico.",
        )
        out["evidence_grade"] = out["soporte_evidencia"]
        out["priority_reason"] = out.get("resumen_contexto", "")
        out["recommended_action"] = out["accion_recomendada"]
        out["decision_claim_boundary"] = out["limite_interpretacion"]
        out["interpretation_caveat"] = out["limite_interpretacion"]
        out["persistence_category"] = out["persistencia"]
        out["persistence_category_es"] = out["persistencia"]
        out["primary_driver"] = out["driver_principal"]
        out["primary_driver_es"] = out["driver_principal"]
        out["score_months_observed"] = out.get("meses_score", out.get("meses_observados", 0))
        out["score_coverage_class_es"] = out.get(
            "cobertura_analitica", "Cobertura analitica no clasificada"
        )
        out["source_months_observed"] = out.get(
            "meses_fuente_coes", out.get("meses_observados", 0)
        )
        out["coverage_semantics_note"] = out.get(
            "nota_cobertura",
            "meses_score describe meses efectivos del indicador; meses_fuente_coes describe trazabilidad de fuente COES.",
        )
    else:
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
        out["signal_stability_label_es"] = out["robustness_flag_es"]
        out["signal_stability_score"] = pd.NA
        out["monthly_top20_months"] = out.get("watchlist_months", 0)
        out["monthly_top20_share"] = 0
        out["monthly_attention_label_es"] = "Zona mensual no disponible"
        out["monthly_attention_interpretation"] = (
            "El Top 20 mensual se usa como zona ejecutiva de seguimiento, no como universo metodologico."
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
        out["primary_driver"] = out["main_driver"]
        out["primary_driver_es"] = out["main_driver"].map(
            lambda value: DRIVER_ES.get(str(value), str(value))
        )
        out["score_months_observed"] = out.get("months_observed", out.get("watchlist_months", 0))
        out["score_coverage_class_es"] = "Cobertura analitica no clasificada"
        out["source_months_observed"] = out["score_months_observed"]
        out["coverage_semantics_note"] = (
            "meses_score describe meses efectivos del indicador; meses_fuente_coes describe trazabilidad de fuente COES."
        )
    out["episodic_stress_category"] = out["persistence_category"]
    out["episodic_stress_category_es"] = out["persistence_category_es"]
    out["topology_context_summary"] = out.get(
        "resumen_contexto",
        out["topology_context_asset"].fillna(out["barra"])
        + " funciona como contexto para revisar la señal nodal actual.",
    )
    out["external_evidence_summary"] = (
        "Caso incluido en la muestra publica tras control de publicacion; la evidencia completa permanece en la capa privada auditada."
    )

    if "rank_icpi" not in out.columns:
        out["rank_icpi"] = out["avg_icpi"].rank(ascending=False, method="min")
    if "rank_oanri" not in out.columns:
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
        monthly_months = out["barra"].map(months).fillna(0).astype(int)
        out["score_months_observed"] = pd.to_numeric(
            out["score_months_observed"], errors="coerce"
        ).fillna(monthly_months).astype(int)
        out["source_months_observed"] = pd.to_numeric(
            out["source_months_observed"], errors="coerce"
        ).fillna(monthly_months).astype(int)
        out["coes_price_key_months_observed"] = out["source_months_observed"]
        out["p90_oanri"] = out["barra"].map(p90_oanri).fillna(out["avg_oanri"])
        out["priority_months"] = out["barra"].map(priority_months).fillna(0).astype(int)
        out["watchlist_months"] = out["barra"].map(watchlist_months).fillna(0).astype(int)
    else:
        out["coes_price_key_first_month"] = "no disponible"
        out["coes_price_key_last_month"] = "no disponible"
        out["score_months_observed"] = pd.to_numeric(
            out["score_months_observed"], errors="coerce"
        ).fillna(0).astype(int)
        out["source_months_observed"] = pd.to_numeric(
            out["source_months_observed"], errors="coerce"
        ).fillna(out["score_months_observed"]).astype(int)
        out["coes_price_key_months_observed"] = out["source_months_observed"]
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
    if "mes_periodo" in out.columns:
        out["month"] = pd.to_datetime(out["mes_periodo"] + "-01", errors="coerce")
        out["ICPI_v8"] = out["estres_nodal"]
        out["OANRI_v10"] = out["prioridad_operativa"]
        out["ranking_mensual_v10"] = out["ranking_mensual"]
        out["decision_tier"] = out["categoria_revision"].map(
            {
                "Prioridad de revisión": "Priority due diligence",
                "Seguimiento": "Watchlist",
                "Monitorear": "Monitor",
                "Menor exposición relativa": "Lower relative exposure",
            }
        ).fillna(out["categoria_revision"])
        out["quality_score_v10"] = out["calidad_dato"]
        out["flag_low_info_v10"] = out["informacion_limitada"]
        out["primary_driver"] = out["driver_principal"]
        out["nivel_tension_kv"] = out["tension_kv"]
        out["mean_price"] = out["precio_promedio"]
        out["p95_price"] = out["precio_p95"]
        out["std_price"] = out["volatilidad"]
        out["duracion_total_critica_h"] = out["horas_criticas"]
        out["volatility_metric"] = out["volatilidad"]
        out["critical_window_hours"] = out["horas_criticas"]
    else:
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
    out["block_volatility_v10"] = (out["std_price"].rank(pct=True)).fillna(0)
    out["block_stress_v10"] = (out["p95_price"].rank(pct=True)).fillna(0)
    out["block_criticality_v10"] = (out["duracion_total_critica_h"].rank(pct=True)).fillna(0)
    out["system_regime_v10_0_1"] = (out["OANRI_v10"] / 100).clip(0, 1)
    out["Estrés nodal"] = out["ICPI_v8"]
    out["Prioridad operativa"] = out["OANRI_v10"]
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
    if "mes_periodo" in out.columns:
        out["month"] = pd.to_datetime(out["mes_periodo"] + "-01", errors="coerce")
        out["system_regime_v10_0_1"] = out["regimen_sistema"]
    else:
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
