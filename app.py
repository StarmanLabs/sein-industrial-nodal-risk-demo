from __future__ import annotations

from html import escape

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
    load_simulator_sample,
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
            ("Revisión inmediata", "Primera cola de due diligence: señal alta, recurrencia y soporte suficiente.", "decision"),
            ("Revisión selectiva", "Candidata relevante; gana prioridad si el sector, contrato o ubicación aumentan exposición.", "evidence"),
            ("Seguimiento mensual", "Caso episódico o sensible a escenarios; se vigila por persistencia y cambios recientes.", "action"),
            ("Contexto base", "Permanece en el universo analítico para comparación, referencia y nuevos eventos.", "caveat"),
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
            ("Ordenar prioridad", "Combina estrés nodal, régimen operativo, robustez y evidencia contextual para priorizar revisión."),
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
    {_kpi_item(priority_a_count, "Revisión inmediata", "Señal alta, recurrencia y soporte suficiente.", "urgent", "warning")}
    {_kpi_item(priority_b_count, "Revisión selectiva", "Prioridad si sector, contrato o ubicación aumentan exposición.", "selective", "target")}
    {_kpi_item(watchlist_count, "Seguimiento mensual", "Caso episódico o sensible; se vigila por persistencia.", "watch", "eye")}
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

    st.html(
        """
<div class="rank-page">
  <div class="rank-header">
    <div>
      <div class="exec-kicker">Panel de soporte a decisiones</div>
      <h1>Ranking de Prioridad por Barra</h1>
      <p><strong>Pregunta de decisión:</strong> ¿Qué barras deberían revisarse primero?</p>
    </div>
    <div class="rank-caveat">
      <span class="exec-icon exec-icon-shield" aria-hidden="true"></span>
      <div>
        <strong>Mayor posición = mayor prioridad de revisión.</strong>
        <span>No significa que la barra sea “mala”. No prueba congestión física ni predice precios.</span>
      </div>
    </div>
  </div>
</div>
"""
    )
    summary_slot = st.empty()

    filter_top = st.columns([0.8, 1.25, 1.15, 1.1, 1])
    with filter_top[0]:
        st.html(
            """
<div class="rank-filter-title">
  <span class="exec-icon exec-icon-filter" aria-hidden="true"></span>
  <strong>Filtros de revisión</strong>
</div>
"""
        )
    with filter_top[4]:
        reset_filters = st.button("Limpiar filtros", key="ranking_clear_filters", use_container_width=True)
    if reset_filters:
        st.session_state["ranking_priority"] = []
        st.session_state["ranking_robustness"] = []
        st.session_state["ranking_tension"] = []

    filter_cols = st.columns([1.25, 1.05, 1.05])
    with filter_cols[0]:
        selected_priorities = priority_filter(df, key="ranking_priority")
    with filter_cols[1]:
        selected_robustness = robustness_filter(df, key="ranking_robustness")
    with filter_cols[2]:
        selected_tension = tension_filter(df, key="ranking_tension")

    filtered = df.copy()
    if selected_priorities:
        filtered = filtered[filtered["due_diligence_priority"].isin(selected_priorities)]
    if selected_robustness:
        robustness_col = "robustness_flag_es" if "robustness_flag_es" in filtered.columns else "robustness_flag"
        filtered = filtered[filtered[robustness_col].astype(str).isin(selected_robustness)]
    if selected_tension:
        filtered = filtered[filtered["nivel_tension_kv"].isin(selected_tension)]
    filtered = filtered.sort_values("decision_priority_score", ascending=False)

    def _count_priority(value: str) -> int:
        return int((filtered["due_diligence_priority"] == value).sum()) if not filtered.empty else 0

    robust_col = "robustness_flag_es" if "robustness_flag_es" in filtered.columns else "robustness_flag"
    robust_high = int(filtered[robust_col].astype(str).str.contains("alta|high", case=False, na=False).sum()) if robust_col in filtered else 0
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
        st.html(
            f"""
<div class="rank-summary-card">
  <div class="rank-summary-left">
    <div class="rank-summary-icon"><span class="exec-icon exec-icon-target" aria-hidden="true"></span></div>
    <div class="rank-summary-kpis">
      <div class="rank-summary-title">Con los filtros actuales:</div>
      <div class="rank-kpi"><strong>{len(filtered):,.0f}</strong><span>barras visibles</span></div>
      <div class="rank-kpi"><strong>{queue_count:,.0f}</strong><span>en cola principal<br>(inmediata / selectiva)</span></div>
      <div class="rank-kpi"><strong>{watch_count:,.0f}</strong><span>en seguimiento mensual<br>(casos episódicos)</span></div>
      <div class="rank-kpi"><strong>{robust_high:,.0f}</strong><span>señales con<br>robustez alta</span></div>
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
    <div><strong>Siguiente paso recomendado:</strong><p>{escape(next_action)}</p></div>
  </div>
</div>
"""
        )

    st.html(
        """
<div class="rank-taxonomy">
  <div class="rank-tax-item red"><strong>Revisión inmediata</strong><span>Primera cola de due diligence. Combina señal alta, recurrencia, robustez y soporte de contexto.</span></div>
  <div class="rank-tax-item amber"><strong>Revisión selectiva</strong><span>Candidata relevante. Gana prioridad cuando sector, contrato, ubicación o contexto industrial aumentan exposición.</span></div>
  <div class="rank-tax-item teal"><strong>Seguimiento mensual</strong><span>Caso episódico o sensible. Se vigila para distinguir persistencia, deterioro reciente o eventos puntuales.</span></div>
  <div class="rank-tax-item steel"><strong>Contexto base</strong><span>Permanece como referencia del universo o necesita mejor contexto antes de una lectura fuerte.</span></div>
  <div class="rank-tax-item purple"><strong>Requiere contexto adicional</strong><span>No exige revisión inmediata; completar evidencia antes de interpretar.</span></div>
</div>
"""
    )

    st.html("<h2 class='rank-section-title'>Cola priorizada de revisión</h2>")
    if filtered.empty:
        action_panel("Sin resultados para los filtros activos", "Amplía prioridad, evidencia, robustez o tensión para recuperar barras candidatas.")
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
            "Priority A": "Abrir revisión estructurada",
            "Priority B": "Revisar después de inmediata",
            "Watchlist": "Monitorear recurrencia",
            "Monitor": "Mantener como referencia",
            "Low information": "Completar contexto",
        }
        reason_short = {
            "Priority A": "Alta prioridad operativa + robustez alta + señal recurrente",
            "Priority B": "Prioridad operativa elevada",
            "Watchlist": "Caso episódico / sensible",
            "Monitor": "Contexto base del universo",
            "Low information": "Requiere más contexto",
        }
        table = page_df.assign(
            **{
                "#": range(start + 1, start + 1 + len(page_df)),
                "Score de revisión": page_df["decision_priority_score"].round(2),
                "Categoría de revisión": page_df["due_diligence_priority_es"],
                "Acción recomendada": page_df["due_diligence_priority"].map(action_short).fillna(page_df["recommended_action"]),
                "¿Por qué aparece?": page_df["due_diligence_priority"].map(reason_short).fillna(page_df["priority_reason"]),
                "Robustez": page_df[robust_col],
                "Estrés nodal prom.": page_df["avg_icpi"].round(2),
                "Prioridad operativa prom.": page_df["avg_oanri"].round(2),
                "Tensión kV": page_df["nivel_tension_kv"].round(1),
                "Soporte de contexto": page_df["evidence_grade"].map(lambda value: "Revisado" if str(value) == "A" else str(value)),
            }
        )[
            [
                "#",
                "barra",
                "Score de revisión",
                "Categoría de revisión",
                "Acción recomendada",
                "¿Por qué aparece?",
                "Robustez",
                "Estrés nodal prom.",
                "Prioridad operativa prom.",
                "Tensión kV",
                "Soporte de contexto",
            ]
        ].rename(columns={"barra": "Barra"})

        def _rank_style(value: object) -> str:
            text = str(value)
            if text == "Revisión inmediata":
                return "background-color: #fde8e6; color: #9d1f17; font-weight: 800; border-radius: 6px"
            if text == "Revisión selectiva":
                return "background-color: #fff0cf; color: #a85a00; font-weight: 800; border-radius: 6px"
            if text == "Seguimiento mensual":
                return "background-color: #dff4f6; color: #087a82; font-weight: 800; border-radius: 6px"
            if text == "Contexto base":
                return "background-color: #eef2f6; color: #4f5d6f; font-weight: 800; border-radius: 6px"
            if text == "Requiere contexto adicional":
                return "background-color: #f2e8f8; color: #7e3fa1; font-weight: 800; border-radius: 6px"
            if "alta" in text.lower():
                return "color: #1f8a5b; font-weight: 800"
            if "moderada" in text.lower():
                return "color: #c47a16; font-weight: 800"
            if text == "Revisado":
                return "color: #1f8a5b; font-weight: 800"
            return ""

        st.dataframe(
            table.style.map(_rank_style).format(precision=2),
            width="stretch",
            hide_index=True,
            height=430,
            column_config={
                "#": st.column_config.NumberColumn("#", width="small"),
                "Barra": st.column_config.TextColumn("Barra", width="medium"),
                "Score de revisión": st.column_config.ProgressColumn("Score de revisión", min_value=0, max_value=100, format="%.2f", width="medium"),
                "Categoría de revisión": st.column_config.TextColumn("Categoría de revisión", width="medium"),
                "Acción recomendada": st.column_config.TextColumn("Acción recomendada", width="medium"),
                "¿Por qué aparece?": st.column_config.TextColumn("¿Por qué aparece?", width="large"),
                "Robustez": st.column_config.TextColumn("Robustez", width="small"),
                "Estrés nodal prom.": st.column_config.NumberColumn("Estrés nodal prom.", format="%.2f", width="small"),
                "Prioridad operativa prom.": st.column_config.NumberColumn("Prioridad operativa prom.", format="%.2f", width="small"),
                "Tensión kV": st.column_config.NumberColumn("Tensión kV", format="%.1f", width="small"),
                "Soporte de contexto": st.column_config.TextColumn("Soporte de contexto", width="small"),
            },
        )
        st.caption(f"Mostrando {start + 1:,} a {min(end, len(filtered)):,} de {len(filtered):,} barras filtradas.")
        st.download_button("Descargar lista filtrada", filtered.to_csv(index=False).encode("utf-8"), file_name="sein_barra_due_diligence_worklist.csv", mime="text/csv")
    st.html(
        """
<div class="rank-bottom-notes">
  <div><span class="exec-icon exec-icon-shield" aria-hidden="true"></span><strong>Nota metodológica:</strong><p>Esta priorización combina señales de precio, recurrencia, robustez y contexto del sistema. No sustituye análisis técnico, contractual u operativo.</p></div>
  <div><span class="exec-icon exec-icon-case" aria-hidden="true"></span><strong>Uso recomendado:</strong><p>Forme una lista corta con los filtros, revise los casos y valide con equipos técnicos y contractuales antes de cualquier decisión.</p></div>
</div>
"""
    )


