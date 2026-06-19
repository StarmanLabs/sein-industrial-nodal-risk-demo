from __future__ import annotations

from html import escape

import pandas as pd
import streamlit as st

from components import narrative_cards as narrative
from components.charts import (
    barra_component_profile,
    barra_month_line,
    barra_profile_score_bars,
    contract_comparison_chart,
    icpi_oanri_scatter,
    sector_exposure_bar_chart,
    system_regime_line,
    top_bar_chart,
    watchlist_heatmap,
)
from components.data import (
    load_contract_scenarios,
    load_monthly_panel,
    load_product_layer,
    load_sector_profiles,
    load_system_regime,
    load_watchlist,
)
from components.filters import (
    CONTRACT_LABELS,
    SECTOR_LABELS,
    barra_selector,
    contract_selector,
    priority_filter,
    robustness_filter,
    sector_selector,
    tension_filter,
)
from components.tables import compact_table, priority_table


action_panel = narrative.action_panel
badge_row = narrative.badge_row
decision_matrix = narrative.decision_matrix
decision_summary_card = narrative.decision_summary_card
hero_header = narrative.hero_header
humanize_analytical_text = narrative.humanize_analytical_text
insight_grid = narrative.insight_grid
metric_card = narrative.metric_card
page_header = narrative.page_header
priority_system_legend = narrative.priority_system_legend
product_sidebar = narrative.product_sidebar
product_sidebar_footer = getattr(narrative, "product_sidebar_footer", lambda: None)
section_header = narrative.section_header
context_summary_panel = narrative.context_summary_panel


def _fallback_markdown_block(css_class: str, title: str, body: str) -> None:
    st.markdown(
        f"""
<div class="{css_class}">
  <strong>{title}</strong>
  <p>{body}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def _fallback_kpi_strip(items: list[tuple[str, object, str, str]]) -> None:
    cols = st.columns(len(items))
    for col, (label, value, note, kind) in zip(cols, items):
        with col:
            metric_card(label, value, note, kind=kind)


def _fallback_decision_flow(steps: list[tuple[str, str]]) -> None:
    text = " | ".join(f"{index}. {title}: {body}" for index, (title, body) in enumerate(steps, start=1))
    _fallback_markdown_block("sein-action-panel", "Flujo del producto", text)


def _fallback_use_path_panel(items: list[tuple[str, str]]) -> None:
    text = " | ".join(f"{label}: {body}" for label, body in items)
    _fallback_markdown_block("sein-action-panel", "Cómo se usa", text)


def _fallback_decision_taxonomy() -> None:
    insight_grid(
        [
            ("Señal prioritaria", "Candidata fuerte: señal alta, recurrencia y soporte suficiente.", "decision"),
            ("Señal condicionada", "Relevante si sector, contrato, ubicación o escenario aumentan exposición.", "evidence"),
            ("Señal episódica", "Tiene picos o meses relevantes; requiere seguimiento mensual.", "action"),
            ("Contexto base", "Permanece en el universo analítico para comparación, referencia y nuevos eventos.", "caveat"),
            ("Información por completar", "Necesita más contexto antes de una lectura fuerte.", "caveat"),
        ]
    )


def _fallback_scope_note(body: str) -> None:
    action_panel("Lectura prudente", body)


executive_kpi_strip = getattr(narrative, "executive_kpi_strip", _fallback_kpi_strip)
decision_flow = getattr(narrative, "decision_flow", _fallback_decision_flow)
use_path_panel = getattr(narrative, "use_path_panel", _fallback_use_path_panel)
decision_taxonomy = getattr(narrative, "decision_taxonomy", _fallback_decision_taxonomy)
compact_scope_note = getattr(narrative, "compact_scope_note", _fallback_scope_note)


st.set_page_config(
    page_title="SEIN Industrial Nodal Risk Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_inicio() -> None:
    profiles = load_product_layer()
    panel = load_monthly_panel()

    hero_header(
        "Prioriza barras del SEIN para due diligence industrial",
        "Un sistema de soporte a decisión que transforma precios marginales COES en señales comparables, "
        "ranking de revisión y escenarios de exposición industrial.",
    )

    if profiles.empty:
        st.error("No se encontró la capa pública del producto. Revisa que `data/public_demo` esté incluido en el despliegue.")
        st.stop()

    revision_queue = int(profiles["due_diligence_priority"].isin(["Priority A", "Priority B"]).sum())
    watchlist_count = int((profiles["due_diligence_priority"] == "Watchlist").sum())
    executive_kpi_strip(
        [
            ("Universo SEIN", f"{profiles['barra'].nunique():,.0f}", "barras comparables", "scope"),
            ("Cobertura", f"{panel['month'].nunique() if not panel.empty else 0:,.0f}", "meses 2023-2025", "signal"),
            ("Panel mensual", f"{len(panel):,.0f}", "observaciones barra-mes", "scope"),
            ("Cola de revisión", f"{revision_queue:,.0f}", "candidatas principales", "action"),
            ("Seguimiento", f"{watchlist_count:,.0f}", "casos de monitoreo mensual", "watch"),
        ]
    )

    decision_flow(
        [
            ("Medir señales", "Captura y normaliza precios marginales, volatilidad, episodios y persistencia por barra."),
            ("Ordenar prioridad", "Combina estrés nodal, régimen operativo, episodios mensuales, estabilidad del resultado y evidencia contextual para priorizar revisión."),
            ("Contrastar evidencia", "Valida contrato, sector, ubicación, demanda industrial y soporte técnico antes de decidir."),
        ]
    )

    use_path_panel(
        [
            ("1. Resumen Ejecutivo", "Identifica dónde se concentran las señales más relevantes."),
            ("2. Ranking de Prioridad", "Filtra y arma tu cola corta de revisión con los casos más críticos."),
            ("3. Caso de Estudio", "Profundiza en una barra específica y entiende por qué merece atención."),
        ]
    )
    decision_taxonomy()
    compact_scope_note(
        "Este dashboard prioriza señales observadas para orientar revisión experta."
    )


def render_resumen() -> None:
    profiles = load_product_layer()
    panel = load_monthly_panel()
    regime = load_system_regime()
    if profiles.empty:
        st.error("La capa producto no está disponible.")
        st.stop()

    priority_a_count = int((profiles["due_diligence_priority"] == "Priority A").sum())
    priority_b_count = int((profiles["due_diligence_priority"] == "Priority B").sum())
    watchlist_count = int((profiles["due_diligence_priority"] == "Watchlist").sum())
    barras_count = int(profiles["barra"].nunique())
    months_count = int(panel["month"].nunique()) if not panel.empty else 0
    top_oanri = profiles.sort_values("rank_oanri", na_position="last").head(1).iloc[0]
    top_icpi = profiles.sort_values("rank_icpi", na_position="last").head(1).iloc[0]

    def _icon(name: str) -> str:
        return f'<span class="exec-icon exec-icon-{escape(name)}" aria-hidden="true"></span>'

    def _kpi_item(value: object, label: str, note: str, kind: str, icon_name: str) -> str:
        return f"""
<div class="exec-kpi-item {kind}">
  <div class="exec-kpi-icon">{_icon(icon_name)}</div>
  <div class="exec-kpi-value">{escape(str(value))}</div>
  <div class="exec-kpi-label">{escape(label)}</div>
  <div class="exec-kpi-note">{escape(note)}</div>
</div>
"""

    def _ranking_rows(data, value_col: str, color: str) -> str:
        top = data.nlargest(10, value_col).reset_index(drop=True)
        max_value = float(top[value_col].max()) if not top.empty else 1.0
        rows = []
        for index, row in top.iterrows():
            width = max(8, min(100, float(row[value_col]) / max_value * 100))
            rows.append(
                f"""
<div class="exec-rank-row">
  <div class="exec-rank-number">{index + 1}</div>
  <div class="exec-rank-name">{escape(str(row['barra']))}</div>
  <div class="exec-rank-bar"><span style="width:{width:.1f}%;background:{color};"></span></div>
  <div class="exec-rank-value">{float(row[value_col]):.1f}</div>
</div>
"""
            )
        return "\n".join(rows)

    top_oanri_rows = _ranking_rows(profiles, "avg_oanri", "linear-gradient(90deg,#f29d24,#f07600)")
    top_icpi_rows = _ranking_rows(profiles, "avg_icpi", "linear-gradient(90deg,#087a82,#46c7bd)")
    shared_mask = profiles.nlargest(10, "avg_oanri")["barra"].isin(profiles.nlargest(10, "avg_icpi")["barra"])
    shared_names = profiles.nlargest(10, "avg_oanri").loc[shared_mask, "barra"].head(2).tolist()
    shared_html = "".join(f"<span>{escape(name)}</span>" for name in shared_names) or "<span>Sin coincidencias top 10</span>"

    st.html(
        f"""
<div class="exec-page">
  <div class="exec-header">
    <div>
      <div class="exec-kicker">Panel de soporte a decisiones</div>
      <h1>Resumen Ejecutivo</h1>
      <p>¿Dónde están las señales más fuertes de due diligence?</p>
    </div>
    <div class="exec-caveat">
      <div class="exec-caveat-icon">{_icon("shield")}</div>
      <div>
        <strong>Este dashboard es una capa de screening y priorización.</strong>
        <span>No prueba congestión física, no predice precios y no reemplaza due diligence técnica, contractual u operativa.</span>
      </div>
    </div>
  </div>
  <div class="exec-kpi-band">
    {_kpi_item(priority_a_count, "Señal prioritaria", "Candidata fuerte: señal alta, recurrencia y soporte suficiente.", "urgent", "warning")}
    {_kpi_item(priority_b_count, "Señal condicionada", "Relevante si sector, contrato o ubicación aumentan exposición.", "selective", "target")}
    {_kpi_item(watchlist_count, "Señal episódica", "Tiene picos o meses relevantes; requiere seguimiento.", "watch", "eye")}
    {_kpi_item(barras_count, "Barras analizadas", "Universo comparable del SEIN.", "scope", "network")}
    {_kpi_item(months_count, "Meses analizados", "Panel histórico 2023-2025.", "scope", "calendar")}
  </div>
  <div class="exec-main-finding">
    <div class="exec-finding-icon">{_icon("trend")}</div>
    <div class="exec-finding-copy">
      <div class="exec-section-kicker">Hallazgo principal</div>
      <h2>La cola está liderada por {escape(str(top_oanri['barra']))} en prioridad operativa y {escape(str(top_icpi['barra']))} en estrés nodal.</h2>
      <p>Estas barras combinan señales relevantes y contexto del sistema que amerita revisión. El siguiente paso es contrastar contrato, demanda industrial, ubicación y evidencia técnica.</p>
    </div>
    <div class="exec-next-steps">
      <div class="exec-section-kicker">¿Qué hacer ahora?</div>
      <div class="exec-step"><strong>1</strong><span><b>Abrir ranking</b><br>Filtrar revisión inmediata y selectiva.</span></div>
      <div class="exec-step"><strong>2</strong><span><b>Contrastar contexto</b><br>Exposición industrial y evidencia topológica.</span></div>
      <div class="exec-step"><strong>3</strong><span><b>Bajar a caso de estudio</b><br>Entender por qué una barra merece atención.</span></div>
    </div>
    <div class="exec-mini-map" aria-hidden="true">
      <svg viewBox="0 0 280 230">
        <path d="M156 10 209 36l-4 39 42 26-18 37 29 43-45 13-8 46-51 13-24 34-50-21-34-39 15-42-37-31 26-45-9-52 45-29Z" fill="rgba(22,140,140,.20)" stroke="#168c8c" stroke-width="2"/>
        <path d="M156 10 128 84 209 36 176 126 247 101 190 169 258 181 205 240M128 84 50 109 176 126 61 185 190 169 154 253" fill="none" stroke="rgba(22,140,140,.42)" stroke-width="1.4"/>
        <g fill="#23d3d3">
          <circle cx="156" cy="10" r="5"/><circle cx="209" cy="36" r="4"/><circle cx="128" cy="84" r="4"/><circle cx="176" cy="126" r="5"/><circle cx="247" cy="101" r="4"/><circle cx="190" cy="169" r="5"/><circle cx="258" cy="181" r="4"/><circle cx="205" cy="240" r="4"/><circle cx="61" cy="185" r="4"/><circle cx="50" cy="109" r="4"/>
        </g>
      </svg>
    </div>
  </div>
  <div class="exec-mid-grid">
    <div class="exec-explain-stack">
      <div class="exec-explain-card orange">
        <div class="exec-explain-icon">{_icon("target")}</div>
        <h3>¿Qué es la prioridad operativa?</h3>
        <p>Combina la señal de la barra con el contexto del sistema.</p>
        <p>Responde: ¿dónde la señal es relevante en meses de mayor presión?</p>
        <strong>Más alto = mayor prioridad para revisar.</strong>
      </div>
      <div class="exec-explain-card teal">
        <div class="exec-explain-icon">{_icon("pulse")}</div>
        <h3>¿Qué es el estrés nodal?</h3>
        <p>Mide qué tan intensa, volátil o extrema fue la señal de precio marginal de la barra frente a las demás.</p>
        <strong>Más alto = señal de precio más intensa.</strong>
      </div>
    </div>
    <div class="exec-rank-zone">
      <div class="exec-rank-grid">
        <div class="exec-rank-card orange">
          <div class="exec-rank-title">{_icon("target")}<span>Top 10 por prioridad operativa</span><em>Puntaje promedio</em></div>
          <div class="exec-rank-header"><span>#</span><span>Barra</span><span></span><span>Puntaje</span></div>
          {top_oanri_rows}
        </div>
        <div class="exec-rank-card teal">
          <div class="exec-rank-title">{_icon("pulse")}<span>Top 10 por estrés nodal</span><em>Puntaje promedio</em></div>
          <div class="exec-rank-header"><span>#</span><span>Barra</span><span></span><span>Puntaje</span></div>
          {top_icpi_rows}
        </div>
      </div>
      <div class="exec-overlap-note">
        <div>{_icon("link")} <strong>Coincidencias relevantes en ambos rankings:</strong> {shared_html}</div>
        <span>→ Prioridad preferente de revisión.</span>
      </div>
    </div>
  </div>
</div>
""",
    )
    if not regime.empty:
        st.html(
            """
<div class="exec-regime-shell">
  <div class="exec-regime-title">
    <div class="exec-regime-icon"><span class="exec-icon exec-icon-trend" aria-hidden="true"></span></div>
    <div>
      <h3>Régimen operativo mensual</h3>
      <p>Contexto del sistema para interpretar la prioridad operativa.</p>
    </div>
  </div>
</div>
""",
        )
        chart_col, note_col = st.columns([4.3, 1.2])
        with chart_col:
            st.plotly_chart(system_regime_line(regime), use_container_width=True)
        with note_col:
            st.html(
                """
<div class="exec-regime-note">
  <div class="exec-regime-note-icon">♢</div>
  <p>Los meses de mayor presión del sistema ayudan a explicar por qué ciertas barras ganan prioridad en determinados periodos.</p>
  <strong>No indica causalidad física por barra específica.</strong>
</div>
""",
            )
    st.html(
        """
<div class="exec-bottom-action">
  <div><strong>Lectura ejecutiva:</strong> usa esta vista como entrada para armar tu lista corta de revisión. El detalle por barra está en el ranking y en el caso de estudio.</div>
  <span>Ir a Ranking de Prioridad →</span>
</div>
""",
    )


def render_ranking() -> None:
    df = load_product_layer()
    if df.empty:
        st.error("La capa producto no está disponible.")
        st.stop()

    st.markdown(
        """
<style>
/* Critical CSS kept in-page so Streamlit Cloud cannot render this tab as plain markdown
   if the shared stylesheet is cached or loaded out of order. */
.block-container {
  max-width: 1500px !important;
  padding-left: 2.35rem !important;
  padding-right: 2.35rem !important;
}

.rank-page,
.rank-page *,
.rank-summary-card,
.rank-summary-card *,
.rank-taxonomy,
.rank-taxonomy *,
.rank-bottom-notes,
.rank-bottom-notes * {
  box-sizing: border-box !important;
}

.rank-page {
  width: 100% !important;
  margin: 0 0 0.65rem 0 !important;
}

.rank-header {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) minmax(330px, 0.35fr) !important;
  gap: 1.35rem !important;
  align-items: start !important;
  width: 100% !important;
  margin: 0.35rem 0 1.05rem 0 !important;
}

