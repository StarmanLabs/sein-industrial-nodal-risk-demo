# SEIN Industrial Nodal Risk Intelligence

SEIN Industrial Nodal Risk Intelligence is a closed-code data product for industrial electricity due diligence in Peru.

It transforms COES nodal marginal-price outputs into a barra-month analytical panel, builds Estrés nodal and System-Adjusted Nodal Risk screening indicators, and translates those signals into due-diligence priorities for industrial exposure analysis.

## Interactive Demo

Live app:

https://sein-industrial-nodal-risk-demo-edaw4ndep4pm9plvudnyov.streamlit.app/

Run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The demo uses only controlled files under `data/public_demo/`. The full production pipeline, raw-data processing layer and internal audit scripts remain private.

## What This Project Does

- Ranks relative nodal marginal-price stress across SEIN barras.
- Combines nodal exposure with system-regime context.
- Produces action-oriented due-diligence candidates.
- Supports industrial exposure scenarios under explicit assumptions.
- Communicates limitations clearly for responsible use.

## What This Project Does Not Do

- It is not a causal grid diagnosis.
- It does not predict electricity prices.
- It does not estimate billing outcomes.
- It does not identify physical causes.
- It does not perform electrical network-flow studies.

## Public Repository Scope

This public showcase documents the methodology, product design, selected visuals, and sanitized sample outputs. The full processing pipeline, complete analytical dataset, and internal topology review materials are maintained in a private repository.

## Product Pages

1. Executive Overview
2. Estrés nodal
3. Prioridad operativa
4. Industrial Exposure Simulator
5. Evidence and Topology Context
6. Methodology and Audit

## Featured Demo Cases

The controlled demo uses selected cases for portfolio storytelling:

- PLANTAETANOL 60 and ZORRITOS 220 as lead public cases.
- TINTAYA EXISTENTE 138 and GE1 33 as sector-relevance cases.
- VALLE DEL CHIRA 220 and JAEN 138 as methodology examples.
- HUAYLLACHO 15 and NCTUMBES60 as reserve cases with explicit caveats.

## Portfolio Value

The project demonstrates data engineering, index construction, energy-economics judgment, industrial analytics, dashboard design, closed-code product strategy, and public communication discipline.

