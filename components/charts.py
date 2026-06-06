from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


COLOR_SEQUENCE = ["#173b57", "#138a8a", "#d9902f", "#c5524a", "#6b778c"]
STRESS_SCALE = ["#f8fafc", "#dbeaf0", "#98c3cf", "#2f6f9f", "#173b57"]
HEAT_SCALE = ["#fff7ed", "#fed7aa", "#fb923c", "#dc5f2e", "#9f2f2a"]
PRIORITY_COLORS = {
    "Revisión inmediata": "#b23a2e",
    "Revisión selectiva": "#c47a16",
    "Seguimiento mensual": "#168c8c",
    "Contexto base": "#64748b",
    "Requiere contexto adicional": "#9aa4b2",
    "Prioridad A": "#c5524a",
    "Prioridad B": "#d9902f",
    "Watchlist": "#2f6f9f",
    "Monitorear": "#6b778c",
    "Baja informacion": "#9aa4b2",
    "Baja información": "#9aa4b2",
    "Priority A": "#c5524a",
    "Priority B": "#d9902f",
    "Monitor": "#6b778c",
    "Low information": "#9aa4b2",
}

METRIC_LABELS = {
    "avg_oanri": "Prioridad operativa promedio",
    "avg_icpi": "Estrés nodal promedio",
}

CONTRACT_LABELS = {
    "balanced_30pct_spot_ppa": "Balanceado: 30% spot + PPA",
    "fixed_reference_ppa": "PPA a referencia fija",
    "full_spot_exposure": "Exposición spot completa",
    "hedged_10pct_spot": "Cobertura alta: 10% spot",
    "indexed_50pct_spot": "Indexado: 50% spot",
}

SECTOR_LABELS = {
    "agroindustry_seasonal": "Agroindustria estacional",
    "cement_and_heavy_materials": "Cemento y materiales pesados",
    "data_center_or_high_availability": "Alta disponibilidad / data center",
    "general_manufacturing": "Manufactura general",
    "mining_continuous_load": "Minería de carga continua",
}


def apply_chart_style(fig, height: int | None = 420):
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        font={"family": "Arial, sans-serif", "color": "#263448", "size": 12},
        title={
            "font": {"size": 16, "color": "#182235"},
            "x": 0.02,
            "xanchor": "left",
        },
        margin={"l": 24, "r": 18, "t": 58, "b": 42},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "title": None,
            "font": {"size": 11},
        },
        coloraxis_colorbar={
            "thickness": 10,
            "len": 0.72,
            "outlinewidth": 0,
        },
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#e8eef4",
        zeroline=False,
        linecolor="#d9e1ea",
        title_font={"size": 12, "color": "#657286"},
        tickfont={"size": 11, "color": "#657286"},
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#eef3f7",
        zeroline=False,
        linecolor="#d9e1ea",
        title_font={"size": 12, "color": "#657286"},
        tickfont={"size": 11, "color": "#657286"},
    )
    return fig


def top_bar_chart(
    df: pd.DataFrame,
    value: str,
    label: str,
    title: str,
    n: int = 10,
):
    data = df.nlargest(n, value).sort_values(value)
    fig = px.bar(
        data,
        x=value,
        y=label,
        orientation="h",
        title=title,
        color=value,
        color_continuous_scale=STRESS_SCALE,
        hover_data=data.columns,
        labels={
            "barra": "Barra",
            value: METRIC_LABELS.get(value, value),
        },
    )
    fig.update_traces(marker_line_width=0, hovertemplate="<b>%{y}</b><br>%{x:.2f}<extra></extra>")
    return apply_chart_style(fig, height=390)


