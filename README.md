# SEIN Industrial Nodal Risk Intelligence

Decision-support dashboard for industrial due diligence on Peruvian nodal electricity price-stress signals.

## Executive Summary

SEIN Industrial Nodal Risk Intelligence is a closed-code analytical product for industrial electricity due diligence in Peru. It transforms COES nodal marginal-price data into a 217-barra, 36-month barra-month screening layer, builds descriptive indicators of nodal stress and operational priority, and translates those signals into an action-oriented review queue for industrial, contractual and energy-infrastructure analysis.

The public repository is a controlled showcase: it presents the dashboard, public-safe documentation and sanitized outputs without exposing the private ingestion pipeline, raw COES files, complete internal audit materials or closed scoring logic.

## Live Demo

Interactive app:

https://sein-industrial-nodal-risk-demo-edaw4ndep4pm9plvudnyov.streamlit.app/

Run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What Decision Does It Support?

The product helps answer:

> Which SEIN barras deserve industrial, contractual, topological or operational review first?

It is designed for analytical triage. The dashboard does not declare a final engineering diagnosis; it helps prioritize where expert due diligence should start.

## Public Demo Scope

The deployed demo uses a controlled public layer:

| Item | Public demo scope |
|---|---:|
| Barras | 217 |
| Period | 2023-2025 |
| Months | 36 |
| Barra-month observations | 6,779 |
| Data exposure | Aggregated / sanitized |
| Raw COES files | Not included |
| Private pipeline | Not included |
| Manual topology registers | Not included |
| Closed scoring logic | Not fully exposed |

## Product Pages

| Page | Decision question |
|---|---|
| Inicio | What does this product do and why does it matter? |
| Resumen Ejecutivo | Where are the strongest signals concentrated? |
| Ranking de Prioridad | Which barras should be reviewed first? |
| Mapa de Señales | Which barras combine nodal stress and operational priority? |
| Seguimiento Mensual | Is the signal persistent, episodic or recent? |
| Exposición Industrial | Which sector-barra-contract combination deserves review under explicit assumptions? |
| Caso de Estudio | Why does this barra deserve attention and what should be reviewed next? |

## Public Metric Names

The dashboard uses decision-oriented Spanish labels instead of internal indicator names.

| Public label | Meaning |
|---|---|
| Estrés nodal | Relative marginal-price stress by barra. |
| Prioridad operativa | Nodal stress read together with monthly system-regime context. |
| Score de revisión | Executive 0-100 score used to order the review queue. |
| Soporte de contexto | Reviewed public context that supports using the barra in the screening layer. |
| Robustez de señal | Whether the signal survives several ranking, persistence and sensitivity checks. |
| Revisión inmediata | First queue for structured due-diligence review. |
| Revisión selectiva | Relevant candidate that needs sector, contract or context filtering. |
| Seguimiento mensual | Episodic or scenario-sensitive signal to monitor over time. |
| Contexto base | Reference universe for comparison and future monitoring. |
| Requiere contexto adicional | Case where stronger interpretation should wait for better context. |

## What This Project Does

- Identifies barras with elevated relative nodal marginal-price stress.
- Orders due-diligence candidates for industrial electricity exposure review.
- Distinguishes persistent, episodic and lower-priority screening signals.
- Combines nodal price behavior with monthly system-regime context.
- Incorporates reviewed topology/context evidence to orient further analysis.
- Supports contract, location, reliability, demand and monthly-follow-up questions.

## What This Project Does Not Do

- It does not prove physical congestion.
- It does not predict future electricity prices.
- It does not calculate real industrial electricity bills.
- It does not estimate causal outage impacts.
- It does not perform electrical network-flow studies.
- It does not reconstruct the full SEIN network.
- It does not produce final investment, engineering or siting decisions.

Recommended caveat:

> This dashboard is a screening and prioritization layer. It orders signals to decide where to investigate further; it does not prove physical congestion, forecast prices or replace contractual, operational or engineering due diligence.

## Featured Demo Cases

The full public demo includes the 217-barra universe. Recommended cases for portfolio screenshots:

- PLANTAETANOL 60 and ZORRITOS 220 as lead decision-queue examples.
- TINTAYA EXISTENTE 138 and GE1 33 as industrial/sector relevance examples.
- VALLE DEL CHIRA 220 and JAEN 138 as methodology/context examples.
- HUAYLLACHO 15 and NCTUMBES60 as reserve examples with explicit caveats.

## Public / Private Split

Public repository includes:

- Streamlit dashboard demo.
- Sanitized 217-barra public layer.
- Public-safe documentation.
- Sample outputs and methodology summary.
- Clear claim boundaries.

Private repository keeps:

- Raw COES data.
- Ingestion and cleaning pipeline.
- Heavy interim files.
- Complete audit layers.
- Manual topology review registers.
- Closed scoring and production logic.

## Portfolio Value

This project demonstrates applied economic analysis, BI product thinking, analytics engineering, data governance, decision storytelling and responsible communication of methodological limits.
