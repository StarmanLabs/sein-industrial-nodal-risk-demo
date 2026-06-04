from __future__ import annotations

from html import escape

import streamlit as st

from components.style import inject_global_style


PRODUCT_CAVEAT = (
    "Alcance analítico: esta vista ordena señales para priorizar revisión. "
    "La decisión final se fortalece contrastando contrato, demanda, confiabilidad, "
    "topología y criterio técnico específico de la barra."
)

TEXT_REPLACEMENTS = {
    "High robustness": "estabilidad alta",
    "Moderate robustness": "estabilidad moderada",
    "Low robustness": "estabilidad baja",
    "Robustez alta": "Estabilidad alta",
    "Robustez moderada": "Estabilidad moderada",
    "Robustez baja": "Estabilidad baja",
    "Not covered by sensitivity top-list": "sin cobertura en top-list de sensibilidad",
    "Topology-aware due diligence, spatial/economic screening, and decision-support context.": "Due diligence con contexto topológico, screening espacial/económico y soporte a decisión.",
    "Final COES canonical joins, physical flow direction, congestion attribution, or causal claims.": "Lectura orientada a screening y priorización; para decisiones finales se complementa con validación contractual, operativa y de red.",
    "Add operation-date-specific filters before using this row in historical 2023-2025 interpretation.": "Agregar filtros por fecha de operación antes de usar esta barra para una interpretación histórica 2023-2025.",
    "Canonical COES bus-key dictionary; then selective level-5 evidence for flows, limits, outages, contingencies, or validated network model.": "Diccionario canónico de barras COES; luego evidencia nivel 5 selectiva sobre flujos, límites, salidas, contingencias o modelo de red validado.",
    "Add one more official/operator source before public portfolio publication if this row becomes a highlighted case.": "Agregar una fuente oficial u operador adicional antes de usar esta barra como caso destacado público.",
    "driver dominante: price_level": "driver dominante: nivel de precio",
    "driver dominante: stress_premium": "driver dominante: prima de estrés",
    "driver dominante: volatility": "driver dominante: volatilidad",
    "price_level": "nivel de precio",
    "stress_premium": "prima de estrés",
    "volatility": "volatilidad",
    "Baja informacion": "Baja información",
    "Priority A": "Revisión inmediata",
    "Priority B": "Revisión selectiva",
    "Watchlist": "Seguimiento mensual",
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
    "episodica": "episódica",
    "decision-support": "soporte a decisión",
}


def humanize_analytical_text(text: object) -> str:
    value = "" if text is None else str(text)
    for raw, display in TEXT_REPLACEMENTS.items():
        value = value.replace(raw, display)
    return value


def product_sidebar() -> None:
    inject_global_style()
    st.sidebar.markdown(
        """
<div class="sein-sidebar-brand">
  <div class="sein-sidebar-mark" aria-hidden="true">
    <svg viewBox="0 0 72 72" role="img">
      <path d="M16 46 31 17l24 12-8 28-31-11Z" fill="none" stroke="#23d3d3" stroke-width="2.5"/>
      <path d="M31 17 47 57M16 46l39-17M23 33l24 24" stroke="#75f2ff" stroke-width="1.6" opacity=".75"/>
      <circle cx="31" cy="17" r="4" fill="#f7a623"/>
      <circle cx="55" cy="29" r="4" fill="#22d3d3"/>
      <circle cx="47" cy="57" r="4" fill="#23d160"/>
      <circle cx="16" cy="46" r="4" fill="#22d3d3"/>
      <circle cx="23" cy="33" r="2.7" fill="#9efcff"/>
    </svg>
  </div>
  <div>
    <div class="sein-sidebar-title">SEIN</div>
    <div class="sein-sidebar-subtitle">Industrial<br>Nodal Risk<br>Intelligence</div>
  </div>
</div>
<div class="sein-sidebar-section">Navegación</div>
""",
        unsafe_allow_html=True,
    )
    st.sidebar.divider()


def product_sidebar_footer() -> None:
    st.sidebar.markdown(
        """
<div class="sein-sidebar-note">
  <div class="sein-sidebar-note-icon">ϟ</div>
  <strong>Energía, datos y criterio económico</strong>
  <span>para mejores decisiones industriales.</span>
</div>
""",
        unsafe_allow_html=True,
    )


