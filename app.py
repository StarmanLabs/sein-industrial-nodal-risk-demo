from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "public_demo"

PRIORITY_COLORS = {
    "Priority A": "#b94b45",
    "Priority B": "#d9902f",
    "Watchlist": "#2f6f9f",
    "Monitor": "#6b778c",
    "Low information": "#9aa4b2",
}


@st.cache_data(show_spinner=False)
def load_demo() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    profiles = pd.read_csv(DATA / "barra_profile_demo.csv")
    monthly = pd.read_csv(DATA / "barra_month_demo.csv")
    system = pd.read_csv(DATA / "monthly_system_context_demo.csv")
    return profiles, monthly, system


def kpi(label: str, value: object, note: str = "") -> None:
    st.markdown(
        f"""
<div class="kpi">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-note">{note}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def claim_boundary() -> None:
    st.info(
        "This dashboard is a public demo of a larger private analytical system. It uses sanitized or reduced outputs for portfolio demonstration. Scores are relative screening indicators for due diligence, not causal grid diagnosis, price forecasts, billing estimates or engineering network studies."
    )


def style() -> None:
    st.markdown(
        """
<style>
.block-container {max-width: 1320px; padding-top: 2rem;}
.hero {
  padding: 1.4rem 1.6rem;
  border-radius: 12px;
  background: linear-gradient(135deg, #102235 0%, #173b57 58%, #1e6a70 100%);
  color: white;
  margin-bottom: 1rem;
}
.hero h1 {font-size: 2.1rem; margin: 0 0 .45rem 0;}
.hero p {font-size: 1rem; opacity: .92; margin: 0;}
.kpi {
  border: 1px solid #d7e1ea;
  border-left: 5px solid #2f6f9f;
  border-radius: 9px;
  padding: .85rem 1rem;
  background: #ffffff;
  min-height: 112px;
}
.kpi-label {font-size: .72rem; color: #607089; font-weight: 800; text-transform: uppercase; letter-spacing: .04em;}
.kpi-value {font-size: 1.8rem; color: #122238; font-weight: 850; margin-top: .25rem;}
.kpi-note {font-size: .78rem; color: #69778a; margin-top: .2rem;}
.section-copy {color: #526174; font-size: .94rem;}
.case-card {
  border: 1px solid #d7e1ea;
  border-radius: 10px;
  background: #ffffff;
  padding: .9rem 1rem;
  min-height: 148px;
}
.case-role {
  color: #2f6f9f;
  font-size: .72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .05em;
}
.case-title {font-size: 1.02rem; font-weight: 850; color: #122238; margin-top: .25rem;}
.case-copy {font-size: .86rem; color: #526174; margin-top: .45rem;}
</style>
""",
        unsafe_allow_html=True,
    )


def chart_style(fig, height: int = 430):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin={"l": 24, "r": 24, "t": 54, "b": 40},
        font={"family": "Arial", "color": "#263448"},
        legend={"orientation": "h", "y": 1.02, "x": 1, "xanchor": "right", "title": None},
    )
    fig.update_xaxes(gridcolor="#e8eef4", zeroline=False)
    fig.update_yaxes(gridcolor="#eef3f7", zeroline=False)
    return fig


def overview(profiles: pd.DataFrame, monthly: pd.DataFrame) -> None:
    st.markdown(
        """
<div class="hero">
  <h1>SEIN Industrial Nodal Risk Intelligence</h1>
  <p>A decision-support demo for industrial exposure to nodal electricity price stress in Peru.</p>
</div>
""",
        unsafe_allow_html=True,
    )
    claim_boundary()
    cols = st.columns(4)
    with cols[0]:
        kpi("Demo barras", profiles["barra"].nunique(), "controlled public sample")
    with cols[1]:
        kpi("Months", monthly["month_label"].nunique(), "2023-2025 panel")
    with cols[2]:
        kpi(
            "Priority A/B",
            int(profiles["due_diligence_tier"].isin(["Priority A", "Priority B"]).sum()),
            "due-diligence queue",
        )
    with cols[3]:
        kpi(
            "Evidence A",
            int(profiles["topology_evidence_grade"].eq("A").sum()),
            "reviewed context",
        )

    st.subheader("Where are the strongest due-diligence signals?")
    st.caption(
        "The demo prioritizes bars where relative price-stress, system-adjusted relevance, robustness and context evidence point to further review."
    )
    featured = profiles[profiles["final_public_role"].isin(["featured_hero", "sector_case_with_caveat"])].copy()
    if not featured.empty:
        st.markdown("#### Featured public cases")
        case_cols = st.columns(min(4, len(featured)))
        for col, (_, row) in zip(case_cols, featured.head(4).iterrows()):
            with col:
                st.markdown(
                    f"""
<div class="case-card">
  <div class="case-role">{row['story_use']}</div>
  <div class="case-title">{row['barra']}</div>
  <div class="case-copy">{row['public_story_angle']}</div>
</div>
""",
                    unsafe_allow_html=True,
                )
    fig = px.bar(
        profiles.sort_values("priority_score").tail(12),
        x="priority_score",
        y="barra",
        orientation="h",
        color="due_diligence_tier",
        color_discrete_map=PRIORITY_COLORS,
        labels={"priority_score": "Due Diligence Priority Score", "barra": "Barra"},
        title="Top demo bars by due-diligence priority",
    )
    st.plotly_chart(chart_style(fig, 440), use_container_width=True)


def nodal_price_stress(profiles: pd.DataFrame, monthly: pd.DataFrame) -> None:
    st.title("Nodal Price Stress")
    st.caption("Decision question: which barras show stronger relative marginal-price stress?")
    selected = st.selectbox("Barra", profiles["barra"].tolist())
    data = monthly[monthly["barra"].eq(selected)].copy()
    fig = px.line(
        data,
        x="month_label",
        y="nodal_price_stress_score",
        markers=True,
        title=f"Nodal Price Stress Score - {selected}",
        labels={"month_label": "Month", "nodal_price_stress_score": "Score 0-100"},
    )
    fig.update_yaxes(range=[0, 105])
    st.plotly_chart(chart_style(fig, 430), use_container_width=True)
    row = profiles[profiles["barra"].eq(selected)].iloc[0]
    st.markdown(
        f"**How to read it:** {selected} is flagged as `{row['due_diligence_tier']}` with main driver `{row['main_driver']}` and `{row['persistence_label']}` behavior."
    )
    claim_boundary()


def system_adjusted_risk(profiles: pd.DataFrame, monthly: pd.DataFrame, system: pd.DataFrame) -> None:
    st.title("System-Adjusted Nodal Risk")
    st.caption("Decision question: which barras remain relevant when nodal stress is read with monthly system-regime context?")
    fig = px.scatter(
        profiles,
        x="nodal_price_stress_score",
        y="system_adjusted_nodal_risk_score",
        color="due_diligence_tier",
        size="priority_score",
        hover_name="barra",
        color_discrete_map=PRIORITY_COLORS,
        title="Nodal Price Stress vs System-Adjusted Nodal Risk",
        labels={
            "nodal_price_stress_score": "Nodal Price Stress Score",
            "system_adjusted_nodal_risk_score": "System-Adjusted Nodal Risk Score",
        },
    )
    st.plotly_chart(chart_style(fig, 560), use_container_width=True)
    if not system.empty:
        fig2 = px.line(
            system,
            x="month_label",
            y="system_regime_score",
            markers=True,
            title="Monthly system-regime context",
            labels={"month_label": "Month", "system_regime_score": "System-regime score"},
        )
        st.plotly_chart(chart_style(fig2, 320), use_container_width=True)
    claim_boundary()


def industrial_exposure(profiles: pd.DataFrame) -> None:
    st.title("Industrial Exposure Screening")
    st.caption("Decision question: which sector-barra combinations deserve further review under explicit assumptions?")
    sector = st.selectbox("Illustrative sector", ["Mining continuous load", "Agroindustry", "Manufacturing", "Data center / high availability"])
    spot_share = st.slider("Spot/indexed exposure assumption", 0.0, 1.0, 0.3, 0.1)
    monthly_mwh = st.number_input("Illustrative monthly consumption (MWh)", min_value=1000, max_value=200000, value=20000, step=1000)
    scenario = profiles.copy()
    scenario["illustrative_exposure_score"] = (
        scenario["system_adjusted_nodal_risk_score"] * (0.55 + spot_share)
        + scenario["priority_score"] * 0.25
    ).round(2)
    st.caption(
        "Under explicit exposure assumptions, this sector-barra combination deserves higher due-diligence priority."
    )
    fig = px.bar(
        scenario.sort_values("illustrative_exposure_score").tail(12),
        x="illustrative_exposure_score",
        y="barra",
        orientation="h",
        color="due_diligence_tier",
        color_discrete_map=PRIORITY_COLORS,
        title=f"Illustrative exposure screening - {sector}",
    )
    st.plotly_chart(chart_style(fig, 430), use_container_width=True)
    st.warning(
        "Industrial exposure scenarios are assumption-based screening outputs. They should not be interpreted as invoice forecasts or project-finance valuations."
    )
    st.caption(f"Scenario assumptions: {monthly_mwh:,.0f} MWh/month and {spot_share:.0%} spot/indexed exposure.")


def evidence_context(profiles: pd.DataFrame) -> None:
    st.title("Evidence and Topology Context")
    st.caption("Decision question: what context supports each candidate, and what should be reviewed next?")
    columns = [
        "barra",
        "final_public_role",
        "story_use",
        "topology_context",
        "topology_context_type",
        "topology_evidence_grade",
        "publication_readiness",
        "outlier_pattern",
        "public_story_angle",
        "recommended_next_step",
    ]
    st.dataframe(profiles[columns], use_container_width=True, hide_index=True)
    claim_boundary()


def methodology() -> None:
    st.title("Methodology and Audit")
    st.markdown(
        """
This public demo is intentionally controlled. It exposes a reduced analytical layer and selected documentation while the full production pipeline remains private.

**Method logic**

- Nodal Price Stress Score summarizes relative marginal-price stress.
- System-Adjusted Nodal Risk Score reads the nodal signal together with monthly system-regime pressure.
- Due Diligence Priority Tier turns the analytical signal into a review queue.
- Topology evidence provides context for review, not physical-causal proof.

**Audit logic**

- No duplicate barra-month keys in the private analytical panel.
- Demo cases are selected from a publication-readiness layer.
- Outlier-heavy cases are treated carefully before public storytelling.
"""
    )
    claim_boundary()


def main() -> None:
    st.set_page_config(page_title="SEIN Nodal Risk Demo", layout="wide")
    style()
    profiles, monthly, system = load_demo()
    pages = {
        "Executive Overview": lambda: overview(profiles, monthly),
        "Nodal Price Stress": lambda: nodal_price_stress(profiles, monthly),
        "System-Adjusted Risk": lambda: system_adjusted_risk(profiles, monthly, system),
        "Industrial Exposure Simulator": lambda: industrial_exposure(profiles),
        "Evidence and Topology Context": lambda: evidence_context(profiles),
        "Methodology and Audit": methodology,
    }
    st.sidebar.title("SEIN Demo")
    st.sidebar.caption("Controlled portfolio demo")
    selected_page = st.sidebar.radio("Page", list(pages))
    pages[selected_page]()


if __name__ == "__main__":
    main()