def icpi_oanri_scatter(df: pd.DataFrame):
    data = df.copy()
    color_col = (
        "due_diligence_priority_es"
        if "due_diligence_priority_es" in data.columns
        else "due_diligence_priority"
    )
    if color_col in data.columns:
        data[color_col] = data[color_col].replace(
            {
                "Baja informacion": "Baja información",
                "Baja información": "Requiere contexto adicional",
                "Low information": "Requiere contexto adicional",
                "Prioridad A": "Revisión inmediata",
                "Prioridad B": "Revisión selectiva",
                "Watchlist": "Seguimiento mensual",
                "Monitorear": "Contexto base",
                "Monitor": "Contexto base",
            }
        )
    hover_cols = [
        "rank_icpi",
        "rank_oanri",
        "evidence_grade",
    ]
    hover_cols.append(
        "robustness_flag_es" if "robustness_flag_es" in df.columns else "robustness_flag"
    )
    hover_cols.append(
        "persistence_category_es"
        if "persistence_category_es" in df.columns
        else "persistence_category"
    )
    fig = px.scatter(
        data,
        x="avg_icpi",
        y="avg_oanri",
        color=color_col,
        size="decision_priority_score",
        hover_name="barra",
        hover_data=hover_cols,
        title=None,
        color_discrete_map=PRIORITY_COLORS,
        labels={
            "avg_icpi": "Estrés nodal promedio",
            "avg_oanri": "Prioridad operativa promedio",
            color_col: "Categoría de revisión",
            "decision_priority_score": "Score de revisión",
            "rank_icpi": "Ranking estrés nodal",
            "rank_oanri": "Ranking prioridad operativa",
            "evidence_grade": "Soporte de contexto",
            "robustness_flag": "Estabilidad de señal",
            "robustness_flag_es": "Estabilidad de señal",
            "persistence_category": "Persistencia",
            "persistence_category_es": "Persistencia",
        },
    )
    x_ref = float(data["avg_icpi"].median())
    y_ref = float(data["avg_oanri"].median())
    fig.add_vline(
        x=x_ref,
        line_width=1,
        line_dash="dot",
        line_color="#9aa4b2",
        annotation_text="Estrés mediano",
        annotation_position="top left",
    )
    fig.add_hline(
        y=y_ref,
        line_width=1,
        line_dash="dot",
        line_color="#9aa4b2",
        annotation_text="Prioridad mediana",
        annotation_position="bottom left",
    )
    quadrant_annotations = [
        (0.98, 0.96, "Revisar<br>primero", "#8e2f2a"),
        (0.03, 0.96, "Sensibilidad<br>a régimen", "#245a73"),
        (0.98, 0.08, "Señal local<br>a revisar", "#8a5a14"),
        (0.03, 0.08, "Contexto<br>base", "#4f5d6f"),
    ]
    for x_pos, y_pos, text, color in quadrant_annotations:
        fig.add_annotation(
            x=x_pos,
            y=y_pos,
            xref="paper",
            yref="paper",
            text=text,
            showarrow=False,
            align="center",
            font={"size": 11, "color": color},
            bgcolor="rgba(255,255,255,0.78)",
            bordercolor="rgba(217,225,234,0.95)",
            borderwidth=1,
            borderpad=4,
        )
    fig.update_traces(
        marker={"line": {"width": 0.7, "color": "#ffffff"}, "opacity": 0.86},
        hovertemplate="<b>%{hovertext}</b><br>Estrés nodal: %{x:.1f}<br>Prioridad operativa: %{y:.1f}<extra></extra>",
    )
    fig = apply_chart_style(fig, height=560)
    fig.update_layout(
        title_text="",
        margin={"l": 54, "r": 24, "t": 42, "b": 54},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.04,
            "xanchor": "left",
            "x": 0,
            "title": None,
            "font": {"size": 10},
            "itemsizing": "constant",
        },
    )
    return fig


def system_regime_line(df: pd.DataFrame):
    data = df.sort_values("month").copy()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["month"],
            y=data["system_regime_v10_0_1"],
            mode="lines+markers",
            line={"color": "#087a82", "width": 3},
            marker={"size": 6, "color": "#087a82"},
            hovertemplate="Mes: %{x|%Y-%m}<br>Presión del sistema: %{y:.2f}<extra></extra>",
            showlegend=False,
        )
    )
    fig.update_layout(
        title=None,
        xaxis_title="Mes",
        yaxis_title="Presión del sistema (0-1)",
        showlegend=False,
    )
    fig = apply_chart_style(fig, height=290)
    fig.update_layout(title_text="", margin={"l": 24, "r": 18, "t": 10, "b": 42})
    return fig


def barra_month_line(df: pd.DataFrame, barra: str):
    data = df[df["barra"] == barra].sort_values("month").copy()
    data["month_label"] = data["month"].dt.strftime("%Y-%m")
    data["Estrés nodal relativo (estrés nodal)"] = data["Estrés nodal"]
    data["Prioridad operativa"] = data["Prioridad operativa"]
    fig = px.line(
        data,
        x="month_label",
        y=["Estrés nodal relativo (estrés nodal)", "Prioridad operativa"],
        markers=True,
        title=f"Evolución mensual de señal - {barra}",
        labels={
            "month_label": "Mes",
            "value": "Puntaje",
            "variable": "Indicador",
        },
        color_discrete_map={
            "Estrés nodal relativo (estrés nodal)": "#173b57",
            "Prioridad operativa": "#c5524a",
        },
    )
    fig.update_xaxes(type="category")
    fig.update_yaxes(range=[0, 105])
    fig.add_hrect(
        y0=75,
        y1=100,
        fillcolor="#fff1d7",
        opacity=0.28,
        line_width=0,
        annotation_text="zona alta relativa",
        annotation_position="top left",
    )
    fig.update_traces(line={"width": 3}, marker={"size": 7})
    return apply_chart_style(fig, height=420)


