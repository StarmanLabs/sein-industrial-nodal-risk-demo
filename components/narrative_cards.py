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
    "High robustness": "robustez alta",
    "Moderate robustness": "robustez moderada",
    "Low robustness": "robustez baja",
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
    st.sidebar.title("SEIN Nodal Risk")
    st.sidebar.caption("Due diligence industrial")
    st.sidebar.divider()
    st.sidebar.caption(
        "Screening analítico para priorizar revisión industrial."
    )


def page_header(title: str, question: str) -> None:
    st.markdown("<div class='sein-page-kicker'>Panel de soporte a decisiones</div>", unsafe_allow_html=True)
    st.title(title)
    st.caption(f"Pregunta de decisión: {question}")


def hero_header(title: str, body: str, kicker: str = "SEIN Industrial Nodal Risk Intelligence") -> None:
    st.markdown(
        f"""
<div class="sein-hero">
  <div class="sein-hero-kicker">{escape(kicker)}</div>
  <div class="sein-hero-title">{escape(title)}</div>
  <div class="sein-hero-body">{escape(body)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def executive_kpi_strip(items: list[tuple[str, object, str, str]]) -> None:
    rendered_items = "\n".join(
        f"""
  <div class="sein-exec-kpi {escape(kind)}">
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
    rendered_steps = "\n".join(
        f"""
  <div class="sein-flow-step">
    <div class="sein-flow-number">{index:02d}</div>
    <div>
      <div class="sein-flow-title">{escape(title)}</div>
      <div class="sein-flow-body">{escape(body)}</div>
    </div>
  </div>
"""
        for index, (title, body) in enumerate(steps, start=1)
    )
    st.markdown(
        f"""
<div class="sein-flow-panel">
  <div class="sein-flow-copy">
    <div class="sein-flow-kicker">Flujo del producto</div>
    <div class="sein-flow-headline">De precios marginales a una cola de revisión industrial</div>
    <div class="sein-flow-text">La app convierte datos técnicos en una secuencia de trabajo: detectar señales, priorizar barras y decidir dónde profundizar.</div>
  </div>
  <div class="sein-flow-steps">
{rendered_steps}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def use_path_panel(items: list[tuple[str, str]]) -> None:
    rendered_items = "\n".join(
        f"""
  <div class="sein-use-step">
    <span>{escape(label)}</span>
    <p>{escape(body)}</p>
  </div>
"""
        for label, body in items
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
        ("Revisión inmediata", "Primera cola de due diligence: señal alta, recurrencia y soporte suficiente.", "urgent"),
        ("Revisión selectiva", "Candidata relevante; gana prioridad si el sector, contrato o ubicación aumentan exposición.", "selective"),
        ("Seguimiento mensual", "Caso episódico o sensible a escenarios; se vigila por persistencia y cambios recientes.", "watch"),
        ("Contexto base", "Permanece en el universo analítico para comparación, referencia y nuevos eventos.", "base"),
    ]
    rendered_items = "\n".join(
        f"""
  <div class="sein-taxonomy-item {escape(kind)}">
    <div class="sein-taxonomy-title">{escape(title)}</div>
    <div class="sein-taxonomy-body">{escape(body)}</div>
  </div>
"""
        for title, body, kind in items
    )
    st.markdown(
        f"""
<div class="sein-taxonomy-panel">
  <div class="sein-taxonomy-header">
    <div>
      <div class="sein-taxonomy-kicker">Taxonomía de decisión</div>
      <div class="sein-taxonomy-headline">Cómo leer la cola de revisión</div>
    </div>
    <div class="sein-taxonomy-caption">Los nombres técnicos quedan para la ficha metodológica; aquí se comunica qué acción tomar.</div>
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
  <strong>Lectura prudente.</strong> {escape(body)}
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
                "Prioridad A",
                "Llegó aquí porque combina señal estrés nodal/prioridad operativa alta, presencia repetida en meses relevantes, robustez fuerte y evidencia revisada. Es la primera cola de revisión.",
                "decision",
            ),
            (
                "Prioridad B",
                "Tiene señal relevante, pero menor intensidad, menor recurrencia o menor soporte que A. Se revisa después de A o si el sector/contrato aumenta su importancia.",
                "evidence",
            ),
            (
                "Watchlist",
                "La barra aparece en meses específicos o bajo ciertos escenarios. No se descarta: se vigila porque puede volverse importante según contrato, sector o mes.",
                "action",
            ),
            (
                "Monitorear / baja información",
                "Permanece como referencia del universo. No exige revisión inmediata, salvo que aparezca nueva evidencia, nueva demanda industrial o cambio de comportamiento mensual.",
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
                "Los índices son relativos 0-100: usan rankings, promedios, colas, volatilidad, episodios críticos, persistencia mensual y sensibilidad. La robustez revisa si la señal sobrevive a varios criterios.",
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
    if "priority a" in text or "prioridad a" in text:
        return "priority-a"
    if "priority b" in text or "prioridad b" in text:
        return "priority-b"
    if "watchlist" in text:
        return "watchlist"
    if "monitor" in text or "monitorear" in text:
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
            "Convierte estrés nodal/prioridad operativa, recurrencia, watchlist, robustez y evidencia revisada en una cola de trabajo. Sirve para decidir dónde empezar la due diligence.",
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
            "Robustez",
            "Mide estabilidad estadística. Una señal robusta no depende de un solo mes o de un solo ranking: aparece bajo varios criterios, sensibilidad, recurrencia o inclusión en listas top.",
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

