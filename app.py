from __future__ import annotations

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
    page_header("Resumen Ejecutivo", "¿Dónde están las señales más fuertes de due diligence?")
    profiles = load_product_layer()
    panel = load_monthly_panel()
    regime = load_system_regime()
    if profiles.empty:
        st.error("La capa producto no está disponible.")
        st.stop()

    cols = st.columns(5)
    with cols[0]:
        metric_card("Barras analizadas", f"{profiles['barra'].nunique():,.0f}", "capa producto", kind="info")
    with cols[1]:
        metric_card("Meses analizados", f"{panel['month'].nunique() if not panel.empty else 0}", "panel histórico")
    with cols[2]:
        metric_card("Revisión inmediata", f"{(profiles['due_diligence_priority'] == 'Priority A').sum():,.0f}", "primera cola", kind="danger")
    with cols[3]:
        metric_card("Revisión selectiva", f"{(profiles['due_diligence_priority'] == 'Priority B').sum():,.0f}", "segunda cola", kind="warning")
    with cols[4]:
        metric_card("Seguimiento mensual", f"{(profiles['due_diligence_priority'] == 'Watchlist').sum():,.0f}", "monitoreo activo", kind="info")

    priority_ab = profiles[profiles["due_diligence_priority"].isin(["Priority A", "Priority B"])]
    top_oanri = profiles.sort_values("rank_oanri", na_position="last").head(1).iloc[0]
    top_icpi = profiles.sort_values("rank_icpi", na_position="last").head(1).iloc[0]
    insight_grid(
        [
            ("Hallazgo ejecutivo", f"{len(priority_ab):,.0f} barras entran a la cola de revisión. Lideran {top_oanri['barra']} por prioridad operativa y {top_icpi['barra']} por estrés nodal.", "decision"),
            ("Por qué importa", "Estrés nodal captura señal relativa por barra; prioridad operativa añade lectura de régimen del sistema para priorizar revisión.", "evidence"),
            ("Siguiente acción", "Abrir revisión inmediata, contrastar exposición industrial y revisar contexto topológico antes de bajar a casos.", "action"),
            ("Lectura correcta", "El ranking ordena una cola de due diligence: sirve para decidir dónde mirar primero y con qué hipótesis.", "caveat"),
        ]
    )

    section_header("Barras que dominan la cola ejecutiva")
    left, right = st.columns(2)
    with left:
        st.plotly_chart(top_bar_chart(profiles, "avg_oanri", "barra", "Top 10 barras por prioridad operativa"), use_container_width=True)
    with right:
        st.plotly_chart(top_bar_chart(profiles, "avg_icpi", "barra", "Top 10 barras por estrés nodal"), use_container_width=True)
    if not regime.empty:
        section_header("Régimen operativo mensual")
        st.plotly_chart(system_regime_line(regime), use_container_width=True)
    action_panel("Lectura ejecutiva", "Usa esta vista como entrada: identifica barras que concentran señal y baja al caso específico para revisar contrato, demanda industrial, contexto topológico y recurrencia mensual.")


def render_ranking() -> None:
    page_header("Ranking de Prioridad por Barra", "¿Qué barras deberían revisarse primero?")
    df = load_product_layer()
    if df.empty:
        st.error("La capa producto no está disponible.")
        st.stop()

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

    cols = st.columns(4)
    with cols[0]:
        metric_card("Barras filtradas", f"{len(filtered):,.0f}", "universo visible", kind="info")
    with cols[1]:
        metric_card("Cola de revisión", f"{filtered['due_diligence_priority'].isin(['Priority A', 'Priority B']).sum():,.0f}", "revisión inmediata/selectiva", kind="warning")
    with cols[2]:
        metric_card("Seguimiento mensual", f"{(filtered['due_diligence_priority'] == 'Watchlist').sum():,.0f}", "casos episódicos", kind="info")
    with cols[3]:
        metric_card("Contexto revisado", f"{filtered['topology_context_asset'].astype(str).str.strip().ne('').sum():,.0f}", "activo/conexión trazable", kind="good")

    section_header("Cómo funcionan las categorías")
    priority_system_legend()
    section_header("Cola de revisión por barra")
    if filtered.empty:
        action_panel("Sin resultados para los filtros activos", "Amplía prioridad, evidencia, robustez o tensión para recuperar barras candidatas.")
    else:
        priority_table(filtered)
        st.download_button("Descargar lista filtrada", filtered.to_csv(index=False).encode("utf-8"), file_name="sein_barra_due_diligence_worklist.csv", mime="text/csv")


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
selected_page = st.sidebar.radio("Página", list(PAGES.keys()), label_visibility="collapsed")
product_sidebar_footer()
PAGES[selected_page]()