def page_header(title: str, question: str) -> None:
    st.markdown("<div class='sein-page-kicker'>Panel de soporte a decisiones</div>", unsafe_allow_html=True)
    st.title(title)
    st.caption(f"Pregunta de decisión: {question}")


def hero_header(title: str, body: str, kicker: str = "SEIN Industrial Nodal Risk Intelligence") -> None:
    st.markdown(
        f"""
<div class="sein-hero">
  <div class="sein-hero-content">
    <div class="sein-hero-kicker">{escape(kicker)}</div>
    <div class="sein-hero-title">{escape(title).replace("due diligence industrial", "<span>due diligence industrial</span>")}</div>
    <div class="sein-hero-body">{escape(body)}</div>
    <div class="sein-hero-proof">Identifica qué barras revisar primero, por qué aparecen y qué evidencia falta contrastar.</div>
    <div class="sein-hero-actions">
      <div class="sein-hero-action primary">Ver resumen ejecutivo <span>→</span></div>
      <div class="sein-hero-action">Abrir ranking <span>→</span></div>
      <div class="sein-hero-action">Analizar caso <span>→</span></div>
    </div>
  </div>
  <div class="sein-hero-visual" aria-hidden="true">
    <svg viewBox="0 0 420 430" role="img">
      <defs>
        <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      <path class="peru-outline" d="M250 20 318 58l-6 54 55 35-24 51 38 58-58 18-10 70-71 18-31 46-68-29-46-53 21-58-51-42 35-62-12-72 61-39Z"/>
      <g class="peru-lines">
        <path d="M250 20 211 126 318 58 274 182 367 147 292 243 381 256 313 344 242 362 143 379 118 268 67 226 102 164 151 53"/>
        <path d="M211 126 102 164 274 182 118 268 292 243 242 362"/>
        <path d="M318 58 367 147 381 256 313 344"/>
      </g>
      <g filter="url(#glow)">
        <circle cx="250" cy="20" r="5"/>
        <circle cx="318" cy="58" r="5"/>
        <circle cx="211" cy="126" r="5"/>
        <circle cx="274" cy="182" r="5"/>
        <circle cx="367" cy="147" r="5"/>
        <circle cx="292" cy="243" r="5"/>
        <circle cx="381" cy="256" r="5"/>
        <circle cx="313" cy="344" r="5"/>
        <circle cx="242" cy="362" r="5"/>
        <circle cx="143" cy="379" r="5"/>
        <circle cx="118" cy="268" r="5"/>
        <circle cx="67" cy="226" r="5"/>
        <circle cx="102" cy="164" r="5"/>
        <circle cx="151" cy="53" r="5"/>
      </g>
    </svg>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def executive_kpi_strip(items: list[tuple[str, object, str, str]]) -> None:
    icons = {
        "Universo SEIN": "pin",
        "Cobertura": "calendar",
        "Panel mensual": "database",
        "Cola de revisión": "users",
        "Seguimiento": "trend",
    }

    def _icon(name: str) -> str:
        icon = icons.get(name, "database")
        if icon == "pin":
            return '<svg viewBox="0 0 24 24"><path d="M12 22s7-6.1 7-13A7 7 0 0 0 5 9c0 6.9 7 13 7 13Z"/><circle cx="12" cy="9" r="2.5"/></svg>'
        if icon == "calendar":
            return '<svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16M8 14h.01M12 14h.01M16 14h.01M8 17h.01M12 17h.01"/></svg>'
        if icon == "users":
            return '<svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"/><circle cx="9.5" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
        if icon == "trend":
            return '<svg viewBox="0 0 24 24"><path d="M3 17h18M4 14l5-5 4 4 7-8"/><path d="M16 5h4v4"/></svg>'
        return '<svg viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v6c0 1.7 3.1 3 7 3s7-1.3 7-3V5"/><path d="M5 11v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/></svg>'

    rendered_items = "\n".join(
        f"""
  <div class="sein-exec-kpi {escape(kind)}">
    <div class="sein-exec-kpi-icon">{_icon(label)}</div>
    <div class="sein-exec-kpi-label">{escape(label)}</div>
    <div class="sein-exec-kpi-value">{escape(str(value))}</div>
    <div class="sein-exec-kpi-note">{escape(note)}</div>
  </div>
"""
        for label, value, note, kind in items
    )
    st.markdown(
        f"""
<div class="sein-exec-kpi-strip">
{rendered_items}
</div>
""",
        unsafe_allow_html=True,
    )


def decision_flow(steps: list[tuple[str, str]]) -> None:
    flow_icons = [
        '<svg viewBox="0 0 24 24"><path d="M4 13h3l2-6 4 12 3-8h4"/></svg>',
        '<svg viewBox="0 0 24 24"><path d="M8 6h13M8 12h13M8 18h13"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/></svg>',
        '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>',
    ]
    rendered_steps = "\n".join(
        f"""
  <div class="sein-flow-step">
    <div class="sein-flow-icon {['signal', 'rank', 'proof'][index - 1]}">{flow_icons[index - 1]}</div>
    <div>
      <div class="sein-flow-title">{index}. {escape(title)}</div>
      <div class="sein-flow-body">{escape(body)}</div>
    </div>
  </div>
"""
        for index, (title, body) in enumerate(steps, start=1)
    )
    st.markdown(
        f"""
<div class="sein-flow-panel">
  <div class="sein-flow-headline">De datos nodales a una cola de revisión</div>
  <div class="sein-flow-steps">
{rendered_steps}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def use_path_panel(items: list[tuple[str, str]]) -> None:
    icons = [
        '<svg viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
        '<svg viewBox="0 0 24 24"><path d="M8 6h13M8 12h13M8 18h13"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/></svg>',
        '<svg viewBox="0 0 24 24"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9Z"/><path d="M14 3v6h6M9 15h5M9 18h3"/></svg>',
    ]
    rendered_items = "\n".join(
        f"""
  <div class="sein-use-step">
    <div class="sein-use-icon {['summary', 'ranking', 'case'][index - 1]}">{icons[index - 1]}</div>
    <span>{escape(label)}</span>
    <p>{escape(body)}</p>
    <a>{['Ir al resumen', 'Abrir ranking', 'Ver caso'][index - 1]} <strong>→</strong></a>
  </div>
"""
        for index, (label, body) in enumerate(items, start=1)
    )
    st.markdown(
        f"""
<div class="sein-use-panel">
  <div class="sein-use-title">Cómo se usa</div>
  <div class="sein-use-grid">
{rendered_items}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def decision_taxonomy() -> None:
    items = [
        ("Revisión inmediata", "Señal alta, recurrencia y soporte suficiente.", "urgent", "warning"),
        ("Revisión selectiva", "Prioridad si sector, contrato o ubicación aumentan exposición.", "selective", "target"),
        ("Seguimiento mensual", "Caso episódico o sensible a escenarios; vigilar persistencia.", "watch", "eye"),
        ("Contexto base", "Permanece en el universo para comparación y referencia.", "base", "database"),
        ("Requiere contexto adicional", "Información limitada; priorizar obtención de evidencia.", "limited", "help"),
    ]
    icons = {
        "warning": '<svg viewBox="0 0 24 24"><path d="M12 3 2 21h20L12 3Z"/><path d="M12 9v5M12 17h.01"/></svg>',
        "target": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/><path d="m15 9 5-5"/></svg>',
        "eye": '<svg viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>',
        "database": '<svg viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v6c0 1.7 3.1 3 7 3s7-1.3 7-3V5"/><path d="M5 11v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/></svg>',
        "help": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.7 2.7 0 0 1 5 1.4c0 2.1-2.5 2.3-2.5 4.1M12 18h.01"/></svg>',
    }
    rendered_items = "\n".join(
        f"""
  <div class="sein-taxonomy-item {escape(kind)}">
    <div class="sein-taxonomy-icon">{icons[icon]}</div>
    <div class="sein-taxonomy-title">{escape(title)}</div>
    <div class="sein-taxonomy-body">{escape(body)}</div>
  </div>
"""
        for title, body, kind, icon in items
    )
    st.markdown(
        f"""
<div class="sein-taxonomy-panel">
  <div class="sein-taxonomy-header">
    <div>
      <div class="sein-taxonomy-headline">Taxonomía de decisión</div>
    </div>
  </div>
  <div class="sein-taxonomy-grid">
{rendered_items}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def compact_scope_note(body: str) -> None:
    st.markdown(
        f"""
<div class="sein-compact-note">
  <div class="sein-compact-note-icon">
    <svg viewBox="0 0 24 24"><path d="M12 3 5 6v5c0 4.5 2.9 8.5 7 10 4.1-1.5 7-5.5 7-10V6l-7-3Z"/><path d="m9 12 2 2 4-5"/></svg>
  </div>
  <div>{escape(body)}<br><strong>No prueba congestión física, no predice precios y no reemplaza due diligence contractual, operativa o de ingeniería.</strong></div>
</div>
""",
        unsafe_allow_html=True,
    )


def section_header(title: str, caption: str | None = None) -> None:
    caption_html = (
        f"<div class='sein-section-caption'>{escape(caption)}</div>" if caption else ""
    )
    st.markdown(
        f"""
<div class="sein-section-title">{escape(title)}</div>
{caption_html}
""",
        unsafe_allow_html=True,
    )


def insight_grid(items: list[tuple[str, str, str]]) -> None:
    rendered_items = "\n".join(
        f"""
  <div class="sein-insight-card {escape(kind)}">
    <div class="sein-insight-title">{escape(title)}</div>
    <div class="sein-insight-body">{escape(body)}</div>
  </div>
"""
        for title, body, kind in items
    )
    st.markdown(
        f"""
<div class="sein-insight-grid">
{rendered_items}
</div>
""",
        unsafe_allow_html=True,
    )


def badge_row(items: list[tuple[str, str]]) -> None:
    rendered_items = "\n".join(
        f"<span class='sein-badge {escape(kind)}'>{escape(label)}</span>"
        for label, kind in items
    )
    st.markdown(f"<div class='sein-badge-row'>{rendered_items}</div>", unsafe_allow_html=True)


def action_panel(title: str, body: str) -> None:
    st.markdown(
        f"""
<div class="sein-action-panel">
  <div class="sein-action-title">{escape(title)}</div>
  <div class="sein-action-body">{escape(body)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def priority_system_legend() -> None:
    insight_grid(
        [
            (
                "Revisión inmediata",
                "Primera cola de due diligence: combina señal alta, recurrencia, estabilidad de señal y soporte de contexto suficiente para iniciar revisión experta.",
                "decision",
            ),
            (
                "Revisión selectiva",
                "Candidata relevante. Gana prioridad cuando el sector, contrato, ubicación o contexto industrial aumentan exposición.",
                "evidence",
            ),
            (
                "Seguimiento mensual",
                "Caso episódico o sensible a escenario. Se vigila para distinguir persistencia, deterioro reciente o eventos puntuales.",
                "action",
            ),
            (
                "Contexto base / requiere contexto adicional",
                "Permanece como referencia del universo o necesita mejor contexto antes de una lectura fuerte. No exige revisión inmediata.",
                "caveat",
            ),
        ]
    )


def due_diligence_definition_grid() -> None:
    insight_grid(
        [
            (
                "Due diligence, en simple",
                "Es una revisión ordenada antes de tomar una decisión seria. En este proyecto significa decidir qué barras merecen revisar contrato, demanda, ubicación, confiabilidad y contexto de red.",
                "decision",
            ),
            (
                "Qué aporta al negocio",
                "Evita revisar 217 barras a ciegas. Convierte datos técnicos en una cola de trabajo: primero lo más prometedor, luego lo secundario, después monitoreo.",
                "action",
            ),
            (
                "Qué valida",
                "No busca una verdad final automática. Ayuda a priorizar dónde conviene invertir análisis experto, documentación técnica y contraste con fuentes externas.",
                "evidence",
            ),
            (
                "Lectura prudente",
                "Una barra priorizada no es una conclusión final. Es una candidata para revisión más profunda con evidencia económica, contractual, operativa y técnica.",
                "caveat",
            ),
        ]
    )


def methodology_definition_grid() -> None:
    insight_grid(
        [
            (
                "Datos usados",
                "La base principal son precios marginales por barra del COES, agregados mensualmente para 2023-2025. Cada barra se compara contra el universo de barras y contra su comportamiento mensual.",
                "decision",
            ),
            (
                "estrés nodal en simple",
                "Es un termómetro relativo de estrés nodal. Si es alto, esa barra mostró precios marginales más intensos, volátiles o extremos frente al resto del sistema.",
                "evidence",
            ),
            (
                "prioridad operativa en simple",
                "Es el estrés nodal leído con contexto del sistema. Si es alto, la barra no solo tuvo señal local: también ganó importancia bajo meses de presión operativa sistémica.",
                "action",
            ),
            (
                "Validez estadística",
                "Los índices son relativos 0-100: usan rankings, promedios, colas, volatilidad, episodios críticos, persistencia mensual y sensibilidad. La estabilidad revisa si la señal sigue siendo relevante bajo criterios alternativos.",
                "caveat",
            ),
        ]
    )


def interpretation_card(title: str, body: str) -> None:
    visual_card(title, body, kind="info")


def caveat_card(body: str = PRODUCT_CAVEAT) -> None:
    visual_card("Lectura operativa", body, kind="warning")


def next_review_card(action: str) -> None:
    visual_card("Siguiente decisión analítica", action, kind="success")


def visual_card(title: str, body: str, kind: str = "info") -> None:
    st.markdown(
        f"""
<div class="sein-card {escape(kind)}">
  <div class="sein-card-title">{escape(title)}</div>
  <div class="sein-card-body">{escape(body)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def meta_strip(items: list[tuple[str, object]]) -> None:
    rendered_items = "\n".join(
        f"""
  <div class="sein-meta-item">
    <div class="sein-meta-label">{escape(str(label))}</div>
    <div class="sein-meta-value">{escape(str(value))}</div>
  </div>
"""
        for label, value in items
    )
    st.markdown(
        f"""
<div class="sein-meta-strip">
{rendered_items}
</div>
""",
        unsafe_allow_html=True,
    )


def context_summary_panel(
    title: str,
    body: str,
    stats: list[tuple[str, object, str | None]],
    eyebrow: str = "Contexto del panel",
) -> None:
    rendered_stats = "\n".join(
        f"""
  <div class="sein-context-stat">
    <strong>{escape(str(value))}</strong>
    <span>{escape(label)}</span>
    {f"<em>{escape(str(note))}</em>" if note else ""}
  </div>
"""
        for label, value, note in stats
    )
    st.markdown(
        f"""
<div class="sein-context-panel">
  <div class="sein-context-copy">
    <div class="sein-context-eyebrow">{escape(eyebrow)}</div>
    <div class="sein-context-title">{escape(title)}</div>
    <div class="sein-context-body">{escape(body)}</div>
  </div>
  <div class="sein-context-stats">
{rendered_stats}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def decision_matrix(cards: list[tuple[str, str, str]]) -> None:
    rendered_cards = "\n".join(
        f"""
  <div class="sein-matrix-card {escape(kind)}">
    <div class="sein-matrix-title">{escape(title)}</div>
    <div class="sein-matrix-body">{escape(body)}</div>
  </div>
"""
        for title, body, kind in cards
    )
    st.markdown(
        f"""
<div class="sein-matrix-grid">
{rendered_cards}
</div>
""",
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: object, note: str | None = None, kind: str = "neutral") -> None:
    note_html = f"<div class='sein-kpi-note'>{escape(note)}</div>" if note else ""
    st.markdown(
        f"""
<div class="sein-kpi {escape(kind)}">
  <div class="sein-kpi-label">{escape(label)}</div>
  <div class="sein-kpi-value">{escape(str(value))}</div>
  {note_html}
</div>
""",
        unsafe_allow_html=True,
    )


def _priority_kind(priority: object) -> str:
    text = str(priority).lower()
    if "priority a" in text or "prioridad a" in text or "revisión inmediata" in text or "revision inmediata" in text:
        return "priority-a"
    if "priority b" in text or "prioridad b" in text or "revisión selectiva" in text or "revision selectiva" in text:
        return "priority-b"
    if "watchlist" in text or "seguimiento mensual" in text:
        return "watchlist"
    if "monitor" in text or "monitorear" in text or "contexto base" in text:
        return "monitor"
    return "monitor"


def decision_summary_card(
    priority: object,
    score: object,
    reason: object,
    action: object,
    evidence: object,
) -> None:
    kind = _priority_kind(priority)
    st.markdown(
        f"""
<div class="sein-decision-card">
  <div class="sein-decision-band {escape(kind)}">
    <div class="sein-decision-label">Decisión sugerida</div>
    <div class="sein-decision-value">{escape(str(priority))}</div>
    <div class="sein-decision-score">Score de prioridad: <strong>{escape(str(score))}</strong><br>Mayor score = señal más intensa dentro del universo analizado.</div>
  </div>
  <div class="sein-decision-body">
    <h4>Por qué aparece aquí</h4>
    <p>{escape(humanize_analytical_text(reason))}</p>
    <h4>Qué hacer con esta señal</h4>
    <p>{escape(humanize_analytical_text(action))}</p>
    <h4>Calidad de soporte</h4>
    <p>{escape(humanize_analytical_text(evidence))}</p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def scope_grid(allowed: object, interpretation_scope: object, next_evidence: object) -> None:
    cards = [
        ("Qué permite hacer", allowed, "use"),
        ("Cómo leerlo", interpretation_scope, "limit"),
        ("Próxima evidencia", next_evidence, "next"),
    ]
    rendered_cards = "\n".join(
        f"""
  <div class="sein-scope-card {escape(kind)}">
    <div class="sein-scope-title">{escape(title)}</div>
    <div class="sein-scope-body">{escape(humanize_analytical_text(body))}</div>
  </div>
"""
        for title, body, kind in cards
    )
    st.markdown(
        f"""
<div class="sein-scope-grid">
{rendered_cards}
</div>
""",
        unsafe_allow_html=True,
    )


def indicator_definition_grid() -> None:
    cards = [
        (
            "estrés nodal",
            "Índice de estrés de precio marginal por barra. Usa nivel de precio, volatilidad, colas altas, prima de estrés y episodios críticos. Escala 0-100: 100 significa señal más intensa dentro del universo analizado, no precio absoluto.",
        ),
        (
            "prioridad operativa",
            "Indicador de prioridad nodal ajustada por régimen operativo. Parte de la señal local y la cruza con meses de presión del sistema. Escala 0-100: mayor valor, mayor prioridad para revisión bajo contexto sistémico.",
        ),
        (
            "Score de prioridad",
            "Convierte estrés nodal/prioridad operativa, recurrencia, seguimiento mensual, estabilidad y evidencia revisada en una cola de trabajo. Sirve para decidir dónde empezar la due diligence.",
        ),
    ]
    rendered_cards = "\n".join(
        f"""
  <div class="sein-definition-card">
    <div class="sein-definition-title">{escape(title)}</div>
    <div class="sein-definition-body">{escape(body)}</div>
  </div>
"""
        for title, body in cards
    )
    st.markdown(
        f"""
<div class="sein-definition-grid">
{rendered_cards}
</div>
""",
        unsafe_allow_html=True,
    )


def evidence_definition_grid() -> None:
    cards = [
        (
            "Evidencia revisada",
            "Todas las barras del producto entran con algún grado de revisión. En la interfaz se comunica como soporte revisado para no sobredimensionar diferencias menores entre A/B.",
        ),
        (
            "Cómo llevarla a nivel A",
            "Una barra solo debe subir a soporte máximo si se confirma con fuentes adicionales: COES, OSINERGMIN, operador, ficha técnica, unifilar, tensión, nombre y conexión coherente.",
        ),
        (
            "Estabilidad de señal",
            "Mide si una barra sigue siendo relevante bajo criterios alternativos. Consistente = señal estable; sensible o contextual = requiere más contraste antes de priorizar.",
        ),
    ]
    rendered_cards = "\n".join(
        f"""
  <div class="sein-definition-card">
    <div class="sein-definition-title">{escape(title)}</div>
    <div class="sein-definition-body">{escape(body)}</div>
  </div>
"""
        for title, body in cards
    )
    st.markdown(
        f"""
<div class="sein-definition-grid">
{rendered_cards}
</div>
""",
        unsafe_allow_html=True,
    )