.rank-header h1 {
  color: #102033 !important;
  font-size: clamp(2.35rem, 3.4vw, 3.4rem) !important;
  line-height: 1 !important;
  margin: 0 0 0.45rem 0 !important;
  font-weight: 880 !important;
  letter-spacing: 0 !important;
}

.rank-header p {
  color: #314258 !important;
  font-size: 1.02rem !important;
  margin: 0 !important;
}

.rank-caveat {
  display: grid !important;
  grid-template-columns: 42px minmax(0, 1fr) !important;
  gap: 0.85rem !important;
  align-items: center !important;
  border: 1px solid #d8e3ea !important;
  border-radius: 8px !important;
  background: rgba(255,255,255,0.88) !important;
  padding: 0.92rem 1.05rem !important;
  box-shadow: 0 10px 26px rgba(16,32,51,0.045) !important;
}

.exec-icon {
  display: inline-grid !important;
  place-items: center !important;
  width: 1.15em !important;
  height: 1.15em !important;
  line-height: 1 !important;
  font-style: normal !important;
}

.exec-icon::before {
  display: block !important;
  font-family: Arial, sans-serif !important;
  font-size: 1em !important;
  line-height: 1 !important;
  font-weight: 900 !important;
}

.exec-icon-shield::before { content: "◇"; }
.exec-icon-target::before { content: "◎"; }
.exec-icon-filter::before { content: "▽"; }
.exec-icon-case::before { content: "▤"; }
.exec-icon-info::before { content: "i"; }

.rank-caveat > .exec-icon {
  color: #2f6f9f !important;
  font-size: 2rem !important;
}

.rank-caveat strong,
.rank-caveat span {
  display: block !important;
  color: #102033 !important;
  font-size: 0.8rem !important;
  line-height: 1.35 !important;
}

.rank-caveat span {
  color: #26384d !important;
  margin-top: 0.15rem !important;
  font-weight: 700 !important;
}

.rank-summary-card {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) minmax(230px, 0.28fr) minmax(275px, 0.34fr) !important;
  gap: 1.1rem !important;
  align-items: center !important;
  width: 100% !important;
  border: 1px solid #cddde7 !important;
  border-radius: 8px !important;
  background: linear-gradient(90deg, #ffffff 0%, #f8fcfd 70%, #edf7fa 100%) !important;
  box-shadow: 0 12px 30px rgba(16,32,51,0.05) !important;
  padding: 1rem 1.15rem !important;
  margin: 0.2rem 0 0.85rem 0 !important;
}

.rank-summary-left {
  display: grid !important;
  grid-template-columns: 74px minmax(0, 1fr) !important;
  gap: 0.9rem !important;
  align-items: center !important;
  min-width: 0 !important;
}

.rank-summary-icon {
  width: 62px !important;
  height: 62px !important;
  border-radius: 50% !important;
  background: #eefafa !important;
  color: #168c8c !important;
  display: grid !important;
  place-items: center !important;
}

.rank-summary-icon .exec-icon {
  font-size: 2.65rem !important;
}

.rank-summary-kpis {
  display: grid !important;
  grid-template-columns: repeat(5, minmax(88px, 1fr)) !important;
  gap: 0.75rem !important;
  align-items: stretch !important;
}

.rank-summary-title {
  grid-column: 1 / -1 !important;
  color: #102033 !important;
  font-size: 0.86rem !important;
  font-weight: 860 !important;
}

.rank-kpi {
  border-right: 1px solid #d8e3ea !important;
  padding-right: 0.65rem !important;
}

.rank-kpi:last-child {
  border-right: 0 !important;
}

.rank-kpi strong {
  display: block !important;
  color: #164a63 !important;
  font-size: 1.72rem !important;
  line-height: 1 !important;
  font-weight: 880 !important;
}

.rank-kpi span {
  display: block !important;
  color: #26384d !important;
  font-size: 0.72rem !important;
  line-height: 1.35 !important;
  margin-top: 0.35rem !important;
}

.rank-start-box {
  border-left: 1px solid #d8e3ea !important;
  padding-left: 1.1rem !important;
}

.rank-start-box strong,
.rank-next-box strong {
  display: block !important;
  color: #102033 !important;
  font-size: 0.82rem !important;
  margin-bottom: 0.45rem !important;
}

.rank-start-box ol {
  list-style: none !important;
  counter-reset: rank-step !important;
  padding: 0 !important;
  margin: 0 !important;
}

.rank-start-box li {
  counter-increment: rank-step !important;
  color: #102033 !important;
  font-size: 0.82rem !important;
  font-weight: 820 !important;
  margin: 0.42rem 0 !important;
  display: grid !important;
  grid-template-columns: 24px minmax(0, 1fr) !important;
  gap: 0.45rem !important;
  align-items: center !important;
}

.rank-start-box li::before {
  content: counter(rank-step) !important;
  width: 21px !important;
  height: 21px !important;
  border-radius: 50% !important;
  background: #168c8c !important;
  color: #fff !important;
  display: grid !important;
  place-items: center !important;
  font-size: 0.72rem !important;
}

.rank-next-box {
  display: grid !important;
  grid-template-columns: 42px minmax(0, 1fr) !important;
  gap: 0.75rem !important;
  border-left: 1px solid #d8e3ea !important;
  padding-left: 1rem !important;
}

.rank-next-box > .exec-icon {
  color: #2f6f9f !important;
  font-size: 2rem !important;
}

.rank-next-box p {
  color: #26384d !important;
  font-size: 0.78rem !important;
  line-height: 1.42 !important;
  margin: 0 0 0.7rem 0 !important;
}

.rank-next-button {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 7px !important;
  background: #164a63 !important;
  color: #ffffff !important;
  font-weight: 820 !important;
  font-size: 0.78rem !important;
  padding: 0.52rem 0.8rem !important;
  min-width: 170px !important;
  text-decoration: none !important;
}

.rank-filter-title {
  display: flex !important;
  gap: 0.55rem !important;
  align-items: center !important;
  color: #102033 !important;
  font-size: 0.86rem !important;
  font-weight: 860 !important;
  min-height: 54px !important;
}

.rank-filter-title .exec-icon {
  color: #2f6f9f !important;
  font-size: 1.25rem !important;
}

.rank-taxonomy {
  display: grid !important;
  grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
  gap: 0 !important;
  border: 1px solid #d8e3ea !important;
  border-radius: 8px !important;
  background: #ffffff !important;
  box-shadow: 0 9px 24px rgba(16,32,51,0.04) !important;
  overflow: hidden !important;
  width: 100% !important;
  margin: 0 0 0.75rem 0 !important;
}

.rank-taxonomy-wrap {
  border: 1px solid #d8e3ea !important;
  border-radius: 8px !important;
  background: #ffffff !important;
  box-shadow: 0 9px 24px rgba(16,32,51,0.04) !important;
  overflow: hidden !important;
  margin: 0.75rem 0 0.75rem 0 !important;
}

.rank-tax-heading {
  color: #102033 !important;
  font-size: 0.82rem !important;
  font-weight: 860 !important;
  padding: 0.7rem 0.9rem 0.2rem 0.9rem !important;
}

.rank-taxonomy-wrap .rank-taxonomy {
  border: 0 !important;
  box-shadow: none !important;
}

.rank-tax-item {
  border-right: 1px solid #d8e3ea !important;
  padding: 0.85rem 0.95rem !important;
  position: relative !important;
  min-height: 92px !important;
  display: grid !important;
  grid-template-columns: 42px minmax(0, 1fr) !important;
  gap: 0.75rem !important;
  align-items: start !important;
}

.rank-tax-item:last-child {
  border-right: 0 !important;
}

.rank-tax-item strong {
  display: block !important;
  font-size: 0.78rem !important;
  margin-bottom: 0.25rem !important;
  color: #102033 !important;
}