def barra_profile_score_bars(row: pd.Series):
    metrics = pd.DataFrame(
        {
            "Métrica": [
                "Estrés nodal promedio",
                "Prioridad operativa promedio",
                "Prioridad operativa p90",
                "Score prioridad",
            ],
            "Valor": [
                row.get("avg_icpi", 0),
                row.get("avg_oanri", 0),
                row.get("p90_oanri", 0),
                row.get("decision_priority_score", 0),
            ],
        }
    )
    fig = px.bar(
        metrics.sort_values("Valor"),
        x="Valor",
        y="Métrica",
        orientation="h",
        title="Lectura comparada de scores del caso",
        color="Valor",
        color_continuous_scale=HEAT_SCALE,
        range_x=[0, 100],
        labels={"Valor": "Score relativo 0-100"},
    )
    fig.add_vrect(x0=60, x1=75, fillcolor="#fff1d7", opacity=0.22, line_width=0)
    fig.add_vrect(x0=75, x1=100, fillcolor="#fde8e6", opacity=0.18, line_width=0)
    fig.update_traces(
        marker_line_width=0,
        text=metrics.sort_values("Valor")["Valor"].map(lambda value: f"{value:.1f}"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>%{x:.2f}<extra></extra>",
    )
    return apply_chart_style(fig, height=330)


def barra_component_profile(df: pd.DataFrame, barra: str):
    component_cols = {
        "block_cost_v10": "Nivel de precio",
        "block_volatility_v10": "Volatilidad",
        "block_stress_v10": "Prima de estrés",
        "block_criticality_v10": "Episodios críticos",
        "system_regime_v10_0_1": "Régimen sistema",
        "quality_score_v10": "Calidad dato",
    }
    data = df[df["barra"] == barra].copy()
    if data.empty:
        return go.Figure()
    values = []
    for column, label in component_cols.items():
        if column in data.columns:
            values.append({"Componente": label, "Valor": float(data[column].mean()) * 100})
    components = pd.DataFrame(values)
    fig = px.bar(
        components.sort_values("Valor"),
        x="Valor",
        y="Componente",
        orientation="h",
        title="Componentes promedio que explican la señal",
        color="Valor",
        color_continuous_scale=STRESS_SCALE,
        range_x=[0, 100],
        labels={"Valor": "Intensidad relativa promedio 0-100"},
    )
    fig.update_traces(
        marker_line_width=0,
        text=components.sort_values("Valor")["Valor"].map(lambda value: f"{value:.0f}"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>%{x:.1f}<extra></extra>",
    )
    return apply_chart_style(fig, height=330)


def watchlist_heatmap(df: pd.DataFrame, order: list[str] | None = None):
    df = df.copy()
    df["month_label"] = df["month"].dt.strftime("%Y-%m")
    value_col = (
        "Prioridad operativa"
        if "Prioridad operativa" in df.columns
        else "OANRI_v10"
        if "OANRI_v10" in df.columns
        else "prioridad_operativa"
    )
    data = df.pivot_table(
        index="barra",
        columns="month_label",
        values=value_col,
        aggfunc="mean",
    )
    if order:
        ordered_index = [barra for barra in order if barra in data.index]
        data = data.loc[ordered_index]
    fig = px.imshow(
        data,
        aspect="auto",
        color_continuous_scale=HEAT_SCALE,
        title="Mapa de calor mensual de seguimiento - prioridad operativa",
        labels={"color": "Prioridad operativa"},
    )
    fig.update_xaxes(title="Mes", type="category")
    fig.update_yaxes(title="Barra")
    return apply_chart_style(fig, height=560)


def sector_exposure_bar_chart(df: pd.DataFrame, n: int = 15):
    data = df.nlargest(n, "profile_priority_score").sort_values("profile_priority_score")
    data = data.copy()
    data["sector_label"] = data["sector"].map(lambda value: SECTOR_LABELS.get(value, value))
    data["contract_label"] = data["contract_type"].map(lambda value: CONTRACT_LABELS.get(value, value))
    fig = px.bar(
        data,
        x="profile_priority_score",
        y="barra",
        orientation="h",
        color="avg_industrial_exposure_score",
        color_continuous_scale=HEAT_SCALE,
        title="Top combinaciones sector-barra del escenario seleccionado",
        labels={
            "profile_priority_score": "Score de prioridad del perfil",
            "avg_industrial_exposure_score": "Exposición promedio",
            "barra": "Barra",
        },
        hover_data=[
            "sector_label",
            "contract_label",
            "avg_industrial_exposure_score",
            "p90_industrial_exposure_score",
            "priority_months",
            "watchlist_months",
            "dominant_driver",
        ],
    )
    fig.update_traces(
        marker_line_width=0,
        text=data["profile_priority_score"].map(lambda value: f"{value:.1f}"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Score perfil: %{x:.1f}<extra></extra>",
    )
    return apply_chart_style(fig, height=500)


def contract_comparison_chart(df: pd.DataFrame):
    if df.empty:
        return go.Figure()
    data = df.sort_values("avg_exposure_score").copy()
    data["contract_label"] = data["contract_type"].map(lambda value: CONTRACT_LABELS.get(value, value))
    fig = px.bar(
        data,
        x="avg_exposure_score",
        y="contract_label",
        orientation="h",
        color="spot_share",
        color_continuous_scale=STRESS_SCALE,
        title="Sensibilidad comparada por arquetipo contractual",
        labels={
            "avg_exposure_score": "Score promedio de exposición",
            "contract_type": "Contrato",
            "spot_share": "Participación spot",
        },
        hover_data=["unique_barras", "monthly_mwh", "p90_exposure_score", "priority_rows"],
    )
    fig.update_traces(marker_line_width=0, hovertemplate="<b>%{y}</b><br>Score prom.: %{x:.1f}<extra></extra>")
    return apply_chart_style(fig, height=360)