def render_icpi_oanri() -> None:
    page_header("Mapa de Señales", "¿Qué barras combinan estrés nodal relativo con prioridad operativa?")
    df = load_product_layer()
    panel = load_monthly_panel()
    if df.empty:
        st.error("La capa producto no está disponible.")
        st.stop()

    valid_months = panel["month"].dropna() if not panel.empty else []
    start_month = valid_months.min().strftime("%Y-%m") if len(valid_months) else "no disponible"
    end_month = valid_months.max().strftime("%Y-%m") if len(valid_months) else "no disponible"
    review_queue = int(df["due_diligence_priority"].isin(["Priority A", "Priority B"]).sum())
    monthly_followup = int((df["due_diligence_priority"] == "Watchlist").sum())
    context_summary_panel(
        "Mapa de decisión: señal local vs prioridad ajustada",
        f"Panel COES mensual {start_month} a {end_month}. Cada punto es una barra; la posición muestra estrés nodal y prioridad operativa promedio, el color muestra prioridad y el tamaño resume el score.",
        [
            ("Barras SEIN", f"{df['barra'].nunique():,.0f}", "muestra pública"),
            ("Cola de revisión", f"{review_queue:,.0f}", f"{review_queue / max(len(df), 1):.0%} del universo"),
            ("Mediana estrés nodal", f"{float(df['avg_icpi'].median()):,.1f}", "línea vertical"),
            ("Seguimiento mensual", f"{monthly_followup:,.0f}", "casos episódicos"),
        ],
    )
    st.plotly_chart(icpi_oanri_scatter(df), use_container_width=True)
    section_header("Cómo leer los cuadrantes")
    decision_matrix(
        [
            ("Estrés alto + prioridad alta", "Candidata de revisión inmediata. La señal local y la lectura operativa apuntan en la misma dirección.", "high"),
            ("Estrés alto + prioridad menor", "Señal local relevante. Revisar persistencia, meses extremos, contrato y evidencia topológica.", "local"),
            ("Estrés menor + prioridad alta", "Sensibilidad a régimen. Revisar si la prioridad aparece en meses de presión sistémica.", "system"),
            ("Estrés menor + prioridad menor", "Contexto base. Útil para comparación dentro del universo completo.", "monitor"),
        ]
    )
    section_header("Candidatas principales")
    compact_table(df.sort_values(["rank_oanri", "rank_icpi"], na_position="last").head(15), ["barra", "nivel_tension_kv", "rank_icpi", "rank_oanri", "avg_icpi", "avg_oanri", "decision_priority_score", "robustness_flag_es", "evidence_grade", "due_diligence_priority_es"])


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