.rank-tax-item.red strong { color: #b23a2e !important; }
.rank-tax-item.amber strong { color: #c47a16 !important; }
.rank-tax-item.teal strong { color: #087a82 !important; }
.rank-tax-item.steel strong { color: #45566b !important; }
.rank-tax-item.purple strong { color: #7e3fa1 !important; }

.rank-tax-item span {
  display: block !important;
  color: #26384d !important;
  font-size: 0.72rem !important;
  line-height: 1.38 !important;
}

.rank-tax-icon {
  width: 34px !important;
  height: 34px !important;
  border-radius: 999px !important;
  display: grid !important;
  place-items: center !important;
  margin-top: 0.05rem !important;
}

.rank-tax-icon svg {
  width: 20px !important;
  height: 20px !important;
  fill: none !important;
  stroke: currentColor !important;
  stroke-width: 2.2 !important;
  stroke-linecap: round !important;
  stroke-linejoin: round !important;
}

.rank-tax-item.red .rank-tax-icon { color: #b23a2e !important; background: #fde8e6 !important; }
.rank-tax-item.amber .rank-tax-icon { color: #c47a16 !important; background: #fff0cf !important; }
.rank-tax-item.teal .rank-tax-icon { color: #087a82 !important; background: #dff4f6 !important; }
.rank-tax-item.steel .rank-tax-icon { color: #2f6f9f !important; background: #e5f2f7 !important; }
.rank-tax-item.purple .rank-tax-icon { color: #7e3fa1 !important; background: #f2e8f8 !important; }

.rank-section-title {
  color: #102033 !important;
  font-size: 1.38rem !important;
  margin: 0.95rem 0 0.55rem 0 !important;
  font-weight: 850 !important;
}

.rank-table-guidance {
  color: #314258 !important;
  font-size: 0.84rem !important;
  line-height: 1.42 !important;
  margin: -0.1rem 0 0.75rem 0 !important;
}

.rank-table-guidance strong {
  color: #102033 !important;
}

.rank-bottom-notes {
  display: grid !important;
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  gap: 0.8rem !important;
  margin-top: 0.75rem !important;
}

.rank-bottom-notes > div {
  display: grid !important;
  grid-template-columns: 38px minmax(0, 1fr) !important;
  gap: 0.75rem !important;
  border: 1px solid #d8e3ea !important;
  border-radius: 8px !important;
  background: #ffffff !important;
  padding: 0.9rem 1rem !important;
  box-shadow: 0 8px 22px rgba(16,32,51,0.035) !important;
}

.rank-bottom-notes .exec-icon {
  color: #2f6f9f !important;
  font-size: 1.6rem !important;
}

.rank-bottom-notes strong {
  display: block !important;
  color: #102033 !important;
  font-size: 0.82rem !important;
}

.rank-bottom-notes p {
  margin: 0.2rem 0 0 0 !important;
  color: #26384d !important;
  font-size: 0.75rem !important;
  line-height: 1.4 !important;
  max-width: 72ch !important;
}

.rank-bottom-notes .rank-note-copy {
  min-width: 0 !important;
  overflow-wrap: normal !important;
  word-break: normal !important;
}

div[data-testid="stDataFrame"] {
  border: 1px solid #d8e3ea !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  box-shadow: 0 8px 24px rgba(24, 34, 53, 0.04) !important;
}

.stMultiSelect [data-baseweb="select"] > div,
.stSelectbox [data-baseweb="select"] > div {
  border-radius: 8px !important;
  border-color: #cbd6e2 !important;
  background: #fbfcfe !important;
}

.stMultiSelect [data-baseweb="tag"] {
  background: #e5f2f7 !important;
  border: 1px solid #b7d7e1 !important;
}

.stMultiSelect [data-baseweb="tag"] span {
  color: #173b57 !important;
  font-weight: 650 !important;
}

@media (max-width: 1050px) {
  .rank-header,
  .rank-summary-card,
  .rank-summary-left,
  .rank-next-box,
  .rank-bottom-notes {
    grid-template-columns: 1fr !important;
  }

  .rank-summary-kpis,
  .rank-taxonomy {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }

  .rank-start-box,
  .rank-next-box {
    border-left: 0 !important;
    border-top: 1px solid #d8e3ea !important;
    padding-left: 0 !important;
    padding-top: 0.85rem !important;
  }
}
</style>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="rank-page">
  <div class="rank-header">
    <div>
      <div class="exec-kicker">Panel de soporte a decisiones</div>
      <h1>Ranking de Prioridad por Barra</h1>
      <p><strong>Pregunta de decisión:</strong> ¿Qué barras deberían revisarse primero?</p>
    </div>
    <div class="rank-caveat">
      <span class="exec-icon exec-icon-info" aria-hidden="true"></span>
      <div>
        <strong>Estar arriba significa mayor prioridad de revisión.</strong>
        <span>No peor barra ni prueba de congestión física ni predicción de precios.</span>
      </div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    summary_slot = st.empty()

    filter_top = st.columns([0.8, 1.25, 1.15, 1.1, 1])
    with filter_top[0]:
        st.markdown(
            """
<div class="rank-filter-title">
  <span class="exec-icon exec-icon-filter" aria-hidden="true"></span>
  <strong>Filtros de revisión</strong>
</div>
""",
            unsafe_allow_html=True,
        )
    with filter_top[4]:
        reset_filters = st.button("Limpiar filtros", key="ranking_clear_filters", width="stretch")
    if reset_filters:
        st.session_state["ranking_level"] = []
        st.session_state["ranking_robustness"] = []
        st.session_state["ranking_tension"] = []

    filter_cols = st.columns([1.25, 1.05, 1.05])
    stability_display = {
        "Estabilidad alta": "Estable",
        "Robustez alta": "Estable",
        "High robustness": "Estable",
        "Baja dependencia": "Estable",
        "Estable": "Estable",
        "Estabilidad moderada": "Sensible",
        "Robustez moderada": "Sensible",
        "Moderate robustness": "Sensible",
        "Dependencia media": "Sensible",
        "Sensible": "Sensible",
        "Estabilidad baja": "Variable",
        "Robustez baja": "Variable",
        "Low robustness": "Variable",
        "Alta dependencia": "Variable",
        "Fuera de top-list de sensibilidad": "Variable",
        "Not covered by sensitivity top-list": "Variable",
        "Variable": "Variable",
    }
    with filter_cols[0]:
        selected_priorities = priority_filter(
            df,
            key="ranking_level",
            label="Tipo de señal",
            placeholder="Seleccionar categorías",
        )
    with filter_cols[1]:
        selected_robustness = robustness_filter(
            df,
            key="ranking_robustness",
            label="Estabilidad del resultado",
            placeholder="Seleccionar estabilidad",
            display_map=stability_display,
        )
    with filter_cols[2]:
        selected_tension = tension_filter(
            df,
            key="ranking_tension",
            label="Tensión kV",
            placeholder="Seleccionar tensión",
        )

    filtered = df.copy()
    if selected_priorities:
        filtered = filtered[filtered["due_diligence_priority"].isin(selected_priorities)]
    if selected_robustness:
        robustness_col = "signal_stability_label_es" if "signal_stability_label_es" in filtered.columns else "robustness_flag_es" if "robustness_flag_es" in filtered.columns else "robustness_flag"
        filtered = filtered[filtered[robustness_col].astype(str).isin(selected_robustness)]
    if selected_tension:
        filtered = filtered[filtered["nivel_tension_kv"].isin(selected_tension)]
    filtered = filtered.sort_values("decision_priority_score", ascending=False)

    def _count_priority(value: str) -> int:
        return int((filtered["due_diligence_priority"] == value).sum()) if not filtered.empty else 0

    robust_col = "signal_stability_label_es" if "signal_stability_label_es" in filtered.columns else "robustness_flag_es" if "robustness_flag_es" in filtered.columns else "robustness_flag"
    def _is_stable_result(value: object) -> bool:
        lower = str(value).lower()
        return (
            "estable" in lower
            or "baja dependencia" in lower
            or "robustez alta" in lower
            or "estabilidad alta" in lower
            or "high robustness" in lower
        )

    stable_count = int(filtered[robust_col].map(_is_stable_result).sum()) if robust_col in filtered else 0
    queue_count = int(filtered["due_diligence_priority"].isin(["Priority A", "Priority B"]).sum()) if not filtered.empty else 0
    watch_count = _count_priority("Watchlist")
    immediate_count = _count_priority("Priority A")
    top_barras = filtered["barra"].head(3).tolist()
    while len(top_barras) < 3:
        top_barras.append("Sin resultado")
    next_action = (
        f"Abrir caso de estudio de {top_barras[0]} para contrastar contrato, demanda industrial, contexto y recurrencia."
        if not filtered.empty
        else "Amplía los filtros para recuperar barras candidatas de revisión."
    )
    with summary_slot.container():
        st.markdown(
            f"""
<div class="rank-summary-card">
  <div class="rank-summary-left">
    <div class="rank-summary-icon"><span class="exec-icon exec-icon-target" aria-hidden="true"></span></div>
    <div class="rank-summary-kpis">
      <div class="rank-summary-title">Con los filtros actuales:</div>
      <div class="rank-kpi"><strong>{len(filtered):,.0f}</strong><span>barras visibles</span></div>
      <div class="rank-kpi"><strong>{queue_count:,.0f}</strong><span>en cola principal<br>(inmediata + selectiva)</span></div>
      <div class="rank-kpi"><strong>{watch_count:,.0f}</strong><span>en seguimiento mensual<br>(casos episódicos)</span></div>
      <div class="rank-kpi"><strong>{stable_count:,.0f}</strong><span>con resultado<br>estable</span></div>
      <div class="rank-kpi"><strong>{immediate_count:,.0f}</strong><span>en revisión inmediata</span></div>
    </div>
  </div>
  <div class="rank-start-box">
    <strong>La revisión empieza por:</strong>
    <ol>
      <li>{escape(str(top_barras[0]))}</li>
      <li>{escape(str(top_barras[1]))}</li>
      <li>{escape(str(top_barras[2]))}</li>
    </ol>
  </div>
  <div class="rank-next-box">
    <span class="exec-icon exec-icon-case" aria-hidden="true"></span>
    <div><strong>Siguiente paso recomendado:</strong><p>{escape(next_action)}</p><a class="rank-next-button" href="?page=Caso%20de%20Estudio">Abrir caso de estudio →</a></div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
<div class="rank-taxonomy-wrap">
  <div class="rank-tax-heading">Taxonomía de señal: qué significa y qué hacer</div>
  <div class="rank-taxonomy">
    <div class="rank-tax-item red"><div class="rank-tax-icon"><svg viewBox="0 0 24 24"><path d="M5 21V4"/><path d="M5 5h11l-1.8 4L16 13H5"/></svg></div><div><strong>1. Señal prioritaria</strong><span>Candidata fuerte: revisar primero y abrir revisión estructurada.</span></div></div>
    <div class="rank-tax-item amber"><div class="rank-tax-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div><strong>2. Señal condicionada</strong><span>Relevante si sector, contrato, ubicación o escenario aumentan exposición.</span></div></div>
    <div class="rank-tax-item teal"><div class="rank-tax-icon"><svg viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg></div><div><strong>3. Señal episódica</strong><span>Tiene picos o meses relevantes; vigilar si se repite o empeora.</span></div></div>
    <div class="rank-tax-item steel"><div class="rank-tax-icon"><svg viewBox="0 0 24 24"><path d="M4 19V5"/><path d="M4 19h17"/><rect x="7" y="12" width="3" height="4"/><rect x="12" y="9" width="3" height="7"/><rect x="17" y="6" width="3" height="10"/></svg></div><div><strong>4. Contexto base</strong><span>Usar como referencia. No prioritaria; sirve para comparar.</span></div></div>
    <div class="rank-tax-item purple"><div class="rank-tax-icon"><svg viewBox="0 0 24 24"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/></svg></div><div><strong>5. Información por completar</strong><span>Completar evidencia o cobertura antes de una lectura fuerte.</span></div></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<h2 class='rank-section-title'>Cola priorizada de revisión</h2>", unsafe_allow_html=True)
    st.markdown(
        """
<p class="rank-table-guidance"><strong>Las primeras filas no son “peores barras”:</strong> son los casos con más razones analíticas para iniciar revisión experta. Soporte contextual revisado disponible para las barras del demo público.</p>
""",
        unsafe_allow_html=True,
    )
    if filtered.empty:
        action_panel("Sin resultados para los filtros activos", "Amplía tipo de señal, estabilidad del resultado o tensión para recuperar barras candidatas.")
    else:
        page_tools = st.columns([1, 1, 4, 1])
        with page_tools[0]:
            rows_per_page = st.selectbox("Filas por página", [10, 25, 50, 100], index=0, key="ranking_rows")
        total_pages = max(1, int((len(filtered) - 1) // rows_per_page) + 1)
        with page_tools[1]:
            page_number = st.number_input("Página", min_value=1, max_value=total_pages, value=1, step=1, key="ranking_page")
        start = (page_number - 1) * rows_per_page
        end = start + rows_per_page
        page_df = filtered.iloc[start:end].copy()

        action_short = {
            "Priority A": "Abrir caso estructurado",
            "Priority B": "Revisar tras prioritarias",
            "Watchlist": "Monitorear recurrencia",
            "Monitor": "Mantener como contexto",
            "Low information": "Completar contexto",
        }
        level_labels = {
            "Priority A": "Señal prioritaria",
            "Priority B": "Señal condicionada",
            "Watchlist": "Señal episódica",
            "Monitor": "Contexto base",
            "Low information": "Información por completar",
        }

        def _stability_label(value: object) -> str:
            text = str(value)
            lower = text.lower()
            if "estable" in lower or "baja dependencia" in lower:
                return "Estable"
            if "sensible" in lower or "dependencia media" in lower:
                return "Sensible"
            if "variable" in lower or "alta dependencia" in lower:
                return "Variable"
            if "alta" in lower or "high" in lower:
                return "Estable"
            if "moderada" in lower or "moderate" in lower:
                return "Sensible"
            if "baja" in lower or "low" in lower:
                return "Variable"
            if "fuera" in lower or "not covered" in lower:
                return "Variable"
            if lower in {"", "nan", "none"}:
                return "No clasificado"
            return "Sensible"

        def _coverage_label(value: object) -> str:
            lower = str(value).lower()
            if "completa" in lower:
                return "Completa"
            if "alta" in lower:
                return "Alta"
            if "parcial" in lower:
                return "Parcial"
            if "limitada" in lower:
                return "Limitada"
            if not lower or lower in {"nan", "none"}:
                return "No clasificada"
            return str(value)

        def _executive_reason(row: pd.Series) -> str:
            priority = str(row.get("due_diligence_priority", ""))
            result_stability = _stability_label(row.get(robust_col, ""))
            persistence = str(row.get("persistence_category_es", row.get("persistence_category", "")))
            priority_months_value = int(row.get("priority_months", 0) or 0)
            watchlist_months_value = int(row.get("watchlist_months", 0) or 0)
            observed_months = int(row.get("score_months_observed", 0) or 0)
            coverage = _coverage_label(row.get("score_coverage_class_es", ""))
            if coverage == "Limitada" and priority in {"Priority A", "Priority B"}:
                return "Señal relevante; validar cobertura"
            if priority == "Priority A":
                if persistence == "Persistente":
                    return "Alta señal + persistencia"
                if result_stability == "Estable":
                    return "Alta señal + resultado estable"
                return "Alta prioridad operativa"
            if priority == "Priority B":
                if result_stability == "Estable" and priority_months_value >= 8:
                    return "Señal relevante + resultado estable"
                if priority_months_value > 0 and watchlist_months_value > 0:
                    return "Recurrencia mensual + contexto"
                if float(row.get("avg_icpi", 0) or 0) >= float(row.get("avg_oanri", 0) or 0):
                    return "Estrés nodal elevado"
                return "Prioridad operativa elevada"
            if priority == "Watchlist":
                if watchlist_months_value > 0:
                    return "Episodios a monitorear"
                return "Caso sensible a escenario"
            if priority == "Monitor":
                return "Contexto base"
            if priority == "Low information":
                if observed_months < 36:
                    return "Completar cobertura"
                return "Completar contexto"
            return str(row.get("priority_reason", "Revisión contextual sugerida"))

        table = page_df.assign(
            **{
                "#": range(start + 1, start + 1 + len(page_df)),
                "Score de revisión": page_df["decision_priority_score"].round(2),
                "Tipo de señal": page_df["due_diligence_priority"].map(level_labels).fillna(page_df["due_diligence_priority_es"]),
                "Acción recomendada": page_df["due_diligence_priority"].map(action_short).fillna(page_df["recommended_action"]),
                "Estabilidad del resultado": page_df[robust_col].map(_stability_label),
                "Cobertura analítica": page_df.get("score_coverage_class_es", pd.Series("", index=page_df.index)).map(_coverage_label),
                "Estrés nodal prom.": page_df["avg_icpi"].round(2),
                "Prioridad operativa prom.": page_df["avg_oanri"].round(2),
            }
        )[
            [
                "#",
                "barra",
                "Score de revisión",
                "Tipo de señal",
                "Acción recomendada",
                "Estabilidad del resultado",
                "Cobertura analítica",
                "Estrés nodal prom.",
                "Prioridad operativa prom.",
            ]
        ].rename(columns={"barra": "Barra"})

        def _rank_style(value: object) -> str:
            text = str(value)
            if text == "Señal prioritaria":
                return "background-color: #fde8e6; color: #9d1f17; font-weight: 800; border-radius: 6px"
            if text == "Señal condicionada":
                return "background-color: #fff0cf; color: #a85a00; font-weight: 800; border-radius: 6px"
            if text == "Señal episódica":
                return "background-color: #dff4f6; color: #087a82; font-weight: 800; border-radius: 6px"
            if text == "Contexto base":
                return "background-color: #eef2f6; color: #4f5d6f; font-weight: 800; border-radius: 6px"
            if text == "Información por completar":
                return "background-color: #f2e8f8; color: #7e3fa1; font-weight: 800; border-radius: 6px"
            if text == "Estable":
                return "background-color: #e9f8ef; color: #1f8a5b; font-weight: 800; border-radius: 999px"
            if text == "Sensible":
                return "background-color: #fff3df; color: #c47a16; font-weight: 800; border-radius: 999px"
            if text in {"Variable", "No clasificado"}:
                return "background-color: #eef2f6; color: #64748b; font-weight: 800; border-radius: 999px"
            if text == "Completa":
                return "background-color: #e9f8ef; color: #1f8a5b; font-weight: 800; border-radius: 999px"
            if text in {"Alta", "Parcial"}:
                return "background-color: #fff3df; color: #c47a16; font-weight: 800; border-radius: 999px"
            if text == "Limitada":
                return "background-color: #fde8e6; color: #9d1f17; font-weight: 800; border-radius: 999px"
            return ""

        st.dataframe(
            table.style.map(_rank_style).format(precision=2),
            width="stretch",
            hide_index=True,
            height=430,
            column_config={
                "#": st.column_config.NumberColumn("#", width="small"),
                "Barra": st.column_config.TextColumn("Barra", width="large"),
                "Score de revisión": st.column_config.ProgressColumn("Score de revisión", min_value=0, max_value=100, format="%.2f", width="medium"),
                "Tipo de señal": st.column_config.TextColumn("Tipo de señal", width="medium"),
                "Acción recomendada": st.column_config.TextColumn("Acción recomendada", width="medium"),
                "Estabilidad del resultado": st.column_config.TextColumn("Estabilidad del resultado", width="small"),
                "Cobertura analítica": st.column_config.TextColumn("Cobertura", width="small"),
                "Estrés nodal prom.": st.column_config.NumberColumn("Estrés nodal prom.", format="%.2f", width="small"),
                "Prioridad operativa prom.": st.column_config.NumberColumn("Prioridad operativa prom.", format="%.2f", width="small"),
            },
        )
        st.caption(f"Mostrando {start + 1:,} a {min(end, len(filtered)):,} de {len(filtered):,} barras filtradas.")
        st.download_button("Descargar lista filtrada", filtered.to_csv(index=False).encode("utf-8"), file_name="sein_barra_due_diligence_worklist.csv", mime="text/csv")
    st.markdown(
        """
<div class="rank-bottom-notes">
  <div><span class="exec-icon exec-icon-shield" aria-hidden="true"></span><div class="rank-note-copy"><strong>Nota metodológica:</strong><p>Esta priorización combina señales de precio, recurrencia mensual, estabilidad del resultado y contexto del sistema. No sustituye análisis técnico, contractual u operativo.</p></div></div>
  <div><span class="exec-icon exec-icon-info" aria-hidden="true"></span><div class="rank-note-copy"><strong>Cómo leer la escala:</strong><p>Estable = la barra sigue apareciendo como relevante bajo criterios alternativos; sensible o variable = conviene contrastar episodios, sector y evidencia antes de priorizar fuerte.</p></div></div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_icpi_oanri() -> None:
    df = load_product_layer()
    panel = load_monthly_panel()
    if df.empty:
        st.error("La capa producto no está disponible.")
        st.stop()

    st.markdown(
        """
<style>
.signal-page {
  width: 100%;
  margin: 0.15rem 0 0.65rem 0;
}

.block-container:has(.signal-page) {
  width: 100% !important;
  max-width: none !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  padding-left: 2rem !important;
  padding-right: 2rem !important;
}

.signal-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(340px, 0.26fr);
  gap: 1.25rem;
  align-items: start;
  margin-bottom: 0.85rem;
}

.signal-header h1 {
  margin: 0 0 0.35rem 0 !important;
  color: #102033 !important;
  font-size: clamp(2.35rem, 3.3vw, 3.25rem) !important;
  line-height: 1 !important;
  font-weight: 880 !important;
  letter-spacing: 0 !important;
}

.signal-header p {
  margin: 0 !important;
  color: #314258 !important;
  font-size: 1rem !important;
}

.signal-caveat {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr);
  gap: 0.8rem;
  align-items: center;
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  background: rgba(255,255,255,0.92);
  padding: 0.95rem 1rem;
  box-shadow: 0 10px 26px rgba(16,32,51,0.045);
}

.signal-caveat-icon {
  width: 34px;
  height: 34px;
  border: 2px solid #164a63;
  color: #164a63;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-weight: 900;
  font-size: 1.1rem;
}

.signal-caveat strong,
.signal-caveat span {
  display: block;
  color: #102033;
  font-size: 0.82rem;
  line-height: 1.35;
}

.signal-caveat span {
  margin-top: 0.1rem;
  color: #314258;
  font-weight: 650;
}

.signal-top-band {
  display: grid;
  grid-template-columns: minmax(330px, 0.23fr) minmax(0, 1fr);
  gap: 0.85rem;
  margin: 0 0 0.85rem 0;
}

.signal-context-card,
.signal-kpi-band,
.signal-chart-shell,
.signal-side-card,
.signal-filter-card,
.signal-note-card,
.signal-guide {
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 10px 26px rgba(16,32,51,0.045);
}

.signal-context-card {
  display: grid;
  grid-template-columns: 40px minmax(0, 1fr);
  gap: 0.75rem;
  padding: 0.9rem 0.95rem;
  min-height: 126px;
}

.signal-map-icon svg,
.signal-card-icon svg,
.signal-guide-icon svg {
  width: 24px;
  height: 24px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2.2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.signal-map-icon {
  color: #164a63;
  padding-top: 0.12rem;
}

.signal-context-card h3,
.signal-side-card h3 {
  margin: 0 0 0.45rem 0;
  color: #102033;
  font-size: 0.95rem;
  font-weight: 850;
}

.signal-context-card p {
  color: #26384d;
  margin: 0 0 0.45rem 0;
  line-height: 1.38;
  font-size: 0.8rem;
}

.signal-context-card small {
  display: block;
  color: #64748b;
  font-size: 0.75rem;
  line-height: 1.4;
}

.signal-kpi-band {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  overflow: hidden;
}

.signal-kpi {
  padding: 1rem 1.05rem;
  border-right: 1px solid #d8e3ea;
  min-height: 126px;
}

.signal-kpi:last-child {
  border-right: 0;
}

.signal-kpi strong {
  display: block;
  color: #102033;
  font-size: 1.65rem;
  line-height: 1;
  margin-bottom: 0.45rem;
  font-weight: 880;
}

.signal-kpi span {
  display: block;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 850;
  font-size: 0.72rem;
  margin-bottom: 0.35rem;
}

.signal-kpi em {
  display: block;
  color: #314258;
  font-style: normal;
  font-size: 0.78rem;
  line-height: 1.35;
}

.signal-chart-shell {
  padding: 0.9rem 1rem 0.55rem 1rem;
  min-height: 0;
}

.signal-chart-title {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
  color: #102033;
  font-size: 1rem;
  font-weight: 880;
  margin-bottom: 0.2rem;
}

.signal-chart-caption {
  color: #64748b;
  font-size: 0.76rem;
  margin-top: 0.15rem;
}

.signal-side-card {
  padding: 0.9rem 0.95rem;
  min-height: auto;
  margin-bottom: 0.75rem;
}

.signal-candidates-card {
  min-height: 100%;
}

.signal-candidates-card .rank-next-button {
  margin-top: 0.8rem;
}

.signal-map-help {
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  background: #eef8fb;
  padding: 0.85rem 0.9rem;
  color: #102033;
}

.signal-map-help strong {
  display: block;
  font-size: 0.86rem;
  margin-bottom: 0.35rem;
}

.signal-map-help p {
  margin: 0 0 0.35rem 0;
  color: #314258;
  font-size: 0.75rem;
  line-height: 1.36;
}

.signal-map-help a {
  color: #087a82;
  font-weight: 850;
  text-decoration: none;
}

.signal-level-list {
  display: grid;
  gap: 0.55rem;
}

.signal-level {
  display: grid;
  grid-template-columns: 38px minmax(0, 1fr);
  gap: 0.62rem;
  align-items: start;
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  padding: 0.68rem 0.72rem;
  background: #ffffff;
}

.signal-card-icon {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: 999px;
}

.signal-level strong {
  display: block;
  font-size: 0.76rem;
  margin-bottom: 0.2rem;
}

.signal-level span {
  display: block;
  color: #314258;
  font-size: 0.7rem;
  line-height: 1.32;
}

.signal-level.red strong { color: #b23a2e; }
.signal-level.amber strong { color: #c47a16; }
.signal-level.teal strong { color: #087a82; }
.signal-level.steel strong { color: #45566b; }
.signal-level.purple strong { color: #7e3fa1; }
.signal-level.red .signal-card-icon { color: #b23a2e; background: #fde8e6; }
.signal-level.amber .signal-card-icon { color: #c47a16; background: #fff0cf; }
.signal-level.teal .signal-card-icon { color: #087a82; background: #dff4f6; }
.signal-level.steel .signal-card-icon { color: #2f6f9f; background: #e5f2f7; }
.signal-level.purple .signal-card-icon { color: #7e3fa1; background: #f2e8f8; }

.signal-filter-card,
.signal-note-card {
  padding: 0.9rem 1rem;
}

.signal-filter-card {
  margin: 0.85rem 0;
}

.signal-filter-title {
  display: flex;
  gap: 0.55rem;
  align-items: center;
  color: #102033;
  font-weight: 860;
  min-height: 48px;
}

.signal-filter-title svg,
.signal-note-card svg {
  width: 25px;
  height: 25px;
  fill: none;
  stroke: #164a63;
  stroke-width: 2.2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.signal-note-card {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr);
  gap: 0.85rem;
  align-items: center;
  min-height: 86px;
}

.signal-note-card strong {
  display: block;
  color: #102033;
  font-size: 0.86rem;
  margin-bottom: 0.2rem;
}

.signal-note-card span {
  display: block;
  color: #314258;
  font-size: 0.78rem;
  line-height: 1.4;
}

.signal-guide {
  padding: 1rem 1.15rem;
  margin-top: 0.85rem;
}

.signal-table-card {
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 10px 26px rgba(16,32,51,0.045);
  margin-top: 0.85rem;
  padding: 1rem 1.05rem;
}

.signal-table-card h3 {
  margin: 0 0 0.22rem 0;
  color: #102033;
  font-size: 1.08rem;
  font-weight: 880;
}

.signal-table-card p {
  margin: 0 0 0.75rem 0;
  color: #314258;
  font-size: 0.82rem;
}

.signal-table-wrap {
  overflow-x: auto;
  border: 1px solid #d8e3ea;
  border-radius: 8px;
}

.signal-candidates-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.78rem;
  color: #102033;
}

.signal-candidates-table th {
  background: #f8fafc;
  color: #45566b;
  font-size: 0.7rem;
  text-transform: none;
  font-weight: 850;
  padding: 0.72rem 0.7rem;
  border-bottom: 1px solid #d8e3ea;
  border-right: 1px solid #e6edf3;
  text-align: left;
}

.signal-candidates-table td {
  padding: 0.58rem 0.7rem;
  border-bottom: 1px solid #e6edf3;
  border-right: 1px solid #edf2f6;
  vertical-align: middle;
}

.signal-candidates-table tr:last-child td {
  border-bottom: 0;
}

.signal-candidates-table .num {
  text-align: center;
  color: #314258;
  width: 42px;
}

.signal-candidates-table .metric {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.signal-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 124px;
  border-radius: 7px;
  padding: 0.25rem 0.45rem;
  font-weight: 850;
  font-size: 0.72rem;
}

.signal-pill.red { color: #9f2f2a; background: #fde8e6; }
.signal-pill.amber { color: #a85d05; background: #fff0cf; }
.signal-pill.teal { color: #087a82; background: #dff4f6; }
.signal-pill.steel { color: #45566b; background: #e5f2f7; }
.signal-pill.purple { color: #7e3fa1; background: #f2e8f8; }

.signal-table-action {
  color: #164a63;
  font-weight: 900;
  text-decoration: none;
  font-size: 1rem;
}

.signal-actions-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 1rem;
  align-items: center;
  margin-top: 0.8rem;
}

.signal-actions-row span {
  color: #314258;
  font-size: 0.82rem;
}

.signal-guide-title {
  color: #102033;
  font-size: 1rem;
  font-weight: 880;
  margin-bottom: 0.85rem;
}

.signal-guide-flow {
  display: grid;
  grid-template-columns: 1fr 32px 1fr 32px 1fr 32px 1fr 42px 1fr;
  gap: 0.75rem;
  align-items: center;
}

.signal-guide-item {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  gap: 0.7rem;
  align-items: center;
}

.signal-guide-icon {
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background: #eef6fa;
  color: #2f6f9f;
}

.signal-guide-item strong {
  display: block;
  color: #102033;
  font-size: 0.78rem;
  margin-bottom: 0.15rem;
}

.signal-guide-item span {
  display: block;
  color: #314258;
  font-size: 0.7rem;
  line-height: 1.35;
}

.signal-guide-op {
  color: #2f6f9f;
  font-size: 1.4rem;
  font-weight: 900;
  text-align: center;
}

@media (max-width: 1150px) {
  .signal-header,
  .signal-top-band,
  .signal-guide-flow {
    grid-template-columns: 1fr;
  }
  .block-container:has(.signal-page) {
    max-width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
  .signal-kpi-band {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .signal-kpi {
    border-bottom: 1px solid #d8e3ea;
  }
}
</style>
""",
        unsafe_allow_html=True,
    )

    valid_months = panel["month"].dropna() if not panel.empty else []
    start_month = valid_months.min().strftime("%Y-%m") if len(valid_months) else "no disponible"
    end_month = valid_months.max().strftime("%Y-%m") if len(valid_months) else "no disponible"
    review_queue = int(df["due_diligence_priority"].isin(["Priority A", "Priority B"]).sum())
    monthly_followup = int((df["due_diligence_priority"] == "Watchlist").sum())
    median_stress = float(df["avg_icpi"].median())
    median_priority = float(df["avg_oanri"].median())

    st.markdown(
        f"""
<div class="signal-page">
  <div class="signal-header">
    <div>
      <div class="exec-kicker">Panel de soporte a decisiones</div>
      <h1>Mapa de Señales</h1>
      <p><strong>Pregunta de decisión:</strong> ¿Qué barras combinan estrés nodal relativo con prioridad operativa?</p>
    </div>
    <div class="signal-caveat">
      <div class="signal-caveat-icon">i</div>
      <div>
        <strong>Este mapa no prueba congestión física ni predice precios.</strong>
        <span>Muestra dónde están las señales que merecen atención experta.</span>
      </div>
    </div>
  </div>
  <div class="signal-top-band">
    <div class="signal-context-card">
      <div class="signal-map-icon">
        <svg viewBox="0 0 24 24"><path d="M9 18 3 21V6l6-3 6 3 6-3v15l-6 3-6-3Z"/><path d="M9 3v15M15 6v15"/></svg>
      </div>
      <div>
        <h3>Contexto del mapa</h3>
        <p>Cada punto es una barra del SEIN. Su posición combina estrés nodal promedio y prioridad operativa promedio. El color indica el nivel de revisión recomendado.</p>
        <small>Periodo: {escape(start_month)} a {escape(end_month)} · Universo mostrado: {df['barra'].nunique():,.0f} barras</small>
      </div>
    </div>
    <div class="signal-kpi-band">
      <div class="signal-kpi"><strong>{df['barra'].nunique():,.0f}</strong><span>Barras SEIN</span><em>muestra pública</em></div>
      <div class="signal-kpi"><strong>{review_queue:,.0f}</strong><span>En cola de revisión</span><em>{review_queue / max(len(df), 1):.0%} del universo</em></div>
      <div class="signal-kpi"><strong>{median_stress:,.1f}</strong><span>Mediana estrés nodal</span><em>línea vertical</em></div>
      <div class="signal-kpi"><strong>{median_priority:,.1f}</strong><span>Mediana prioridad operativa</span><em>línea horizontal</em></div>
      <div class="signal-kpi"><strong>{monthly_followup:,.0f}</strong><span>En seguimiento mensual</span><em>casos episódicos</em></div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    priority_label_map = {
        "Priority A": "Señal prioritaria",
        "Priority B": "Señal condicionada",
        "Watchlist": "Señal episódica",
        "Monitor": "Contexto base",
        "Low information": "Información por completar",
        "Baja informacion": "Información por completar",
        "Baja información": "Información por completar",
        "Prioridad A": "Señal prioritaria",
        "Prioridad B": "Señal condicionada",
        "Revisión inmediata": "Señal prioritaria",
        "Revisión selectiva": "Señal condicionada",
        "Seguimiento mensual": "Señal episódica",
        "Monitorear": "Contexto base",
        "Requiere contexto adicional": "Información por completar",
    }

    def public_priority_label(value: object) -> str:
        text = str(value) if pd.notna(value) else "Contexto base"
        return priority_label_map.get(text, text)

    if "due_diligence_priority_es" in df.columns:
        reset_priority_labels = (
            df["due_diligence_priority_es"]
            .dropna()
            .map(public_priority_label)
            .drop_duplicates()
            .tolist()
        )
    else:
        reset_priority_labels = (
            df["due_diligence_priority"]
            .dropna()
            .map(public_priority_label)
            .drop_duplicates()
            .tolist()
        )

    stability_display = {
        "Estabilidad alta": "Estable",
        "Robustez alta": "Estable",
        "High robustness": "Estable",
        "Baja dependencia": "Estable",
        "Estable": "Estable",
        "Estabilidad moderada": "Sensible",
        "Robustez moderada": "Sensible",
        "Moderate robustness": "Sensible",
        "Dependencia media": "Sensible",
        "Sensible": "Sensible",
        "Estabilidad baja": "Variable",
        "Robustez baja": "Variable",
        "Low robustness": "Variable",
        "Alta dependencia": "Variable",
        "Fuera de top-list de sensibilidad": "Variable",
        "Not covered by sensitivity top-list": "Variable",
        "Variable": "Variable",
    }
    stability_col_name = (
        "signal_stability_label_es"
        if "signal_stability_label_es" in df.columns
        else "robustness_flag_es"
        if "robustness_flag_es" in df.columns
        else "robustness_flag"
    )
    reset_stability_labels = (
        df[stability_col_name]
        .dropna()
        .astype(str)
        .map(lambda value: stability_display.get(value, value))
        .drop_duplicates()
        .tolist()
        if stability_col_name in df.columns
        else []
    )
    reset_tension_values = sorted(df["nivel_tension_kv"].dropna().unique()) if "nivel_tension_kv" in df.columns else []

    def reset_signal_filters() -> None:
        st.session_state["signal_priority"] = reset_priority_labels
        st.session_state["signal_stability"] = reset_stability_labels
        st.session_state["signal_tension"] = reset_tension_values

    st.markdown(
        """
<div class="signal-filter-card">
  <div class="signal-filter-title">
    <svg viewBox="0 0 24 24"><path d="M3 5h18l-7 8v5l-4 2v-7Z"/></svg>
    <strong>Filtros del mapa</strong>
  </div>
""",
        unsafe_allow_html=True,
    )
    filter_cols = st.columns([1.25, 1.25, 1.05, 0.72], gap="medium")
    with filter_cols[0]:
        selected_priorities = priority_filter(
            df,
            key="signal_priority",
            label="Tipo de señal",
            placeholder="Todas seleccionadas",
        )
    with filter_cols[1]:
        selected_robustness = robustness_filter(
            df,
            key="signal_stability",
            label="Estabilidad del resultado",
            placeholder="Todas seleccionadas",
            display_map=stability_display,
        )
    with filter_cols[2]:
        selected_tension = tension_filter(
            df,
            key="signal_tension",
            label="Tensión kV",
            placeholder="Todas",
        )
    with filter_cols[3]:
        st.write("")
        st.button("Limpiar filtros", key="signal_clear_filters", on_click=reset_signal_filters, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

    filtered = df.copy()
    if selected_priorities:
        filtered = filtered[filtered["due_diligence_priority"].isin(selected_priorities)]
    if selected_robustness:
        robustness_col = (
            "signal_stability_label_es"
            if "signal_stability_label_es" in filtered.columns
            else "robustness_flag_es"
            if "robustness_flag_es" in filtered.columns
            else "robustness_flag"
        )
        filtered = filtered[filtered[robustness_col].astype(str).isin(selected_robustness)]
    if selected_tension:
        filtered = filtered[filtered["nivel_tension_kv"].isin(selected_tension)]

    chart_col, read_col = st.columns([2.25, 0.95], gap="medium")
    with chart_col:
        st.markdown(
            """
<div class="signal-chart-shell">
  <div class="signal-chart-title">Mapa de señales: estrés nodal vs prioridad operativa</div>
""",
            unsafe_allow_html=True,
        )
        chart_slot = st.empty()
        st.markdown(
            """
  <div class="signal-chart-caption">El tamaño del punto refleja el score de revisión; el color marca el nivel de revisión recomendado.</div>
</div>
""",
            unsafe_allow_html=True,
        )
    with read_col:
        st.markdown(
            """
<div class="signal-side-card">
  <h3>Cómo leer el mapa</h3>
  <div class="signal-level-list">
    <div class="signal-level red"><div class="signal-card-icon"><svg viewBox="0 0 24 24"><path d="M5 21V4"/><path d="M5 5h11l-1.8 4L16 13H5"/></svg></div><div><strong>Señal prioritaria</strong><span>Candidata fuerte: alta prioridad operativa y alto estrés nodal.</span></div></div>
    <div class="signal-level amber"><div class="signal-card-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div><strong>Señal condicionada</strong><span>Relevante si sector, contrato, ubicación o escenario aumentan exposición.</span></div></div>
    <div class="signal-level teal"><div class="signal-card-icon"><svg viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg></div><div><strong>Señal episódica</strong><span>Tiene picos o meses relevantes; monitorear recurrencia o deterioro.</span></div></div>
    <div class="signal-level steel"><div class="signal-card-icon"><svg viewBox="0 0 24 24"><path d="M4 19V5"/><path d="M4 19h17"/><rect x="7" y="12" width="3" height="4"/><rect x="12" y="9" width="3" height="7"/><rect x="17" y="6" width="3" height="10"/></svg></div><div><strong>Contexto base</strong><span>Sirve como contexto del universo. No requiere revisión prioritaria.</span></div></div>
    <div class="signal-level purple"><div class="signal-card-icon"><svg viewBox="0 0 24 24"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/></svg></div><div><strong>Información por completar</strong><span>Falta contexto para interpretar fuerte. Completar evidencia antes de concluir.</span></div></div>
  </div>
</div>
<div class="signal-map-help">
  <strong>¿En qué se diferencia del Ranking de Prioridad?</strong>
  <p><b>Mapa de Señales:</b> muestra dónde se ubican las barras según estrés nodal y prioridad operativa.</p>
  <p><b>Ranking de Prioridad:</b> ordena las barras para decidir qué revisar primero.</p>
  <a href="?page=Ranking%20de%20Prioridad">→ Ir a Ranking de Prioridad</a>
</div>
""",
            unsafe_allow_html=True,
        )

    if filtered.empty:
        chart_slot.warning("Sin barras para los filtros activos. Amplía el tipo de señal, estabilidad del resultado o tensión.")
        candidate_rows = pd.DataFrame()
    else:
        chart_slot.plotly_chart(icpi_oanri_scatter(filtered), use_container_width=True)
        candidate_rows = (
            filtered.sort_values("decision_priority_score", ascending=False)
            .head(10)
            .reset_index(drop=True)
        )

    def level_class(label: str) -> str:
        return {
            "Revisión inmediata": "red",
            "Revisión selectiva": "amber",
            "Seguimiento mensual": "teal",
            "Señal prioritaria": "red",
            "Señal condicionada": "amber",
            "Señal episódica": "teal",
            "Contexto base": "steel",
            "Requiere contexto adicional": "purple",
            "Información por completar": "purple",
        }.get(label, "steel")

    def map_reading(row: pd.Series) -> str:
        high_stress = float(row.get("avg_icpi", 0)) >= median_stress
        high_priority = float(row.get("avg_oanri", 0)) >= median_priority
        label = public_priority_label(row.get("due_diligence_priority_es", row.get("due_diligence_priority", "")))
        if label == "Señal prioritaria":
            return "Alta prioridad y alto estrés"
        if high_priority and high_stress:
            return "Alta prioridad y alto estrés"
        if high_priority:
            return "Prioridad alta + estrés medio"
        if high_stress:
            return "Estrés alto + prioridad baja"
        return "Estrés medio + prioridad media"

    if candidate_rows.empty:
        table_rows = "<tr><td colspan='8'>Sin candidatos para los filtros activos.</td></tr>"
    else:
        rendered_rows = []
        for idx, row in candidate_rows.iterrows():
            label = public_priority_label(row.get("due_diligence_priority_es", row.get("due_diligence_priority", "")))
            rendered_rows.append(
                "<tr>"
                f"<td class='num'>{idx + 1}</td>"
                f"<td><strong>{escape(str(row['barra']))}</strong></td>"
                f"<td><span class='signal-pill {level_class(label)}'>{escape(label)}</span></td>"
                f"<td>{escape(map_reading(row))}</td>"
                f"<td class='metric'>{float(row['avg_icpi']):.2f}</td>"
                f"<td class='metric'>{float(row['avg_oanri']):.2f}</td>"
                f"<td class='metric'>{float(row['decision_priority_score']):.2f}</td>"
                "<td class='num'><a class='signal-table-action' href='?page=Caso%20de%20Estudio'>↗</a></td>"
                "</tr>"
            )
        table_rows = "\n".join(rendered_rows)

    shown_count = len(candidate_rows)
    filtered_count = len(filtered)
    st.markdown(
        f"""
<div class="signal-table-card">
  <h3>Candidatos principales del mapa</h3>
  <p>Barras destacadas según los filtros actuales. Para ver la cola completa, abre <strong>Ranking de Prioridad</strong>.</p>
  <div class="signal-table-wrap">
    <table class="signal-candidates-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Barra</th>
          <th>Tipo de señal</th>
          <th>Lectura en el mapa</th>
          <th>Estrés nodal prom.</th>
          <th>Prioridad operativa prom.</th>
          <th>Score de revisión</th>
          <th>Acción</th>
        </tr>
      </thead>
      <tbody>
        {table_rows}
      </tbody>
    </table>
  </div>
  <div class="signal-actions-row">
    <span>Mostrando 1 a {shown_count:,} de {filtered_count:,} barras en cola de revisión según filtros.</span>
    <a class="rank-next-button" href="?page=Ranking%20de%20Prioridad">Ver cola completa en Ranking de Prioridad →</a>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    note_cols = st.columns([2.55, 0.65], gap="medium")
    with note_cols[0]:
        st.markdown(
            """
<div class="signal-note-card">
  <div><svg viewBox="0 0 24 24"><path d="M12 3 5 6v5c0 4.5 2.9 8.5 7 10 4.1-1.5 7-5.5 7-10V6l-7-3Z"/><path d="m9 12 2 2 4-5"/></svg></div>
  <div>
    <strong>Notas metodológicas</strong>
    <span>Este mapa combina promedios mensuales de estrés nodal y prioridad operativa. Las señales se clasifican en niveles de revisión para orientar atención experta. No se usan para pruebas de causalidad ni predicción de congestión.</span>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
    with note_cols[1]:
        st.download_button(
            "Descargar lista filtrada",
            filtered.to_csv(index=False).encode("utf-8"),
            file_name="sein_signal_map_filtered.csv",
            mime="text/csv",
            width="stretch",
        )

    st.markdown(
        """
<div class="signal-guide">
  <div class="signal-guide-title">Guía rápida: cómo se combinan las señales</div>
  <div class="signal-guide-flow">
    <div class="signal-guide-item"><div class="signal-guide-icon"><svg viewBox="0 0 24 24"><path d="M4 19V5"/><path d="M4 19h17"/><path d="m7 15 4-4 3 3 5-7"/></svg></div><div><strong>Estrés nodal</strong><span>Indica dónde se concentra la tensión relativa en la red.</span></div></div>
    <div class="signal-guide-op">+</div>
    <div class="signal-guide-item"><div class="signal-guide-icon"><svg viewBox="0 0 24 24"><path d="M12 3 5 6v5c0 4.5 2.9 8.5 7 10 4.1-1.5 7-5.5 7-10V6l-7-3Z"/><path d="M9 13h6"/></svg></div><div><strong>Prioridad operativa</strong><span>Indica dónde el sistema resulta más relevante.</span></div></div>
    <div class="signal-guide-op">+</div>
    <div class="signal-guide-item"><div class="signal-guide-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div><div><strong>Estabilidad del resultado</strong><span>Indica si la barra sigue siendo relevante bajo criterios alternativos.</span></div></div>
    <div class="signal-guide-op">=</div>
    <div class="signal-guide-item"><div class="signal-guide-icon"><svg viewBox="0 0 24 24"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5"/></svg></div><div><strong>Tipo de señal</strong><span>Traduce los datos en lectura ejecutiva.</span></div></div>
    <div class="signal-guide-op">→</div>
    <div class="signal-guide-item"><div class="signal-guide-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="7" r="4"/><path d="M5 21a7 7 0 0 1 14 0"/></svg></div><div><strong>Acción experta</strong><span>La decisión final requiere análisis técnico y contractual.</span></div></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def classify_pattern(rows) -> str:
    if rows.empty:
        return "Patrón sin información suficiente para lectura temporal."
    priority_months = int((rows["decision_tier"] == "Priority due diligence").sum())
    watchlist_months = int((rows["decision_tier"] == "Watchlist").sum())
    total = max(len(rows), 1)
    if priority_months / total >= 0.35:
        return "Señal persistente: aparece de forma recurrente en meses de prioridad y merece seguimiento mensual estructurado."
    if priority_months + watchlist_months >= 4:
        return "Señal episódica recurrente: reaparece lo suficiente para mantenerla en seguimiento mensual."
    if priority_months > 0:
        return "Episodio puntual relevante: conviene revisar el mes específico y contrastarlo con contrato, demanda y contexto operativo."
    return "Señal baja o intermitente: útil como referencia de contexto dentro del universo analítico."


def _watch_col(data: pd.DataFrame, candidates: list[str]) -> str | None:
    return next((column for column in candidates if column in data.columns), None)


def _monthly_delta_labels(data: pd.DataFrame, value_col: str, threshold: float = 0.25) -> dict[str, str]:
    if data.empty or value_col not in data.columns or "month" not in data.columns:
        return {}
    work = data[["barra", "month", value_col]].dropna().copy()
    if work.empty:
        return {}
    work = work.sort_values(["barra", "month"])
    last_two = work.groupby("barra", group_keys=False).tail(2)
    labels: dict[str, str] = {}
    for barra, rows in last_two.groupby("barra"):
        if len(rows) < 2:
            labels[str(barra)] = "Sin comparación"
            continue
        values = pd.to_numeric(rows[value_col], errors="coerce").to_list()
        if len(values) < 2 or pd.isna(values[-1]) or pd.isna(values[-2]):
            labels[str(barra)] = "Sin comparación"
        elif values[-1] - values[-2] > threshold:
            labels[str(barra)] = "↑ Aumentó"
        elif values[-2] - values[-1] > threshold:
            labels[str(barra)] = "↓ Disminuyó"
        else:
            labels[str(barra)] = "→ Se mantuvo"
    return labels


def _monthly_delta_labels_for_month(data: pd.DataFrame, value_col: str, month: pd.Timestamp, threshold: float = 0.25) -> dict[str, str]:
    if data.empty or value_col not in data.columns or "month" not in data.columns:
        return {}
    selected_month = pd.Timestamp(month)
    previous_month = data.loc[data["month"] < selected_month, "month"].max()
    if pd.isna(previous_month):
        return {}
    current = data[data["month"] == selected_month].set_index("barra")[value_col]
    previous = data[data["month"] == previous_month].set_index("barra")[value_col]
    deltas = pd.to_numeric(current, errors="coerce") - pd.to_numeric(previous.reindex(current.index), errors="coerce")
    labels: dict[str, str] = {}
    for barra, value in deltas.dropna().items():
        if value > threshold:
            labels[str(barra)] = "↑ Aumentó"
        elif value < -threshold:
            labels[str(barra)] = "↓ Disminuyó"
        else:
            labels[str(barra)] = "→ Se mantuvo"
    return labels


def _watch_category_label(value: object) -> str:
    text = str(value).strip()
    return {
        "Priority due diligence": "Prioritaria",
        "Priority A": "Prioritaria",
        "Priority B": "Condicionada",
        "Watchlist": "En seguimiento",
        "Monitor": "Contexto base",
        "Lower relative exposure": "Contexto base",
        "Prioridad de revisión": "Prioritaria",
        "Seguimiento": "En seguimiento",
        "Monitorear": "Contexto base",
        "Menor exposición relativa": "Contexto base",
        "Señal prioritaria": "Prioritaria",
        "Señal condicionada": "Condicionada",
        "Señal episódica": "En seguimiento",
        "Contexto base": "Contexto base",
        "Información por completar": "Información por completar",
    }.get(text, text if text else "No clasificado")


def _render_watchlist_table(table_df: pd.DataFrame, full_df: pd.DataFrame) -> None:
    if table_df.empty:
        st.markdown(
            '<div class="watch-empty">No hay barras para los filtros activos. Prueba ampliar el tipo de señal o seleccionar otra barra.</div>',
            unsafe_allow_html=True,
        )
        return

    display = table_df.copy()
    rename = {
        "month_label": "Mes",
        "barra": "Barra",
        "stress": "Estrés nodal prom.",
        "priority": "Prioridad operativa prom.",
        "rank": "Ranking mensual",
        "reading": "Lectura recomendada",
        "stability": "Estabilidad del resultado",
        "driver": "Driver principal",
        "evolution": "Evolución vs. mes anterior",
    }
    display = display.rename(columns=rename)
    preferred_order = [
        "Mes",
        "Barra",
        "Ranking mensual",
        "Lectura recomendada",
        "Evolución vs. mes anterior",
        "Estabilidad del resultado",
        "Prioridad operativa prom.",
        "Estrés nodal prom.",
        "Driver principal",
    ]
    display = display[[column for column in preferred_order if column in display.columns]]
    for column in ["Estrés nodal prom.", "Prioridad operativa prom."]:
        if column in display.columns:
            display[column] = pd.to_numeric(display[column], errors="coerce").map(lambda value: f"{value:.2f}" if pd.notna(value) else "")

    def _style(row: pd.Series) -> list[str]:
        styles = [""] * len(row)
        for idx, column in enumerate(row.index):
            value = str(row[column])
            if column == "Lectura recomendada":
                if value == "Prioritaria":
                    styles[idx] = "background-color:#fde8e6;color:#9f2f2a;font-weight:800;border-radius:6px;"
                elif value == "Condicionada":
                    styles[idx] = "background-color:#fff0cf;color:#a85f00;font-weight:800;border-radius:6px;"
                elif value == "En seguimiento":
                    styles[idx] = "background-color:#dff4f6;color:#087a82;font-weight:800;border-radius:6px;"
            if column == "Estabilidad del resultado":
                if value == "Estable":
                    styles[idx] = "background-color:#e7f7ed;color:#147a44;font-weight:800;border-radius:6px;"
                elif value == "Sensible":
                    styles[idx] = "background-color:#fff0cf;color:#a85f00;font-weight:800;border-radius:6px;"
                elif value == "Variable":
                    styles[idx] = "background-color:#edf2f7;color:#526174;font-weight:800;border-radius:6px;"
        return styles

    st.dataframe(
        display.style.apply(_style, axis=1),
        use_container_width=True,
        hide_index=True,
        height=360,
        column_config={
            "Mes": st.column_config.TextColumn("Mes", width="small"),
            "Barra": st.column_config.TextColumn("Barra", width="medium"),
            "Lectura recomendada": st.column_config.TextColumn("Lectura recomendada", width="medium"),
            "Estabilidad del resultado": st.column_config.TextColumn("Estabilidad del resultado", width="medium"),
            "Evolución vs. mes anterior": st.column_config.TextColumn("Evolución vs. mes anterior", width="medium"),
        },
    )
    left, right = st.columns([1, 1])
    with left:
        st.caption(f"Mostrando {len(display):,.0f} filas del ranking mensual seleccionado.")
    with right:
        st.download_button(
            "Descargar tabla CSV",
            display.to_csv(index=False).encode("utf-8"),
            file_name="seguimiento_mensual_filtrado.csv",
            mime="text/csv",
            width="stretch",
        )


def render_watchlist() -> None:
    watchlist = load_watchlist()
    panel = load_monthly_panel()
    profiles = load_product_layer()
    if watchlist.empty:
        st.error("La capa de seguimiento mensual no está disponible.")
        st.stop()

    watchlist_priority_col = _watch_col(watchlist, ["Prioridad operativa", "OANRI_v10", "prioridad_operativa"])
    watchlist_stress_col = _watch_col(watchlist, ["Estrés nodal", "ICPI_v8", "estres_nodal"])
    if watchlist_priority_col is None or watchlist_stress_col is None:
        st.error("La vista mensual requiere columnas de estrés nodal y prioridad operativa.")
        st.stop()

    st.markdown(
        """
<style>
.block-container:has(.watch-page) {
  width: 100% !important;
  max-width: none !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  padding-left: 1.45rem !important;
  padding-right: 1.45rem !important;
}

.watch-page {
  width: 100%;
  margin: 0.15rem 0 0.65rem 0;
}

.watch-main-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(360px, 0.34fr);
  gap: 0.9rem;
  align-items: start;
  margin-top: 0.55rem;
}

.watch-line-shell {
  margin-top: 0.75rem;
}

.watch-side-card {
  margin-top: 0 !important;
  padding: 0.82rem !important;
}

.watch-side-card.note {
  margin-top: 0.65rem !important;
}

.watch-guide-row {
  margin-bottom: 0.45rem !important;
  padding: 0.58rem 0.65rem !important;
}

.watch-filter-row [data-testid="stSelectbox"],
.watch-filter-row [data-testid="stMultiSelect"] {
  margin-bottom: 0 !important;
}

.block-container:has(.watch-page) [data-testid="stPlotlyChart"] {
  padding: 0.45rem 0.55rem 0.05rem 0.55rem !important;
}

.block-container:has(.watch-page) [data-testid="stPlotlyChart"] > div {
  min-height: 0 !important;
}

@media (max-width: 1150px) {
  .block-container:has(.watch-page) {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
  .watch-main-grid {
    grid-template-columns: 1fr;
  }
}
</style>
<div class="watch-page"></div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="watch-header">
  <div>
    <div class="exec-kicker">PANEL DE SOPORTE A DECISIONES</div>
    <h1>Seguimiento Mensual</h1>
    <p>Pregunta de decisión: ¿Qué barras requieren seguimiento mensual por señales de corto y/o mediano plazo?</p>
  </div>
  <div class="watch-caveat">
    <div class="exec-icon exec-icon-info"></div>
    <div>
      <strong>En esta vista puedes monitorear la evolución mensual de las señales para entender si se mantienen, aumentan o disminuyen.</strong>
      <span>No predice precios ni prueba congestión física.</span>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    available_months = sorted(watchlist["month"].dropna().dt.strftime("%Y-%m").unique().tolist())
    default_month_idx = len(available_months) - 1 if available_months else 0
    st.markdown('<div class="watch-filter-row">', unsafe_allow_html=True)
    filter_cols = st.columns([1.65, 0.78, 0.78], gap="medium")
    with filter_cols[0]:
        selected_priorities = priority_filter(
            profiles,
            key="watchlist_priority",
            label="Tipo de señal",
            placeholder="Todas las categorías",
        )
    filtered_profiles = profiles[profiles["due_diligence_priority"].isin(selected_priorities)] if selected_priorities else profiles
    candidate_barras = filtered_profiles.sort_values("decision_priority_score", ascending=False)["barra"].dropna().astype(str).tolist()
    with filter_cols[1]:
        selected_label = st.selectbox(
            "Barra o ubicación en el mapa",
            ["Todas"] + candidate_barras,
            key="watchlist_barra_select",
        )
    with filter_cols[2]:
        selected_month_label = st.selectbox(
            "Mes de análisis",
            available_months,
            index=default_month_idx,
            key="watchlist_month_select",
        )
    st.markdown("</div>", unsafe_allow_html=True)
    selected_month = pd.to_datetime(f"{selected_month_label}-01", errors="coerce") if selected_month_label else watchlist["month"].max()

    top_n = 18
    ordered_barras = candidate_barras[:top_n]
    if selected_label != "Todas":
        ordered_barras = [selected_label] + [barra for barra in ordered_barras if barra != selected_label]
        ordered_barras = ordered_barras[:top_n]
    heatmap_data = watchlist[watchlist["barra"].isin(ordered_barras)]

    latest_month = selected_month if pd.notna(selected_month) else watchlist["month"].max()
    prev_month = watchlist.loc[watchlist["month"] < latest_month, "month"].max()
    filtered_watchlist = watchlist[watchlist["barra"].isin(candidate_barras)]
    latest_rows = filtered_watchlist[filtered_watchlist["month"] == latest_month].copy()
    prev_rows = filtered_watchlist[filtered_watchlist["month"] == prev_month].copy() if pd.notna(prev_month) else pd.DataFrame()
    latest_priority = latest_rows.set_index("barra")[watchlist_priority_col] if not latest_rows.empty else pd.Series(dtype=float)
    prev_priority = prev_rows.set_index("barra")[watchlist_priority_col] if not prev_rows.empty else pd.Series(dtype=float)
    deltas = (latest_priority - prev_priority.reindex(latest_priority.index)).dropna()
    up_count = int((deltas > 0.25).sum())
    down_count = int((deltas < -0.25).sum())
    active_barras = latest_rows.loc[
        pd.to_numeric(latest_rows.get("ranking_mensual_v10", pd.Series(index=latest_rows.index)), errors="coerce") <= 20,
        "barra",
    ].nunique() if not latest_rows.empty else 0
    month_top_count = int((pd.to_numeric(latest_rows.get("ranking_mensual_v10", pd.Series(dtype=float)), errors="coerce") <= 20).sum()) if not latest_rows.empty else 0

    st.markdown(
        f"""
<div class="watch-kpi-band">
  <div class="watch-kpi hot"><span>Barras observadas</span><strong>{len(filtered_profiles):,.0f}</strong><em>universo filtrado</em></div>
  <div class="watch-kpi"><span>Barras con señal activa</span><strong>{active_barras:,.0f}</strong><em>en el mes seleccionado</em></div>
  <div class="watch-kpi"><span>Aumentaron vs. mes previo</span><strong>{up_count:,.0f}</strong><em>señales en aumento</em></div>
  <div class="watch-kpi"><span>Disminuyeron vs. mes previo</span><strong>{down_count:,.0f}</strong><em>señales en disminución</em></div>
  <div class="watch-kpi warm"><span>Priorizadas este mes</span><strong>{month_top_count:,.0f}</strong><em>requieren revisión</em></div>
</div>
""",
        unsafe_allow_html=True,
    )

    selected_barra = selected_label if selected_label != "Todas" else (ordered_barras[0] if ordered_barras else None)
    st.markdown('<div class="watch-main-grid">', unsafe_allow_html=True)
    heatmap_col, side_col = st.columns([2.35, 0.82], gap="medium")
    with heatmap_col:
        st.markdown(
            '<div class="watch-block-title">Mapa de calor mensual de señales: prioridad operativa <span>Colores más cálidos indican mayor prioridad mensual. Filas repetidamente intensas sugieren persistencia; bloques aislados sugieren episodios puntuales.</span></div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(watchlist_heatmap(heatmap_data, order=ordered_barras), use_container_width=True)
    with side_col:
        st.markdown(
            """
<div class="watch-side-card">
  <h3>Cómo leer esta vista</h3>
  <div class="watch-guide-row red"><span>▦</span><div><strong>Mapa de calor</strong><p>Prioridad operativa por barra y mes. Rojo = mayor prioridad relativa.</p></div></div>
  <div class="watch-guide-row blue"><span>↗</span><div><strong>Evolución mensual</strong><p>Compara estrés nodal relativo y prioridad operativa en el tiempo.</p></div></div>
  <div class="watch-guide-row teal"><span>☷</span><div><strong>Top mensual</strong><p>Barras con mayor prioridad según métricas combinadas del mes.</p></div></div>
  <div class="watch-guide-row green"><span>◇</span><div><strong>Estabilidad del resultado</strong><p>Indica persistencia de la señal bajo criterios alternativos.</p></div></div>
</div>
""",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    if selected_barra and not panel.empty:
        st.markdown('<div class="watch-line-shell">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="watch-block-title">Evolución mensual de señal - {escape(str(selected_barra))}<span>Compara estrés nodal relativo y prioridad operativa en el tiempo para distinguir persistencia, deterioro o episodios puntuales.</span></div>',
            unsafe_allow_html=True,
        )
        selected_rows = panel[panel["barra"] == selected_barra].sort_values("month")
        st.plotly_chart(barra_month_line(panel, selected_barra), use_container_width=True)
        st.markdown(
            f'<div class="watch-pattern">{escape(classify_pattern(selected_rows))}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f'<div class="watch-section-title">Top mensual de señales — {escape(str(selected_month_label))}</div>', unsafe_allow_html=True)
    stability_by_barra = (
        profiles.set_index("barra")["signal_stability_label_es"].to_dict()
        if "signal_stability_label_es" in profiles.columns
        else {}
    )
    evolution_by_barra = _monthly_delta_labels_for_month(filtered_watchlist, watchlist_priority_col, latest_month)
    top_month = (
        latest_rows.sort_values("ranking_mensual_v10", ascending=True).head(10)
        if "ranking_mensual_v10" in latest_rows.columns
        else latest_rows.sort_values(watchlist_priority_col, ascending=False).head(10)
    ).copy()
    table_df = pd.DataFrame(
        {
            "month_label": top_month["month"].dt.strftime("%Y-%m") if "month" in top_month else "",
            "barra": top_month["barra"],
            "stress": pd.to_numeric(top_month[watchlist_stress_col], errors="coerce"),
            "priority": pd.to_numeric(top_month[watchlist_priority_col], errors="coerce"),
            "rank": pd.to_numeric(top_month.get("ranking_mensual_v10", pd.Series(index=top_month.index)), errors="coerce").astype("Int64"),
            "reading": top_month.get("prioridad_barra", top_month.get("decision_tier", pd.Series(index=top_month.index))).map(_watch_category_label),
            "stability": top_month["barra"].map(stability_by_barra).fillna("No clasificado"),
            "driver": top_month.get("primary_driver", pd.Series(index=top_month.index)).fillna("Nivel de precio"),
            "evolution": top_month["barra"].map(evolution_by_barra).fillna("Sin comparación"),
        }
    )
    _render_watchlist_table(table_df, filtered_watchlist)

    st.markdown(
        """
<div class="watch-method-note">
  <strong>Notas metodológicas</strong>
  <span>Esta página combina promedios mensuales de estrés nodal y prioridad operativa. La estabilidad del resultado ayuda a distinguir señales que se mantienen bajo criterios alternativos. No se usa para causalidad, predicción de congestión ni cálculo de facturas.</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_exposicion() -> None:
    sector_df = load_sector_profiles()
    contract_df = load_contract_scenarios()
    if sector_df.empty:
        st.error("Los perfiles sector-barra no están disponibles.")
        st.stop()

    st.markdown(
        """
<style>
.block-container:has(.exposure-page) {
  width: 100% !important;
  max-width: none !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  padding-left: 1.45rem !important;
  padding-right: 1.45rem !important;
}

.exposure-page { width: 100%; margin: 0.15rem 0 0.65rem 0; }

.exposure-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(350px, 0.36fr);
  gap: 1.2rem;
  align-items: start;
  margin: 0.35rem 0 0.85rem 0;
}

.exposure-header h1 {
  color: #102033;
  font-size: clamp(2.15rem, 3.9vw, 3.15rem);
  line-height: 1;
  margin: 0.2rem 0 0 0;
  font-weight: 880;
}

.exposure-caveat {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr);
  gap: 0.85rem;
  align-items: center;
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  background: rgba(255,255,255,0.90);
  padding: 0.95rem 1rem;
  box-shadow: 0 10px 26px rgba(16,32,51,0.045);
}

.exposure-caveat strong,
.exposure-caveat span {
  display: block;
  color: #102033;
  font-size: 0.82rem;
  line-height: 1.38;
}

.exposure-caveat span {
  color: #314258;
  margin-top: 0.18rem;
  font-weight: 720;
}

.exposure-section-label {
  color: #102033;
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin: 0.8rem 0 0.4rem 0;
}

.exposure-card {
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  background: #ffffff;
  padding: 0.85rem 0.95rem;
  box-shadow: 0 8px 22px rgba(16,32,51,0.035);
}

.exposure-filter-card [data-testid="stSelectbox"] { margin-bottom: 0 !important; }

.exposure-selected {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: 1px solid #cfe2ec;
  border-radius: 8px;
  background: #f8fcfd;
  color: #26384d;
  font-size: 0.82rem;
  font-weight: 720;
  padding: 0.62rem 0.75rem;
  margin-top: 0.7rem;
}

.exposure-selected b { color: #102033; }
.exposure-selected span:first-child { color: #1f8a5b; font-weight: 950; }

.exposure-kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
}

.exposure-kpi {
  min-height: 112px;
  display: grid;
  grid-template-columns: 58px minmax(0, 1fr);
  gap: 0.82rem;
  align-items: center;
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  background: #ffffff;
  padding: 0.95rem 1rem;
  box-shadow: 0 8px 22px rgba(16,32,51,0.035);
}

.exposure-kpi.hot { background: linear-gradient(180deg, #fff8ef 0%, #ffffff 100%); }
.exposure-kpi.soft { background: linear-gradient(180deg, #f7fcfd 0%, #ffffff 100%); }

.exposure-kpi-icon {
  width: 46px;
  height: 46px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  color: #087a82;
  background: #e6f7f8;
  font-size: 1.35rem;
  font-weight: 900;
}

.exposure-kpi.hot .exposure-kpi-icon { color: #c47a16; background: #fff0cf; }
.exposure-kpi.risk .exposure-kpi-icon { color: #b23a2e; background: #fde8e6; }
.exposure-kpi.good .exposure-kpi-icon { color: #1f8a5b; background: #e7f7ed; }
.exposure-kpi.purple .exposure-kpi-icon { color: #6d4aa2; background: #f0e9f8; }

.exposure-kpi span {
  display: block;
  color: #526174;
  font-size: 0.70rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 850;
}

.exposure-kpi strong {
  display: block;
  color: #102033;
  font-size: 1.85rem;
  line-height: 1;
  font-weight: 880;
  margin-top: 0.4rem;
}

.exposure-kpi em {
  display: block;
  color: #314258;
  font-style: normal;
  font-size: 0.78rem;
  margin-top: 0.38rem;
}

.exposure-insight-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.8rem;
}

.exposure-insight {
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  background: #ffffff;
  padding: 0.95rem 1rem;
  min-height: 132px;
  box-shadow: 0 8px 22px rgba(16,32,51,0.035);
}

.exposure-insight strong {
  display: block;
  color: #102033;
  font-size: 0.86rem;
  margin-bottom: 0.42rem;
}

.exposure-insight p {
  color: #314258;
  font-size: 0.80rem;
  line-height: 1.45;
  margin: 0;
}

.exposure-insight .dot {
  width: 30px;
  height: 30px;
  border-radius: 999px;
  display: inline-grid;
  place-items: center;
  margin-right: 0.4rem;
  color: white;
  background: #164a63;
  font-weight: 900;
}

.exposure-chart-title,
.exposure-table-title {
  color: #102033;
  font-size: 0.96rem;
  font-weight: 900;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  margin: 0.9rem 0 0.32rem 0;
}

.exposure-chart-title span,
.exposure-table-title span {
  display: block;
  color: #526174;
  font-size: 0.76rem;
  font-weight: 620;
  letter-spacing: 0;
  text-transform: none;
  margin-top: 0.22rem;
}

.exposure-bottom-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(360px, 0.92fr);
  gap: 0.9rem;
  align-items: stretch;
  margin-top: 0.85rem;
}

.exposure-reading-card {
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  background: #ffffff;
  padding: 0.95rem 1rem;
  box-shadow: 0 8px 22px rgba(16,32,51,0.035);
  margin-bottom: 0.75rem;
}

.exposure-reading-card h3 {
  color: #102033;
  font-size: 1rem;
  margin: 0 0 0.5rem 0;
}

.exposure-reading-card p,
.exposure-reading-card li {
  color: #314258;
  font-size: 0.80rem;
  line-height: 1.45;
}

.exposure-reading-card ul {
  margin: 0.25rem 0 0 0;
  padding-left: 1rem;
}

.exposure-notes {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.7rem 1.2rem;
  border: 1px solid #d8e3ea;
  border-radius: 8px;
  background: #ffffff;
  color: #314258;
  font-size: 0.78rem;
  line-height: 1.42;
  padding: 0.9rem 1rem;
  margin-top: 0.55rem;
}

.exposure-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.65rem;
  align-items: center;
  margin-top: 0.85rem;
}

.exposure-rank-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 0 1.05rem;
  border-radius: 8px;
  background: #164a63;
  color: #ffffff !important;
  text-decoration: none !important;
  font-weight: 850;
  font-size: 0.86rem;
}

.block-container:has(.exposure-page) [data-testid="stPlotlyChart"] {
  padding: 0.50rem 0.62rem 0.08rem 0.62rem !important;
}

@media (max-width: 1150px) {
  .block-container:has(.exposure-page) {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
  .exposure-header,
  .exposure-bottom-grid {
    grid-template-columns: 1fr;
  }
  .exposure-kpi-grid,
  .exposure-insight-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
<div class="exposure-page"></div>
""",
        unsafe_allow_html=True,
    )

    sectors = sorted(sector_df["sector"].dropna().unique()) if "sector" in sector_df else []
    contracts = sorted(sector_df["contract_type"].dropna().unique()) if "contract_type" in sector_df else []
    sector_label_to_value = {SECTOR_LABELS.get(value, value): value for value in sectors}
    contract_label_to_value = {CONTRACT_LABELS.get(value, value): value for value in contracts}

    st.markdown(
        """
<div class="exposure-header">
  <div>
    <div class="exec-kicker">PANEL DE SOPORTE A DECISIONES</div>
    <h1>Exposición Industrial</h1>
  </div>
  <div class="exposure-caveat">
    <div class="exec-icon exec-icon-info" aria-hidden="true"></div>
    <div>
      <strong>Esta vista no predice precios ni congestión física.</strong>
      <span>Mide exposición industrial relativa para priorizar revisión y negociación contractual.</span>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="exposure-section-label">1. Configuración del escenario</div>', unsafe_allow_html=True)
    st.markdown('<div class="exposure-card exposure-filter-card">', unsafe_allow_html=True)
    selector_cols = st.columns(2, gap="medium")
    with selector_cols[0]:
        selected_sector_label = st.selectbox(
            "Arquetipo industrial",
            list(sector_label_to_value.keys()),
            key="exposure_sector",
        )
    with selector_cols[1]:
        selected_contract_label = st.selectbox(
            "Arquetipo contractual",
            list(contract_label_to_value.keys()),
            key="exposure_contract",
        )
    sector = sector_label_to_value[selected_sector_label]
    contract = contract_label_to_value[selected_contract_label]
    st.markdown(
        f"""
<div class="exposure-selected"><span>✓</span><div>Escenario seleccionado: <b>{escape(selected_sector_label)}</b> <span>|</span> <b>{escape(selected_contract_label)}</b></div></div>
</div>
""",
        unsafe_allow_html=True,
    )

    filtered = sector_df.copy()
    if sector:
        filtered = filtered[filtered["sector"] == sector]
    if contract:
        filtered = filtered[filtered["contract_type"] == contract]
    scenario_score_col = "avg_industrial_exposure_score"
    filtered = filtered.sort_values(scenario_score_col, ascending=False)
    sector_label = SECTOR_LABELS.get(sector, sector) if sector else "Todos los sectores"
    contract_label = CONTRACT_LABELS.get(contract, contract) if contract else "Todos los contratos"

    leader = filtered.iloc[0] if not filtered.empty else None
    stable_pct = (
        filtered["signal_stability_label_es"].astype(str).str.strip().eq("Estable").mean() * 100
        if "signal_stability_label_es" in filtered and not filtered.empty
        else 0
    )
    score_series = pd.to_numeric(filtered[scenario_score_col], errors="coerce") if not filtered.empty else pd.Series(dtype=float)
    avg_exposure = score_series.mean() if not score_series.empty else 0
    p90_exposure = score_series.quantile(0.90) if not score_series.empty else 0
    avg_priority_months = filtered["priority_months"].mean() if "priority_months" in filtered and not filtered.empty else 0
    combo_count = (
        filtered[["sector", "contract_type", "barra"]].drop_duplicates().shape[0]
        if {"sector", "contract_type", "barra"}.issubset(filtered.columns)
        else len(filtered)
    )
    leader_text = (
        f"Bajo {sector_label} y {contract_label}, {leader['barra']} lidera el escenario con score de exposición {leader[scenario_score_col]:.1f}."
        if leader is not None
        else "No hay combinaciones para el filtro activo."
    )

    st.markdown('<div class="exposure-section-label">2. Resumen del escenario</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="exposure-kpi-grid">
  <div class="exposure-kpi soft"><div class="exposure-kpi-icon">▥</div><div><span>Combinaciones evaluadas</span><strong>{combo_count:,.0f}</strong><em>sector-contrato-barra</em></div></div>
  <div class="exposure-kpi soft"><div class="exposure-kpi-icon">⌖</div><div><span>Barras candidatas</span><strong>{filtered['barra'].nunique():,.0f}</strong><em>candidatas</em></div></div>
  <div class="exposure-kpi hot"><div class="exposure-kpi-icon">↗</div><div><span>Exposición promedio del escenario</span><strong>{avg_exposure:.1f}</strong><em>exposición media</em></div></div>
  <div class="exposure-kpi risk"><div class="exposure-kpi-icon">◎</div><div><span>Cola alta del escenario (P90)</span><strong>{p90_exposure:.1f}</strong><em>cola del escenario</em></div></div>
  <div class="exposure-kpi purple"><div class="exposure-kpi-icon">▦</div><div><span>Meses revisión inmediata prom.</span><strong>{avg_priority_months:.1f}</strong><em>meses</em></div></div>
  <div class="exposure-kpi good"><div class="exposure-kpi-icon">◇</div><div><span>Perfiles estables</span><strong>{stable_pct:.0f}%</strong><em>resultados estables</em></div></div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="exposure-section-label">3. Insights del escenario</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="exposure-insight-grid">
  <div class="exposure-insight"><strong><span class="dot">?</span>Pregunta de decisión</strong><p>¿Qué combinaciones sector-barra deben revisarse primero bajo supuestos explícitos de exposición?</p></div>
  <div class="exposure-insight"><strong><span class="dot">↗</span>Hallazgo del escenario</strong><p>{escape(leader_text)}</p></div>
  <div class="exposure-insight"><strong><span class="dot">✓</span>Acción recomendada</strong><p>Revisar covenants contractuales, participación spot, demanda mensual y sensibilidad operativa del sector seleccionado.</p></div>
  <div class="exposure-insight"><strong><span class="dot">!</span>Caveat metodológico</strong><p>Los escenarios son salidas de screening basadas en supuestos; no forecast de factura ni valoración financiera.</p></div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="exposure-chart-title">4. Barras con mayor exposición bajo el escenario seleccionado'
        '<span>Un mayor score indica mayor prioridad relativa de revisión bajo el escenario seleccionado, no mayor monto real de factura.</span></div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(sector_exposure_bar_chart(filtered), use_container_width=True)

    st.markdown('<div class="exposure-table-title">5. Top combinaciones candidatas</div>', unsafe_allow_html=True)
    top_table = filtered.head(10).copy()
    table = pd.DataFrame(
        {
            "Barra": top_table["barra"],
            "Score exposición prom.": top_table["avg_industrial_exposure_score"].round(2),
            "Score exposición p90": top_table["p90_industrial_exposure_score"].round(2),
            "Meses revisión inmediata": top_table["priority_months"].astype("Int64"),
            "Meses seguimiento": top_table["watchlist_months"].astype("Int64"),
            "Estabilidad del resultado": top_table["signal_stability_label_es"].fillna("No clasificado"),
        }
    )
    st.dataframe(
        table,
        hide_index=True,
        use_container_width=True,
        height=315,
        column_config={
            "Score exposición prom.": st.column_config.NumberColumn(format="%.2f"),
            "Score exposición p90": st.column_config.NumberColumn(format="%.2f"),
        },
    )

    st.markdown('<div class="exposure-section-label">6. Sensibilidad y lectura del escenario</div>', unsafe_allow_html=True)
    bottom_left, bottom_right = st.columns([1.05, 0.95], gap="medium")
    with bottom_left:
        st.markdown(
            '<div class="exposure-chart-title" style="margin-top:0;">Sensibilidad por tipo de contrato'
            '<span>Exposición promedio por arquetipo contractual bajo el escenario seleccionado.</span></div>',
            unsafe_allow_html=True,
        )
        if not contract_df.empty:
            selected_contract_df = contract_df[contract_df["sector"] == sector] if sector else contract_df
            st.plotly_chart(contract_comparison_chart(selected_contract_df), use_container_width=True)
    with bottom_right:
        st.markdown(
            f"""
<div class="exposure-reading-card">
  <h3>Lectura del escenario</h3>
  <p>Una combinación con mayor score merece más atención porque reúne señal nodal, prioridad mensual, participación spot, consumo y supuestos sectoriales. Es un screening bajo supuestos explícitos: no debe interpretarse como forecast de factura ni valoración financiera.</p>
</div>
<div class="exposure-reading-card">
  <h3>Acciones sugeridas</h3>
  <ul>
    <li>Priorizar revisión de contratos en los perfiles con mayor exposición.</li>
    <li>Evaluar alternativas de mezcla spot y PPA como supuestos de exposición, no como recomendación automática.</li>
    <li>Completar lectura de meses de revisión inmediata y perfiles sensibles.</li>
    <li>Monitorear resultados si cambian los supuestos del escenario.</li>
  </ul>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="exposure-section-label">7. Notas importantes</div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="exposure-notes">
  <div>Los scores son relativos dentro del universo filtrado.</div>
  <div>Sirven para priorizar revisión contractual y gestión de flexibilidad.</div>
  <div>No predice precios futuros ni congestión física.</div>
  <div>Basado en supuestos explícitos definidos para el escenario.</div>
</div>
""",
        unsafe_allow_html=True,
    )

    action_cols = st.columns([1, 1, 1.2])
    download_df = pd.DataFrame()
    if not filtered.empty:
        download_df = pd.DataFrame(
            {
                "Sector industrial": filtered["sector"].map(lambda value: SECTOR_LABELS.get(value, value)),
                "Arquetipo contractual": filtered["contract_type"].map(lambda value: CONTRACT_LABELS.get(value, value)),
                "Barra": filtered["barra"],
                "Score exposición prom.": pd.to_numeric(filtered["avg_industrial_exposure_score"], errors="coerce").round(2),
                "Score exposición p90": pd.to_numeric(filtered["p90_industrial_exposure_score"], errors="coerce").round(2),
                "Meses revisión inmediata": pd.to_numeric(filtered["priority_months"], errors="coerce").fillna(0).astype(int),
                "Meses seguimiento": pd.to_numeric(filtered["watchlist_months"], errors="coerce").fillna(0).astype(int),
                "Estabilidad del resultado": filtered["signal_stability_label_es"].fillna("No clasificado"),
                "Participación spot asumida": pd.to_numeric(filtered["spot_share"], errors="coerce").round(2),
                "Consumo mensual supuesto MWh": pd.to_numeric(filtered["monthly_mwh"], errors="coerce").round(0).astype("Int64"),
                "Driver principal": filtered["dominant_driver"].fillna("No clasificado"),
            }
        )
    with action_cols[1]:
        st.download_button(
            "Descargar tabla CSV",
            download_df.to_csv(index=False).encode("utf-8"),
            file_name="industrial_exposure_filtered.csv",
            mime="text/csv",
            width="stretch",
        )
    with action_cols[2]:
        st.markdown('<a class="exposure-rank-link" href="?page=Ranking%20de%20Prioridad">Ver Ranking de Prioridad →</a>', unsafe_allow_html=True)


def render_caso() -> None:
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

    def _clean(value: object, fallback: str = "No disponible en la capa producto") -> str:
        text = "" if value is None else str(value).strip()
        if not text or text.lower() in {"nan", "none", "nat"}:
            return fallback
        return humanize_analytical_text(text)

    cols = st.columns(5)
    with cols[0]:
        metric_card("Categoría", priority_label, "decisión sugerida", kind="warning")
    with cols[1]:
        metric_card("Score", f"{row['decision_priority_score']:.1f}", "0-100 relativo", kind="warning")
    with cols[2]:
        metric_card("Rank estrés", f"{row['rank_icpi']:.0f}", "1 = mayor señal", kind="info")
    with cols[3]:
        metric_card("Rank prioridad", f"{row['rank_oanri']:.0f}", "1 = mayor prioridad", kind="info")
    with cols[4]:
        metric_card("Soporte", row["evidence_grade"], "contexto revisado", kind="good")

    decision_summary_card(
        priority_label,
        f"{row['decision_priority_score']:.1f}/100",
        row["priority_reason"],
        row["recommended_action"],
        (
            f"Soporte de contexto {row['evidence_grade']}; "
            f"{humanize_analytical_text(row.get('signal_stability_label_es', row.get('robustness_flag_es', row['robustness_flag'])))}; "
            f"{humanize_analytical_text(row.get('score_coverage_class_es', 'cobertura analítica no clasificada'))}."
        ),
    )
    section_header("Contexto actual de la barra")
    price_window = f"{_clean(row.get('coes_price_key_first_month'), 'sin inicio')} a {_clean(row.get('coes_price_key_last_month'), 'sin fin')}"
    insight_grid(
        [
            ("Activo o conexión relevante", _clean(row.get("topology_context_asset"), row["barra"]), "decision"),
            ("Tipo de contexto", f"{_clean(row.get('topology_context_type_es'))}. Rol: {_clean(row.get('evidence_family_es'))}.", "evidence"),
            (
                "Cobertura analítica",
                "Periodo fuente: "
                f"{price_window}; meses efectivos de score: {_clean(row.get('score_months_observed'), '0')}; "
                f"meses de fuente COES: {_clean(row.get('source_months_observed', row.get('coes_price_key_months_observed')), '0')}.",
                "action",
            ),
            ("Límite de lectura", _clean(row.get("decision_claim_boundary")), "caveat"),
        ]
    )
    action_panel("Por qué este contexto importa", _clean(row.get("topology_context_summary")))
    section_header("Componentes de la señal", "Scores en escala relativa 0-100. Valores más altos indican mayor intensidad dentro del universo analizado.")
    left, right = st.columns(2)
    with left:
        st.plotly_chart(barra_profile_score_bars(row), use_container_width=True)
    with right:
        if not panel.empty:
            st.plotly_chart(barra_component_profile(panel, barra), use_container_width=True)
    section_header("Evolución mensual")
    if not panel.empty:
        st.plotly_chart(barra_month_line(panel, barra), use_container_width=True)
    section_header("Due-diligence checklist")
    c1, c2 = st.columns(2)
    with c1:
        action_panel("Validaciones analíticas", "1. Confirmar si la señal es persistente o episódica. 2. Revisar meses con mayor prioridad operativa. 3. Comparar ranking de estrés nodal y prioridad operativa. 4. Verificar estabilidad del resultado, episodios y evidencia.")
    with c2:
        action_panel("Preguntas de negocio", "1. ¿Existe demanda industrial cercana? 2. ¿La exposición es spot, indexada o cubierta? 3. ¿La evidencia topológica soporta revisión adicional? 4. ¿Hay indicadores de confiabilidad relevantes?")


product_sidebar()
PAGES = {
    "Inicio": render_inicio,
    "Resumen Ejecutivo": render_resumen,
    "Ranking de Prioridad": render_ranking,
    "Mapa de Señales": render_icpi_oanri,
    "Seguimiento Mensual": render_watchlist,
    "Exposición Industrial": render_exposicion,
    "Caso de Estudio": render_caso,
}
page_names = list(PAGES.keys())
query_page = st.query_params.get("page", "Inicio")
default_page_index = page_names.index(query_page) if query_page in PAGES else 0
selected_page = st.sidebar.radio("Página", page_names, index=default_page_index, label_visibility="collapsed")
product_sidebar_footer()
PAGES[selected_page]()