def render_watchlist() -> None:
    page_header("Seguimiento Mensual", "¿Cuándo aparecen episodios de estrés y son persistentes o episódicos?")
    watchlist = load_watchlist()
    panel = load_monthly_panel()
    profiles = load_product_layer()
    if watchlist.empty:
        st.error("La capa de seguimiento mensual no está disponible.")
        st.stop()

    filter_cols = st.columns([1.1, 1.2])
    with filter_cols[0]:
        selected_priorities = priority_filter(profiles, key="watchlist_priority")
    with filter_cols[1]:
        top_n = st.slider("Barras visibles en heatmap", min_value=10, max_value=50, value=25, step=5)
    filtered_profiles = profiles[profiles["due_diligence_priority"].isin(selected_priorities)] if selected_priorities else profiles
    ordered_barras = filtered_profiles.sort_values("decision_priority_score", ascending=False)["barra"].head(top_n).tolist()
    heatmap_data = watchlist[watchlist["barra"].isin(ordered_barras)]

    cols = st.columns(4)
    with cols[0]:
        metric_card("Barras en mapa", f"{heatmap_data['barra'].nunique():,.0f}", "top por prioridad", kind="info")
    with cols[1]:
        metric_card("Meses en seguimiento", f"{watchlist['month'].nunique():,.0f}", "cobertura mensual")
    with cols[2]:
        metric_card("Observaciones top", f"{len(watchlist):,.0f}", "barra-mes")
    with cols[3]:
        metric_card("Máx. prioridad operativa", f"{watchlist['Prioridad operativa'].max():.1f}", "episodio más alto", kind="warning")

    section_header("Mapa mensual de seguimiento", "Color más intenso significa prioridad operativa mensual más alta. Filas repetidamente intensas sugieren persistencia; bloques aislados sugieren episodios puntuales.")
    st.plotly_chart(watchlist_heatmap(heatmap_data, order=ordered_barras), use_container_width=True)
    section_header("Lectura por barra")
    selected_barra = barra_selector(heatmap_data, key="watchlist_barra")
    if selected_barra and not panel.empty:
        selected_rows = panel[panel["barra"] == selected_barra].sort_values("month")
        action_panel("Interpretación automática", classify_pattern(selected_rows))
        st.plotly_chart(barra_month_line(panel, selected_barra), use_container_width=True)

    section_header("Top mensual de señales")
    compact_table(watchlist.sort_values(["month", "ranking_mensual_v10"]).head(120), ["month", "barra", "Estrés nodal", "Prioridad operativa", "ranking_mensual_v10", "decision_tier", "primary_driver"])


def render_exposicion() -> None:
    page_header("Exposición Industrial", "¿Qué combinaciones sector-barra-contrato merecen revisión bajo supuestos explícitos?")
    sector_df = load_sector_profiles()
    contract_df = load_contract_scenarios()
    sample = load_simulator_sample()
    if sector_df.empty:
        st.error("Los perfiles sector-barra no están disponibles.")
        st.stop()

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

    cols = st.columns(4)
    with cols[0]:
        metric_card("Perfiles filtrados", f"{len(filtered):,.0f}", "sector-contrato-barra", kind="info")
    with cols[1]:
        metric_card("Barras únicas", f"{filtered['barra'].nunique():,.0f}", "candidatas")
    with cols[2]:
        metric_card("Score promedio", f"{filtered['avg_industrial_exposure_score'].mean():.1f}", "exposición media", kind="warning")
    with cols[3]:
        metric_card("Score p90", f"{filtered['p90_industrial_exposure_score'].mean():.1f}", "cola del escenario", kind="danger")

    leader = filtered.iloc[0] if not filtered.empty else None
    leader_text = f"Bajo {sector_label} y {contract_label}, {leader['barra']} lidera el escenario con score {leader['profile_priority_score']:.1f}." if leader is not None else "No hay combinaciones para el filtro activo."
    insight_grid(
        [
            ("Pregunta de decisión", "¿Qué combinación sector-barra debe revisarse primero bajo supuestos explícitos de exposición?", "decision"),
            ("Hallazgo principal", leader_text, "evidence"),
            ("Acción recomendada", "Revisar cobertura contractual, participación spot, demanda mensual y sensibilidad operativa del sector seleccionado.", "action"),
            ("Caveat metodológico", "Los escenarios son salidas de screening basadas en supuestos; se interpretan como cola de revisión, no como forecast de factura.", "caveat"),
        ]
    )
    section_header("Ranking sector-barra", "Bajo supuestos explícitos de exposición, esta combinación sector-barra merece mayor prioridad de due diligence.")
    st.plotly_chart(sector_exposure_bar_chart(filtered), use_container_width=True)
    compact_table(filtered.head(50), ["sector", "contract_type", "barra", "avg_industrial_exposure_score", "p90_industrial_exposure_score", "priority_months", "watchlist_months", "robustness_inclusion_share", "dominant_driver", "profile_priority_score"])
    if not contract_df.empty:
        section_header("Sensibilidad contractual")
        selected_contract_df = contract_df[contract_df["sector"] == sector] if sector else contract_df
        st.plotly_chart(contract_comparison_chart(selected_contract_df), use_container_width=True)
    if not sample.empty:
        st.download_button("Descargar muestra del simulador", sample.head(500).to_csv(index=False).encode("utf-8"), file_name="industrial_exposure_sample.csv", mime="text/csv")
    action_panel("Lectura del escenario", "Una combinación con mayor score merece más atención porque reúne señal nodal, prioridad mensual, participación spot, consumo y supuestos sectoriales. Es un screening bajo supuestos explícitos: no debe interpretarse como forecast de factura ni valorización financiera.")


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

    decision_summary_card(priority_label, f"{row['decision_priority_score']:.1f}/100", row["priority_reason"], row["recommended_action"], f"Soporte de contexto {row['evidence_grade']}; {humanize_analytical_text(row.get('robustness_flag_es', row['robustness_flag']))}.")
    section_header("Contexto actual de la barra")
    price_window = f"{_clean(row.get('coes_price_key_first_month'), 'sin inicio')} a {_clean(row.get('coes_price_key_last_month'), 'sin fin')}"
    insight_grid(
        [
            ("Activo o conexión relevante", _clean(row.get("topology_context_asset"), row["barra"]), "decision"),
            ("Tipo de contexto", f"{_clean(row.get('topology_context_type_es'))}. Rol: {_clean(row.get('evidence_family_es'))}.", "evidence"),
            ("Cobertura COES", f"Serie mensual usada para estrés nodal/prioridad operativa: {price_window}; meses observados: {_clean(row.get('coes_price_key_months_observed'), '0')}.", "action"),
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
        action_panel("Validaciones analíticas", "1. Confirmar si la señal es persistente o episódica. 2. Revisar meses con mayor prioridad operativa. 3. Comparar ranking de estrés nodal y prioridad operativa. 4. Verificar robustez y evidencia.")
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
